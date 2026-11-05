#!/usr/bin/env python3
"""Build the three Acemoglu fixtures for the v2-candidate gates from Grok's run.

Input: the Stage-2c output of the Acemoglu audit run, committed by its producer on
yungmulaBABY1/Provenance-Atlas branch audit/acemoglu-colonial-origins at
    examples/research/acemoglu-colonial-origins/citation-network/02c_citation_network.md
(git blob 0c23beed0c914bea21b09c3094b33e976561f601). The file is read as data and
must match the pinned sha256; nothing in it is executed. Run with python3 -I:

    python3 -I build_acemoglu_fixtures.py /path/to/02c_citation_network.md OUTDIR

Outputs (all test inputs, none of them a re-grade of the original run):

  acemoglu-as-run-transcribed.txt  The run's own declarations, re-expressed in the
      candidate ledger format by the mechanical rules below, with nothing repaired.
  acemoglu-repaired.txt            The same evidence, re-ledgered to comply with the
      candidate; each change is one named entry in REPAIRS.
  acemoglu-structural-control.txt  A clean control: a structural question that
      metadata alone answers, using the same corpus at METADATA access only.

The run, its receipts and its producing instrument are not modified. The transcription
is this script's interpretation of the run's prose and tables; every rule is listed
here so a reviewer can contest it.
"""
from __future__ import annotations

import hashlib
import re
import sys
from pathlib import Path

INPUT_SHA256 = "884887fe5a7b98d77921fbc31b488c7c9b7dc8406eb60340e4d5881436f3016c"
INPUT_BLOB = "0c23beed0c914bea21b09c3094b33e976561f601"
VERSION_LINE = "INSTRUMENT VERSION: 2-citation-network v2-candidate.2"
MAP_LINE = "DIMENSION CLASS MAP: cn7-map-2"
STAGE_2A_BLOB = "05599d8ce1f83bd95c6fc91127c4b15b0c18dcd7"

# ---------------------------------------------------------------------------
# Transcription rules (Gate A columns), applied to the run's Section B table,
# Section C prose and Artifacts 3 and 4.
#
# Source access
#   node listed after "Full texts retrieved:" (02c line 126)        -> FULL-TEXT
#   otherwise Section B state begins ABSTRACT-CONFIRMED               -> ABSTRACT
#   otherwise Section B state LOCATED                                 -> METADATA
# Citation context
#   FULL-TEXT and listed after "Version mismatch:" (02c line 131)     -> VERSION-MISMATCH
#   FULL-TEXT otherwise                                               -> INSPECTED
#   not FULL-TEXT                                                     -> NOT-INSPECTED
# Passage locator (Supported inference of an INSPECTED row)
#   the evidence IDs (for example RD-E1) or "reference list" that the run's own Artifact 4 row
#   gives for the node; N21 from Section C question 17 (02c line 128). A node whose row gives
#   neither has no locator, and the transcription records none.
# Relation to target
#   N01-N15: Artifact 4 polarity  supportive -> SUPPORTS; critical -> CHALLENGES;
#            perfunctory, neutral/background -> MENTIONS; used as premise -> PREMISE;
#            unclear without full text -> CITES-UNINSPECTED
#   N21: SUPPORTS, from Section C question 17 (02c line 128); Artifact 4 stops at rank 15
#   other N16-N50 and recent rows: CITES-UNINSPECTED (they cite the target by construction)
#   + REUSES when the Section B relation text contains "reuses" or "re-analys"
# Question relevance (first matching rule)
#   code "primary empirical test of the central claim"               -> DIRECT
#   code "primary empirical study (not of the central claim)"        -> BACKGROUND
#        (the run defines this code as work on a different question that cites AJR
#        as background or premise, 02c line 60)
#   relation text contains "central claim"                           -> DIRECT
#   relation text contains "background"                              -> BACKGROUND
#   relation text contains adjacent / rival / construct / synthesis  -> ADJACENT
#   otherwise                                                         -> UNKNOWN
#   recent rows (no relevance coding in the run)                      -> UNKNOWN
# Evidence contribution (first matching rule)
#   code primary test, text "reuses"                                  -> SHARED-DATA
#   text "independent data origin"                                    -> INDEPENDENT-DATA
#   text "re-analys"                                                  -> REANALYSIS
#   code primary study not of the central claim                       -> NONE
#   code review article -> REVIEW; theoretical / conceptual -> THEORY;
#   commentary / editorial -> COMMENTARY; otherwise                   -> UNKNOWN
# Disposition of transcribed inferences
#   Every inference that an as-run score or confirmed finding relied on is transcribed
#   with the disposition SUPPORTED (or SUPPORTED-WITHIN-SAMPLE for the polarity sample):
#   the run used it as sufficient, and the transcription makes that claim explicit.
# ---------------------------------------------------------------------------

POLARITY = {"supportive": "SUPPORTS", "critical": "CHALLENGES", "perfunctory": "MENTIONS",
            "neutral/background": "MENTIONS", "used as premise": "PREMISE",
            "unclear without full text": "CITES-UNINSPECTED"}

OUTSIDE_ROWS = {
    "N00": ("N00 W3124166904 2001 AJR, The Colonial Origins of Comparative Development (target)",
            "DIRECT (field 6)", "NOT-CITING", "INDEPENDENT-DATA", "FULL-TEXT (AER 2001)",
            "NOT-APPLICABLE", "target, read in full before this stage (02c line 9)"),
    "NP": ("NP Nobel popular background 2024", "ADJACENT", "SUPPORTS", "REVIEW",
           "FULL-TEXT (2024 popular background)", "INSPECTED",
           "NP-E1: restatement read; Artifact 4 polarity inflated (02c line 416)"),
    "NS": ("NS Nobel scientific background 2024", "ADJACENT", "SUPPORTS+QUALIFIES", "REVIEW",
           "FULL-TEXT (2024 scientific background)", "INSPECTED",
           "NS-E1, NS-E2: restatement and critique discussion read (02c line 417)"),
    "AL": ("AL W1969918011 2012 Albouy, AER Comment", "DIRECT (field 6)", "CHALLENGES",
           "REANALYSIS", "FULL-TEXT (AER 2012, read in Stage 2a)", "INSPECTED",
           "critique of the settler-mortality data (02c line 234)"),
    "SA": ("SA Sachs 2003, NBER WP 9490", "DIRECT (L3 rival R1)", "UNKNOWN", "UNKNOWN",
           "FULL-TEXT (NBER WP 9490)", "NOT-INSPECTED",
           "own result read; its citation of AJR not inspected (02c line 196)"),
}

DIMENSIONS = [
    "Founding-cluster dominance", "Internal citation density", "Recent-paper dependence",
    "Review-hub laundering", "Proxy mismatch", "Claim mutation", "Adjacent-field neglect",
    "Lack of decisive tests", "Poor critique uptake", "Intervention-evidence ratchet",
    "Model non-updating",
]


def read_input(path: Path) -> list[str]:
    raw = path.read_bytes()
    digest = hashlib.sha256(raw).hexdigest()
    if digest != INPUT_SHA256:
        raise SystemExit(f"input sha256 {digest} is not the pinned run output {INPUT_SHA256}")
    return raw.decode("utf-8").splitlines()


def cells(line: str) -> list[str]:
    return [c.strip() for c in line.strip().strip("|").split("|")]


def short_title(title: str, words: int = 6) -> str:
    parts = re.sub(r"[|]", "", title).split()
    return " ".join(parts[:words]) + (" ..." if len(parts) > words else "")


def parse_run(lines: list[str]) -> dict:
    section_b = {}
    for line in lines:
        if re.match(r"^\| N\d\d \| W\d+ \|", line):
            row = cells(line)
            section_b[row[0]] = {"wid": row[1], "year": row[2], "title": row[4], "code": row[5],
                                 "text": row[6], "state": row[7]}
    assert len(section_b) == 50, len(section_b)

    text = "\n".join(lines)
    ft_block = text[text.index("Full texts retrieved:"):text.index("Retrieval failed")]
    full_text = {}
    for match in re.finditer(r"\b(N\d\d)\b(?: \(([^)]*)\))?", ft_block):
        full_text[match[1]] = match[2] or ""
    assert len(full_text) == 13, sorted(full_text)
    vm_block = text[text.index("Version mismatch:"):]
    vm_block = vm_block[:vm_block.index("(")]
    mismatch = set(re.findall(r"\bN\d\d\b", vm_block))
    assert mismatch == {"N13", "N16"}, mismatch

    polarity, locators = {}, {}
    start = lines.index("ARTIFACT 4: CITATION POLARITY TABLE")
    for line in lines[start:start + 25]:
        match = re.match(r"^\| (N\d\d) ", line)
        if match:
            polarity[match[1]] = cells(line)[3]
            found = re.findall(r"\b[A-Z]{2,4}-E\d+\b|reference list", line)
            if found:
                locators[match[1]] = ", ".join(dict.fromkeys(found))
    assert sorted(polarity) == [f"N{i:02d}" for i in range(1, 16)], sorted(polarity)
    supportive = next(line for line in lines if line.startswith("17. Supportive:"))
    assert "N21 (EL-E1" in supportive, supportive[:80]
    polarity["N21"] = "supportive"
    locators["N21"] = "EL-E1"
    assert locators == {"N02": "RD-E1, RD-E3, RD-E4", "N03": "GL-E1, GL-E2",
                        "N04": "reference list", "N05": "HB-E1", "N06": "DML-E1, DML-E2",
                        "N12": "HW-E1", "N21": "EL-E1"}, locators

    recent = {}
    for line in lines:
        match = re.match(r"^\| (R\d\d) (.+?) \((W\d+)\) \| (\d{4}) \| ([^|]+) \|", line)
        if match:
            recent[match[1]] = {"title": match[2], "wid": match[3], "year": match[4],
                                "state": match[5]}
    assert len(recent) == 25, len(recent)
    band = next(line for line in lines if line.startswith("RISK BAND: "))
    band = band.split(" — ")[0] + " — " + band.split(" — ")[1].split(";")[0]
    assert band.startswith("RISK BAND: >20%–40% normal field clustering"), band
    return {"band": band, "b": section_b, "full_text": full_text, "mismatch": mismatch,
            "polarity": polarity, "locators": locators, "recent": recent}


def relevance(code: str, text: str) -> str:
    low = text.lower()
    if code == "primary empirical test of the central claim":
        return "DIRECT"
    if code == "primary empirical study (not of the central claim)":
        return "BACKGROUND"
    if "central claim" in low:
        return "DIRECT"
    if "background" in low:
        return "BACKGROUND"
    if any(word in low for word in ("adjacent", "rival", "construct", "synthesis")):
        return "ADJACENT"
    return "UNKNOWN"


def contribution(code: str, text: str) -> str:
    low = text.lower()
    if code == "primary empirical test of the central claim":
        return "SHARED-DATA" if "reuses" in low else "INDEPENDENT-DATA"
    if "independent data origin" in low:
        return "INDEPENDENT-DATA"
    if "re-analys" in low:
        return "REANALYSIS"
    return {"primary empirical study (not of the central claim)": "NONE",
            "review article": "REVIEW", "theoretical / conceptual paper": "THEORY",
            "commentary / editorial": "COMMENTARY"}.get(code, "UNKNOWN")


def reception_rows(run: dict) -> dict[str, list[str]]:
    rows = {}
    for node, b in run["b"].items():
        if node in run["full_text"]:
            version = run["full_text"][node]
            access = f"FULL-TEXT ({version})" if version else "FULL-TEXT"
            context = "VERSION-MISMATCH" if node in run["mismatch"] else "INSPECTED"
        elif b["state"].startswith("ABSTRACT-CONFIRMED"):
            access, context = "ABSTRACT", "NOT-INSPECTED"
        elif b["state"].startswith("LOCATED"):
            access, context = "METADATA (LOCATED)", "NOT-INSPECTED"
        else:
            raise SystemExit(f"{node}: unmapped state {b['state']!r}")
        relation = [POLARITY[run["polarity"][node]]] if node in run["polarity"] else [
            "CITES-UNINSPECTED"]
        if re.search(r"reuses|re-analys", b["text"], re.IGNORECASE):
            relation.append("REUSES")
        supported = {"INSPECTED": "citing passage read",
                     "VERSION-MISMATCH": "retrieved version lacks the citation",
                     }.get(context, "abstract read; citation not inspected"
                           if access == "ABSTRACT" else "record only; not read")
        if context == "INSPECTED" and node in run["locators"]:
            supported = f"{run['locators'][node]}: {supported}"
        rows[node] = [f"{node} {b['wid']} {b['year']} {short_title(b['title'])}", "RECEPTION-1",
                      relevance(b["code"], b["text"]), "+".join(relation),
                      contribution(b["code"], b["text"]), access, context, supported]
    return rows


def recent_rows(run: dict) -> dict[str, list[str]]:
    rows = {}
    for rid, r in run["recent"].items():
        access = "ABSTRACT" if "ABSTRACT-CONFIRMED" in r["state"] else "METADATA (LOCATED)"
        rows[rid] = [f"{rid} {r['wid']} {r['year']} {short_title(r['title'])}", "RECENT-1",
                     "UNKNOWN", "CITES-UNINSPECTED", "UNKNOWN", access, "NOT-INSPECTED",
                     "reference list only; citing passage not read"]
    return rows


def outside_rows(keys: list[str]) -> dict[str, list[str]]:
    return {k: [OUTSIDE_ROWS[k][0], "OUTSIDE", *OUTSIDE_ROWS[k][1:]] for k in keys}


# Inference ledger as transcribed. Columns: id, class, corpus, scope, sampling, members,
# disposition, statement. Statements are this script's summaries with 02c line references.
AS_RUN_INFERENCES = [
    ("I01", "GRAPH-STRUCTURE", "RECEPTION-1", "CORPUS", "EXHAUSTIVE", "ALL", "SUPPORTED",
     "Directed density 136/2450 inside the top-50 citing corpus; closure beyond it neither "
     "established nor excluded (02c lines 29-34)"),
    ("I02", "DATABASE-RECORD", "—", "NAMED", "NOT-APPLICABLE", "N00, N01", "SUPPORTED",
     "OpenAlex conflates the 2012 Reply record with AJR 2001 and indexes 13 references for "
     "AJR 2001 (02c line 36; Finding 1)"),
    ("I03", "CO-CITATION", "POPULATION", "POPULATION", "NOT-APPLICABLE", "UNSCREENED",
     "SUPPORTED", "Reversal of Fortune co-cited by 336/2,695 and the AJR handbook by 276/2,695 "
     "recent AJR citers (02c lines 204-205)"),
    ("I04", "DATABASE-RECORD", "RECEPTION-1", "CORPUS", "EXHAUSTIVE", "ALL", "SUPPORTED",
     "8/50 corpus members have an AJR author (02c line 40)"),
    ("I05", "CITATION-USE", "RECENT-1", "CORPUS", "PRESPECIFIED-RULE", "ALL", "SUPPORTED",
     "Recent citers mostly use AJR as a background premise for governance-index regressions "
     "(02c line 467); no recent citing passage was read (02c lines 132, 142)"),
    ("I06", "RESTATEMENT", "—", "NAMED", "NOT-APPLICABLE", "N05, N00", "SUPPORTED",
     "The handbook working paper restates the p. 1387 magnitude without the upper-bound "
     "qualifier (HB-E1 against AJR-E2; Finding 3)"),
    ("I07", "CO-CITATION", "POPULATION", "POPULATION", "NOT-APPLICABLE", "UNSCREENED",
     "SUPPORTED", "1,400/1,676 recent citers of the handbook do not cite AJR 2001 "
     "(02c line 206)"),
    ("I08", "RESTATEMENT", "—", "NAMED", "NOT-APPLICABLE", "N05, N06, N12, N00", "SUPPORTED",
     "The handbook names the expropriation index economic institutions; DML and "
     "Hanushek-Woessmann keep the proxy wording (HB-E1, DML-E1, HW-E1; 02c line 469)"),
    ("I09", "RESTATEMENT", "—", "NAMED", "NOT-APPLICABLE", "NP, NS", "SUPPORTED",
     "Popular prize text states a clear chain of causality; scientific background says "
     "grain of salt (NP-E1, NS-E1; Finding 4)"),
    ("I10", "SOURCE-RESULT", "—", "NAMED", "NOT-APPLICABLE", "N00", "SUPPORTED",
     "At the source layer AJR 2001 tests geography and malaria controls and uses the "
     "Knack-Keefer data (02c lines 169, 448)"),
    ("I11", "CO-CITATION", "POPULATION", "POPULATION", "NOT-APPLICABLE", "UNSCREENED",
     "SUPPORTED", "Sachs 2003 co-cited by 494/11,316 and Glaeser et al. 2004 by 1,539/11,316 "
     "union AJR citers (02c lines 196-197)"),
    ("I12", "ABSENCE", "RECEPTION-1", "LITERATURE", "CONVENIENCE", "ALL", "SUPPORTED",
     "No instrument-independent test of the cross-country magnitude exists (02c lines 472, "
     "667)"),
    ("I13", "SOURCE-RESULT", "—", "NAMED", "NOT-APPLICABLE", "NS, N02", "SUPPORTED",
     "The scientific background says institutions and settler human capital are very hard "
     "to distinguish (NS-E3); Rodrik et al. say AJR do not directly test colonial policies "
     "(RD-E4)"),
    ("I14", "DATA-ORIGIN", "—", "NAMED", "NOT-APPLICABLE", "N01, N02, N21, N06, N31",
     "SUPPORTED", "Every cross-country re-estimate in the top 50 uses the AJR "
     "settler-mortality series (02c line 56)"),
    ("I15", "DATA-ORIGIN", "RECEPTION-1", "LITERATURE", "CONVENIENCE", "ALL", "SUPPORTED",
     "Independent confirmation of L3 shrinks to one data origin (02c line 56; Finding 2 "
     "scope loss)"),
    ("I16", "ENGAGEMENT", "—", "NAMED", "NOT-APPLICABLE", "N01, NS", "SUPPORTED",
     "The Reply answers Albouy; the scientific background cites the critique and the "
     "human-capital argument (02c line 236)"),
    ("I17", "CO-CITATION", "POPULATION", "POPULATION", "NOT-APPLICABLE", "UNSCREENED",
     "SUPPORTED", "Albouy co-cited by 220/7,375 2013+ citers of AJR 2001 or the Reply; "
     "baseline Rodriguez-Rodrik 1,181/5,570 (02c line 236)"),
    ("I18", "CITATION-USE", "RECEPTION-1", "WITHIN-SAMPLE", "CONVENIENCE",
     "N01, N02, N03, N04, N05, N06, N08, N09, N11, N12, N14", "SUPPORTED-WITHIN-SAMPLE",
     "Polarity of the top-15 members given a class other than unclear (Artifact 4, 02c lines "
     "401-415)"),
    ("I19", "COMPOSITION", "RECEPTION-1", "CORPUS", "EXHAUSTIVE", "ALL", "SUPPORTED",
     "Relevance composition of the citing set: the three primary tests and the authors' "
     "reanalysis are DIRECT (02c lines 115-117); describes the citing set, not the evidence "
     "base"),
    ("I20", "SOURCE-RESULT", "—", "NAMED", "NOT-APPLICABLE", "N00, SA, N03", "SUPPORTED",
     "AJR's malaria control lowers the estimate to 0.69; Sachs rejects the null with malaria "
     "risk; Glaeser et al. find malaria significant alongside settler mortality (Finding 6)"),
]

# Direction tags: (+) the run used the inference as evidence of concern; (-) as evidence of no
# concern (02c lines 465-475 and the Section E, H dispositions they summarise).
AS_RUN_DIMENSIONS = {
    "Founding-cluster dominance": ("SCORED 1", "I03 (+), I04 (+)", "02c line 465"),
    "Internal citation density": ("SCORED 0", "I01 (-)", "02c line 466"),
    "Recent-paper dependence": ("SCORED 1", "I05 (+)", "02c line 467"),
    "Review-hub laundering": ("SCORED 1", "I06 (+), I07 (+)",
                              "NESTED under claim mutation; 02c line 468"),
    "Proxy mismatch": ("SCORED 1", "I08 (+)", "02c line 469"),
    "Claim mutation": ("SCORED 1", "I06 (+), I09 (+)", "02c line 470"),
    "Adjacent-field neglect": ("SCORED 1", "I10 (-), I11 (+)",
                               "source layer affirmative; downstream co-citation low (02c line 448)"),
    "Lack of decisive tests": ("SCORED 1", "I12 (+), I13 (+), I14 (+)", "02c line 472"),
    "Poor critique uptake": ("SCORED 1", "I16 (-), I17 (+)",
                             "cluster engaged; citing-mass co-citation low (02c line 473)"),
    "Intervention-evidence ratchet": ("N/A", "—", "No intervention claim (02c line 474)"),
    "Model non-updating": ("UNINFORMATIVE", "—", "Four-link gate link 2 not met: the "
                           "disconfirming evidence is contested, not verified (02c line 475)"),
}

AS_RUN_FINDINGS = [("Finding 1", "confirmed", "I02"), ("Finding 2", "confirmed", "I14, I15"),
                   ("Finding 3", "confirmed", "I06"), ("Finding 4", "confirmed", "I09"),
                   ("Finding 5", "confirmed", "I16, I17"), ("Finding 6", "contested", "I11, I20"),
                   ("Finding 7", "confirmed", "I01")]

# Each repair is one documented change from the transcription. Nothing new is retrieved.
REPAIRS = [
    ("R1", "N11 relation PREMISE -> CITES-UNINSPECTED: the published chapter was not read and "
     "the run says its polarity was assumed from N05 (02c line 411)."),
    ("R2", "RECEPTION-1 coverage 13/50 -> 11/50: N13 and N16 retrieved versions do not contain "
     "the citation (02c line 131); they are VERSION-MISMATCH, not inspected (R12 lowers it "
     "further to 8/50)."),
    ("R3", "Register ADJUDICATION-1 with CORPUS DISCOVERY: NONE, assembled from claim-testing "
     "sources the run already retrieved (N01, N02, N03, N21, N42, AL, SA). No adjudication "
     "search is added."),
    ("R4", "N42 relevance BACKGROUND -> DIRECT (L3): the run itself treats it as an "
     "independent data origin bearing on L3 (02c lines 105, 221). This is the only recoded "
     "relevance value."),
    ("R5", "I05 (recent citation use) -> INSUFFICIENT; recent-paper dependence -> UNASSESSED."),
    ("R6", "I12 (absence of instrument-independent tests) -> INSUFFICIENT on ADJUDICATION-1 "
     "(see R15 for the dimension)."),
    ("R7", "N31 relation drops REUSES and I14 drops N31: the record was located but never "
     "read (02c line 94), so its reuse of the AJR instrument is not established. I14 keeps "
     "N01, N02, N21, N06."),
    ("R8", "I15 (literature-wide data origin) -> INSUFFICIENT on ADJUDICATION-1; Finding 2 "
     "rests on I14, scoped to the named re-estimates."),
    ("R9", "I18 drops N11 from the inspected polarity sample."),
    ("R10", "I19 statement updated for R4: N42 is now DIRECT, so 5 of 50 citing-set members "
     "are DIRECT; the composition line is recomputed from the ledger."),
    # Revision 2 (cn7-map-2, locators, bounded absence, searched adjudication for evidence-base
    # claims). Still no new retrieval.
    ("R11", "N01 and AL get passage locators from the same run's Stage 2a (02a_internal_"
     "validity.md line 203: AJR 2012 pp. 3078-80; Albouy 2012 pp. 3060-72)."),
    ("R12", "N08, N09 and N14 have no recorded passage locator anywhere in the run, so their "
     "citation context becomes NOT-INSPECTED and their relation CITES-UNINSPECTED. RECEPTION-1 "
     "coverage 11/50 -> 8/50; I18 keeps the 7 locatable top-15 passages."),
    ("R13", "Adjacent-field neglect SCORED 1 -> UNASSESSED: its concern rests only on co-citation "
     "over unscreened citers (I11); the source-layer evidence (I10) points the other way."),
    ("R14", "Poor critique uptake SCORED 1 -> UNASSESSED: its concern rests only on co-citation "
     "over unscreened citers (I17); the dominant cluster engaged the critique (I16). SCORED 0 on "
     "I16 is the alternative if the dominant cluster is taken as the uptake population "
     "(instrument Section H steps 3-4); that is the executor's call, not a repair."),
    ("R15", "Lack of decisive tests SCORED 1 -> UNASSESSED: a concern score needs an absence "
     "over a SEARCHED adjudication corpus (cn7-map-2); none was run (I12)."),
    ("R16", "Direction tags and the DIMENSION CLASS MAP line added."),
    ("R17", "RISK BAND >20%-40% (02c line 329) -> WITHHELD: coverage after Gate B is 5/10, "
     "below the PROVISIONAL 70% gate. The arithmetic band position is unchanged."),
]


def table(headers: list[str], rows: list[list[str]]) -> list[str]:
    out = ["| " + " | ".join(headers) + " |", "|" + "---|" * len(headers)]
    out += ["| " + " | ".join(row) + " |" for row in rows]
    return out


def composition_line(iid: str, corpus: str, ledger: dict[str, list[str]]) -> str:
    counts: dict[str, int] = {}
    members = [row for row in ledger.values() if corpus in row[1].split("+")]
    for row in members:
        code = row[2].split("(")[0].strip()
        counts[code] = counts.get(code, 0) + 1
    order = ["DIRECT", "ADJACENT", "BACKGROUND", "UNRELATED", "UNKNOWN"]
    parts = "; ".join(f"{code}={counts.get(code, 0)}" for code in order)
    return f"COMPOSITION: {iid} | relevance | {parts} | TOTAL={len(members)}"


def register(entries: list[dict]) -> list[str]:
    out = []
    for e in entries:
        out += [f"CORPUS ID: {e['id']}", f"CORPUS ROLE: {e['role']}",
                f"CORPUS QUESTION: {e['question']}", f"CORPUS SELECTION RULE: {e['rule']}",
                f"CORPUS DISCOVERY: {e['discovery']}",
                f"SELECTED ON TARGET CITATION: {e['selected']}", f"CORPUS SIZE: {e['size']}",
                f"CITATION CONTEXT COVERAGE: {e['id']} {e['coverage']}", ""]
    return out


def render(title: str, notes: list[str], corpora: list[dict], ledger: dict[str, list[str]],
           inferences: list[tuple], compositions: list[str], dimensions: dict,
           findings: list[tuple], tail: tuple[str, ...] = ()) -> str:
    out = [title, "", *notes, "", VERSION_LINE, "",
           "SECTION A0: CORPUS REGISTER AND SOURCE ELIGIBILITY", "", *register(corpora),
           "SOURCE ELIGIBILITY LEDGER", ""]
    out += table(["Source", "Corpus membership", "Question relevance", "Relation to target",
                  "Evidence contribution", "Source access", "Citation context",
                  "Supported inference"], list(ledger.values()))
    out += ["", "SECTION K0: EVIDENCE SUFFICIENCY LEDGER", "", "INFERENCE LEDGER", ""]
    out += table(["Inference", "Class", "Corpus", "Claimed scope", "Sampling rule",
                  "Members used", "Disposition", "Statement"], [list(i) for i in inferences])
    out += ["", *compositions, "", "DIMENSION EVIDENCE BASIS", "", MAP_LINE, ""]
    out += table(["Scorecard dimension", "Scorecard disposition", "Inference IDs", "Basis note"],
                 [[name, *dimensions[name]] for name in DIMENSIONS])
    out += ["", "FINDING EVIDENCE BASIS", ""]
    out += table(["Finding", "Finding status", "Inference IDs"], [list(f) for f in findings])
    if tail:
        out += ["", *tail]
    return "\n".join(out) + "\n"


def provenance_notes(kind: str) -> list[str]:
    return [
        f"FIXTURE KIND: {kind}",
        "Generated by tests/cases/citation-network-v2-gates/build_acemoglu_fixtures.py from the "
        "Acemoglu Stage-2c run output",
        f"(Provenance-Atlas branch audit/acemoglu-colonial-origins, git blob {INPUT_BLOB}, "
        f"sha256 {INPUT_SHA256}).",
        "This is a test input for the v2-candidate gates. It is not the run, not a re-grade of "
        "the run, and not evidence about the literature.",
    ]


def reception_register(coverage: str) -> dict:
    return {"id": "RECEPTION-1", "role": "RECEPTION",
            "question": "How AJR 2001 is cited by its most-cited citing works",
            "rule": "OpenAlex works API filter=cites:W3124166904&sort=cited_by_count:desc&"
                    "per-page=50, executed 2026-11-04, no date or type bound, no screening "
                    "(02c line 24)",
            "discovery": "SEARCHED — the OpenAlex query above (raw/top50_citers.json)",
            "selected": "YES", "size": 50, "coverage": coverage}


RECENT_REGISTER = {"id": "RECENT-1", "role": "RECEPTION",
                   "question": "How recent works cite AJR 2001",
                   "rule": "OpenAlex filter=cites:W3124166904,from_publication_date:2021-11-04&"
                           "sort=cited_by_count:desc&per-page=25 (02c line 365)",
                   "discovery": "SEARCHED — the OpenAlex query above (recent5y_top25.json)",
                   "selected": "YES", "size": 25, "coverage": "0/25"}


def build(run: dict) -> dict[str, str]:
    base = {**reception_rows(run), **recent_rows(run),
            **outside_rows(["N00", "NP", "NS", "AL", "SA"])}

    # --- as-run transcription: nothing repaired -------------------------------------
    as_run = render(
        "CANDIDATE GATE FIXTURE — ACEMOGLU AS-RUN, TRANSCRIBED",
        provenance_notes("as-run transcription (expected: FAIL)") + [
            "Coverage line below repeats the run's own figure: citing passages retrieved for "
            "13 of 50 top citers (02c line 686).",
            "The run registered no adjudication corpus; none is registered here."],
        [reception_register("13/50"), RECENT_REGISTER], base, AS_RUN_INFERENCES,
        [composition_line("I19", "RECEPTION-1", base)], AS_RUN_DIMENSIONS, AS_RUN_FINDINGS,
        (run["band"],))

    # --- repaired: the same evidence, re-ledgered (REPAIRS R1-R9) ----------------------
    rep = {k: list(v) for k, v in base.items()}
    rep["N11"][3] = "CITES-UNINSPECTED"                                     # R1
    rep["N31"][3] = "CITES-UNINSPECTED"                                     # R7
    for sid in ("N01", "N02", "N03", "N21", "N42"):                         # R3
        rep[sid][1] = "RECEPTION-1+ADJUDICATION-1"
    for sid in ("AL", "SA"):
        rep[sid][1] = "ADJUDICATION-1"
    rep["N42"][2] = "DIRECT (L3)"                                           # R4
    rep["N42"][4] = "INDEPENDENT-DATA"
    rep["N01"][7] = ("AJR 2012 Reply pp. 3078-80 (Stage 2a, 02a line 203): citing passage "
                     "read")                                                 # R11
    rep["AL"][7] = ("Albouy 2012 pp. 3060-72 (Stage 2a, 02a line 203): critique of the "
                    "settler-mortality data")
    for sid in ("N08", "N09", "N14"):                                       # R12
        rep[sid][3] = "CITES-UNINSPECTED"
        rep[sid][6] = "NOT-INSPECTED"
        rep[sid][7] = "full text read; no passage locator recorded"
    rec_inspected = sum(1 for row in rep.values()
                        if "RECEPTION-1" in row[1].split("+") and row[6] == "INSPECTED")
    adjudication = [row for row in rep.values() if "ADJUDICATION-1" in row[1].split("+")]
    adj_inspected = sum(1 for row in adjudication if row[6] == "INSPECTED")
    adjudication_register = {
        "id": "ADJUDICATION-1", "role": "ADJUDICATION",
        "question": "Studies that test the field-6 estimate, L3, or the rivals R1 and R2",
        "rule": "Assembled from claim-testing sources the run retrieved for other sections "
                "(02c lines 38, 117, 196-197, 221, 234); no adjudication search was run",
        "discovery": "NONE — assembled from retrieved sources; supports statements about its "
                     "named members only",
        "selected": "NO", "size": len(adjudication),
        "coverage": f"{adj_inspected}/{len(adjudication)}"}
    replace = {
        "I05": ("I05", "CITATION-USE", "RECENT-1", "CORPUS", "PRESPECIFIED-RULE", "ALL",
                "INSUFFICIENT", "How recent citers use AJR is not established: 0/25 citing "
                "passages read; needs inspected passages for a prespecified sample (02c lines "
                "132, 142, 467)"),
        "I12": ("I12", "ABSENCE", "ADJUDICATION-1", "LITERATURE", "CONVENIENCE", "ALL",
                "INSUFFICIENT", "Whether an instrument-independent cross-country test exists "
                "is not established: needs an adjudication corpus SEARCHED for such tests; "
                "unscreened candidates include Hall-Jones 1999, co-cited by 10.5% of recent "
                "citers (02c line 395)"),
        "I14": ("I14", "DATA-ORIGIN", "—", "NAMED", "NOT-APPLICABLE", "N01, N02, N21, N06",
                "SUPPORTED", "The named re-estimates N01, N02, N21 and N06 use the AJR "
                "settler-mortality series (RD-E1, EL-E2, DML-E1); N31 was not read and is not "
                "counted"),
        "I15": ("I15", "DATA-ORIGIN", "ADJUDICATION-1", "LITERATURE", "CONVENIENCE", "ALL",
                "INSUFFICIENT", "Whether independent confirmation of L3 rests on one data "
                "origin across the literature is not established: needs a SEARCHED "
                "adjudication corpus"),
        "I19": ("I19", "COMPOSITION", "RECEPTION-1", "CORPUS", "EXHAUSTIVE", "ALL",
                "SUPPORTED", "Relevance composition of the citing set: the three primary "
                "tests, the authors' reanalysis and N42 are DIRECT (02c lines 105, 115-117); "
                "describes the citing set, not the evidence base"),
        "I18": ("I18", "CITATION-USE", "RECEPTION-1", "WITHIN-SAMPLE", "CONVENIENCE",
                "N01, N02, N03, N04, N05, N06, N12", "SUPPORTED-WITHIN-SAMPLE",
                "Polarity of the 7 top-15 members whose citing passage was read and can be "
                "located; 8 of the top 15 remain unclear"),
    }
    rep_inferences = [replace.get(i[0], i) for i in AS_RUN_INFERENCES]
    rep_dimensions = dict(AS_RUN_DIMENSIONS)
    rep_dimensions["Recent-paper dependence"] = (
        "UNASSESSED", "—", "Recent corpus selected on citing AJR 2001, so founding-paper "
        "citation is 100% by construction; 0/25 passages read (I05). Assessable with inspected "
        "passages for a prespecified sample, or with co-citation beyond the target (that "
        "evidence is owned by founding-cluster dominance and would be NESTED)")
    rep_dimensions["Lack of decisive tests"] = (
        "UNASSESSED", "—", "A concern score needs an absence over a SEARCHED adjudication corpus "
        "(I12 INSUFFICIENT). Named statements I13 and the data-origin result I14 stand as "
        "findings but cannot carry the score under cn7-map-2")
    rep_dimensions["Adjacent-field neglect"] = (
        "UNASSESSED", "—", "Concern rested only on co-citation over unscreened citers (I11); the "
        "source layer engaged the rivals (I10). Assessable with read downstream engagement in a "
        "screened population, or the dominant cluster's reference lists for the locked "
        "directly-adjudicating sources")
    rep_dimensions["Poor critique uptake"] = (
        "UNASSESSED", "—", "Concern rested only on co-citation over unscreened citers (I17). The "
        "dominant cluster engaged the critique (I16), which would support SCORED 0 if that "
        "cluster is the uptake population (Section H steps 3-4); otherwise needs read uptake in "
        "screened citers that rely on the settler-mortality data")
    rep_findings = [("Finding 2", "confirmed", "I14") if f[0] == "Finding 2" else f
                    for f in AS_RUN_FINDINGS]
    repaired = render(
        "CANDIDATE GATE FIXTURE — ACEMOGLU REPAIRED (SAME EVIDENCE)",
        provenance_notes("repaired (expected: PASS-WITH-REVIEW; formal band withheld, coverage 5/10)")
        + ["Repairs applied to the transcription (no new retrieval):"]
        + [f"  {rid}: {text}" for rid, text in REPAIRS],
        [reception_register(f"{rec_inspected}/50"), RECENT_REGISTER, adjudication_register], rep,
        rep_inferences, [composition_line("I19", "RECEPTION-1", rep)], rep_dimensions,
        rep_findings, ("RISK BAND: WITHHELD — coverage after Gate B is 5/10, below the "
                       "PROVISIONAL 70% gate (R17)",))

    # --- clean control: a structural question that metadata answers -------------------
    ctl = {}
    for sid, row in base.items():
        if row[1] == "RECEPTION-1":
            ctl[sid] = [row[0], "RECEPTION-1", "UNKNOWN", "CITES-UNINSPECTED", "UNKNOWN",
                        "METADATA", "NOT-INSPECTED", "reference list and record only"]
    ctl["N00"] = [OUTSIDE_ROWS["N00"][0], "OUTSIDE", "UNKNOWN", "NOT-CITING", "UNKNOWN",
                  "METADATA", "NOT-APPLICABLE", "database records only"]
    keep = {"I01", "I02", "I03", "I04"}
    ctl_inferences = [i for i in AS_RUN_INFERENCES if i[0] in keep]
    ctl_dimensions = {}
    for name in DIMENSIONS:
        if name == "Founding-cluster dominance":
            ctl_dimensions[name] = ("SCORED 1", "I03 (+), I04 (+)",
                                    "authorship and co-citation counts")
        elif name == "Internal citation density":
            ctl_dimensions[name] = ("SCORED 0", "I01 (-)", "inside the defined corpus only")
        elif name == "Intervention-evidence ratchet":
            ctl_dimensions[name] = ("N/A", "—", "No intervention claim")
        else:
            ctl_dimensions[name] = ("UNASSESSED", "—", "Outside this structural question; "
                                    "needs read citing passages or claim-testing sources")
    control = render(
        "CANDIDATE GATE FIXTURE — ACEMOGLU STRUCTURAL CLEAN CONTROL",
        provenance_notes("clean control, metadata sufficient (expected: PASS, no review "
                         "items)") + [
            "Question: is the top-50 AJR-citing corpus internally dense, and are single-"
            "database records for AJR 2001 reliable? Reference lists and records answer both,",
            "so no citing passage is needed and none is claimed."],
        [reception_register("0/50"),
         {"id": "ADJUDICATION-1", "role": "ADJUDICATION",
          "question": "Not needed: no evidence-base inference is made",
          "rule": "none", "discovery": "NONE — no claim-testing inference is made",
          "selected": "NO", "size": 0, "coverage": "0/0"}],
        ctl, ctl_inferences, [], ctl_dimensions,
        [("Finding 1", "confirmed", "I02"), ("Finding 2", "confirmed", "I01")])
    return {"acemoglu-as-run-transcribed.txt": as_run, "acemoglu-repaired.txt": repaired,
            "acemoglu-structural-control.txt": control}


def main() -> int:
    source, outdir = Path(sys.argv[1]), Path(sys.argv[2])
    run = parse_run(read_input(source))
    for name, text in build(run).items():
        path = outdir / name
        path.write_text(text, encoding="utf-8")
        print(f"{name}\tsha256 {hashlib.sha256(text.encode()).hexdigest()}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
