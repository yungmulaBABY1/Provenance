#!/usr/bin/env python3
"""Build the live-run fixture from Grok's v2-candidate.2 run on AJR 2001.

Input: the run directory examples/research/acemoglu-colonial-origins/citation-network-v2cand/
on Provenance-Atlas branch audit/acemoglu-colonial-origins-v2cand (commit 84d1800). The output
file must match its pinned sha256. The six adjudication search responses must match pinned
digests taken with every abstract_inverted_index field removed, so the fixture rebuilds from the
run as committed or after its abstracts are stripped. Everything is read as data; nothing in
the run is executed. Run with python3 -I:

    python3 -I build_live_v2cand_fixture.py /path/to/citation-network-v2cand OUTDIR

Output: live-v2cand2-acemoglu.txt. It is the run's own SECTION A0 and SECTION K0 and its RISK
BAND line, observed, with only the declarations revision 3 requires added from the run's own
records (rules L1-L6 below). Nothing in the run's ledger is corrected: duplicate records, the
zeros on partial bases and the search's missed items stay as observed, so the revision-3 gates
show what they make visible. It is a test input, not a re-grade of the run, which was produced
under revision 2 and passed revision 2's gates.
"""
from __future__ import annotations

import hashlib
import json
import re
import sys
from pathlib import Path

OUTPUT_SHA256 = "a1abbbee2b568f177913a3a7e9a89b2c04abac42d12152001d07fef4b1cd07c3"
RUN_COMMIT = "84d1800faf71788c46bb4c4e968ab3cb42d24b11"
# raw/adj1_Q1..Q6.json: sha256 of canonical JSON (sort_keys, compact separators) with every
# abstract_inverted_index key removed, computed from the files at RUN_COMMIT.
SEARCH_DIGESTS = {
    1: "9292398da28f669f191f7d16b7793da447a53c3cd5117082adbfc41b49238810",
    2: "9052c65d9c50bf8a1eb9ec51d2bc8967f6bde43969d2b32cd9bbd2985ec8632f",
    3: "e9c999268af0d31fdbe4daf139bb77299c269b96e4a3913da7c30d5a2f9d5d3b",
    4: "b72e03c923904430d4fbf10476377c1268593f80eaaebb266e8dbe186f254e3f",
    5: "2a8b4a545ddc42bc8311ebeda33bc064c10705049178f9dd788a4f4d7e9dbfae",
    6: "40a8e83d4dd4ce4855b01cfeb2b3782dcd3ee94b9207897730ed26cff269f1cc",
}

# Rules
# L1  Version and map lines become revision 3's (2-citation-network v2-candidate.3, cn7-map-3).
# L2  CLAIM LAYERS AND RIVALS: the run states that its layer and rival codes are those of its
#     v1 output (Section E, 02c v1 line 156); those definitions are inserted. "noSM" in
#     DIRECT (L3-noSM) is the run's own sub-label (no settler-mortality instrument).
# L3  RECORD QUALITY per corpus, from the run's own statements (I03, I24; RUN_REPORT P05, P07).
# L4  KNOWN-ITEM RECALL for ADJUDICATION-1. Known items: the claim-testing works the run's
#     exposure declaration says it had read before the search. Returned or not is computed
#     from the run's six committed search responses. Sachs 2003 has no OpenAlex record in the
#     run and entered as POST HOC (X03), so it counts as not returned.
# L5  SAMPLE ATTRITION for I06, from the run's own statement (4 of 6 sampled texts failed).
# L6  In SCORED dimension rows, an inference the basis note cites that the run itself declared
#     INSUFFICIENT or NOT-ASSESSED is listed with the (?) tag (uptake cites I22).
LAYERS = [
    "CLAIM LAYER: L1 — the field-6 estimate (64 former colonies, 2SLS 0.94, SE 0.16)",
    "CLAIM LAYER: L2 — the field-3 weaker defensible claim",
    "CLAIM LAYER: L3 — downstream: institutions explain income differences",
    "CLAIM LAYER: L4 — public wording",
    "RIVAL: R1 — direct geography or disease channel",
    "RIVAL: R2 — human capital carried by settlers",
]
QUALITY = {
    "RECEPTION-1": "4 works appear as two records each, and record N01 conflates the 2012 Reply "
                   "with AJR 2001 (I03, I24; run report P05, P07)",
    "RECENT-1": "the recent population changed from 2,695 to 3,026 between runs (I24)",
    "ADJUDICATION-1": "NOT-CITING codes rest on OpenAlex reference lists; AJR 2001's list "
                      "changed from 13 to 55 entries between runs (I24, run report P05)",
}
KNOWN_ITEMS = [  # (label, OpenAlex ID or None)
    ("Albouy 2012 Comment", "W1969918011"),
    ("AJR 2012 Reply", "W3124131699"),
    ("Rodrik et al. 2004", "W2994756033"),
    ("Glaeser et al. 2004", "W2890314743"),
    ("Easterly-Levine 2003", "W3122513675"),
    ("Sachs 2003", None),
]


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def without_abstracts(value):
    if isinstance(value, dict):
        return {k: without_abstracts(v) for k, v in value.items()
                if k != "abstract_inverted_index"}
    if isinstance(value, list):
        return [without_abstracts(v) for v in value]
    return value


def search_digest(data) -> str:
    canonical = json.dumps(without_abstracts(data), sort_keys=True, separators=(",", ":"),
                           ensure_ascii=False)
    return hashlib.sha256(canonical.encode("utf-8")).hexdigest()


def main() -> int:
    run_dir, outdir = Path(sys.argv[1]), Path(sys.argv[2])
    output = run_dir / "02c_citation_network_v2cand2.md"
    if sha(output) != OUTPUT_SHA256:
        raise SystemExit("output is not the pinned run output")
    sums = {}
    for line in (run_dir / "SHA256SUMS").read_text(encoding="utf-8").splitlines():
        if line.strip():
            digest, name = line.split(None, 1)
            sums[name.strip().lstrip("*").removeprefix("./")] = digest
    if sums.get("02c_citation_network_v2cand2.md") != OUTPUT_SHA256:
        raise SystemExit("the run's SHA256SUMS does not pin this output")
    returned_ids = set()
    for q in range(1, 7):
        path = run_dir / "raw" / f"adj1_Q{q}.json"
        data = json.loads(path.read_text(encoding="utf-8"))
        if search_digest(data) != SEARCH_DIGESTS[q]:
            raise SystemExit(f"{path.name} differs from the run's search response (abstract "
                             "fields aside)")
        returned_ids |= {w["id"].rsplit("/", 1)[-1] for w in data["results"]}

    lines = output.read_text(encoding="utf-8").splitlines()

    def block(start: str, stop: str) -> list[str]:
        i = lines.index(start)
        j = next(k for k in range(i + 1, len(lines)) if lines[k] == stop)
        return lines[i:j]

    a0 = block("SECTION A0: CORPUS REGISTER AND SOURCE ELIGIBILITY",
               "SECTION A: CITATION NETWORK STRUCTURE AND CARTEL DETECTION")
    k0 = block("SECTION K0: EVIDENCE SUFFICIENCY LEDGER", "SECTION K: CARTEL-RISK SCORING")
    band = next(line for line in lines if line.startswith("RISK BAND:"))
    assert lines.count("INSTRUMENT VERSION: 2-citation-network v2-candidate.2") == 1

    # L2, L3, L4
    returned = [label for label, wid in KNOWN_ITEMS if wid in returned_ids]
    missed = [label for label, wid in KNOWN_ITEMS if wid not in returned_ids]
    recall = (f"KNOWN-ITEM RECALL: ADJUDICATION-1 {len(returned)}/{len(KNOWN_ITEMS)} (returned: "
              f"{', '.join(returned) or 'none'}; not returned: {', '.join(missed)})")
    out_a0 = [a0[0], "", "CLAIM LAYERS AND RIVALS", "", *LAYERS]
    for line in a0[1:]:
        out_a0.append(line)
        match = re.match(r"^CITATION CONTEXT COVERAGE:\s*(\S+)\s", line)
        if match:
            out_a0.append(f"RECORD QUALITY: {QUALITY[match[1]]}")
            if match[1] == "ADJUDICATION-1":
                out_a0.append(recall)
    assert sum(1 for line in out_a0 if line.startswith("RECORD QUALITY:")) == 3

    # L1, L5, L6
    out_k0, tagged, i06_seen, attrition_added = [], 0, False, False
    for line in k0:
        if line.strip() == "DIMENSION CLASS MAP: cn7-map-2":
            line = "DIMENSION CLASS MAP: cn7-map-3"
        if line.startswith("| Poor critique uptake | SCORED"):
            assert "(I22)" in line and "I18 (-)" in line, line
            line = line.replace("I18 (-)", "I18 (-), I22 (?)")
            tagged += 1
        if line.startswith("| I06 |"):
            assert "4/6 sampled full texts were not retrieved" in line, line[:120]
            i06_seen = True
        elif i06_seen and not attrition_added and not line.startswith("|"):
            # first line after the inference table ends; the table itself is not split
            out_k0 += ["", "SAMPLE ATTRITION: I06 2/6 (4 of the 6 sampled full texts could not "
                       "be retrieved; I06 and the run report)"]
            attrition_added = True
        out_k0.append(line)
    assert tagged == 1 and attrition_added

    notes = [
        "CANDIDATE GATE FIXTURE — LIVE RUN, ACEMOGLU, v2-candidate.2 LEDGER UNDER REVISION 3",
        "",
        "FIXTURE KIND: observed live-run ledger (expected under revision 3: PASS-WITH-REVIEW; "
        "coverage 8/10 after Gate B, 4/10 with review-pending dimensions withdrawn)",
        "Generated by tests/cases/citation-network-v2-gates/build_live_v2cand_fixture.py from "
        f"Grok's run (Provenance-Atlas commit {RUN_COMMIT}, output sha256 {OUTPUT_SHA256}).",
        "The run's SECTION A0, SECTION K0 and RISK BAND line, unchanged except for rules L1-L6 "
        "in the build script. A test input, not a re-grade: the run was made under revision 2.",
        "",
        "INSTRUMENT VERSION: 2-citation-network v2-candidate.3",
        "",
    ]
    text = "\n".join(notes + out_a0 + out_k0 + ["", band]) + "\n"
    path = outdir / "live-v2cand2-acemoglu.txt"
    path.write_text(text, encoding="utf-8")
    print(f"{path.name}\tsha256 {hashlib.sha256(text.encode()).hexdigest()}\t{recall}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
