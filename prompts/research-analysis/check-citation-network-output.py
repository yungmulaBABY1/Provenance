#!/usr/bin/env python3
"""Deterministically check citation-network audit execution compliance.

Hard checks:
- every required heading appears exactly once as a standalone line;
- required headings appear in the critical order;
- the Completion Ledger contains exactly one row for every required heading;
- ledger presence/status claims agree with actual standalone-heading presence;
- when a required analytical section or Artifact 1–9 is absent, Artifact 10 is
  withheld rather than issuing a substantive verdict;
- a missing Completion Ledger fails the execution test.

Content-form checks:
- canonical verification-state whitelist, with counts and line numbers;
- separation of COMPUTED-FROM-RETRIEVED from verification-state positions;
- explicit risk-band disposition and reason when withheld;
- graph receipts when internal citation density is SCORED;
- source-lock record, source classification, and aggregation form.

Review routing:
- emits targeted review items for truth/classification/nesting judgments that
  deterministic checks cannot establish;
- never returns bare PASS while review items remain.

Diagnostic checks:
- headings that appear only as line-start formatting variants;
- bodies too short to clear a crude placeholder screen;
- raw N/A / PROVISIONAL / INCOMPLETE labels for manual review.

IMPORTANT:
The body-length screen catches empty or placeholder-like output. It does NOT
establish that a section is analytically adequate. Manual review remains
load-bearing, especially for Sections A, F, J, and other high-burden sections.
"""

from collections import Counter
from dataclasses import dataclass
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

# This is a placeholder screen, not an adequacy threshold.
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

CANONICAL_VERIFICATION_STATES = {
    "LOCATED",
    "ABSTRACT-CONFIRMED",
    "FULL-TEXT-CONFIRMED",
    "RECEPTION-CONFIRMED",
    "CONTESTED",
    "REBUTTED",
    "PROVISIONAL",
    "CROSS-SOURCE-CONFIRMED",
}

# Deliberately narrow: catch invented compound authority labels without treating
# arbitrary uppercase prose as a verification state.
AUTHORITY_TOKEN_RE = re.compile(r"\b[A-Z][A-Z0-9-]*-(?:VERIFIED|CONFIRMED)\b")

ALWAYS_REQUIRED_CONTENT_LABELS = [
    "SOURCE-LOCK METHOD:",
    "Independent scored dimensions:",
    "Nested scored dimensions:",
    "Verified risk denominator:",
    "ARITHMETIC BAND POSITION:",
    "RISK BAND:",
    "MECHANISM LABEL:",
]

SOURCE_LOCK_FIELDS = [
    "SOURCE-LOCK DATABASE:",
    "SOURCE-LOCK QUERY OR SOURCE LIST:",
    "SOURCE-LOCK DATE CUTOFF:",
    "SOURCE-LOCK RANKING RULE:",
    "SOURCE-LOCK N:",
    "SOURCE-LOCK DEDUPLICATION RULE:",
    "SOURCE-LOCK TIMESTAMP OR HASH:",
]

GRAPH_RECEIPT_LABELS = [
    "GRAPH CORPUS DEFINITION:",
    "GRAPH CORPUS NODE LIST:",
    "INTERNAL EDGE LIST:",
    "DENSITY CALCULATION:",
    "DENSITY NUMERATOR:",
    "DENSITY DENOMINATOR:",
    "DENSITY INPUT COVERAGE:",
    "DENSITY INFERENCE SCOPE:",
    "DERIVATION MODE: COMPUTED-FROM-RETRIEVED",
]

EXPECTED_DIMENSIONS = {
    "founding-cluster dominance",
    "internal citation density",
    "recent-paper dependence",
    "review-hub laundering",
    "proxy mismatch",
    "claim mutation",
    "adjacent-field neglect",
    "lack of decisive tests",
    "poor critique uptake",
    "intervention-evidence ratchet",
    "model non-updating",
}

SOURCE_CLASSES = {
    "CONSTRUCT-DEFINING",
    "MECHANISM-SUPPORTING",
    "DIRECTLY-ADJUDICATING",
}

EMPTY_VALUES = {"", "—", "-", "N/A", "NA", "NONE", "UNKNOWN", "TBD"}

@dataclass
class Table:
    header_line: int
    headers: list[str]
    rows: list[tuple[int, list[str], str]]

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

def classify_status(body: str, clears_placeholder_screen: bool) -> str:
    labels = [name for name, pattern in STATUS_PATTERNS.items() if pattern.search(body)]
    if labels:
        return ",".join(labels)
    return "COMPLETED_INFERRED" if clears_placeholder_screen else "UNMARKED_THIN"

def parse_markdown_cells(line: str) -> list[str]:
    if not line.lstrip().startswith("|"):
        return []
    return [cell.strip() for cell in line.strip().strip("|").split("|")]

def is_separator_row(cells: list[str]) -> bool:
    return bool(cells) and all(re.fullmatch(r":?-{3,}:?", cell) for cell in cells)

def normalize_cell(value: str) -> str:
    return re.sub(r"\s+", " ", value.strip()).casefold()

def parse_markdown_tables(lines: list[str]) -> list[Table]:
    tables: list[Table] = []
    index = 0
    while index < len(lines) - 1:
        headers = parse_markdown_cells(lines[index])
        separator = parse_markdown_cells(lines[index + 1])
        if not headers or not is_separator_row(separator):
            index += 1
            continue

        rows: list[tuple[int, list[str], str]] = []
        cursor = index + 2
        while cursor < len(lines):
            cells = parse_markdown_cells(lines[cursor])
            if not cells:
                break
            rows.append((cursor + 1, cells, lines[cursor].strip()))
            cursor += 1

        tables.append(Table(index + 1, headers, rows))
        index = max(cursor, index + 1)
    return tables

def header_index(headers: list[str], label: str, *, startswith: bool = False) -> int | None:
    target = normalize_cell(label)
    for index, header in enumerate(headers):
        normalized = normalize_cell(header)
        if normalized == target or (startswith and normalized.startswith(target)):
            return index
    return None

def nonempty(value: str) -> bool:
    return value.strip().upper() not in EMPTY_VALUES

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

def verdict_is_withheld(body: str) -> bool:
    return bool(
        re.search(r"\bWITHHELD\b", body, re.IGNORECASE)
        and re.search(r"\bcompletion gate failed\b", body, re.IGNORECASE)
    )

# The prompt mandates an ASCII hyphen here ("INCOMPLETE RUN  -  REQUIRED
# SECTION OMITTED"). An earlier version of this check required an em dash, so a
# model that followed the prompt exactly failed the declaration test in the one
# scenario the completion gate exists for. Accept any dash, or none, and do not
# depend on the surrounding spacing.
INCOMPLETE_RUN_RE = re.compile(
    r"\bINCOMPLETE RUN\s*[-‐-―−:]?\s*REQUIRED SECTION OMITTED\b",
    re.IGNORECASE,
)

def incomplete_run_declared(text: str) -> bool:
    return bool(INCOMPLETE_RUN_RE.search(text))

def check_verification_vocabulary(
    lines: list[str],
) -> tuple[Counter[str], dict[str, list[int]]]:
    observed: Counter[str] = Counter()
    invalid_lines: dict[str, list[int]] = {}
    for line_number, line in enumerate(lines, start=1):
        for token in AUTHORITY_TOKEN_RE.findall(line):
            observed[token] += 1
            if token not in CANONICAL_VERIFICATION_STATES:
                invalid_lines.setdefault(token, []).append(line_number)
    return observed, invalid_lines

def computed_in_verification_positions(lines: list[str], tables: list[Table]) -> list[int]:
    offending: set[int] = set()
    for line_number, line in enumerate(lines, start=1):
        if re.search(
            r"(?i)verification\s*(?:state)?\s*:\s*.*\bCOMPUTED-FROM-RETRIEVED\b",
            line,
        ):
            offending.add(line_number)

    for table in tables:
        verification_index = header_index(table.headers, "verification state")
        if verification_index is None:
            continue
        for line_number, cells, _raw in table.rows:
            if verification_index < len(cells) and "COMPUTED-FROM-RETRIEVED" in cells[verification_index]:
                offending.add(line_number)
    return sorted(offending)

def find_scorecard_table(tables: list[Table]) -> Table | None:
    for table in tables:
        if (
            header_index(table.headers, "dimension") is not None
            and header_index(table.headers, "dimension disposition") is not None
        ):
            return table
    return None

def integer_line_value(text: str, label: str) -> int | None:
    value = line_value(text, label)
    if value is None:
        return None
    matches = re.findall(r"\b\d+\b", value)
    return int(matches[-1]) if matches else None

def line_value(text: str, label: str) -> str | None:
    match = re.search(
        rf"(?mi)^\s*(?:[-*]\s*)?{re.escape(label)}\s*(.*?)\s*$",
        text,
    )
    return match.group(1).strip() if match else None

def label_has_content(lines: list[str], label: str) -> bool:
    pattern = re.compile(rf"^\s*(?:[-*]\s*)?{re.escape(label)}\s*(.*)$", re.IGNORECASE)
    for index, line in enumerate(lines):
        match = pattern.match(line)
        if not match:
            continue
        if nonempty(match.group(1)):
            return True
        for following in lines[index + 1:index + 16]:
            stripped = following.strip()
            if not stripped:
                continue
            if re.match(r"^[A-Z][A-Z0-9 /-]+:\s*", stripped):
                return False
            return True
        return False
    return False

def check_source_lock(text: str, review_items: list[str]) -> bool:
    failed = False
    method = line_value(text, "SOURCE-LOCK METHOD:")
    valid_methods = {"LOCKED QUERY", "LOCKED SOURCES", "POST HOC"}
    normalized = method.rstrip(".").strip().upper() if method is not None else ""
    if normalized not in valid_methods:
        print(
            "SOURCE_LOCK_FAIL\texpected LOCKED QUERY, LOCKED SOURCES, or POST HOC"
            f"\tgot={method if method is not None else 'MISSING'}"
        )
        failed = True
    else:
        print(f"SOURCE_LOCK_METHOD_PASS\t{normalized}")

    record: list[str] = []
    for label in SOURCE_LOCK_FIELDS:
        value = line_value(text, label)
        if value is None or not nonempty(value):
            print(f"SOURCE_LOCK_RECORD_FAIL\tmissing or empty\t{label}")
            failed = True
        else:
            record.append(f"{label} {value}")

    if not failed:
        print("SOURCE_LOCK_FORM_PASS\tmethod and seven-field lock record present.")
        if normalized in {"LOCKED QUERY", "LOCKED SOURCES"}:
            review_items.append(
                "SOURCE_LOCK_TRUTH — verify the lock predates citation inspection and the "
                "query/source list deterministically fixes the exemplars: " + " | ".join(record)
            )
    return failed

def check_source_classification(
    tables: list[Table], review_items: list[str]
) -> bool:
    failed = False
    source_tables = [
        table for table in tables
        if header_index(table.headers, "source class", startswith=True) is not None
    ]
    if not source_tables:
        print("SOURCE_CLASS_FAIL\tNo table with a Source class column was found.")
        return True

    directly_adjudicating: list[tuple[int, str]] = []
    classified_count = 0
    required_direct_headers = [
        "actual result",
        "explanation favored",
        "explanation weakened",
        "precise revision required",
    ]

    for table in source_tables:
        class_index = header_index(table.headers, "source class", startswith=True)
        assert class_index is not None
        direct_indexes = {
            name: header_index(table.headers, name) for name in required_direct_headers
        }
        for line_number, cells, raw in table.rows:
            class_value = cells[class_index] if class_index < len(cells) else ""
            matched = [name for name in SOURCE_CLASSES if name in class_value.upper()]
            if len(matched) != 1:
                print(
                    f"SOURCE_CLASS_FAIL\tline={line_number}\texpected exactly one class"
                    f"\tvalue={class_value or 'MISSING'}"
                )
                failed = True
                continue
            classified_count += 1
            if matched[0] != "DIRECTLY-ADJUDICATING":
                continue

            row_complete = True
            for name, index in direct_indexes.items():
                value = cells[index] if index is not None and index < len(cells) else ""
                if not nonempty(value):
                    print(
                        f"DIRECT_ADJUDICATION_FORM_FAIL\tline={line_number}\t"
                        f"missing={name}"
                    )
                    failed = True
                    row_complete = False
            if row_complete:
                directly_adjudicating.append((line_number, raw))

    if classified_count == 0:
        print("SOURCE_CLASS_FORM_PASS\tNo nominated-source rows to classify.")
    elif not failed:
        print(
            f"SOURCE_CLASS_FORM_PASS\tclassified_sources={classified_count}\t"
            f"directly_adjudicating={len(directly_adjudicating)}"
        )

    if directly_adjudicating:
        extract = " || ".join(
            f"line {line_number}: {raw}" for line_number, raw in directly_adjudicating
        )
        review_items.append(
            f"DIRECT_ADJUDICATION_SUBSTANCE — {len(directly_adjudicating)} source(s) "
            "classified DIRECTLY-ADJUDICATING; verify each classification and its actual "
            "result, favored explanation, weakened explanation, and required revision: "
            + extract
        )
    return failed

def check_scorecard(
    text: str, tables: list[Table], review_items: list[str]
) -> tuple[bool, bool]:
    """Return (failed, internal_density_is_scored)."""
    table = find_scorecard_table(tables)
    if table is None:
        print("AGGREGATION_FAIL\tNo scorecard table was found.")
        return True, False

    dimension_index = header_index(table.headers, "dimension")
    disposition_index = header_index(table.headers, "dimension disposition")
    aggregation_index = header_index(table.headers, "aggregation status", startswith=True)
    assert dimension_index is not None and disposition_index is not None

    internal_density_scored = False
    for _line_number, cells, _raw in table.rows:
        if dimension_index >= len(cells) or disposition_index >= len(cells):
            continue
        if normalize_cell(cells[dimension_index]) == "internal citation density":
            internal_density_scored = bool(
                re.search(r"\bSCORED\s+[0-3]\b", cells[disposition_index], re.IGNORECASE)
            )
            break

    if aggregation_index is None:
        print("AGGREGATION_FAIL\tScorecard lacks an AGGREGATION STATUS column.")
        return True, internal_density_scored

    failed = False
    seen_dimensions: set[str] = set()
    independent_count = 0
    nested_rows: list[tuple[int, str]] = []
    for line_number, cells, raw in table.rows:
        if dimension_index >= len(cells) or disposition_index >= len(cells):
            continue
        dimension = normalize_cell(cells[dimension_index])
        if dimension not in EXPECTED_DIMENSIONS:
            continue
        seen_dimensions.add(dimension)
        disposition = cells[disposition_index].upper()
        scored = bool(re.search(r"\bSCORED\s+[0-3]\b", disposition))
        if dimension == "internal citation density":
            internal_density_scored = scored
        if not scored:
            continue

        aggregation = cells[aggregation_index].strip() if aggregation_index < len(cells) else ""
        if re.fullmatch(r"INDEPENDENT\.?", aggregation, re.IGNORECASE):
            independent_count += 1
        elif re.match(r"NESTED\s+under\s+\S", aggregation, re.IGNORECASE):
            nested_rows.append((line_number, raw))
        else:
            failed = True
            print(
                f"AGGREGATION_FAIL\tline={line_number}\t{dimension}\t"
                f"invalid status={aggregation or 'MISSING'}"
            )

    missing_dimensions = sorted(EXPECTED_DIMENSIONS - seen_dimensions)
    for dimension in missing_dimensions:
        failed = True
        print(f"AGGREGATION_FAIL\tmissing scorecard dimension\t{dimension}")

    declared_independent = integer_line_value(text, "Independent scored dimensions:")
    declared_nested = integer_line_value(text, "Nested scored dimensions:")
    declared_denominator = integer_line_value(text, "Verified risk denominator:")
    expected_denominator = 3 * independent_count

    comparisons = [
        ("independent count", declared_independent, independent_count),
        ("nested count", declared_nested, len(nested_rows)),
        ("verified risk denominator", declared_denominator, expected_denominator),
    ]
    for label, declared, expected in comparisons:
        if declared != expected:
            failed = True
            print(
                f"AGGREGATION_ARITHMETIC_FAIL\t{label}\t"
                f"declared={declared if declared is not None else 'MISSING'}\texpected={expected}"
            )

    if not failed:
        print(
            f"AGGREGATION_FORM_PASS\tindependent={independent_count}\t"
            f"nested={len(nested_rows)}\tdenominator={expected_denominator}"
        )

    if nested_rows:
        extract = " || ".join(f"line {line}: {raw}" for line, raw in nested_rows)
        review_items.append(
            f"NESTING_SUBSTANCE — {len(nested_rows)} dimension(s) marked NESTED; verify "
            "the parent owns the shared evidence and no independent inferential work was "
            "lost: " + extract
        )
    return failed, internal_density_scored

def check_graph_receipts(lines: list[str], internal_density_scored: bool) -> bool:
    if not internal_density_scored:
        print("GRAPH_RECEIPTS_NOT_REQUIRED\tInternal citation density is not SCORED.")
        return False

    failed = False
    for label in GRAPH_RECEIPT_LABELS:
        if label == "DERIVATION MODE: COMPUTED-FROM-RETRIEVED":
            present = any(label in line for line in lines)
        else:
            present = label_has_content(lines, label)
        if not present:
            failed = True
            print(f"GRAPH_RECEIPT_FAIL\tmissing or empty\t{label}")
    if not failed:
        print("GRAPH_RECEIPTS_PASS\tAll scored-density receipts are present.")
    return failed

def main() -> int:
    args = sys.argv[1:]
    vocab_only = False
    if "--vocab-only" in args:
        vocab_only = True
        args.remove("--vocab-only")

    if len(args) not in (1, 2):
        print(
            "Usage: check-citation-network-output.py "
            "[--vocab-only] <audit-output.txt> "
            "[minimum-placeholder-screen-word-count]"
        )
        return 2

    path = Path(args[0])
    min_words = DEFAULT_MIN_WORDS
    if len(args) == 2:
        try:
            min_words = int(args[1])
        except ValueError:
            print("ERROR\tminimum-placeholder-screen-word-count must be an integer")
            return 2
        if min_words < 0:
            print("ERROR\tminimum-placeholder-screen-word-count must be nonnegative")
            return 2

    text = path.read_text(encoding="utf-8")
    lines = text.splitlines()
    tables = parse_markdown_tables(lines)

    observed_authority_tokens, invalid_authority_lines = check_verification_vocabulary(lines)
    canonical_authority_count = sum(
        count
        for token, count in observed_authority_tokens.items()
        if token in CANONICAL_VERIFICATION_STATES
    )

    print(f"Checked: {path}")
    content_failed = False
    if invalid_authority_lines:
        content_failed = True
        for token, line_numbers in sorted(invalid_authority_lines.items()):
            print(
                f"VERIFICATION_VOCAB_FAIL\t{token}\tcount={len(line_numbers)}\t"
                f"lines={','.join(map(str, line_numbers))}"
            )

    if canonical_authority_count == 0:
        print(
            "VERIFICATION_VOCAB_DIAGNOSTIC\tNo canonical *-CONFIRMED "
            "verification state appears in the output. A fully PROVISIONAL run may "
            "still be structurally valid, but manual review must confirm that no "
            "retrieval claim was silently relabeled."
        )
    else:
        print(
            "VERIFICATION_VOCAB_PASS\t"
            f"canonical_confirmed_tokens={canonical_authority_count}"
        )

    if vocab_only:
        if content_failed:
            print("CONTENT_RESULT\tFAIL")
            print("FAIL\tVerification-vocabulary whitelist failed.")
            return 1
        print("CONTENT_RESULT\tPASS")
        print("PASS\tVerification-vocabulary whitelist passed; no other checks requested.")
        return 0

    positions = standalone_positions(lines)
    missing = [heading for heading, found in positions.items() if not found]
    duplicates = {heading: found for heading, found in positions.items() if len(found) > 1}

    print(f"Required headings: {len(REQUIRED)}")
    print(f"Present: {len(REQUIRED) - len(missing)}")
    print(f"Missing: {len(missing)}")
    print(f"Placeholder-screen threshold: {min_words} words")
    print(
        "NOTICE\tA body-length pass means only that the section is not empty or an "
        "obvious placeholder. It does not establish analytical adequacy."
    )

    structural_failed = False
    review_items: list[str] = []

    derivation_position_lines = computed_in_verification_positions(lines, tables)
    if derivation_position_lines:
        content_failed = True
        print(
            "DERIVATION_SEPARATION_FAIL\tCOMPUTED-FROM-RETRIEVED appears in a "
            "verification-state position\tlines="
            + ",".join(map(str, derivation_position_lines))
        )
    else:
        print("DERIVATION_SEPARATION_PASS\tDerivation mode is separate from verification state.")

    if missing:
        structural_failed = True
        for heading in missing:
            print(f"MISSING\t{heading}")
            variants = line_start_variants(lines, heading)
            if variants:
                print(
                    f"FORMAT_VARIANT\t{heading}\t"
                    f"line-start variants={','.join(str(i+1) for i in variants)}"
                )

    if duplicates:
        structural_failed = True
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
                structural_failed = True
                print(f"ORDER_FAIL\t{earlier} must appear before {later}")
            else:
                print(f"ORDER_PASS\t{earlier} precedes {later}")

    all_heading_lines = set(unique_line.values())
    thin_sections = []
    status_counts = {
        "N/A": 0,
        "PROVISIONAL": 0,
        "INCOMPLETE": 0,
        "COMPLETED_INFERRED": 0,
        "UNMARKED_THIN": 0,
    }
    bodies: dict[str, str] = {}

    for heading in REQUIRED:
        if heading not in unique_line:
            continue

        body = body_for(lines, unique_line[heading], all_heading_lines)
        bodies[heading] = body
        words = count_words(body)
        placeholder = any(pattern.match(body) for pattern in PLACEHOLDER_PATTERNS)
        clears_screen = words >= min_words and not placeholder
        status = classify_status(body, clears_screen)

        for label in status.split(","):
            if label in status_counts:
                status_counts[label] += 1

        if not clears_screen:
            structural_failed = True
            thin_sections.append((heading, words, status))
            print(f"PLACEHOLDER_SCREEN_FAIL\t{heading}\t{words} words\tstatus={status}")
        else:
            print(
                f"PLACEHOLDER_SCREEN_PASS\t{heading}\t{words} words\tstatus={status}"
            )

    # Completion Ledger cross-check.
    ledger_body = bodies.get("COMPLETION LEDGER", "")
    ledger_rows = parse_completion_ledger(ledger_body)

    if "COMPLETION LEDGER" not in unique_line:
        structural_failed = True
        print("LEDGER_ABSENT\tCompletion Ledger heading is missing.")
    else:
        for heading in REQUIRED:
            rows = ledger_rows.get(heading, [])
            actual_count = len(positions[heading])

            if not rows:
                structural_failed = True
                print(f"LEDGER_ROW_MISSING\t{heading}")
                continue

            if len(rows) > 1:
                structural_failed = True
                print(f"LEDGER_ROW_DUPLICATE\t{heading}\trows={len(rows)}")
                continue

            row = rows[0]
            actual_present = actual_count == 1

            if ledger_claims_present(row) and not actual_present:
                structural_failed = True
                print(
                    f"LEDGER_FALSE_PRESENT\t{heading}\t"
                    f"ledger={row['present']}/{row['status']}\tactual_count={actual_count}"
                )
            elif ledger_claims_absent(row) and actual_present:
                structural_failed = True
                print(
                    f"LEDGER_FALSE_ABSENT\t{heading}\t"
                    f"ledger={row['present']}/{row['status']}\tactual_count={actual_count}"
                )
            elif not ledger_claims_present(row) and not ledger_claims_absent(row):
                structural_failed = True
                print(
                    f"LEDGER_PRESENT_VALUE_INVALID\t{heading}\tvalue={row['present']}"
                )

            if ledger_claims_completed(row) and not actual_present:
                structural_failed = True
                print(
                    f"LEDGER_FALSE_COMPLETE\t{heading}\t"
                    f"status={row['status']}\tactual_count={actual_count}"
                )

            if ledger_claims_omitted(row) and actual_present:
                structural_failed = True
                print(
                    f"LEDGER_FALSE_OMITTED\t{heading}\t"
                    f"status={row['status']}\tactual_count={actual_count}"
                )

    # Gate-behavior cross-check.
    missing_gate_blocks = [heading for heading in GATE_REQUIRED if not positions[heading]]
    artifact10_body = bodies.get("ARTIFACT 10: FINAL VERDICT", "")
    if missing_gate_blocks:
        withheld = verdict_is_withheld(artifact10_body)
        incomplete_declared = incomplete_run_declared(text)

        if not withheld and not incomplete_declared:
            structural_failed = True
            print(
                "SILENT_OMISSION\tRequired block(s) are missing, no INCOMPLETE RUN "
                "declaration appears, and Artifact 10 was not withheld."
            )
        else:
            if withheld:
                print("GATE_PASS\tArtifact 10 withheld after required-block omission.")
            if incomplete_declared:
                print("INCOMPLETE_DECLARATION_PASS\tRequired omission was declared.")

        if not withheld:
            structural_failed = True
            print(
                "GATE_FAIL\tRequired block(s) missing but Artifact 10 was not "
                "explicitly withheld."
            )
        if not incomplete_declared:
            structural_failed = True
            print(
                "INCOMPLETE_DECLARATION_MISSING\tRequired omission was not declared "
                "with the mandated INCOMPLETE RUN line."
            )
    else:
        for label in ALWAYS_REQUIRED_CONTENT_LABELS:
            value = line_value(text, label)
            if value is None or not nonempty(value):
                content_failed = True
                print(f"CONTENT_FORM_FAIL\tmissing or empty\t{label}")

        risk_band_value = line_value(text, "RISK BAND:")
        if "WITHHELD" in (risk_band_value or "").upper() and not re.search(
            r"WITHHELD\s*[—–-]\s*\S", risk_band_value or ""
        ):
            content_failed = True
            print("RISK_BAND_FAIL\tWITHHELD requires an inline reason.")
        elif risk_band_value is not None and nonempty(risk_band_value):
            print("RISK_BAND_FORM_PASS\tExplicit disposition is present.")

        if check_source_lock(text, review_items):
            content_failed = True
        if check_source_classification(tables, review_items):
            content_failed = True
        aggregation_failed, internal_density_scored = check_scorecard(
            text, tables, review_items
        )
        if aggregation_failed:
            content_failed = True
        if check_graph_receipts(lines, internal_density_scored):
            content_failed = True

    print(
        "STATUS_SUMMARY\t"
        f"N/A={status_counts['N/A']}\t"
        f"PROVISIONAL={status_counts['PROVISIONAL']}\t"
        f"INCOMPLETE={status_counts['INCOMPLETE']}\t"
        f"COMPLETED_INFERRED={status_counts['COMPLETED_INFERRED']}\t"
        f"UNMARKED_THIN={status_counts['UNMARKED_THIN']}"
    )

    print(f"STRUCTURAL_RESULT\t{'FAIL' if structural_failed else 'PASS'}")
    if content_failed:
        print("CONTENT_RESULT\tFAIL")
    elif review_items:
        print(f"CONTENT_RESULT\tPASS-WITH-REVIEW\titems={len(review_items)}")
    else:
        print("CONTENT_RESULT\tPASS")

    for index, item in enumerate(review_items, start=1):
        print(f"REVIEW_ITEM_{index}\t{item}")

    if structural_failed or content_failed:
        print(
            "FAIL\tAt least one deterministic structural or content-form check failed; "
            f"targeted_review_items={len(review_items)}."
        )
        return 1

    if review_items:
        print(
            f"PASS-WITH-REVIEW: {len(review_items)} items\tAll deterministic checks "
            "passed; the listed substantive judgments remain for human review."
        )
        return 0

    print(
        "PASS\tAll deterministic structural and content-form checks passed; no "
        "targeted review item was generated."
    )
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
