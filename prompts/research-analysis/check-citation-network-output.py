#!/usr/bin/env python3
"""Check citation-network audit execution compliance.

Hard checks:
- every required heading appears exactly once as a standalone line;
- required headings appear in the critical order;
- the Completion Ledger contains exactly one row for every required heading;
- ledger presence/status claims agree with the actual standalone headings;
- when a required analytical section or Artifact 1–9 is absent, Artifact 10 is
  withheld rather than issuing a substantive verdict.

Diagnostic checks:
- headings that appear only as line-start formatting variants;
- sections with very little substantive content;
- raw N/A / PROVISIONAL / INCOMPLETE labels for manual review.

The checker cannot decide whether an N/A or PROVISIONAL classification is
substantively justified.
"""

from pathlib import Path
import re
import sys

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
    "COMPLETION LEDGER",
    "ARTIFACT 10: FINAL VERDICT",
    "FINAL SECTION: STANDARDIZED FINDING TABLE",
]

GATE_REQUIRED = [
    heading
    for heading in REQUIRED
    if heading.startswith("SECTION ")
    or heading == "PRE-AUDIT CLAIM CONFIRMATION"
    or (
        heading.startswith("ARTIFACT ")
        and not heading.startswith("ARTIFACT 10:")
    )
]

ORDER_RULES = [
    ("ARTIFACT 9: NETWORK MAP", "COMPLETION LEDGER"),
    ("COMPLETION LEDGER", "ARTIFACT 10: FINAL VERDICT"),
    ("ARTIFACT 10: FINAL VERDICT", "FINAL SECTION: STANDARDIZED FINDING TABLE"),
]

DEFAULT_MIN_WORDS = 12

STATUS_PATTERNS = {
    "N/A": re.compile(r"\bN/?A\b", re.IGNORECASE),
    "PROVISIONAL": re.compile(r"\bPROVISIONAL\b", re.IGNORECASE),
    "INCOMPLETE": re.compile(r"\bINCOMPLETE RUN\b", re.IGNORECASE),
}

PLACEHOLDER_PATTERNS = [
    re.compile(r"^\s*$"),
    re.compile(r"^\s*(tbd|todo|placeholder|none)\s*[.!]?\s*$", re.IGNORECASE),
]

def standalone_positions(lines: list[str]) -> dict[str, list[int]]:
    positions = {heading: [] for heading in REQUIRED}
    for index, line in enumerate(lines):
        stripped = line.strip()
        if stripped in positions:
            positions[stripped].append(index)
    return positions

def line_start_variants(lines: list[str], heading: str) -> list[int]:
    variants = []
    for index, line in enumerate(lines):
        stripped = line.strip()
        if stripped != heading and stripped.startswith(heading):
            variants.append(index)
    return variants

def body_for(lines: list[str], heading_line: int, all_heading_lines: set[int]) -> str:
    body_lines = []
    for index in range(heading_line + 1, len(lines)):
        if index in all_heading_lines:
            break
        body_lines.append(lines[index])
    return "\n".join(body_lines).strip()

def count_words(text: str) -> int:
    return len(re.findall(r"\b[\w'-]+\b", text))

def classify_status(body: str) -> str:
    labels = [name for name, pattern in STATUS_PATTERNS.items() if pattern.search(body)]
    return ",".join(labels) if labels else "UNLABELED"

def parse_markdown_cells(line: str) -> list[str]:
    if not line.lstrip().startswith("|"):
        return []
    cells = [cell.strip() for cell in line.strip().strip("|").split("|")]
    return cells

def normalize_ledger_heading(value: str) -> str:
    value = value.strip()
    if len(value) >= 2 and value[0] == "`" and value[-1] == "`":
        value = value[1:-1]
    return value.strip()

def parse_completion_ledger(body: str) -> dict[str, list[dict[str, str]]]:
    rows: dict[str, list[dict[str, str]]] = {heading: [] for heading in REQUIRED}
    for line in body.splitlines():
        cells = parse_markdown_cells(line)
        if len(cells) < 3:
            continue
        heading = normalize_ledger_heading(cells[0])
        if heading not in rows:
            continue
        rows[heading].append(
            {
                "present": cells[1].strip().lower(),
                "status": cells[2].strip().lower(),
                "raw": line.strip(),
            }
        )
    return rows

def ledger_claims_present(row: dict[str, str]) -> bool:
    return row["present"] in {"yes", "y", "true", "present"}

def ledger_claims_absent(row: dict[str, str]) -> bool:
    return row["present"] in {"no", "n", "false", "absent"}

def ledger_claims_completed(row: dict[str, str]) -> bool:
    status = row["status"]
    return "completed" in status or status == "n/a" or status.startswith("n/a ")

def ledger_claims_omitted(row: dict[str, str]) -> bool:
    return "omitted" in row["status"]

def main() -> int:
    if len(sys.argv) not in (2, 3):
        print(
            "Usage: check-citation-network-output.py "
            "<audit-output.txt> [minimum-body-word-count]"
        )
        return 2

    path = Path(sys.argv[1])
    min_words = DEFAULT_MIN_WORDS
    if len(sys.argv) == 3:
        try:
            min_words = int(sys.argv[2])
        except ValueError:
            print("ERROR\tminimum-body-word-count must be an integer")
            return 2
        if min_words < 0:
            print("ERROR\tminimum-body-word-count must be nonnegative")
            return 2

    text = path.read_text(encoding="utf-8")
    lines = text.splitlines()
    positions = standalone_positions(lines)
    missing = [heading for heading, found in positions.items() if not found]
    duplicates = {heading: found for heading, found in positions.items() if len(found) > 1}

    print(f"Checked: {path}")
    print(f"Required headings: {len(REQUIRED)}")
    print(f"Present: {len(REQUIRED) - len(missing)}")
    print(f"Missing: {len(missing)}")
    print(f"Thin-section threshold: {min_words} words")

    failed = False

    if missing:
        failed = True
        for heading in missing:
            print(f"MISSING\t{heading}")
            variants = line_start_variants(lines, heading)
            if variants:
                print(
                    f"FORMAT_VARIANT\t{heading}\t"
                    f"line-start variants={','.join(str(i+1) for i in variants)}"
                )

    if duplicates:
        failed = True
        for heading, found in duplicates.items():
            print(f"DUPLICATE\t{heading}\tstandalone lines={','.join(str(i+1) for i in found)}")

    unique_line = {
        heading: found[0]
        for heading, found in positions.items()
        if len(found) == 1
    }

    for earlier, later in ORDER_RULES:
        if earlier in unique_line and later in unique_line:
            if unique_line[earlier] >= unique_line[later]:
                failed = True
                print(f"ORDER_FAIL\t{earlier} must appear before {later}")
            else:
                print(f"ORDER_PASS\t{earlier} precedes {later}")

    all_heading_lines = set(unique_line.values())
    thin_sections = []
    status_counts = {"N/A": 0, "PROVISIONAL": 0, "INCOMPLETE": 0, "UNLABELED": 0}
    bodies: dict[str, str] = {}

    for heading in REQUIRED:
        if heading not in unique_line:
            continue

        body = body_for(lines, unique_line[heading], all_heading_lines)
        bodies[heading] = body
        words = count_words(body)
        status = classify_status(body)

        for label in status.split(","):
            if label in status_counts:
                status_counts[label] += 1

        placeholder = any(pattern.match(body) for pattern in PLACEHOLDER_PATTERNS)
        if words < min_words or placeholder:
            thin_sections.append((heading, words, status))
            print(f"THIN\t{heading}\t{words} words\tstatus={status}")
        else:
            print(f"BODY_PASS\t{heading}\t{words} words\tstatus={status}")

    # Completion Ledger cross-check.
    ledger_body = bodies.get("COMPLETION LEDGER", "")
    ledger_rows = parse_completion_ledger(ledger_body)

    if "COMPLETION LEDGER" in unique_line:
        for heading in REQUIRED:
            rows = ledger_rows.get(heading, [])
            actual_count = len(positions[heading])

            if not rows:
                failed = True
                print(f"LEDGER_ROW_MISSING\t{heading}")
                continue

            if len(rows) > 1:
                failed = True
                print(f"LEDGER_ROW_DUPLICATE\t{heading}\trows={len(rows)}")
                continue

            row = rows[0]
            actual_present = actual_count == 1

            if ledger_claims_present(row) and not actual_present:
                failed = True
                print(
                    f"LEDGER_FALSE_PRESENT\t{heading}\t"
                    f"ledger={row['present']}/{row['status']}\tactual_count={actual_count}"
                )
            elif ledger_claims_absent(row) and actual_present:
                failed = True
                print(
                    f"LEDGER_FALSE_ABSENT\t{heading}\t"
                    f"ledger={row['present']}/{row['status']}\tactual_count={actual_count}"
                )
            elif not ledger_claims_present(row) and not ledger_claims_absent(row):
                failed = True
                print(
                    f"LEDGER_PRESENT_VALUE_INVALID\t{heading}\tvalue={row['present']}"
                )

            if ledger_claims_completed(row) and not actual_present:
                failed = True
                print(
                    f"LEDGER_FALSE_COMPLETE\t{heading}\t"
                    f"status={row['status']}\tactual_count={actual_count}"
                )

            if ledger_claims_omitted(row) and actual_present:
                failed = True
                print(
                    f"LEDGER_FALSE_OMITTED\t{heading}\t"
                    f"status={row['status']}\tactual_count={actual_count}"
                )

    # Gate-behavior cross-check.
    missing_gate_blocks = [heading for heading in GATE_REQUIRED if not positions[heading]]
    artifact10_body = bodies.get("ARTIFACT 10: FINAL VERDICT", "")
    if missing_gate_blocks and "ARTIFACT 10: FINAL VERDICT" in unique_line:
        withheld = bool(
            re.search(r"\bWITHHELD\b", artifact10_body, re.IGNORECASE)
            and re.search(r"\bcompletion gate failed\b", artifact10_body, re.IGNORECASE)
        )
        if not withheld:
            failed = True
            print(
                "GATE_FAIL\tRequired block(s) missing but Artifact 10 was not "
                "explicitly withheld."
            )
        else:
            print("GATE_PASS\tArtifact 10 withheld after required-block omission.")

    print(
        "STATUS_SUMMARY\t"
        f"N/A={status_counts['N/A']}\t"
        f"PROVISIONAL={status_counts['PROVISIONAL']}\t"
        f"INCOMPLETE={status_counts['INCOMPLETE']}\t"
        f"UNLABELED={status_counts['UNLABELED']}"
    )

    if thin_sections:
        print(
            "MANUAL_REVIEW\t"
            f"{len(thin_sections)} present heading(s) contain fewer than "
            f"{min_words} words or placeholder-only content."
        )

    if failed:
        return 1

    print(
        "PASS\tAll required headings are unique standalone lines in the required "
        "order; Completion Ledger claims match actual presence. Review THIN and "
        "status labels manually."
    )
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
