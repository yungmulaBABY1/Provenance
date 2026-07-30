#!/usr/bin/env python3
"""Check whether a citation-network audit output contains every required heading."""

from pathlib import Path
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
    "ARTIFACT 10: FINAL VERDICT",
    "COMPLETION LEDGER",
    "FINAL SECTION: STANDARDIZED FINDING TABLE",
]

def main() -> int:
    if len(sys.argv) != 2:
        print("Usage: check_citation_network_output.py <audit-output.txt>")
        return 2

    path = Path(sys.argv[1])
    text = path.read_text(encoding="utf-8")
    missing = [heading for heading in REQUIRED if heading not in text]

    print(f"Checked: {path}")
    print(f"Required headings: {len(REQUIRED)}")
    print(f"Present: {len(REQUIRED) - len(missing)}")
    print(f"Missing: {len(missing)}")

    if missing:
        for heading in missing:
            print(f"MISSING\t{heading}")
        return 1

    print("PASS\tAll required headings are present.")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
