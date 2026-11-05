#!/usr/bin/env python3
"""Regression checks for the NON-CANONICAL citation-network v2-candidate gates (revision 3).

Fixtures here are tuned regressions built around one observed v1 run (Acemoglu, FAIL-CN-007),
one live run of candidate revision 2 on the same paper, and hand-written controls. Passing them
shows the candidate checker behaves as designed on these inputs. It is not held-out
validation: the live run was used to design revision 3, so it is a regression input too.

    python3 tests/test-citation-network-v2-gates.py

Set CN7_02C_PATH to the Acemoglu Stage-2c output (Provenance-Atlas branch
audit/acemoglu-colonial-origins) to also rebuild the Acemoglu fixtures and compare bytes, and
CN7_LIVE_RUN_DIR to the live run's directory (Provenance-Atlas branch
audit/acemoglu-colonial-origins-v2cand, examples/research/acemoglu-colonial-origins/
citation-network-v2cand) to rebuild the live fixture.
"""
from __future__ import annotations

import os
import re
import subprocess
import sys
import tempfile
from pathlib import Path

TESTS = Path(__file__).resolve().parent
REPO = TESTS.parent
CANDIDATES = REPO / "candidates" / "research-analysis"
# CN7_GATES_PATH lets tests/ablate-citation-network-v2-gates.py point the suite at a sabotaged copy.
GATES = Path(os.environ.get("CN7_GATES_PATH", CANDIDATES / "check-citation-network-v2-gates.py"))
V1_CHECKER = REPO / "prompts" / "research-analysis" / "check-citation-network-output.py"
V1_PROMPT = REPO / "prompts" / "research-analysis" / "2-citation-network.txt"
CASES = TESTS / "cases" / "citation-network-v2-gates"
V1_CONTROL = TESTS / "cases" / "citation-network-checker" / "complete-clean-control.md"

AS_RUN = CASES / "acemoglu-as-run-transcribed.txt"
REPAIRED = CASES / "acemoglu-repaired.txt"
CONTROL = CASES / "acemoglu-structural-control.txt"
OVERLAP = CASES / "overlap-synthetic.txt"
POWER_BLOCKS = CASES / "power-posing-v2-blocks.txt"
LIVE = CASES / "live-v2cand2-acemoglu.txt"

checks = 0


def require(condition: bool, message: str) -> None:
    global checks
    checks += 1
    if not condition:
        raise AssertionError(message)


def run_tool(tool: Path, *args: str) -> tuple[int, str]:
    result = subprocess.run([sys.executable, "-I", str(tool), *args], check=False,
                            capture_output=True, text=True)
    return result.returncode, result.stdout + result.stderr


def gates_text(text: str, *args: str) -> tuple[int, str]:
    with tempfile.TemporaryDirectory() as tmp:
        path = Path(tmp) / "case.txt"
        path.write_text(text, encoding="utf-8")
        return run_tool(GATES, str(path), *args)


def failure_codes(output: str) -> list[str]:
    return sorted(line.split("\t")[1] for line in output.splitlines()
                  if line.startswith("GATE_FAIL\t"))


def review_codes(output: str) -> list[str]:
    return sorted(m[1] for m in re.finditer(r"^REVIEW_ITEM_\d+\t([A-Z_]+) — ", output, re.M))


def result_line(output: str) -> str:
    return next(line for line in output.splitlines() if line.startswith("V2_GATES_RESULT"))


def mutate(text: str, old: str, new: str) -> str:
    count = text.count(old)
    require(count == 1, f"mutation anchor found {count} times: {old[:70]!r}")
    return text.replace(old, new)


def expect_fail(name: str, text: str, code: str) -> None:
    status, output = gates_text(text)
    require(status == 1, f"{name}: expected FAIL, got exit {status}\n{output}")
    require(code in failure_codes(output), f"{name}: expected {code}, got "
            f"{failure_codes(output)}")


def expect_review(name: str, text: str, code: str) -> None:
    status, output = gates_text(text)
    require(status == 0, f"{name}: expected PASS-WITH-REVIEW, got exit {status}\n{output}")
    require(code in review_codes(output), f"{name}: expected review {code}, got "
            f"{review_codes(output)}")


def test_acemoglu_as_run() -> None:
    status, output = run_tool(GATES, str(AS_RUN))
    require(status == 1, "as-run transcription must FAIL")
    expected = sorted([
        "LOCATOR_MISSING",              # N01: inspected, no locator in 02c
        "LOCATOR_MISSING",              # N08
        "LOCATOR_MISSING",              # N09
        "LOCATOR_MISSING",              # N14
        "LOCATOR_MISSING",              # AL
        "USE_WITHOUT_CONTEXT",          # N11 polarity assumed from N05, never read
        "REUSE_WITHOUT_ACCESS",         # N31 reuse claimed from a located record
        "ADJUDICATION_CORPUS_MISSING",  # one reception corpus did both jobs
        "COVERAGE_MISMATCH",            # 13/50 declared; 11/50 inspected
        "INFERENCE_OVERCLAIMED",        # I05 recent citation use, 0/25 read
        "INFERENCE_OVERCLAIMED",        # I12 absence claim with no adjudication search
        "INFERENCE_OVERCLAIMED",        # I14 data origin includes unread N31
        "INFERENCE_OVERCLAIMED",        # I15 literature-wide data origin from reception
        "INFERENCE_OVERCLAIMED",        # I18 polarity sample includes unread N11
        "SCORED_ON_INSUFFICIENT",       # recent-paper dependence
        "SCORED_ON_INSUFFICIENT",       # lack of decisive tests
        "EVIDENCE_BASE_UNSEARCHED",     # lack of decisive tests scored with no adjudication search
        "DIMENSION_CLASS_MISSING",      # adjacent-field neglect: concern only from co-citation
        "DIMENSION_CLASS_MISSING",      # poor critique uptake: concern only from co-citation
        "FINDING_ON_INSUFFICIENT",      # Finding 2
        "BAND_ISSUED_BELOW_GATE",       # the run's >20-40% band, with 5/10 after Gate B
    ])
    require(failure_codes(output) == expected, f"as-run failures changed: "
            f"{failure_codes(output)}")
    require(review_codes(output) == ["CODED_FROM_METADATA", "POSSIBLE_DUPLICATE_WORK"],
            f"as-run review items changed: {review_codes(output)}")
    require("1 pairs of rows look like one work under two records" in output
            and "N05/N11 (RECEPTION-1)" in output, "the Handbook chapter and its working paper "
            "should be flagged as one work")
    for iid in ("I05", "I12", "I14", "I15", "I18"):
        require(f"INFERENCE_OVERCLAIMED\t{iid} " in output, f"{iid} not caught")
    require("RECEPTION-1 declared 13/50, ledger 11/50" in output, "coverage recount missing")
    require("COVERAGE_DECLARED\t9/10" in output and "COVERAGE_AFTER_GATES\t5/10" in output
            and "PROVISIONAL_70_GATE\tNOT MET" in output,
            "as-run coverage after gates should fall to 5/10, below the provisional gate")
    for iid in ("I01", "I02", "I06", "I08", "I09", "I13", "I16", "I19", "I20"):
        require(re.search(rf"inference {iid}\t\S+\t\S+\tdeclared SUPPORTED\trecomputed "
                          r"SUPPORTED$", output, re.M), f"valid inference {iid} not passed")


def test_acemoglu_repaired() -> None:
    status, output = run_tool(GATES, str(REPAIRED))
    require(status == 0, f"repaired must pass gates\n{output}")
    require(result_line(output) == "V2_GATES_RESULT\tPASS-WITH-REVIEW\titems=1", result_line(output))
    require(review_codes(output) == ["CODED_FROM_METADATA"], review_codes(output))
    # The formal band is withheld on this evidence: 5 of 10 applicable dimensions survive.
    require("COVERAGE_AFTER_GATES\t5/10 (50%)" in output, "repaired coverage should be 5/10")
    require("PROVISIONAL_70_GATE\tNOT MET" in output, "repaired case should not meet the gate")
    # Valid findings survive: every standardized finding keeps a passing basis.
    require("FINDING_ON_INSUFFICIENT" not in output, "a valid finding was rejected")
    require("RECEPTION-1\tRECEPTION\tmembers 49\tcontexts inspected 8" in output,
            "reception coverage recount (11 read, 8 locatable; 49 works after R18)")
    text = REPAIRED.read_text(encoding="utf-8")
    band = next(line for line in text.splitlines() if line.startswith("RISK BAND:"))
    require(band.startswith("RISK BAND: WITHHELD"), "repaired fixture must withhold the band")
    expect_fail("band issued below the gate", mutate(
        text, band, "RISK BAND: >20%–40% normal field clustering with some weaknesses"),
        "BAND_ISSUED_BELOW_GATE")


def test_structural_control() -> None:
    status, output = run_tool(GATES, str(CONTROL))
    require(status == 0 and result_line(output) == "V2_GATES_RESULT\tPASS",
            f"metadata-sufficient control must PASS cleanly\n{output}")
    require(not review_codes(output), "clean control produced review items")
    require("contexts inspected 0" in output, "control should have no inspected contexts")


def test_overlap() -> None:
    text = OVERLAP.read_text(encoding="utf-8")
    status, output = gates_text(text)
    require(status == 0 and result_line(output) == "V2_GATES_RESULT\tPASS",
            f"overlap control must PASS\n{output}")
    require("corpus RECEPTION-1\tRECEPTION\tmembers 4" in output, "reception count")
    require("corpus ADJUDICATION-1\tADJUDICATION\tmembers 4" in output, "adjudication count")
    s2 = next(line for line in text.splitlines() if line.startswith("| S2 "))
    expect_fail("overlap: one row per corpus", mutate(
        text, s2, s2.replace("RECEPTION-1+ADJUDICATION-1", "RECEPTION-1") + "\n"
        + s2.replace("RECEPTION-1+ADJUDICATION-1", "ADJUDICATION-1")), "DUPLICATE_SOURCE")
    expect_fail("overlap: non-citing source in a target-selected corpus", mutate(
        text, "| S5 synthetic earlier independent test | ADJUDICATION-1 |",
        "| S5 synthetic earlier independent test | RECEPTION-1+ADJUDICATION-1 |"),
        "NOT_CITING_IN_TARGET_CORPUS")
    expect_fail("overlap: adjudication composition double-counts an overlap source", mutate(
        text, "DIRECT=3; ADJACENT=1; BACKGROUND=0; UNRELATED=0; UNKNOWN=0 | TOTAL=4",
        "DIRECT=4; ADJACENT=1; BACKGROUND=0; UNRELATED=0; UNKNOWN=0 | TOTAL=5"),
        "INFERENCE_OVERCLAIMED")
    unscreened = mutate(mutate(
        text, "| ADJUDICATION-1 | DIRECT (L1) | CITES-UNINSPECTED |",
        "| ADJUDICATION-1 | UNKNOWN | CITES-UNINSPECTED |"),
        "DIRECT=3; ADJACENT=1; BACKGROUND=0; UNRELATED=0; UNKNOWN=0 | TOTAL=4",
        "DIRECT=2; ADJACENT=1; BACKGROUND=0; UNRELATED=0; UNKNOWN=1 | TOTAL=4")
    status, output = gates_text(unscreened)
    require(status == 1 and "INFERENCE_OVERCLAIMED\tO5 " in output
            and "ABSENCE with 1 unscreened members" in output
            and "INFERENCE_OVERCLAIMED\tO3 " not in output,
            f"overlap: absence over an unscreened member must fail alone\n{output}")
    o6 = next(line for line in text.splitlines() if line.startswith("| O6 "))
    random_sample = mutate(text, o6, o6.replace("| WITHIN-SAMPLE | CONVENIENCE | INSPECTED | "
                                                "SUPPORTED-WITHIN-SAMPLE |",
                                                "| CORPUS | PRESPECIFIED-RANDOM | S2, S3 | "
                                                "SUPPORTED |"))
    expect_review("overlap: corpus-wide estimate from a declared random sample", random_sample,
                  "SAMPLE_DECLARED_RANDOM")
    o5 = next(line for line in text.splitlines() if line.startswith("| O5 "))
    for name, old, new, message in (
            ("absence over a partial result set", "| EXHAUSTIVE |", "| CONVENIENCE |",
             "ABSENCE needs the whole search result set"),
            ("absence claimed at corpus scope", "| LITERATURE |", "| CORPUS |",
             "ABSENCE is LITERATURE-scope")):
        status, output = gates_text(mutate(text, o5, o5.replace(old, new)))
        require(status == 1 and "INFERENCE_OVERCLAIMED\tO5 " in output and message in output,
                f"overlap: {name}\n{output}")
    bounded = mutate(unscreened, o5, "| O5 | ABSENCE | ADJUDICATION-1 | WITHIN-SAMPLE | "
                     "PRESPECIFIED-RULE | SCREENED | SUPPORTED-WITHIN-SAMPLE | No preregistered "
                     "replication among the 3/4 screened results; 1 unscreened |")
    status, output = gates_text(bounded)
    require(status == 0 and "BOUNDED_ABSENCE" in review_codes(output)
            and "COVERAGE_IF_REVIEW_ITEMS_WITHDRAWN\t1/10 (10%)\twithdrawn: lack of decisive "
                "tests" in output,
            f"overlap: a bounded absence must pass to review and show in sensitivity\n{output}")
    status, output = gates_text(mutate(
        bounded, "CORPUS DISCOVERY: SEARCHED — synthetic topic query; 4 results, all screened",
        "CORPUS DISCOVERY: NONE — assembled"))
    require(status == 1 and "INFERENCE_OVERCLAIMED\tO5 " in output
            and "ABSENCE needs an ADJUDICATION corpus that was SEARCHED" in output,
            f"overlap: a bounded absence still needs a searched corpus\n{output}")
    expect_fail("overlap: bounded absence without screened/total", mutate(
        bounded, "among the 3/4 screened results", "among the screened results"),
        "INFERENCE_OVERCLAIMED")
    expect_fail("overlap: searched adjudication corpus without a lock", mutate(
        text, "CORPUS LOCK: synthetic search record locked before screening (sha256 "
        "0000-synthetic)\n", ""), "REGISTER_FIELD")
    uptake = mutate(mutate(text, "| O7 | SOURCE-RESULT |",
                           "| O8 | ENGAGEMENT | — | NAMED | NOT-APPLICABLE | S3 | SUPPORTED | S3 "
                           "cites S2's objection without addressing it |\n| O9 | CO-CITATION | "
                           "POPULATION | POPULATION | NOT-APPLICABLE | UNSCREENED | SUPPORTED | "
                           "S2 co-cited by 1/10 citers of T |\n| O7 | SOURCE-RESULT |"),
                    "| Poor critique uptake | UNASSESSED | — | synthetic case: no critique traced |",
                    "| Poor critique uptake | SCORED 1 | O8 (+), O9 (+) | S3 does not address S2 |")
    status, output = gates_text(uptake)
    require(status == 0 and "CO_CITATION_UNSCREENED" in review_codes(output)
            and "COVERAGE_AFTER_GATES\t3/10" in output
            and "withdrawn: poor critique uptake" in output,
            f"overlap: co-citation beside qualifying engagement goes to review\n{output}")
    expect_fail("overlap: uptake concern from co-citation alone", mutate(
        uptake, "| SCORED 1 | O8 (+), O9 (+) |", "| SCORED 1 | O9 (+) |"),
        "DIMENSION_CLASS_MISSING")
    seven = uptake
    for old, new in (
            ("| Founding-cluster dominance | UNASSESSED | — | synthetic case: no authorship or "
             "co-citation data |", "| Founding-cluster dominance | SCORED 1 | O1 (+) | x |"),
            ("| Recent-paper dependence | UNASSESSED | — | synthetic case: no recent corpus |",
             "| Recent-paper dependence | SCORED 1 | O6 (+) | x |"),
            ("| Proxy mismatch | UNASSESSED | — | synthetic case: no construct comparison |",
             "| Proxy mismatch | SCORED 1 | O7 (+) | x |"),
            ("| Adjacent-field neglect | UNASSESSED | — | synthetic case: no Section E lock |",
             "| Adjacent-field neglect | SCORED 1 | O8 (+) | x |")):
        seven = mutate(seven, old, new)
    status, output = gates_text(seven + "\nRISK BAND: >20%–40% synthetic band\n")
    require(status == 0 and "COVERAGE_AFTER_GATES\t7/10" in output
            and "COVERAGE_IF_REVIEW_ITEMS_WITHDRAWN\t5/10 (50%)\twithdrawn: adjacent-field "
                "neglect, poor critique uptake" in output
            and "NAMED_ONLY_BASIS" in review_codes(output)
            and "PROVISIONAL_70_GATE\tMET ONLY IF REVIEW ITEMS RESOLVE FOR THE SCORE" in output
            and "BAND_CONDITIONAL" in review_codes(output),
            f"a band that meets the gate only with review-pending dimensions goes to review\n"
            f"{output}")
    status, output = gates_text(seven + "\nRISK BAND: WITHHELD — pending review items\n")
    require(status == 0 and "BAND_CONDITIONAL" not in review_codes(output),
            "a withheld band raises no band review")
    status, output = gates_text(mutate(
        text, "UNKNOWN=1 | TOTAL=4", "UNKNOWN=1 | TOTAL=5"))
    require(status == 1 and "TOTAL=5, members 4" in output, "composition TOTAL not checked")
    expect_fail("overlap: corpus-wide use claim from an unrandomized subset", mutate(
        random_sample, "| CORPUS | PRESPECIFIED-RANDOM | S2, S3 |",
        "| CORPUS | PRESPECIFIED-RULE | S2, S3 |"), "INFERENCE_OVERCLAIMED")
    expect_fail("overlap: literature scope without an adjudication search", mutate(
        text, "CORPUS DISCOVERY: SEARCHED — synthetic topic query; 4 results, all screened",
        "CORPUS DISCOVERY: NONE — assembled"), "INFERENCE_OVERCLAIMED")


def test_adversarial_mutations() -> None:
    text = REPAIRED.read_text(encoding="utf-8")
    # N11 is merged into N05 in the repaired ledger (R18); N27 is a record-only row.
    n27 = next(line for line in text.splitlines() if line.startswith("| N27 "))
    rows = {line.split("|")[1].strip(): line for line in text.splitlines()
            if re.match(r"^\| I\d\d \|", line)}

    # Gate A
    expect_fail("use class without an inspected passage",
                mutate(text, n27, n27.replace("CITES-UNINSPECTED", "PREMISE")),
                "USE_WITHOUT_CONTEXT")
    expect_fail("inspected without full text or excerpt",
                mutate(text, n27, n27.replace("NOT-INSPECTED", "INSPECTED")),
                "CONTEXT_WITHOUT_ACCESS")
    expect_fail("coverage overstated by counting passages that cannot be located",
                mutate(text, "CITATION CONTEXT COVERAGE: RECEPTION-1 8/49",
                       "CITATION CONTEXT COVERAGE: RECEPTION-1 11/49"), "COVERAGE_MISMATCH")
    expect_fail("coverage restated wrongly elsewhere in the output",
                text + "\nConfidence: CITATION CONTEXT COVERAGE: RECEPTION-1 13/50\n",
                "COVERAGE_MISMATCH")
    expect_fail("corpus size does not match the ledger",
                mutate(text, "CORPUS SIZE: 25", "CORPUS SIZE: 2695"), "CORPUS_SIZE_MISMATCH")
    expect_fail("adjudication corpus removed",
                mutate(text, "CORPUS ROLE: ADJUDICATION", "CORPUS ROLE: RECEPTION"),
                "ADJUDICATION_CORPUS_MISSING")
    control = CONTROL.read_text(encoding="utf-8")
    n27c = next(line for line in control.splitlines() if line.startswith("| N27 "))
    expect_review("relevance coded from a record only",
                  mutate(control, n27c, n27c.replace("| UNKNOWN | CITES-UNINSPECTED |",
                                                     "| BACKGROUND | CITES-UNINSPECTED |")),
                  "CODED_FROM_METADATA")

    # Gate B
    expect_fail("recent citation use re-declared sufficient",
                mutate(text, rows["I05"], rows["I05"].replace("| INSUFFICIENT |",
                                                              "| SUPPORTED |")),
                "INFERENCE_OVERCLAIMED")
    expect_fail("absence re-declared sufficient without an adjudication search",
                mutate(text, rows["I12"], rows["I12"].replace("| INSUFFICIENT |",
                                                              "| SUPPORTED |")),
                "INFERENCE_OVERCLAIMED")
    expect_fail("extrapolating a convenience sample to the corpus",
                mutate(text, rows["I18"], rows["I18"].replace("| WITHIN-SAMPLE |",
                                                              "| CORPUS |")),
                "INFERENCE_OVERCLAIMED")
    expect_fail("within-sample statement labelled as corpus-wide support",
                mutate(text, rows["I18"], rows["I18"].replace("| SUPPORTED-WITHIN-SAMPLE |",
                                                              "| SUPPORTED |")),
                "DISPOSITION_MISMATCH")
    expect_fail("engagement claimed for a background user",
                mutate(text, rows["I16"], rows["I16"].replace("| N01, NS |", "| N01, NS, N04 |")),
                "INFERENCE_OVERCLAIMED")
    expect_fail("graph statement extended beyond a target-selected corpus",
                mutate(text, rows["I01"], rows["I01"].replace("| CORPUS |", "| LITERATURE |")),
                "INFERENCE_OVERCLAIMED")
    expect_fail("unknown codes dropped from a composition",
                mutate(text, "UNKNOWN=14 | TOTAL=49", "UNKNOWN=0 | TOTAL=49"),
                "INFERENCE_OVERCLAIMED")
    expect_fail("unknown rows silently reclassified in the count",
                mutate(text, "BACKGROUND=24; UNRELATED=0; UNKNOWN=14",
                       "BACKGROUND=38; UNRELATED=0; UNKNOWN=0"), "INFERENCE_OVERCLAIMED")
    expect_fail("population count with no k/n",
                mutate(text, rows["I17"], re.sub(r"\d+/\d+", "few", rows["I17"])),
                "INFERENCE_OVERCLAIMED")
    status, output = gates_text(mutate(text, rows["I13"], rows["I13"].replace(
        "| SUPPORTED |", "| INSUFFICIENT |")))
    require(status == 0 and "OVER_WITHHELD" in review_codes(output),
            "withholding a supportable inference must be routed to review, not accepted")

    # Dimensions and findings
    recent = next(line for line in text.splitlines() if line.startswith("| Recent-paper dependence |"))
    expect_fail("recent dependence scored on unread passages",
                mutate(text, recent, "| Recent-paper dependence | SCORED 1 | I05 (+) | 02c line "
                       "467 |"), "SCORED_ON_INSUFFICIENT")
    lack = next(line for line in text.splitlines() if line.startswith("| Lack of decisive tests |"))
    expect_fail("lack of decisive tests scored on the withheld absence claim", mutate(
        text, lack, "| Lack of decisive tests | SCORED 1 | I12 (+), I13 (+) | x |"),
        "SCORED_ON_INSUFFICIENT")
    expect_fail("lack of decisive tests scored on named statements without a search", mutate(
        text, lack, "| Lack of decisive tests | SCORED 1 | I13 (+), I14 (+) | x |"),
        "EVIDENCE_BASE_UNSEARCHED")
    expect_fail("a zero for lack of decisive tests on named results without a search", mutate(
        text, lack, "| Lack of decisive tests | SCORED 0 | I13 (-), I14 (-) | x |"),
        "EVIDENCE_BASE_UNSEARCHED")
    uptake = next(line for line in text.splitlines() if line.startswith("| Poor critique uptake |"))
    expect_fail("uptake concern from co-citation, with engagement pointing the other way",
                mutate(text, uptake, "| Poor critique uptake | SCORED 1 | I16 (-), I17 (+) | x |"),
                "DIMENSION_CLASS_MISSING")
    status, output = gates_text(mutate(text, uptake, "| Poor critique uptake | SCORED 0 | I16 (-) "
                                       "| dominant cluster engaged |"))
    require(status == 0 and "COVERAGE_AFTER_GATES\t6/10 (60%)" in output
            and "PROVISIONAL_70_GATE\tNOT MET" in output
            and "NAMED_ONLY_BASIS" in review_codes(output)
            and "COVERAGE_IF_REVIEW_ITEMS_WITHDRAWN\t5/10 (50%)\twithdrawn: poor critique "
                "uptake" in output,
            f"the executor's alternative (uptake SCORED 0 on named works) passes to review and "
            f"the band stays withheld\n{output}")
    adjacent = next(line for line in text.splitlines()
                    if line.startswith("| Adjacent-field neglect |"))
    expect_fail("neglect concern from a rival's result plus co-citation", mutate(
        text, adjacent, "| Adjacent-field neglect | SCORED 1 | I11 (+), I20 (+) | x |"),
        "DIMENSION_CLASS_MISSING")
    founding = next(line for line in text.splitlines()
                    if line.startswith("| Founding-cluster dominance |"))
    expect_fail("an untagged inference", mutate(text, founding, founding.replace(
        "I03 (+), I04 (+)", "I03, I04 (+)")), "DIRECTION_TAG_MISSING")
    expect_fail("a concern score with only no-concern evidence", mutate(text, founding, founding.replace(
        "I03 (+), I04 (+)", "I03 (-), I04 (-)")), "NO_CONCERN_BASIS")
    expect_fail("a zero score with no affirmative evidence", mutate(
        text, "| Internal citation density | SCORED 0 | I01 (-) |",
        "| Internal citation density | SCORED 0 | I01 (+) |"), "NO_AFFIRMATIVE_BASIS")
    expect_fail("map line removed", mutate(text, "DIMENSION CLASS MAP: cn7-map-3\n", ""),
                "MAP_VERSION_MISSING")
    expect_fail("output declares another map", mutate(text, "DIMENSION CLASS MAP: cn7-map-3",
                                                       "DIMENSION CLASS MAP: cn7-map-2"),
                "MAP_VERSION_MISMATCH")
    n02 = next(line for line in text.splitlines() if line.startswith("| N02 "))
    expect_fail("inspected row without a locator", mutate(
        text, n02, n02.replace("RD-E1, RD-E3, RD-E4: ", "")), "LOCATOR_MISSING")
    n08 = next(line for line in text.splitlines() if line.startswith("| N08 "))
    relocated = mutate(mutate(mutate(
        text, n08, n08.replace("| CITES-UNINSPECTED |", "| MENTIONS |").replace(
            "| NOT-INSPECTED | full text read; no passage locator recorded |",
            "| INSPECTED | citing passage read |")),
        "CITATION CONTEXT COVERAGE: RECEPTION-1 8/49", "CITATION CONTEXT COVERAGE: RECEPTION-1 9/49"),
        "| N01, N02, N03, N04, N05, N06, N12 |", "| N01, N02, N03, N04, N05, N06, N08, N12 |")
    status, output = gates_text(relocated)
    require(status == 1 and "LOCATOR_MISSING" in failure_codes(output)
            and "INFERENCE_OVERCLAIMED\tI18 " in output and "has no locator" in output,
            f"a passage without a locator cannot carry a citation-use inference\n{output}")
    expect_fail("score with no basis",
                mutate(text, recent, "| Recent-paper dependence | SCORED 0 | — | none |"),
                "SCORED_WITHOUT_BASIS")
    expect_fail("unassessed with no note",
                mutate(text, recent, "| Recent-paper dependence | UNASSESSED | — | — |"),
                "BASIS_NOTE_MISSING")
    expect_fail("a dimension row removed", mutate(text, recent + "\n", ""), "DIMENSION_ROWS")
    expect_fail("unscored dimension listing an inference",
                mutate(text, "| Recent-paper dependence | UNASSESSED | — |",
                       "| Recent-paper dependence | UNASSESSED | I05 |"), "UNSCORED_WITH_BASIS")
    expect_fail("finding re-based on the literature-wide claim",
                mutate(text, "| Finding 2 | confirmed | I14 |", "| Finding 2 | confirmed | I14, I15 |"),
                "FINDING_ON_INSUFFICIENT")
    status, output = gates_text(mutate(text, "| Finding 2 | confirmed | I14 |",
                                       "| Finding 2 | provisional | I14, I15 |"))
    require(status == 0, "a provisional finding may list an insufficient inference")
    expect_review("recent dependence re-based on co-citation over the citing population",
                  mutate(text, recent, "| Recent-paper dependence | SCORED 1 | I03 (+) | "
                         "co-citation of other cluster members |"), "BY_CONSTRUCTION_RISK")


def test_applicability() -> None:
    status, output = run_tool(GATES, str(V1_CONTROL))
    require(status == 3 and output.startswith("NOT_APPLICABLE"),
            "a v1 output must be NOT_APPLICABLE, not judged")
    status, output = run_tool(GATES, str(V1_CONTROL), "--require-v2")
    require(status == 1 and "VERSION_LINE_MISSING" in output,
            "--require-v2 must fail a missing version line")
    text = REPAIRED.read_text(encoding="utf-8").replace(
        "INSTRUMENT VERSION: 2-citation-network v2-candidate.3\n", "")
    status, output = gates_text(text)
    require(status == 3, "a fragment without the version line is not judged")
    for old_revision in ("v2-candidate", "v2-candidate.2"):
        status, output = gates_text(REPAIRED.read_text(encoding="utf-8").replace(
            "v2-candidate.3\n", old_revision + "\n"))
        require(status == 3, f"an output of {old_revision} is not judged by revision 3")


def assemble_power_posing() -> str:
    blocks = POWER_BLOCKS.read_text(encoding="utf-8")

    def block(name: str) -> str:
        return blocks.split(f"BEGIN {name}\n", 1)[1].split(f"END {name}\n", 1)[0]

    text = V1_CONTROL.read_text(encoding="utf-8")
    first_break = text.index("\n\n")
    text = text[:first_break] + "\n\n" + block("VERSION").strip() + text[first_break:]
    text = mutate(text, "\nSECTION A: CITATION NETWORK STRUCTURE AND CARTEL DETECTION\n",
                  "\n" + block("BLOCK A0") + "\nSECTION A: CITATION NETWORK STRUCTURE AND "
                  "CARTEL DETECTION\n")
    text = mutate(text, "\nSECTION K: CARTEL-RISK SCORING\n",
                  "\n" + block("BLOCK K0") + "\nSECTION K: CARTEL-RISK SCORING\n")
    return text


def v1_summary(path: Path) -> tuple[int, list[str]]:
    status, output = run_tool(V1_CHECKER, str(path))
    keep = [line for line in output.splitlines()
            if line.split("\t")[0] in {"STRUCTURAL_RESULT", "CONTENT_RESULT", "PASS", "FAIL",
                                       "PASS-WITH-REVIEW"} or "_FAIL\t" in line
            or line.startswith("REVIEW_ITEM_")]
    return status, keep


def test_interactions() -> None:
    combined = assemble_power_posing()
    with tempfile.TemporaryDirectory() as tmp:
        path = Path(tmp) / "power-posing-with-v2.md"
        path.write_text(combined, encoding="utf-8")
        before, after = v1_summary(V1_CONTROL), v1_summary(path)
        require(before == after, f"v1 checker result changed by v2 blocks:\n{before}\n{after}")
        require(before[0] == 0, "v1 control must still pass the v1 checker")

        sys.path.insert(0, str(REPO))
        from atlas import native  # noqa: E402  (Provenance's copy of the Atlas parser)
        original = native.parse(V1_CONTROL.read_text(encoding="utf-8"))
        parsed = native.parse(combined)

        def strip_lines(findings: list) -> list:
            return [{k: v for k, v in f.items() if not k.startswith("line")
                     and k not in {"field_lines"}} for f in findings]
        require(not parsed["issues"], f"native parser issues: {parsed['issues']}")
        require(strip_lines(parsed["findings"]) == strip_lines(original["findings"]),
                "native parser findings changed")

        status, output = run_tool(GATES, str(path))
        require(status == 1, "candidate gates must FAIL the v1-era control")
        require(failure_codes(output) == sorted([
            "SCORED_WITHOUT_BASIS", "SCORED_WITHOUT_BASIS",       # two SCORED 0 rows, no evidence
            "EVIDENCE_BASE_UNSEARCHED",                           # lack of decisive tests 2, no search
            "LOCATOR_MISSING", "LOCATOR_MISSING", "LOCATOR_MISSING",  # S2-S4 have no page refs
            "INFERENCE_OVERCLAIMED",     # P02 citation use rests on those unlocatable passages
            "FINDING_ON_INSUFFICIENT"]),  # Finding 2 relies on P02
                f"unexpected gate result on the v1 control: {failure_codes(output)}")
        require("INFERENCE_OVERCLAIMED\tP02 " in output, "P02 should fail on locators")
        require("Recent-paper dependence is SCORED 0 with no listed inference" in output
                and "Adjacent-field neglect is SCORED 0 with no listed inference" in output,
                "expected the two SCORED 0 rows that rest on no evidence")
        require("SCORECARD_DISAGREES" not in output, "basis table must mirror Artifact 8")
        require(review_codes(output) == ["NAMED_ONLY_BASIS"]
                and "Poor critique uptake is SCORED 0 on named works only (P05)" in output,
                f"uptake SCORED 0 on a named engagement should go to review\n{output}")
        disagree = mutate(combined, "| Recent-paper dependence | SCORED 0 | — | Artifact 8 basis: "
                          "supplied packet only; no recent corpus |",
                          "| Recent-paper dependence | UNASSESSED | — | no recent corpus |")
        status, output = gates_text(disagree)
        require("SCORECARD_DISAGREES" in failure_codes(output),
                "a basis disposition that differs from Artifact 8 must fail")
        status, output = gates_text(mutate(combined, "| Finding 2 | confirmed | P01, P02, P05 |\n",
                                           ""))
        require("FINDING_ROWS" in failure_codes(output), "a finding without a basis row")
        status, output = gates_text(mutate(combined, "| Finding 2 | confirmed | P01, P02, P05 |\n",
                                           "| Finding 2 | confirmed | P01, P02, P05 |\n"
                                           "| Finding 3 | confirmed | P01 |\n"))
        require("FINDING_ROWS" in failure_codes(output), "a basis row for a missing finding")

    vocab = re.compile(r"\b[A-Z][A-Z0-9-]*-(?:VERIFIED|CONFIRMED)\b")
    for path in (AS_RUN, REPAIRED, CONTROL, OVERLAP, POWER_BLOCKS, LIVE,
                 CANDIDATES / "2-citation-network.v2-candidate.txt"):
        text = path.read_text(encoding="utf-8")
        if path.name.endswith("v2-candidate.txt"):
            v1 = V1_PROMPT.read_text(encoding="utf-8")
            new = set(vocab.findall(text)) - set(vocab.findall(v1))
            require(not new, f"candidate adds authority tokens: {new}")
        else:
            require(not vocab.findall(text), f"{path.name} uses -CONFIRMED/-VERIFIED tokens")


def test_revision3_rules() -> None:
    """Each revision-3 rule, by mutation of a fixture that passes without it."""
    text = OVERLAP.read_text(encoding="utf-8")
    layers = ("CLAIM LAYER: L1 — the synthetic target claim T makes\n"
              "RIVAL: R1 — a synthetic rival explanation\n")
    status, output = gates_text(mutate(text, layers, ""))
    require(status == 1 and {"CLAIM_LAYERS_MISSING", "UNDEFINED_LAYER"} <= set(
        failure_codes(output)), f"claim layers removed\n{output}")
    s6 = next(line for line in text.splitlines() if line.startswith("| S6 "))
    status, output = gates_text(mutate(text, s6, s6.replace("DIRECT (L1)", "DIRECT (L2)")))
    require(status == 1 and failure_codes(output) == ["UNDEFINED_LAYER"]
            and "L2 is used in 1 relevance values (S6" in output,
            f"a relevance value naming an undefined layer\n{output}")
    expect_fail("record quality missing", mutate(
        text, "RECORD QUALITY: none known (synthetic records)\nKNOWN-ITEM", "KNOWN-ITEM"),
        "REGISTER_FIELD")
    recall = "KNOWN-ITEM RECALL: ADJUDICATION-1 2/2 (returned: S2, S5; not returned: none)"
    status, output = gates_text(mutate(text, recall + "\n", ""))
    require(status == 1 and failure_codes(output) == ["KNOWN_ITEM_RECALL"],
            f"a SEARCHED adjudication corpus without known-item recall\n{output}")
    expect_fail("recall above the known-item count", mutate(
        text, recall, recall.replace("2/2", "3/2")), "KNOWN_ITEM_RECALL")
    missed = mutate(text, recall, "KNOWN-ITEM RECALL: ADJUDICATION-1 1/2 (returned: S2; not "
                    "returned: S5)")
    status, output = gates_text(missed)
    require(status == 1 and "SEARCH_RECALL" in review_codes(output)
            and all(f"INFERENCE_OVERCLAIMED\t{i} " in output for i in ("O3", "O4", "O5"))
            and "missed known items (known-item recall 1/2)" in output,
            f"a search that missed a known item cannot bound literature-scope statements\n"
            f"{output}")
    o3 = next(line for line in missed.splitlines() if line.startswith("| O3 "))
    o4 = next(line for line in missed.splitlines() if line.startswith("| O4 "))
    o5 = next(line for line in missed.splitlines() if line.startswith("| O5 "))
    bounded = missed
    for row in (o3, o4):
        bounded = mutate(bounded, row, row.replace("| LITERATURE |", "| CORPUS |"))
    bounded = mutate(bounded, o5, "| O5 | ABSENCE | ADJUDICATION-1 | WITHIN-SAMPLE | "
                     "PRESPECIFIED-RULE | SCREENED | SUPPORTED-WITHIN-SAMPLE | No preregistered "
                     "replication among the 4/4 screened results |")
    status, output = gates_text(bounded)
    require(status == 0 and "SEARCH_RECALL" in review_codes(output),
            f"statements bounded to the search survive a recall shortfall, to review\n{output}")

    # A zero carries the same burden as a concern.
    lack = next(line for line in text.splitlines() if line.startswith("| Lack of decisive tests |"))
    zero = mutate(text, lack, "| Lack of decisive tests | SCORED 0 | O7 (-) | S5 and S6 test L1 |")
    expect_review("a zero for lack of decisive tests on named results", zero,
                  "DECISIVE_TEST_CLAIMED")
    expect_fail("that zero without a searched adjudication corpus", mutate(
        zero, "CORPUS DISCOVERY: SEARCHED — synthetic topic query; 4 results, all screened",
        "CORPUS DISCOVERY: NONE — assembled"), "EVIDENCE_BASE_UNSEARCHED")
    status, output = gates_text(mutate(text, lack, "| Lack of decisive tests | SCORED 1 | O7 (+) "
                                       "| S5 and S6 conflict |"))
    require(status == 0 and "DIMENSION_CLASS_MISSING" not in output,
            f"conflicting source results may carry the concern under cn7-map-3\n{output}")
    density = "| Internal citation density | SCORED 0 | O1 (-) |"
    expect_fail("(?) on an inference that passed Gate B", mutate(
        text, density, "| Internal citation density | SCORED 0 | O1 (-), O2 (?) |"),
        "PARTIAL_TAG_ON_PASSING")
    s5 = next(line for line in text.splitlines() if line.startswith("| S5 "))
    # S5 uncoded except for NOT-CITING, from its record only (compositions then fail; the review
    # item is what is checked here).
    status, output = gates_text(mutate(text, s5, "| S5 synthetic earlier independent test | "
                                       "ADJUDICATION-1 | UNKNOWN | NOT-CITING | UNKNOWN | METADATA "
                                       "| NOT-APPLICABLE | record only |"))
    require("CODED_FROM_METADATA" in review_codes(output)
            and "confirm each record shows it: S5" in output,
            f"NOT-CITING coded from a record only goes to review\n{output}")
    expect_fail("a data-origin result standing in for a decisive-test concern", mutate(
        text, lack, "| Lack of decisive tests | SCORED 1 | O4 (+) | one data origin |"),
        "DIMENSION_CLASS_MISSING")

    # Withholding is reviewed whichever word withholds it.
    repaired = REPAIRED.read_text(encoding="utf-8")
    i13 = next(line for line in repaired.splitlines() if line.startswith("| I13 "))
    status, output = gates_text(mutate(repaired, i13, i13.replace("| SUPPORTED |",
                                                                  "| NOT-ASSESSED |")))
    require(status == 0 and "OVER_WITHHELD" in review_codes(output)
            and "I13 (SOURCE-RESULT) declared NOT-ASSESSED" in output,
            f"NOT-ASSESSED on supportable evidence must go to review\n{output}")

    # One row per work.
    n05 = next(line for line in repaired.splitlines() if line.startswith("| N05 "))
    split = mutate(repaired, n05, n05 + "\n" + n05.replace(
        "| N05 W2108614304+W1580107285 2004 Institutions as the Fundamental Cause of ... |",
        "| N50 W1580107285 2005 Chapter 6 Institutions as a Fundamental Cause of ... |"))
    split = mutate(mutate(split, "CORPUS SIZE: 49", "CORPUS SIZE: 50"),
                   "CITATION CONTEXT COVERAGE: RECEPTION-1 8/49",
                   "CITATION CONTEXT COVERAGE: RECEPTION-1 9/50")
    status, output = gates_text(split)
    require("POSSIBLE_DUPLICATE_WORK" in review_codes(output) and "N05/N50" in output,
            f"a work entered under two records must be flagged\n{output}")
    generic = mutate(mutate(text, "| S1 synthetic highly cited user of T for another question |",
                            "| S1 Reply |"), "| S4 synthetic record, highly cited |",
                     "| S4 Reply (2012) |")
    status, output = gates_text(generic)
    require(status == 0 and "POSSIBLE_DUPLICATE_WORK" not in output,
            f"two short generic titles are not evidence of one work\n{output}")


def test_live_run() -> None:
    """Grok's live run of revision 2 (AJR 2001), with only revision 3's declarations added."""
    text = LIVE.read_text(encoding="utf-8")
    status, output = run_tool(GATES, str(LIVE))
    require(status == 0 and result_line(output) == "V2_GATES_RESULT\tPASS-WITH-REVIEW\titems=9",
            f"live fixture result changed\n{output}")
    require(review_codes(output) == sorted([
        "CODED_FROM_METADATA",      # ten adjudication rows coded or NOT-CITING from records
        "SEARCH_RECALL",            # the locked search returned 1 of 6 known items
        "POSSIBLE_DUPLICATE_WORK",  # nine record pairs that look like one work
        "SAMPLE_DECLARED_RANDOM",   # I06
        "BY_CONSTRUCTION_RISK",     # recent-paper dependence on a target-selected set
        "NAMED_ONLY_BASIS",         # adjacent-field neglect SCORED 0 on I19
        "DECISIVE_TEST_CLAIMED",    # lack of decisive tests SCORED 0 on I11
        "PARTIAL_BASIS",            # poor critique uptake SCORED 0 while I22 is NOT-ASSESSED
        "NAMED_ONLY_BASIS",         # poor critique uptake SCORED 0 on I18
    ]), f"live review items changed: {review_codes(output)}")
    require("COVERAGE_AFTER_GATES\t8/10 (80%)" in output
            and "COVERAGE_IF_REVIEW_ITEMS_WITHDRAWN\t4/10 (40%)\twithdrawn: adjacent-field "
                "neglect, lack of decisive tests, poor critique uptake, recent-paper "
                "dependence" in output
            and "PROVISIONAL_70_GATE\tMET ONLY IF REVIEW ITEMS RESOLVE FOR THE SCORE" in output,
            f"live coverage changed\n{output}")
    require("9 pairs of rows look like one work" in output and "returned 1/6 known items"
            in output and "BAND_CONDITIONAL" not in output, output)
    require(next(line for line in text.splitlines() if line.startswith("RISK BAND:"))
            .startswith("RISK BAND: WITHHELD"), "the run withheld its band")
    # The live run passed revision 2's gates; it would not have passed revision 3's without the
    # declarations revision 3 adds. That is a property of the new rules, not a re-grade.
    observed = text
    for line in text.splitlines():
        if line.startswith(("CLAIM LAYER:", "RIVAL:", "RECORD QUALITY:", "KNOWN-ITEM RECALL:",
                            "SAMPLE ATTRITION:")):
            observed = mutate(observed, line + "\n", "")
    observed = mutate(observed, "I18 (-), I22 (?)", "I18 (-)")
    status, output = gates_text(observed)
    require(status == 1 and failure_codes(output) == sorted(
        ["CLAIM_LAYERS_MISSING", "UNDEFINED_LAYER", "UNDEFINED_LAYER", "UNDEFINED_LAYER",
         "UNDEFINED_LAYER", "REGISTER_FIELD", "REGISTER_FIELD", "REGISTER_FIELD",
         "KNOWN_ITEM_RECALL", "SAMPLE_ATTRITION_UNREPORTED"])
            and all(f"UNDEFINED_LAYER\t{code} is used" in output for code in ("L1", "L3", "R1",
                                                                             "R2")),
            f"revision-3 declarations missing from the observed ledger: {failure_codes(output)}")
    expect_fail("attrition misreported", mutate(text, "SAMPLE ATTRITION: I06 2/6",
                                                "SAMPLE ATTRITION: I06 3/6"),
                "SAMPLE_ATTRITION_UNREPORTED")


def test_candidate_reproducible() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        out = Path(tmp) / "candidate.txt"
        status, output = run_tool(CANDIDATES / "make_v2_candidate.py", str(V1_PROMPT), str(out))
        require(status == 0, output)
        committed = (CANDIDATES / "2-citation-network.v2-candidate.txt").read_bytes()
        require(out.read_bytes() == committed, "committed candidate differs from its build")


def test_fixture_rebuild() -> None:
    source = os.environ.get("CN7_02C_PATH")
    if not source:
        print("SKIP\tAcemoglu fixture rebuild (set CN7_02C_PATH to the Stage-2c output)")
        return
    with tempfile.TemporaryDirectory() as tmp:
        status, output = run_tool(CASES / "build_acemoglu_fixtures.py", source, tmp)
        require(status == 0, output)
        for name in (AS_RUN.name, REPAIRED.name, CONTROL.name):
            require((Path(tmp) / name).read_bytes() == (CASES / name).read_bytes(),
                    f"{name} differs from its rebuild")
    print("REBUILT\tAcemoglu fixtures match their build from the pinned run output")


def test_live_fixture_rebuild() -> None:
    run_dir = os.environ.get("CN7_LIVE_RUN_DIR")
    if not run_dir:
        print("SKIP\tlive fixture rebuild (set CN7_LIVE_RUN_DIR to the live run directory)")
        return
    with tempfile.TemporaryDirectory() as tmp:
        status, output = run_tool(CASES / "build_live_v2cand_fixture.py", run_dir, tmp)
        require(status == 0, output)
        require((Path(tmp) / LIVE.name).read_bytes() == LIVE.read_bytes(),
                f"{LIVE.name} differs from its rebuild")
    status, output = run_tool(GATES, str(Path(run_dir) / "02c_citation_network_v2cand2.md"))
    require(status == 3 and output.startswith("NOT_APPLICABLE"),
            "the revision-2 run itself is not judged by revision 3")
    print("REBUILT\tlive fixture matches its build from the pinned run; the run is NOT_APPLICABLE")


def main() -> int:
    for test in (test_acemoglu_as_run, test_acemoglu_repaired, test_structural_control,
                 test_overlap, test_adversarial_mutations, test_revision3_rules, test_live_run,
                 test_applicability, test_interactions, test_candidate_reproducible,
                 test_fixture_rebuild, test_live_fixture_rebuild):
        test()
        print(f"ok\t{test.__name__}")
    print(f"PASS\t{checks} checks")
    return 0


if __name__ == "__main__":
    sys.exit(main())
