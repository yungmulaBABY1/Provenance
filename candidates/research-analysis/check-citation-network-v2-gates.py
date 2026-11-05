#!/usr/bin/env python3
"""Candidate gate checker for the citation-network v2-candidate instrument.

NOT CANONICAL. Checks SECTION A0 (corpus register and source eligibility, Gate A)
and SECTION K0 (evidence sufficiency, Gate B) of an output, or of a fragment that
contains only those blocks. It does not replace or wrap the v1 checker
(prompts/research-analysis/check-citation-network-output.py); run both.

What it can establish: that the declared ledgers are internally consistent, that
every declared disposition matches the disposition recomputed from the declared
evidence, and that scores and findings rest only on inferences that pass. What it
cannot establish: that a passage marked INSPECTED exists, that a code is correct,
or that a sample is representative. Those stay with a reviewer.

Applicability: an output that does not contain the line
    INSTRUMENT VERSION: 2-citation-network v2-candidate
was not produced under this candidate, and these gates do not judge it. The
checker prints NOT_APPLICABLE and exits 3. With --require-v2 (for callers whose
run record says the producing instrument is the candidate) the missing line FAILs.

Exit codes: 0 PASS or PASS-WITH-REVIEW; 1 FAIL; 2 usage error; 3 NOT_APPLICABLE.
Output lines are tab-separated. Review items use the v1 checker's format,
REVIEW_ITEM_<n>\t<CODE> — <detail>, so existing review tooling can read them.
"""
from __future__ import annotations

import argparse
import re
import sys
from dataclasses import dataclass, field
from pathlib import Path

VERSION_LINE = "INSTRUMENT VERSION: 2-citation-network v2-candidate"

RELEVANCE = {"DIRECT", "ADJACENT", "BACKGROUND", "UNRELATED", "UNKNOWN"}
RELATION = {"SUPPORTS", "CHALLENGES", "QUALIFIES", "PREMISE", "MENTIONS", "REUSES",
            "CITES-UNINSPECTED", "NOT-CITING", "UNKNOWN"}
USE_RELATIONS = {"SUPPORTS", "CHALLENGES", "QUALIFIES", "PREMISE", "MENTIONS"}
CONTRIBUTION = {"INDEPENDENT-DATA", "SHARED-DATA", "REANALYSIS", "THEORY", "REVIEW",
                "METHOD", "COMMENTARY", "NONE", "UNKNOWN"}
ACCESS = {"FULL-TEXT", "EXCERPT", "ABSTRACT", "METADATA", "INACCESSIBLE"}
CONTEXT = {"INSPECTED", "NOT-INSPECTED", "VERSION-MISMATCH", "NOT-APPLICABLE"}
ROLES = {"RECEPTION", "ADJUDICATION"}

CLASSES = {"GRAPH-STRUCTURE", "CO-CITATION", "DATABASE-RECORD", "COMPOSITION",
           "CITATION-USE", "ENGAGEMENT", "RESTATEMENT", "DATA-ORIGIN", "SOURCE-RESULT",
           "ABSENCE"}
SCOPES = {"NAMED", "WITHIN-SAMPLE", "CORPUS", "POPULATION", "LITERATURE"}
SAMPLING = {"EXHAUSTIVE", "PRESPECIFIED-RANDOM", "PRESPECIFIED-RULE", "CONVENIENCE",
            "NOT-APPLICABLE"}
DISPOSITIONS = {"SUPPORTED", "SUPPORTED-WITHIN-SAMPLE", "INSUFFICIENT", "NOT-ASSESSED"}
PASSING = {"SUPPORTED", "SUPPORTED-WITHIN-SAMPLE"}
METADATA_CLASSES = {"GRAPH-STRUCTURE", "CO-CITATION", "DATABASE-RECORD"}

# Minimum Source access for each member used, by class. None = any access except
# INACCESSIBLE. CITATION-USE and ENGAGEMENT have extra conditions below.
MEMBER_ACCESS = {
    "GRAPH-STRUCTURE": None, "CO-CITATION": None, "DATABASE-RECORD": None,
    "COMPOSITION": None, "CITATION-USE": None, "ABSENCE": None,
    "ENGAGEMENT": {"FULL-TEXT"},
    "RESTATEMENT": {"FULL-TEXT", "EXCERPT"},
    "DATA-ORIGIN": {"FULL-TEXT", "ABSTRACT"},
    "SOURCE-RESULT": {"FULL-TEXT", "ABSTRACT"},
}

DIMENSIONS = [
    "founding-cluster dominance", "internal citation density", "recent-paper dependence",
    "review-hub laundering", "proxy mismatch", "claim mutation", "adjacent-field neglect",
    "lack of decisive tests", "poor critique uptake", "intervention-evidence ratchet",
    "model non-updating",
]
DIMENSION_CLASSES = {
    "internal citation density": {"GRAPH-STRUCTURE"},
    "founding-cluster dominance": {"GRAPH-STRUCTURE", "CO-CITATION", "DATABASE-RECORD"},
    "recent-paper dependence": {"CITATION-USE", "GRAPH-STRUCTURE", "CO-CITATION"},
    "review-hub laundering": {"RESTATEMENT"},
    "claim mutation": {"RESTATEMENT"},
    "proxy mismatch": {"RESTATEMENT", "CITATION-USE", "SOURCE-RESULT"},
    "lack of decisive tests": {"ABSENCE", "SOURCE-RESULT"},
    "poor critique uptake": {"ENGAGEMENT"},
}
CO_CITATION_REVIEW_DIMENSIONS = {"poor critique uptake", "adjacent-field neglect"}
DISPOSITION_RE = re.compile(r"^(SCORED [0-3]|UNASSESSED|UNINFORMATIVE|N/A)$")
FINDING_STATUSES = {"confirmed", "contested", "provisional"}
EMPTY = {"", "—", "-"}

REGISTER_LABELS = ["CORPUS ROLE", "CORPUS QUESTION", "CORPUS SELECTION RULE",
                   "CORPUS DISCOVERY", "SELECTED ON TARGET CITATION", "CORPUS SIZE"]


@dataclass
class Corpus:
    cid: str
    line: int
    labels: dict = field(default_factory=dict)

    @property
    def role(self) -> str:
        return self.labels.get("CORPUS ROLE", "").strip()

    @property
    def searched(self) -> bool:
        return self.labels.get("CORPUS DISCOVERY", "").strip().upper().startswith("SEARCHED")

    @property
    def selected_on_target(self) -> bool:
        return self.labels.get("SELECTED ON TARGET CITATION", "").strip().upper() == "YES"


@dataclass
class Source:
    sid: str
    line: int
    membership: list
    relevance: str
    relation: list
    contribution: str
    access: str
    context: str
    supported: str


@dataclass
class Inference:
    iid: str
    line: int
    klass: str
    corpus: str
    scope: str
    sampling: str
    members: str
    disposition: str
    statement: str


class Report:
    def __init__(self) -> None:
        self.failures: list[str] = []
        self.reviews: list[str] = []
        self.info: list[str] = []

    def fail(self, code: str, detail: str) -> None:
        self.failures.append(f"GATE_FAIL\t{code}\t{detail}")

    def review(self, code: str, detail: str) -> None:
        self.reviews.append((code, detail))

    def note(self, text: str) -> None:
        self.info.append(f"INFO\t{text}")


def cells(line: str) -> list[str] | None:
    stripped = line.strip()
    if not (stripped.startswith("|") and stripped.endswith("|")):
        return None
    return [c.strip() for c in stripped[1:-1].split("|")]


def is_separator(row: list[str]) -> bool:
    return all(re.fullmatch(r":?-{3,}:?", c) for c in row if c)


def find_table(lines: list[str], headers: list[str]) -> list[tuple[int, list[str]]] | None:
    """Return the rows of the first table whose header row equals `headers`."""
    want = [h.casefold() for h in headers]
    for index, line in enumerate(lines):
        row = cells(line)
        if row is None or [c.casefold() for c in row] != want:
            continue
        rows = []
        for offset, body in enumerate(lines[index + 1:], start=index + 2):
            parsed = cells(body)
            if parsed is None:
                break
            if is_separator(parsed):
                continue
            rows.append((offset, parsed))
        return rows
    return None


def head(value: str) -> str:
    """First token of a coded cell: 'DIRECT (L3)' -> 'DIRECT'."""
    return value.split("(")[0].strip().split()[0] if value.strip() else ""


def parse_register(lines: list[str], report: Report) -> dict[str, Corpus]:
    corpora: dict[str, Corpus] = {}
    current: Corpus | None = None
    for number, line in enumerate(lines, start=1):
        match = re.match(r"^CORPUS ID:\s*(\S+)\s*$", line.strip())
        if match:
            cid = match[1]
            if cid in corpora:
                report.fail("DUPLICATE_CORPUS", f"{cid} line {number}")
            current = corpora.setdefault(cid, Corpus(cid, number))
            continue
        if current is None:
            continue
        label = next((lab for lab in REGISTER_LABELS if line.strip().startswith(lab + ":")), None)
        if label:
            current.labels[label] = line.strip()[len(label) + 1:].strip()
        elif line.strip().startswith("SOURCE ELIGIBILITY LEDGER") or line.startswith("|"):
            current = None
    return corpora


def parse_sources(lines: list[str], report: Report) -> dict[str, Source]:
    rows = find_table(lines, ["Source", "Corpus membership", "Question relevance",
                              "Relation to target", "Evidence contribution", "Source access",
                              "Citation context", "Supported inference"])
    sources: dict[str, Source] = {}
    if rows is None:
        report.fail("LEDGER_MISSING", "SOURCE ELIGIBILITY LEDGER table not found")
        return sources
    for number, row in rows:
        if len(row) != 8:
            report.fail("LEDGER_ROW", f"line {number}: expected 8 cells, found {len(row)}")
            continue
        sid = row[0].split()[0] if row[0].split() else ""
        if not sid:
            report.fail("LEDGER_ROW", f"line {number}: empty source identifier")
            continue
        if sid in sources:
            report.fail("DUPLICATE_SOURCE", f"{sid} lines {sources[sid].line} and {number}: "
                        "record a source once, with every corpus in Corpus membership")
            continue
        sources[sid] = Source(
            sid, number, [m.strip() for m in row[1].split("+") if m.strip()], head(row[2]),
            [r.strip() for r in head_list(row[3])], head(row[4]), head(row[5]), head(row[6]),
            row[7])
    return sources


def head_list(value: str) -> list[str]:
    base = value.split("(")[0]
    return [part.strip() for part in base.split("+") if part.strip()]


def check_sources(sources: dict[str, Source], corpora: dict[str, Corpus],
                  report: Report) -> None:
    metadata_coded = []
    for s in sources.values():
        where = f"{s.sid} line {s.line}"
        for name, value, vocab in (("Question relevance", s.relevance, RELEVANCE),
                                   ("Evidence contribution", s.contribution, CONTRIBUTION),
                                   ("Source access", s.access, ACCESS),
                                   ("Citation context", s.context, CONTEXT)):
            if value not in vocab:
                report.fail("VOCABULARY", f"{where}: {name} {value!r}")
        for rel in s.relation:
            if rel not in RELATION:
                report.fail("VOCABULARY", f"{where}: Relation to target {rel!r}")
        for member in s.membership:
            if member != "OUTSIDE" and member not in corpora:
                report.fail("UNREGISTERED_CORPUS", f"{where}: {member}")
        if "OUTSIDE" in s.membership and len(s.membership) > 1:
            report.fail("MEMBERSHIP", f"{where}: OUTSIDE cannot be combined with a corpus")
        uses = sorted(set(s.relation) & USE_RELATIONS)
        if uses and s.context != "INSPECTED":
            report.fail("USE_WITHOUT_CONTEXT", f"{where}: {'+'.join(uses)} with Citation "
                        f"context {s.context}; use CITES-UNINSPECTED")
        if s.context == "INSPECTED" and s.access not in {"FULL-TEXT", "EXCERPT"}:
            report.fail("CONTEXT_WITHOUT_ACCESS", f"{where}: INSPECTED with access {s.access}")
        if "REUSES" in s.relation and s.access not in {"FULL-TEXT", "ABSTRACT"}:
            report.fail("REUSE_WITHOUT_ACCESS", f"{where}: REUSES with access {s.access}")
        if s.context == "NOT-APPLICABLE" and "NOT-CITING" not in s.relation:
            report.fail("CONTEXT_STATE", f"{where}: NOT-APPLICABLE requires NOT-CITING")
        if "NOT-CITING" in s.relation:
            for member in s.membership:
                corpus = corpora.get(member)
                if corpus and corpus.selected_on_target:
                    report.fail("NOT_CITING_IN_TARGET_CORPUS",
                                f"{where}: {member} is SELECTED ON TARGET CITATION")
        if s.access in {"METADATA", "INACCESSIBLE"} and (
                s.relevance not in {"UNKNOWN", ""} or s.contribution not in {"UNKNOWN", ""}):
            metadata_coded.append(s.sid)
    if metadata_coded:
        report.review("CODED_FROM_METADATA", f"{len(metadata_coded)} rows carry a relevance "
                      "or contribution code from METADATA-only access; confirm each record "
                      f"shows it: {', '.join(metadata_coded)}")


def members_of(corpus_id: str, sources: dict[str, Source]) -> list[Source]:
    return [s for s in sources.values() if corpus_id in s.membership]


def check_register(lines: list[str], corpora: dict[str, Corpus],
                   sources: dict[str, Source], report: Report) -> None:
    if not corpora:
        report.fail("REGISTER_MISSING", "no CORPUS ID entries found")
    if not any(c.role == "ADJUDICATION" for c in corpora.values()):
        report.fail("ADJUDICATION_CORPUS_MISSING", "register an ADJUDICATION corpus, with "
                    "CORPUS DISCOVERY: NONE if no adjudication search was run")
    for c in corpora.values():
        for label in REGISTER_LABELS:
            if not c.labels.get(label):
                report.fail("REGISTER_FIELD", f"{c.cid}: {label} missing or empty")
        if c.role and c.role not in ROLES:
            report.fail("VOCABULARY", f"{c.cid}: CORPUS ROLE {c.role!r}")
        discovery = c.labels.get("CORPUS DISCOVERY", "").upper()
        if discovery and not (discovery.startswith("SEARCHED") or discovery.startswith("NONE")):
            report.fail("VOCABULARY", f"{c.cid}: CORPUS DISCOVERY must begin SEARCHED or NONE")
        selected = c.labels.get("SELECTED ON TARGET CITATION", "").upper()
        if selected and selected not in {"YES", "NO"}:
            report.fail("VOCABULARY", f"{c.cid}: SELECTED ON TARGET CITATION {selected!r}")
        size = c.labels.get("CORPUS SIZE", "")
        actual = len(members_of(c.cid, sources))
        if not re.fullmatch(r"\d+", size or ""):
            report.fail("REGISTER_FIELD", f"{c.cid}: CORPUS SIZE {size!r} is not a count")
        elif int(size) != actual:
            report.fail("CORPUS_SIZE_MISMATCH", f"{c.cid}: declared {size}, ledger rows {actual}")
    seen = set()
    for number, line in enumerate(lines, start=1):
        match = re.search(r"CITATION CONTEXT COVERAGE:\s*(\S+)\s+(\d+)\s*/\s*(\d+)", line)
        if not match:
            continue
        cid, k, n = match[1], int(match[2]), int(match[3])
        seen.add(cid)
        if cid not in corpora:
            report.fail("UNREGISTERED_CORPUS", f"coverage line {number}: {cid}")
            continue
        members = members_of(cid, sources)
        inspected = sum(1 for s in members if s.context == "INSPECTED")
        if (k, n) != (inspected, len(members)):
            report.fail("COVERAGE_MISMATCH", f"line {number}: {cid} declared {k}/{n}, ledger "
                        f"{inspected}/{len(members)} (VERSION-MISMATCH is not inspected)")
    for cid in corpora:
        if cid not in seen:
            report.fail("COVERAGE_LINE_MISSING", f"{cid}: no CITATION CONTEXT COVERAGE line")


def parse_inferences(lines: list[str], report: Report) -> dict[str, Inference]:
    rows = find_table(lines, ["Inference", "Class", "Corpus", "Claimed scope", "Sampling rule",
                              "Members used", "Disposition", "Statement"])
    inferences: dict[str, Inference] = {}
    if rows is None:
        report.fail("INFERENCE_LEDGER_MISSING", "INFERENCE LEDGER table not found")
        return inferences
    for number, row in rows:
        if len(row) != 8:
            report.fail("INFERENCE_ROW", f"line {number}: expected 8 cells, found {len(row)}")
            continue
        inf = Inference(row[0], number, *row[1:])
        if inf.iid in inferences:
            report.fail("DUPLICATE_INFERENCE", f"{inf.iid} line {number}")
            continue
        for name, value, vocab in (("Class", inf.klass, CLASSES), ("Claimed scope", inf.scope,
                                   SCOPES), ("Sampling rule", inf.sampling, SAMPLING),
                                   ("Disposition", inf.disposition, DISPOSITIONS)):
            if value not in vocab:
                report.fail("VOCABULARY", f"{inf.iid} line {number}: {name} {value!r}")
        inferences[inf.iid] = inf
    return inferences


def composition_lines(lines: list[str]) -> dict[str, tuple[int, str, dict, int]]:
    found = {}
    pattern = re.compile(r"^COMPOSITION:\s*(\S+)\s*\|\s*(\w+)\s*\|\s*(.+?)\s*\|\s*TOTAL=(\d+)\s*$")
    for number, line in enumerate(lines, start=1):
        match = pattern.match(line.strip())
        if match:
            counts = {}
            for part in match[3].split(";"):
                if "=" in part:
                    key, value = part.split("=", 1)
                    counts[key.strip()] = int(value.strip()) if value.strip().isdigit() else -1
            found[match[1]] = (number, match[2].lower(), counts, int(match[4]))
    return found


def resolve_members(inf: Inference, corpora: dict[str, Corpus], sources: dict[str, Source]
                    ) -> tuple[list[Source] | None, list[str]]:
    problems = []
    value = inf.members.strip()
    upper = value.upper()
    if inf.scope == "POPULATION":
        return [], problems
    if upper in {"ALL", "INSPECTED"}:
        corpus = corpora.get(inf.corpus)
        if corpus is None:
            return None, [f"Members used {upper} needs a registered corpus, found {inf.corpus!r}"]
        members = members_of(corpus.cid, sources)
        if upper == "INSPECTED":
            members = [s for s in members if s.context == "INSPECTED"]
        return members, problems
    members = []
    for sid in [part.strip() for part in value.split(",") if part.strip()]:
        if sid not in sources:
            problems.append(f"member {sid} is not in the eligibility ledger")
        else:
            members.append(sources[sid])
    return members, problems


def recompute(inf: Inference, corpora: dict[str, Corpus], sources: dict[str, Source],
              compositions: dict, report: Report) -> tuple[str, list[str]]:
    """Return the disposition the declared evidence supports, and the reasons."""
    reasons: list[str] = []
    corpus = corpora.get(inf.corpus)
    if inf.corpus not in {"POPULATION", "—", "-"} and corpus is None:
        reasons.append(f"corpus {inf.corpus!r} is not registered")
    members, problems = resolve_members(inf, corpora, sources)
    reasons += problems
    if members is None:
        return "INSUFFICIENT", reasons
    scope = inf.scope

    if scope == "POPULATION":
        if inf.klass not in {"CO-CITATION", "DATABASE-RECORD"}:
            reasons.append(f"POPULATION scope is for CO-CITATION and DATABASE-RECORD, not "
                           f"{inf.klass}")
        if not re.search(r"\d+\s*/\s*\d+", inf.statement):
            reasons.append("POPULATION statement gives no k/n count")
        if not re.match(r"^(UNSCREENED|SCREENED:\s*\S.*)$", inf.members.strip()):
            reasons.append("POPULATION Members used must be UNSCREENED or SCREENED: [rule]")
        return ("INSUFFICIENT" if reasons else "SUPPORTED"), reasons

    if scope in {"CORPUS", "LITERATURE"} and inf.members.strip().upper() != "ALL":
        if not (inf.klass in {"CITATION-USE", "ENGAGEMENT"}
                and inf.sampling == "PRESPECIFIED-RANDOM" and scope == "CORPUS"):
            reasons.append(f"{scope} scope requires Members used ALL")
    if not members and inf.klass != "ABSENCE":
        reasons.append("no members used")

    if scope == "LITERATURE":
        allowed = {"ABSENCE", "COMPOSITION", "DATA-ORIGIN", "GRAPH-STRUCTURE"}
        if inf.klass not in allowed:
            reasons.append(f"{inf.klass} cannot claim LITERATURE scope")
        elif corpus is None:
            reasons.append("LITERATURE scope needs a registered corpus")
        elif inf.klass == "GRAPH-STRUCTURE":
            if corpus.selected_on_target or not corpus.searched:
                reasons.append("graph statements beyond the corpus need a corpus not selected "
                               "on target citation and SEARCHED")
        elif corpus.role != "ADJUDICATION" or not corpus.searched:
            reasons.append(f"{inf.klass} at LITERATURE scope needs an ADJUDICATION corpus with "
                           f"CORPUS DISCOVERY: SEARCHED ({corpus.cid} is {corpus.role}, "
                           f"{'SEARCHED' if corpus.searched else 'NONE'})")

    if inf.klass == "ABSENCE":
        if scope != "LITERATURE":
            reasons.append("ABSENCE is a LITERATURE-scope inference")
        if corpus is not None and (corpus.role != "ADJUDICATION" or not corpus.searched):
            reasons.append("ABSENCE needs an ADJUDICATION corpus that was SEARCHED")
        unknown = [s.sid for s in members if s.relevance == "UNKNOWN"]
        if unknown:
            reasons.append(f"ABSENCE with {len(unknown)} unscreened members (relevance "
                           f"UNKNOWN): {', '.join(unknown[:6])}{' ...' if len(unknown) > 6 else ''}")
        if inf.sampling not in {"EXHAUSTIVE", "PRESPECIFIED-RULE"}:
            reasons.append("ABSENCE needs the whole search result set (EXHAUSTIVE or "
                           "PRESPECIFIED-RULE)")

    if (scope == "CORPUS" and inf.klass in {"CITATION-USE", "ENGAGEMENT"}
            and inf.sampling == "PRESPECIFIED-RANDOM"):
        # A listed random sample may stand for the corpus; otherwise Members used must be
        # ALL (checked above) and every member must meet the minimum (checked below).
        report.review("SAMPLE_DECLARED_RANDOM", f"{inf.iid}: confirm the inspected sample "
                      "was drawn at random before inspection and that the statement is an "
                      "estimate with its uncertainty")

    need = MEMBER_ACCESS.get(inf.klass)
    short = []
    for s in members:
        if s.access == "INACCESSIBLE":
            short.append(f"{s.sid} INACCESSIBLE")
        elif need is not None and s.access not in need:
            short.append(f"{s.sid} access {s.access}")
        if inf.klass == "CITATION-USE" and s.context != "INSPECTED":
            short.append(f"{s.sid} context {s.context}")
        if inf.klass == "ENGAGEMENT" and s.relevance not in {"DIRECT", "ADJACENT"}:
            short.append(f"{s.sid} relevance {s.relevance} (engagement not expected)")
    if short:
        shown = "; ".join(short[:6]) + (f"; and {len(short) - 6} more" if len(short) > 6 else "")
        reasons.append(f"{inf.klass} evidence below minimum for {len(short)} of "
                       f"{len(members)} members: {shown}")

    if inf.klass == "COMPOSITION":
        reasons += check_composition(inf, members, compositions)

    if reasons:
        return "INSUFFICIENT", reasons
    return ("SUPPORTED-WITHIN-SAMPLE" if scope == "WITHIN-SAMPLE" else "SUPPORTED"), reasons


def check_composition(inf: Inference, members: list[Source], compositions: dict) -> list[str]:
    entry = compositions.get(inf.iid)
    if entry is None:
        return ["no COMPOSITION line"]
    number, column, counts, total = entry
    attribute = {"relevance": "relevance", "contribution": "contribution", "access": "access",
                 "context": "context"}.get(column)
    if attribute is None:
        return [f"COMPOSITION line {number}: unknown column {column!r}"]
    actual: dict[str, int] = {}
    for s in members:
        key = getattr(s, attribute)
        actual[key] = actual.get(key, 0) + 1
    problems = []
    if total != len(members):
        problems.append(f"COMPOSITION line {number}: TOTAL={total}, members {len(members)}")
    for key in sorted(set(actual) | {k for k, v in counts.items() if v}):
        if counts.get(key, 0) != actual.get(key, 0):
            problems.append(f"COMPOSITION line {number}: {key}={counts.get(key, 0)}, ledger "
                            f"{actual.get(key, 0)} (UNKNOWN is counted, never dropped)")
    return problems


def check_inferences(inferences: dict[str, Inference], corpora: dict[str, Corpus],
                     sources: dict[str, Source], compositions: dict,
                     report: Report) -> dict[str, str]:
    recomputed = {}
    for inf in inferences.values():
        actual, reasons = recompute(inf, corpora, sources, compositions, report)
        recomputed[inf.iid] = actual
        declared = inf.disposition
        why = "; ".join(reasons) if reasons else "evidence meets the minimum"
        if declared in PASSING and actual == "INSUFFICIENT":
            report.fail("INFERENCE_OVERCLAIMED", f"{inf.iid} ({inf.klass}, {inf.scope}) "
                        f"declared {declared}: {why}")
        elif declared in PASSING and actual != declared:
            report.fail("DISPOSITION_MISMATCH", f"{inf.iid}: declared {declared}, evidence "
                        f"supports {actual}")
        elif declared == "INSUFFICIENT" and actual in PASSING:
            report.review("OVER_WITHHELD", f"{inf.iid} ({inf.klass}) declared INSUFFICIENT but "
                          "its declared evidence meets the minimum; confirm the stated reason")
        report.note(f"inference {inf.iid}\t{inf.klass}\t{inf.scope}\tdeclared {declared}\t"
                    f"recomputed {actual}")
    for iid, entry in compositions.items():
        if iid not in inferences:
            report.fail("COMPOSITION_ORPHAN", f"COMPOSITION line {entry[0]}: no inference {iid}")
    return recomputed



def split_ids(value: str) -> list[str]:
    if value.strip() in EMPTY:
        return []
    return [part.strip() for part in re.split(r"[,;]", value) if part.strip()]


def check_dimensions(lines: list[str], inferences: dict[str, Inference], recomputed: dict,
                     corpora: dict[str, Corpus], report: Report) -> dict[str, str]:
    rows = find_table(lines, ["Scorecard dimension", "Scorecard disposition", "Inference IDs",
                              "Basis note"])
    dispositions: dict[str, str] = {}
    if rows is None:
        report.fail("DIMENSION_BASIS_MISSING", "DIMENSION EVIDENCE BASIS table not found")
        return dispositions
    for number, row in rows:
        if len(row) != 4:
            report.fail("DIMENSION_ROW", f"line {number}: expected 4 cells")
            continue
        name, disposition, ids, note = row
        key = name.strip().casefold()
        if key not in DIMENSIONS:
            report.fail("DIMENSION_ROW", f"line {number}: unknown dimension {name!r}")
            continue
        if key in dispositions:
            report.fail("DIMENSION_ROW", f"line {number}: {name} listed twice")
            continue
        dispositions[key] = disposition
        if not DISPOSITION_RE.match(disposition):
            report.fail("VOCABULARY", f"line {number}: Scorecard disposition {disposition!r}")
            continue
        listed = split_ids(ids)
        unknown = [i for i in listed if i not in inferences]
        if unknown:
            report.fail("UNKNOWN_INFERENCE", f"{name}: {', '.join(unknown)}")
        listed = [i for i in listed if i in inferences]
        if disposition.startswith("SCORED"):
            if not listed:
                report.fail("SCORED_WITHOUT_BASIS", f"{name} is {disposition} with no listed "
                            "inference")
                continue
            weak = [i for i in listed if recomputed.get(i) not in PASSING
                    or inferences[i].disposition not in PASSING]
            if weak:
                report.fail("SCORED_ON_INSUFFICIENT", f"{name} is {disposition} but relies on "
                            f"{', '.join(weak)}; mark it UNASSESSED or list only passing "
                            "inferences")
            required = DIMENSION_CLASSES.get(key)
            if required and not any(inferences[i].klass in required for i in listed):
                report.fail("DIMENSION_CLASS_MISSING", f"{name} needs one of "
                            f"{', '.join(sorted(required))}")
            score = int(disposition.split()[1])
            if key in CO_CITATION_REVIEW_DIMENSIONS and score > 0:
                for i in listed:
                    inf = inferences[i]
                    if inf.klass == "CO-CITATION" and inf.members.strip().upper() == "UNSCREENED":
                        report.review("CO_CITATION_UNSCREENED", f"{name} {disposition} uses {i}, "
                                      "a co-citation rate over an unscreened population; "
                                      "confirm engagement was expected of that population")
            if key == "recent-paper dependence":
                for i in listed:
                    inf = inferences[i]
                    corpus = corpora.get(inf.corpus)
                    by_construction = (inf.corpus == "POPULATION"
                                       or (corpus is not None and corpus.selected_on_target))
                    if inf.klass in {"GRAPH-STRUCTURE", "CO-CITATION"} and by_construction:
                        report.review("BY_CONSTRUCTION_RISK", f"{name} uses {i} on a set "
                                      "selected on target citation; confirm it measures "
                                      "citation beyond the target")
        else:
            if listed:
                report.fail("UNSCORED_WITH_BASIS", f"{name} is {disposition} but lists "
                            f"{', '.join(listed)}; list the inferences in the basis note")
            if note.strip() in EMPTY:
                report.fail("BASIS_NOTE_MISSING", f"{name} is {disposition}: state what is "
                            "missing and what would make it assessable")
    missing = [d for d in DIMENSIONS if d not in dispositions]
    if missing:
        report.fail("DIMENSION_ROWS", f"missing rows: {', '.join(missing)}")
    applicable = [d for d, v in dispositions.items() if v != "N/A"]
    scored = [d for d, v in dispositions.items() if v.startswith("SCORED")]
    report.note(f"dimensions SCORED after gates\t{len(scored)}/{len(applicable)} applicable")
    return dispositions


def check_scorecard_agreement(lines: list[str], dispositions: dict, report: Report) -> None:
    for index, line in enumerate(lines):
        row = cells(line)
        if not row:
            continue
        lowered = [c.casefold() for c in row]
        if "dimension" in lowered and "dimension disposition" in lowered:
            d_col, s_col = lowered.index("dimension"), lowered.index("dimension disposition")
            for number, body in enumerate(lines[index + 1:], start=index + 2):
                parsed = cells(body)
                if parsed is None:
                    break
                if is_separator(parsed) or len(parsed) <= max(d_col, s_col):
                    continue
                key = parsed[d_col].strip().casefold()
                if key in dispositions and parsed[s_col].strip() != dispositions[key]:
                    report.fail("SCORECARD_DISAGREES", f"line {number}: Artifact 8 has "
                                f"{parsed[s_col].strip()!r} for {parsed[d_col]}, basis table "
                                f"has {dispositions[key]!r}")
            return
    report.note("Artifact 8 scorecard not present; basis table checked alone")


def check_findings(lines: list[str], inferences: dict[str, Inference], recomputed: dict,
                   report: Report) -> None:
    rows = find_table(lines, ["Finding", "Finding status", "Inference IDs"])
    if rows is None:
        report.fail("FINDING_BASIS_MISSING", "FINDING EVIDENCE BASIS table not found")
        return
    listed = set()
    for number, row in rows:
        if len(row) != 3:
            report.fail("FINDING_ROW", f"line {number}: expected 3 cells")
            continue
        name, status, ids = row
        listed.add(name.strip())
        if status.strip().lower() not in FINDING_STATUSES:
            report.fail("VOCABULARY", f"line {number}: Finding status {status!r}")
            continue
        used = split_ids(ids)
        unknown = [i for i in used if i not in inferences]
        if unknown:
            report.fail("UNKNOWN_INFERENCE", f"{name}: {', '.join(unknown)}")
        used = [i for i in used if i in inferences]
        if not used:
            report.fail("FINDING_WITHOUT_BASIS", f"{name} ({status}) lists no inference")
            continue
        if status.strip().lower() in {"confirmed", "contested"}:
            weak = [i for i in used if recomputed.get(i) not in PASSING
                    or inferences[i].disposition not in PASSING]
            if weak:
                report.fail("FINDING_ON_INSUFFICIENT", f"{name} is {status} but relies on "
                            f"{', '.join(weak)}")
    table_findings = {f"Finding {m[1]}" for line in lines
                      if (m := re.fullmatch(r"Finding (\d+)", line.strip()))}
    if table_findings:
        for name in sorted(table_findings - listed):
            report.fail("FINDING_ROWS", f"{name} has no FINDING EVIDENCE BASIS row")
        for name in sorted(listed - table_findings):
            report.fail("FINDING_ROWS", f"{name} is not in the standardized finding table")


def run(text: str, require_v2: bool) -> tuple[int, list[str]]:
    lines = text.splitlines()
    out: list[str] = []
    if not any(line.strip() == VERSION_LINE for line in lines):
        if require_v2:
            out.append(f"GATE_FAIL\tVERSION_LINE_MISSING\t{VERSION_LINE}")
            out.append("V2_GATES_RESULT\tFAIL\tfailures=1")
            return 1, out
        out.append("NOT_APPLICABLE\toutput does not declare the v2-candidate instrument; "
                   "these gates do not judge outputs of other versions")
        return 3, out
    report = Report()
    corpora = parse_register(lines, report)
    sources = parse_sources(lines, report)
    check_sources(sources, corpora, report)
    check_register(lines, corpora, sources, report)
    compositions = composition_lines(lines)
    inferences = parse_inferences(lines, report)
    recomputed = check_inferences(inferences, corpora, sources, compositions, report)
    dispositions = check_dimensions(lines, inferences, recomputed, corpora, report)
    if dispositions:
        check_scorecard_agreement(lines, dispositions, report)
    check_findings(lines, inferences, recomputed, report)
    for c in corpora.values():
        members = members_of(c.cid, sources)
        inspected = sum(1 for s in members if s.context == "INSPECTED")
        report.note(f"corpus {c.cid}\t{c.role}\tmembers {len(members)}\tcontexts inspected "
                    f"{inspected}\tdiscovery {'SEARCHED' if c.searched else 'NONE'}")
    out += report.info
    out += report.failures
    for number, (code, detail) in enumerate(report.reviews, start=1):
        out.append(f"REVIEW_ITEM_{number}\t{code} — {detail}")
    if report.failures:
        out.append(f"V2_GATES_RESULT\tFAIL\tfailures={len(report.failures)}")
        return 1, out
    if report.reviews:
        out.append(f"V2_GATES_RESULT\tPASS-WITH-REVIEW\titems={len(report.reviews)}")
        return 0, out
    out.append("V2_GATES_RESULT\tPASS")
    return 0, out


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("path")
    parser.add_argument("--require-v2", action="store_true",
                        help="fail, rather than skip, an output without the version line")
    args = parser.parse_args()
    try:
        text = Path(args.path).read_text(encoding="utf-8")
    except OSError as error:
        print(f"USAGE_ERROR\t{error}")
        return 2
    code, out = run(text, args.require_v2)
    print("\n".join(out))
    return code


if __name__ == "__main__":
    sys.exit(main())
