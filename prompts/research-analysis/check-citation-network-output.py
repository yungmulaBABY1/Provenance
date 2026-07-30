#!/usr/bin/env python3
"""Check citation-network audit heading presence, order, and thin sections.

This checker is diagnostic. It mechanically verifies exact heading presence and
critical order. It also flags sections whose body contains too little substantive
content for manual review. A thin-section flag is not itself a failed run because
legitimate N/A or PROVISIONAL sections may be concise.
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

ORDER_RULES = [
    ("ARTIFACT 9: NETWORK MAP", "COMPLETION LEDGER"),
    ("COMPLETION LEDGER", "ARTIFACT 10: FINAL VERDICT"),
    ("ARTIFACT 10: FINAL VERDICT", "FINAL SECTION: STANDARDIZED FINDING TABLE"),
]

# Low enough not to punish valid concise N/A / PROVISIONAL sections, but high
# enough to catch a bare heading, placeholder, or one-line evasion.
DEFAULT_MIN_WORDS = 12

STATUS_PATTERNS = {
    "N/A": re.compile(r"\bN/?A\b", re.IGNORECASE),
    "PROVISIONAL": re.compile(r"\bPROVISIONAL\b", re.IGNORECASE),
    "INCOMPLETE": re.compile(r"\bINCOMPLETE RUN\b", re.IGNORECASE),
}

TOO_SMALL_PATTERNS = [
    re.compile(r"^\s*$"),
    re.compile(r"^\s*(tbd|todo|placeholder|none)\s*[.!]?\s*$", re.IGNORECASE),
]

def body_between(text: str, heading: str, later_headings: list[str]) -> str:
    """Return text after heading up to the nearest later required heading."""
    start = text.find(heading)
    if start == -1:
        return ""
    body_start = start + len(heading)
    later_positions = [
        text.find(candidate, body_start)
        for candidate in later_headings
        if text.find(candidate, body_start) != -1
    ]
    body_end = min(later_positions) if later_positions else len(text)
    return text[body_start:body_end].strip()

def count_words(text: str) -> int:
    return len(re.findall(r"\b[\w'-]+\b", text))

def classify_status(body: str) -> str:
    labels = [name for name, pattern in STATUS_PATTERNS.items() if pattern.search(body)]
    return ",".join(labels) if labels else "UNLABELED"

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
    missing = [heading for heading in REQUIRED if heading not in text]

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

    for earlier, later in ORDER_RULES:
        if earlier in text and later in text:
            if text.rfind(earlier) >= text.rfind(later):
                failed = True
                print(f"ORDER_FAIL\t{earlier} must appear before {later}")
            else:
                print(f"ORDER_PASS\t{earlier} precedes {later}")

    thin_sections = []
    status_counts = {"N/A": 0, "PROVISIONAL": 0, "INCOMPLETE": 0, "UNLABELED": 0}

    for index, heading in enumerate(REQUIRED):
        if heading not in text:
            continue

        later = REQUIRED[index + 1 :]
        body = body_between(text, heading, later)
        words = count_words(body)
        status = classify_status(body)

        for label in status.split(","):
            if label in status_counts:
                status_counts[label] += 1

        empty_or_placeholder = any(pattern.match(body) for pattern in TOO_SMALL_PATTERNS)
        if words < min_words or empty_or_placeholder:
            thin_sections.append((heading, words, status))
            print(f"THIN\t{heading}\t{words} words\tstatus={status}")
        else:
            print(f"BODY_PASS\t{heading}\t{words} words\tstatus={status}")

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
        "PASS\tAll required headings are present in the required order. "
        "Review THIN flags manually; they do not automatically fail the run."
    )
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
