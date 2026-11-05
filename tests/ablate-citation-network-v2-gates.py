#!/usr/bin/env python3
"""Rule ablation for the candidate v2 gate checker (FAIL-CN-007).

For each named rule, copy the checker to a temporary directory, disable that one rule, and run
tests/test-citation-network-v2-gates.py against the copy. A rule whose removal leaves the suite
passing has no test that depends on it. The committed checker is never modified.

    python3 tests/ablate-citation-network-v2-gates.py
"""
from __future__ import annotations

import os
import subprocess
import sys
import tempfile
from pathlib import Path

TESTS = Path(__file__).resolve().parent
CHECKER = TESTS.parent / "candidates" / "research-analysis" / "check-citation-network-v2-gates.py"
SUITE = TESTS / "test-citation-network-v2-gates.py"

# name: (exact source text, replacement). Each anchor must occur exactly once.
SABOTAGE = {
    "use without context": ('if uses and s.context != "INSPECTED":', 'if False:'),
    "inspected without access": ('if s.context == "INSPECTED" and s.access not in {"FULL-TEXT", "EXCERPT"}:', 'if False:'),
    "locator missing": ('if s.context == "INSPECTED" and not LOCATOR_RE.search(s.supported):', 'if False:'),
    "reuse without access": ('if "REUSES" in s.relation and s.access not in {"FULL-TEXT", "ABSTRACT"}:', 'if False:'),
    "not-citing in target corpus": ('if corpus and corpus.selected_on_target:', 'if False:'),
    "duplicate source": ('        if sid in sources:\n            report.fail("DUPLICATE_SOURCE"', '        if False:\n            report.fail("DUPLICATE_SOURCE"'),
    "metadata-coded review": ('    if metadata_coded:', '    if False:'),
    "adjudication corpus missing": ('if not any(c.role == "ADJUDICATION" for c in corpora.values()):', 'if False:'),
    "search lock": ('if c.role == "ADJUDICATION" and c.searched and not c.labels.get("CORPUS LOCK"):', 'if False:'),
    "corpus size": ('elif int(size) != actual:', 'elif False:'),
    "coverage recount": ('if (k, n) != (inspected, len(members)):', 'if False:'),
    "screened members": ('            members = [s for s in members if s.relevance != "UNKNOWN"]', '            pass'),
    "literature scope": ('elif corpus.role != "ADJUDICATION" or not corpus.searched:', 'elif False:'),
    "graph beyond corpus": ('if corpus.selected_on_target or not corpus.searched:', 'if False:'),
    "absence scope": ('        if scope not in {"LITERATURE", "WITHIN-SAMPLE"}:', '        if False:'),
    "absence needs search": ('        if corpus is None or corpus.role != "ADJUDICATION" or not corpus.searched:\n            reasons.append("ABSENCE needs', '        if False:\n            reasons.append("ABSENCE needs'),
    "bounded absence fraction": ('            if not re.search(rf"\\b{screened}\\s*/\\s*{total}\\b", inf.statement):', '            if False:'),
    "absence unscreened members": ('        if unknown:\n            reasons.append(f"ABSENCE with', '        if False:\n            reasons.append(f"ABSENCE with'),
    "absence result set": ('        if inf.sampling not in {"EXHAUSTIVE", "PRESPECIFIED-RULE"}:', '        if False:'),
    "corpus scope needs all": ('            reasons.append(f"{scope} scope requires Members used ALL")', '            pass'),
    "random-sample review": ('        report.review("SAMPLE_DECLARED_RANDOM"', '        (lambda *a: None)("SAMPLE_DECLARED_RANDOM"'),
    "member access": ('elif need is not None and s.access not in need:', 'elif False:'),
    "citation use needs context": ('if inf.klass == "CITATION-USE" and s.context != "INSPECTED":', 'if False:'),
    "citation use needs locator": ('elif inf.klass == "CITATION-USE" and not LOCATOR_RE.search(s.supported):', 'elif False:'),
    "engagement population": ('if inf.klass == "ENGAGEMENT" and s.relevance not in {"DIRECT", "ADJACENT"}:', 'if False:'),
    "population k/n": ('if not re.search(r"\\d+\\s*/\\s*\\d+", inf.statement):', 'if False:'),
    "composition total": ('    if total != len(members):', '    if False:'),
    "composition counts": ('if counts.get(key, 0) != actual.get(key, 0):', 'if False:'),
    "overclaimed": ('if declared in PASSING and actual == "INSUFFICIENT":', 'if False:'),
    "disposition mismatch": ('elif declared in PASSING and actual != declared:', 'elif False:'),
    "over-withheld review": ('elif declared == "INSUFFICIENT" and actual in PASSING:', 'elif False:'),
    "map missing": ('    if not maps:\n        report.fail("MAP_VERSION_MISSING"', '    if False:\n        report.fail("MAP_VERSION_MISSING"'),
    "map mismatch": ('    elif any(m != MAP_ID for m in maps):', '    elif False:'),
    "unscored with basis": ('        if listed:\n            report.fail("UNSCORED_WITH_BASIS"', '        if False:\n            report.fail("UNSCORED_WITH_BASIS"'),
    "basis note": ('if note.strip() in EMPTY:', 'if False:'),
    "direction tag": ('    if untagged:\n        report.fail("DIRECTION_TAG_MISSING"', '    if False:\n        report.fail("DIRECTION_TAG_MISSING"'),
    "scored without basis": ('        if not untagged:\n            report.fail("SCORED_WITHOUT_BASIS"', '        if False:\n            report.fail("SCORED_WITHOUT_BASIS"'),
    "scored on insufficient": ('    if weak:\n        report.fail("SCORED_ON_INSUFFICIENT"', '    if False:\n        report.fail("SCORED_ON_INSUFFICIENT"'),
    "direction side required": ('    if not side:\n        code = "NO_CONCERN_BASIS"', '    if False:\n        code = "NO_CONCERN_BASIS"'),
    "dimension class map": ('elif classes and not any(inferences[i].klass in classes for i in side):', 'elif False:'),
    "absence required for decisive tests": ('    "lack of decisive tests": {"ABSENCE"},', '    "lack of decisive tests": {"ABSENCE", "SOURCE-RESULT"},'),
    "co-citation excluded from uptake": ('    "poor critique uptake": {"ENGAGEMENT", "GRAPH-STRUCTURE"},\n    "adjacent', '    "poor critique uptake": {"ENGAGEMENT", "GRAPH-STRUCTURE", "CO-CITATION"},\n    "adjacent'),
    "co-citation review": ('if inf.klass == "CO-CITATION" and inf.members.strip().upper() == "UNSCREENED":', 'if False:'),
    "by-construction review": ('if inf.klass in {"GRAPH-STRUCTURE", "CO-CITATION"} and by_construction:', 'if False:'),
    "bounded-absence review": ('if t == "+" and inf.klass == "ABSENCE" and inf.scope == "WITHIN-SAMPLE":', 'if False:'),
    "dimension rows": ('    if missing:\n        report.fail("DIMENSION_ROWS"', '    if False:\n        report.fail("DIMENSION_ROWS"'),
    "failed rows leave coverage": ('    scored = [d for d in declared if d not in failed]', '    scored = list(declared)'),
    "review rows leave sensitivity": ('    held = sorted(d for d in scored if d in under_review)', '    held = []'),
    "gate threshold": ('meets, meets_without = a and 100 * k >= 70 * a, a and 100 * k2 >= 70 * a', 'meets, meets_without = True, True'),
    "band below gate": ('        if gate == "NOT MET":\n            report.fail("BAND_ISSUED_BELOW_GATE"', '        if False:\n            report.fail("BAND_ISSUED_BELOW_GATE"'),
    "conditional band review": ('        elif gate != "MET":\n            report.review("BAND_CONDITIONAL"', '        elif False:\n            report.review("BAND_CONDITIONAL"'),
    "withheld band accepted": ('        if withheld:\n            continue', '        if False:\n            continue'),
    "scorecard agreement": ('if key in dispositions and parsed[s_col].strip() != dispositions[key]:', 'if False:'),
    "finding on insufficient": ('            if weak:\n                report.fail("FINDING_ON_INSUFFICIENT"', '            if False:\n                report.fail("FINDING_ON_INSUFFICIENT"'),
    "finding rows (missing)": ('        for name in sorted(table_findings - listed):', '        for name in []:'),
    "finding rows (extra)": ('        for name in sorted(listed - table_findings):', '        for name in []:'),
    "not applicable": ('if not any(line.strip() == VERSION_LINE for line in lines):', 'if False:'),
    "require v2": ('        if require_v2:', '        if False:'),
}


def main() -> int:
    source = CHECKER.read_text(encoding="utf-8")
    survived = []
    with tempfile.TemporaryDirectory() as tmp:
        copy = Path(tmp) / CHECKER.name
        for name, (old, new) in SABOTAGE.items():
            if source.count(old) != 1:
                print(f"ANCHOR\t{name}\tfound {source.count(old)} times")
                return 2
            copy.write_text(source.replace(old, new), encoding="utf-8")
            env = dict(os.environ, CN7_GATES_PATH=str(copy))
            result = subprocess.run([sys.executable, str(SUITE)], env=env, capture_output=True,
                                    text=True)
            caught = result.returncode != 0
            print(f"{'caught' if caught else 'SURVIVED'}\t{name}")
            if not caught:
                survived.append(name)
    print(f"ABLATION\t{len(SABOTAGE) - len(survived)}/{len(SABOTAGE)} rules caught"
          + (f"\tsurvived: {', '.join(survived)}" if survived else ""))
    return 1 if survived else 0


if __name__ == "__main__":
    sys.exit(main())
