"""Bounded citation-network Markdown grammar; all raw field values survive.

Only top-level standardized finding tables, Artifact 8 scorecards and explicit
source-lock lines are structured. Other audit text remains in the input receipt.
This parser does not infer a label from prose or translate old vocabularies.

Rule failures are CURRENT_CONTRACT_MISMATCH: they are relative to the grammar
implemented here, not to whatever instrument produced the output. Whether the
producing instrument was violated is decided per run, not by this parser.
"""

import re

# Bump VERSION whenever parse() output can change for the same input text;
# restore re-derives native records only for versions listed as supported.
NAME = "atlas-citation-network-native"
VERSION = "3"
SUPPORTED_VERSIONS = frozenset({VERSION})

FINAL = "FINAL SECTION: STANDARDIZED FINDING TABLE"
FIELDS = ("Finding", "Target claim", "What was measured", "What was claimed",
          "Failure mode", "Severity", "Concede test", "Scope loss if NARROWS",
          "Evidence", "Evidence type", "Verification state", "Possible innocent explanation",
          "What would weaken this", "Failure location", "Status")
VERIFICATION = {"LOCATED", "ABSTRACT-CONFIRMED", "FULL-TEXT-CONFIRMED",
                "RECEPTION-CONFIRMED", "CONTESTED", "REBUTTED", "PROVISIONAL",
                "CROSS-SOURCE-CONFIRMED"}
ENUMS = {"Concede test": {"SURVIVES", "NARROWS", "DEFEATS"},
         "Status": {"confirmed", "contested", "provisional"}}
PREFIX_ENUMS = {"Severity": {"none", "minor", "moderate", "major", "fatal-for-strong-claim"},
               "Failure location": {"PAPER", "CITATION", "PR-MEDIA", "MODEL-RETRIEVAL", "MIXED"}}
LOCK_FIELDS = ("SOURCE-LOCK METHOD", "SOURCE-LOCK DATABASE", "SOURCE-LOCK QUERY OR SOURCE LIST",
               "SOURCE-LOCK DATE CUTOFF", "SOURCE-LOCK RANKING RULE", "SOURCE-LOCK N",
               "SOURCE-LOCK DEDUPLICATION RULE", "SOURCE-LOCK TIMESTAMP OR HASH")
DIMENSIONS = {"Founding-cluster dominance", "Internal citation density", "Recent-paper dependence",
              "Review-hub laundering", "Proxy mismatch", "Claim mutation", "Adjacent-field neglect",
              "Lack of decisive tests", "Poor critique uptake", "Intervention-evidence ratchet",
              "Model non-updating"}


def issue(code, field, line=None):
    return {"code": code, "field": field, "line": line}


def top_level_lines(text):
    """Ignore fenced/quoted source blocks for grammar, without changing raw text."""
    fence = None
    for number, raw in enumerate(text.splitlines(), 1):
        stripped = raw.strip()
        match = re.match(r"^ {0,3}(`{3,}|~{3,})", raw)
        if match:
            marker = match[1]
            if fence is None:
                fence = marker
            elif marker[0] == fence[0] and len(marker) >= len(fence):
                fence = None
            continue
        if fence or raw.startswith(("    ", "\t")) or stripped.startswith(">"):
            continue
        yield number, stripped


def output_span(text, first_line, last_line):
    """Half-open code-point span of one-based lines, using the parser's line model.

    The last line's terminator is excluded; CRLF and other separators count as
    the characters they are.
    """
    lines = text.splitlines(keepends=True)
    start = sum(len(line) for line in lines[:first_line - 1])
    end = sum(len(line) for line in lines[:last_line - 1]) + len(lines[last_line - 1].splitlines()[0])
    return start, end


def cells(line):
    if not (line.startswith("|") and line.endswith("|")):
        return None
    return [s.strip().replace(r"\|", "|") for s in re.split(r"(?<!\\)\|", line[1:-1])]


def prefix_label(raw, values):
    for value in sorted(values, key=len, reverse=True):
        if raw == value or raw.startswith(value + " "):
            return value
    return None


def parse(text):
    lines = list(top_level_lines(text))
    errors = []
    starts = [i for i, (_, line) in enumerate(lines) if line == FINAL]
    if len(starts) != 1:
        errors.append(issue("MISSING" if not starts else "DUPLICATE_FIELD", FINAL))
        return {"findings": [], "issues": errors, "scorecard": [], "source_lock": {},
                "null_assertion": None, "semantic_review": "SEMANTIC_REVIEW_REQUIRED"}
    tail = lines[starts[0] + 1:]
    headers = [(i, int(m[1])) for i, (_, line) in enumerate(tail)
               if (m := re.fullmatch(r"Finding (\d+)", line))]
    findings, seen = [], set()
    for idx, (start, number) in enumerate(headers):
        end = headers[idx + 1][0] if idx + 1 < len(headers) else len(tail)
        block = tail[start:end]
        fields, field_lines, local = {}, {}, []
        if number in seen:
            local.append(issue("DUPLICATE_ID", f"Finding {number}", block[0][0]))
        seen.add(number)
        for line_no, line in block[1:]:
            row = cells(line)
            if row is None:
                if line.startswith("|"):
                    local.append(issue("PARTIAL_OUTPUT", "table row", line_no))
                continue
            if row == ["Field", "Entry"] or all(re.fullmatch(r":?-{3,}:?", x) for x in row):
                continue
            if len(row) != 2:
                local.append(issue("INVALID_TABLE", "finding row", line_no))
                continue
            key, value = row
            if key in fields:
                local.append(issue("DUPLICATE_FIELD", key, line_no))
                # Keep both occurrences in raw block; don't resolve the collision.
                continue
            fields[key], field_lines[key] = value, line_no
            if key not in FIELDS:
                local.append(issue("UNKNOWN_FIELD", key, line_no))
        labels = {}
        for field in FIELDS:
            if not fields.get(field):
                local.append(issue("MISSING", field, field_lines.get(field)))
        if "Status" not in fields:
            local.append(issue("PARTIAL_OUTPUT", "unterminated finding block", block[0][0]))
        for field, values in ENUMS.items():
            if fields.get(field):
                if fields[field] not in values:
                    local.append(issue("INVALID_LABEL", field, field_lines[field]))
                else:
                    labels[field] = fields[field]
        for field, values in PREFIX_ENUMS.items():
            if fields.get(field):
                value = prefix_label(fields[field], values)
                if value is None:
                    local.append(issue("INVALID_LABEL", field, field_lines[field]))
                else:
                    labels[field] = value
        if fields.get("Verification state"):
            states = [v.strip() for v in fields["Verification state"].split(";")]
            if any(v not in VERIFICATION for v in states) or len(set(states)) != len(states):
                local.append(issue("INVALID_LABEL", "Verification state", field_lines["Verification state"]))
            else:
                labels["Verification state"] = states
        if labels.get("Concede test") == "NARROWS":
            scope = prefix_label(fields.get("Scope loss if NARROWS", ""),
                                 {"incidental", "material", "near-defeat"})
            if not scope:
                local.append(issue("INVALID_LABEL", "Scope loss if NARROWS"))
        severe = labels.get("Severity") in {"major", "fatal-for-strong-claim"}
        if severe and (labels.get("Concede test") == "SURVIVES"
                       or "PROVISIONAL" in labels.get("Verification state", [])):
            local.append(issue("CURRENT_CONTRACT_MISMATCH", "severity/verification/concede consistency"))
        first, last = block[0][0], block[-1][0]
        raw_block = "\n".join(text.splitlines()[first - 1:last])
        findings.append({"number": number, "fields": fields, "labels": labels,
                         "field_lines": field_lines, "line_start": first, "line_end": last,
                         "raw_block": raw_block, "issues": local,
                         "semantic_review": "SEMANTIC_REVIEW_REQUIRED"})
        errors.extend(local)
    nulls = [(n, s) for n, s in tail if s == "No findings of consequence."]
    null_assertion = nulls[0][1] if len(nulls) == 1 else None
    if not findings and null_assertion is None:
        errors.append(issue("PARTIAL_OUTPUT", "no explicit finding or supported null assertion"))
    if findings and null_assertion:
        errors.append(issue("CONFLICTING_NULL_ASSERTION", FINAL))

    # Exact field names, including source-lock values, survive in the receipt.
    source_lock = {}
    for number, line in lines[:starts[0]]:
        for label in LOCK_FIELDS:
            if line.startswith(label + ":"):
                if label in source_lock:
                    errors.append(issue("DUPLICATE_FIELD", label, number))
                else:
                    source_lock[label] = line[len(label) + 1:].strip()
    for label in LOCK_FIELDS:
        if not source_lock.get(label):
            errors.append(issue("MISSING", label))
    if source_lock.get("SOURCE-LOCK METHOD") not in {None, "LOCKED QUERY", "LOCKED SOURCES", "POST HOC"}:
        errors.append(issue("INVALID_LABEL", "SOURCE-LOCK METHOD"))

    scorecard = []
    in_scorecard = False
    table_header = None
    for number, line in lines:
        if line == "ARTIFACT 8: CARTEL-RISK SCORECARD":
            in_scorecard = True
            continue
        if in_scorecard and line.startswith("ARTIFACT 9:"):
            break
        if not in_scorecard:
            continue
        row = cells(line)
        if row and row[0] == "Dimension":
            if table_header is not None:
                errors.append(issue("DUPLICATE_FIELD", "scorecard header", number))
            table_header = row
            if len(row) != len(set(row)):
                errors.append(issue("DUPLICATE_FIELD", "scorecard column", number))
            continue
        if not row or all(re.fullmatch(r":?-{3,}:?", x) for x in row):
            continue
        if not table_header or len(table_header) != len(row):
            errors.append(issue("INVALID_TABLE", "scorecard", number))
            continue
        fields = dict(zip(table_header, row))
        disposition = fields.get("Dimension disposition")
        if disposition not in {"UNASSESSED", "UNINFORMATIVE", "N/A", "SCORED 0", "SCORED 1", "SCORED 2", "SCORED 3"}:
            errors.append(issue("INVALID_LABEL", "Dimension disposition", number))
        if disposition and disposition.startswith("SCORED "):
            if fields.get("Score if SCORED") != disposition[-1]:
                errors.append(issue("CURRENT_CONTRACT_MISMATCH", "score disagrees with disposition", number))
            aggregation = fields.get("AGGREGATION STATUS", "")
            if aggregation != "INDEPENDENT" and not re.fullmatch(r"NESTED under \S.*", aggregation):
                errors.append(issue("INVALID_LABEL", "AGGREGATION STATUS", number))
        elif fields.get("Score if SCORED") not in {"", "—", "-", "N/A"}:
            errors.append(issue("CURRENT_CONTRACT_MISMATCH", "unscored dimension has numeric score", number))
        scorecard.append({"fields": fields, "line": number, "raw": line})
    names = [r["fields"].get("Dimension") for r in scorecard]
    if len(names) != len(set(names)):
        errors.append(issue("DUPLICATE_FIELD", "scorecard dimension"))
    for name in sorted(DIMENSIONS - set(names)):
        errors.append(issue("MISSING", "scorecard dimension: " + name))
    # Sorted: set iteration order varies with the per-process hash seed.
    for name in sorted(set(names) - DIMENSIONS, key=str):
        errors.append(issue("INVALID_LABEL", "scorecard dimension: " + str(name)))
    return {"findings": findings, "issues": errors, "scorecard": scorecard,
            "source_lock": source_lock, "null_assertion": null_assertion,
            "semantic_review": "SEMANTIC_REVIEW_REQUIRED"}
