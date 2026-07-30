#!/usr/bin/env python3
"""Check whether a citation-network audit output contains every required heading.

FIXES A FATAL BUG IN THE FIRST VERSION.

The original used `heading not in text` — a substring search over the whole
document. But the COMPLETION LEDGER enumerates all 25 required headings in its
own rows. Every heading therefore appeared in the ledger, and the checker
returned PASS even when every actual section was missing.

It validated that the ledger existed. It did not validate that the sections did.
That is exactly backwards: the ledger is the claim, the sections are the fact,
and the checker's job is to test the claim against the fact.

This version:
  1. Matches headings only at LINE START, so markdown table rows (which begin
     with '|') cannot satisfy the check.
  2. Parses the ledger and cross-checks its claims against actual presence,
     catching a ledger that reports 'completed' for a section that is absent.
  3. Distinguishes exit states so a run that correctly withheld its verdict is
     not scored the same as a run that silently omitted sections.
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

REQUIRED = [
    "PRE-AUDIT CLAIM CONFIRMATION",
    "SECTION A: CITATION NETWORK STRUCTURE AND CARTEL DETECTION",
    "SECTION B: EVIDENCE TYPE CODING",
    "SECTION C: CITATION POLARITY AND CLAIM USE",
    "SECTION D: CLAIM MUTATION TRACKING",
    "SECTION E: ADJACENT FIELD ENGAGEMENT / NEGLECT",
    "SECTION F: HUB DEPENDENCY AND REVIEW-PAPER LAUNDERING",
    "SECTION G: PATTERN RECOGNITION AND RATCHET BEHAVIOR",
    "SECTION H: IGNORED CRITIQUE AND NON-UPTAKE",
    "SECTION I: AUTHOR, INSTITUTION, JOURNAL, AND FUNDING CLUSTERING",
    "SECTION J: FALSE-POSITIVE AND BASELINE CHECK",
    "SECTION J2: THE CONCEDE TEST",
    "SECTION K: CARTEL-RISK SCORING",
    "ARTIFACT 1: TOP 15 CITATION SPINE TABLE",
    "ARTIFACT 2: FOUNDING CLUSTER TABLE",
    "ARTIFACT 3: RECENT 5-YEAR CITATION BEHAVIOR TABLE",
    "ARTIFACT 4: CITATION POLARITY TABLE",
    "ARTIFACT 5: CLAIM MUTATION TABLE",
    "ARTIFACT 6: ADJACENT-LITERATURE NEGLECT TABLE",
    "ARTIFACT 7: CRITIQUE-UPTAKE TABLE",
    "ARTIFACT 8: CARTEL-RISK SCORECARD",
    "ARTIFACT 9: NETWORK MAP",
    "ARTIFACT 10: FINAL VERDICT",
    "COMPLETION LEDGER",
    "FINAL SECTION: STANDARDIZED FINDING TABLE",
]

# Exit codes
OK = 0
SECTIONS_MISSING = 1
USAGE = 2
LEDGER_FALSE = 3          # ledger claims a section that is not present
LEDGER_ABSENT = 4         # no ledger at all — run fails the execution test


def heading_present(text: str, heading: str) -> bool:
    """True only if the heading appears at the start of a line.

    Markdown table rows begin with '|', so a ledger row naming the heading will
    not satisfy this. Optional leading '#' allows markdown headings.
    """
    pattern = re.compile(
        r"^[ \t]*#{0,6}[ \t]*" + re.escape(heading) + r"[ \t]*$",
        re.MULTILINE,
    )
    return bool(pattern.search(text))


def find_ledger_block(text: str) -> str | None:
    """Return the text between COMPLETION LEDGER and the next line-start heading."""
    start = re.search(r"^[ \t]*#{0,6}[ \t]*COMPLETION LEDGER", text, re.MULTILINE)
    if not start:
        return None
    rest = text[start.end():]
    nxt = re.search(
        r"^[ \t]*#{0,6}[ \t]*(FINAL SECTION|COMPLETION GATE|ARTIFACT)", rest, re.MULTILINE
    )
    return rest[: nxt.start()] if nxt else rest


def parse_ledger_claims(block: str) -> dict[str, str]:
    """Map heading -> claimed status, from markdown table rows."""
    claims: dict[str, str] = {}
    for line in block.splitlines():
        if not line.strip().startswith("|"):
            continue
        cells = [c.strip() for c in line.strip().strip("|").split("|")]
        if len(cells) < 3:
            continue
        for heading in REQUIRED:
            if heading.lower() in cells[0].lower():
                claims[heading] = " ".join(cells[1:]).lower()
                break
    return claims


def main() -> int:
    if len(sys.argv) != 2:
        print("Usage: check-citation-network-output.py <audit-output.txt>")
        return USAGE

    path = Path(sys.argv[1])
    text = path.read_text(encoding="utf-8")

    present = {h: heading_present(text, h) for h in REQUIRED}
    missing = [h for h, ok in present.items() if not ok]

    print(f"Checked: {path}")
    print(f"Required headings: {len(REQUIRED)}")
    print(f"Present (line-start match): {len(REQUIRED) - len(missing)}")
    print(f"Missing: {len(missing)}")

    for h in missing:
        print(f"MISSING\t{h}")

    # --- ledger cross-check -------------------------------------------------
    ledger = find_ledger_block(text)
    if ledger is None:
        print()
        print("LEDGER ABSENT\tNo COMPLETION LEDGER found.")
        print("Per the prompt: if the ledger is omitted, the run fails the "
              "execution test.")
        return LEDGER_ABSENT

    claims = parse_ledger_claims(ledger)
    print()
    print(f"Ledger rows parsed: {len(claims)} of {len(REQUIRED)}")

    false_claims = []
    for heading, claim in claims.items():
        claims_done = ("completed" in claim or "yes" in claim) and "omitted" not in claim
        if claims_done and not present[heading]:
            false_claims.append(heading)

    unlisted = [h for h in REQUIRED if h not in claims]
    for h in unlisted:
        print(f"NOT IN LEDGER\t{h}")

    if false_claims:
        print()
        print("LEDGER CONTRADICTED BY OUTPUT — the ledger reports these as "
              "completed but they do not appear as line-start headings:")
        for h in false_claims:
            print(f"FALSE CLAIM\t{h}")
        print()
        print("This is the failure mode the mechanical check exists to catch. "
              "Treat the whole run as unverified, not merely incomplete.")
        return LEDGER_FALSE

    # --- gate state ---------------------------------------------------------
    gate_fired = "INCOMPLETE RUN — REQUIRED SECTION OMITTED" in text
    withheld = "WITHHELD — completion gate failed" in text

    print()
    if missing:
        if gate_fired and withheld:
            print("GATE FIRED CORRECTLY\tSections are missing AND the run "
                  "declared INCOMPLETE and withheld the verdict.")
            print("This is a well-behaved incomplete run, not a silent omission.")
        else:
            print("SILENT OMISSION\tSections are missing and the run did NOT "
                  "declare INCOMPLETE or withhold the verdict.")
            print("This is the original failure the execution contract targets.")
        return SECTIONS_MISSING

    if gate_fired or withheld:
        print("INCONSISTENT\tThe run declared INCOMPLETE but all required "
              "headings are present. Check whether a section is present but "
              "empty, or marked N/A without a reason.")
        return SECTIONS_MISSING

    print("PASS\tAll required headings present at line start, and the ledger "
          "does not contradict the output.")
    print()
    print("NOTE: this checks PRESENCE, not quality. A section can be present "
          "and empty. Presence is mechanically verifiable; substance is not.")
    return OK


if __name__ == "__main__":
    raise SystemExit(main())
