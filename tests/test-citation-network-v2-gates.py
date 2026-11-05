#!/usr/bin/env python3
"""Regression checks for the NON-CANONICAL citation-network v2-candidate gates (revision 2).

Fixtures here are tuned regressions built around one observed run (Acemoglu, FAIL-CN-007)
plus hand-written controls. Passing them shows the candidate checker behaves as designed
on these inputs. It is not held-out validation and not evidence from a live run.

    python3 tests/test-citation-network-v2-gates.py

Set CN7_02C_PATH to the Acemoglu Stage-2c output (Provenance-Atlas branch
audit/acemoglu-colonial-origins) to also rebuild the Acemoglu fixtures and compare bytes.
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
        "DIMENSION_CLASS_MISSING",      # adjacent-field neglect: concern only from co-citation
        "DIMENSION_CLASS_MISSING",      # poor critique uptake: concern only from co-citation
        "FINDING_ON_INSUFFICIENT",      # Finding 2
        "BAND_ISSUED_BELOW_GATE",       # the run's >20-40% band, with 5/10 after Gate B
    ])
    require(failure_codes(output) == expected, f"as-run failures changed: "
            f"{failure_codes(output)}")
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
    require("RECEPTION-1\tRECEPTION\tmembers 50\tcontexts inspected 8" in output,
            "reception coverage recount (11 read, 8 locatable)")
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
            and "COVERAGE_IF_REVIEW_ITEMS_WITHDRAWN\t6/10" in output
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
    n11 = next(line for line in text.splitlines() if line.startswith("| N11 "))
    rows = {line.split("|")[1].strip(): line for line in text.splitlines()
            if re.match(r"^\| I\d\d \|", line)}

    # Gate A
    expect_fail("use class without an inspected passage",
                mutate(text, n11, n11.replace("CITES-UNINSPECTED", "PREMISE")),
                "USE_WITHOUT_CONTEXT")
    expect_fail("inspected without full text or excerpt",
                mutate(text, n11, n11.replace("NOT-INSPECTED", "INSPECTED")),
                "CONTEXT_WITHOUT_ACCESS")
    expect_fail("coverage overstated by counting passages that cannot be located",
                mutate(text, "CITATION CONTEXT COVERAGE: RECEPTION-1 8/50",
                       "CITATION CONTEXT COVERAGE: RECEPTION-1 11/50"), "COVERAGE_MISMATCH")
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
                mutate(text, "UNKNOWN=14 | TOTAL=50", "UNKNOWN=0 | TOTAL=50"),
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
        "DIMENSION_CLASS_MISSING")
    uptake = next(line for line in text.splitlines() if line.startswith("| Poor critique uptake |"))
    expect_fail("uptake concern from co-citation, with engagement pointing the other way",
                mutate(text, uptake, "| Poor critique uptake | SCORED 1 | I16 (-), I17 (+) | x |"),
                "DIMENSION_CLASS_MISSING")
    status, output = gates_text(mutate(text, uptake, "| Poor critique uptake | SCORED 0 | I16 (-) "
                                       "| dominant cluster engaged |"))
    require(status == 0 and "COVERAGE_AFTER_GATES\t6/10 (60%)" in output
            and "PROVISIONAL_70_GATE\tNOT MET" in output,
            f"the executor's alternative (uptake SCORED 0) passes and the band stays withheld\n"
            f"{output}")
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
    expect_fail("map line removed", mutate(text, "DIMENSION CLASS MAP: cn7-map-2\n", ""),
                "MAP_VERSION_MISSING")
    expect_fail("output declares another map", mutate(text, "DIMENSION CLASS MAP: cn7-map-2",
                                                       "DIMENSION CLASS MAP: cn7-map-1"),
                "MAP_VERSION_MISMATCH")
    n02 = next(line for line in text.splitlines() if line.startswith("| N02 "))
    expect_fail("inspected row without a locator", mutate(
        text, n02, n02.replace("RD-E1, RD-E3, RD-E4: ", "")), "LOCATOR_MISSING")
    n08 = next(line for line in text.splitlines() if line.startswith("| N08 "))
    relocated = mutate(mutate(mutate(
        text, n08, n08.replace("| CITES-UNINSPECTED |", "| MENTIONS |").replace(
            "| NOT-INSPECTED | full text read; no passage locator recorded |",
            "| INSPECTED | citing passage read |")),
        "CITATION CONTEXT COVERAGE: RECEPTION-1 8/50", "CITATION CONTEXT COVERAGE: RECEPTION-1 9/50"),
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
        "INSTRUMENT VERSION: 2-citation-network v2-candidate.2\n", "")
    status, output = gates_text(text)
    require(status == 3, "a fragment without the version line is not judged")
    status, output = gates_text(REPAIRED.read_text(encoding="utf-8").replace(
        "v2-candidate.2\n", "v2-candidate\n"))
    require(status == 3, "an output of candidate revision 1 is not judged by revision 2")


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
            "DIMENSION_CLASS_MISSING",                            # lack of decisive tests 2, no search
            "LOCATOR_MISSING", "LOCATOR_MISSING", "LOCATOR_MISSING",  # S2-S4 have no page refs
            "INFERENCE_OVERCLAIMED",     # P02 citation use rests on those unlocatable passages
            "FINDING_ON_INSUFFICIENT"]),  # Finding 2 relies on P02
                f"unexpected gate result on the v1 control: {failure_codes(output)}")
        require("INFERENCE_OVERCLAIMED\tP02 " in output, "P02 should fail on locators")
        require("Recent-paper dependence is SCORED 0 with no listed inference" in output
                and "Adjacent-field neglect is SCORED 0 with no listed inference" in output,
                "expected the two SCORED 0 rows that rest on no evidence")
        require("SCORECARD_DISAGREES" not in output, "basis table must mirror Artifact 8")
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
    for path in (AS_RUN, REPAIRED, CONTROL, OVERLAP, POWER_BLOCKS,
                 CANDIDATES / "2-citation-network.v2-candidate.txt"):
        text = path.read_text(encoding="utf-8")
        if path.name.endswith("v2-candidate.txt"):
            v1 = V1_PROMPT.read_text(encoding="utf-8")
            new = set(vocab.findall(text)) - set(vocab.findall(v1))
            require(not new, f"candidate adds authority tokens: {new}")
        else:
            require(not vocab.findall(text), f"{path.name} uses -CONFIRMED/-VERIFIED tokens")


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


def main() -> int:
    for test in (test_acemoglu_as_run, test_acemoglu_repaired, test_structural_control,
                 test_overlap, test_adversarial_mutations, test_applicability,
                 test_interactions, test_candidate_reproducible, test_fixture_rebuild):
        test()
        print(f"ok\t{test.__name__}")
    print(f"PASS\t{checks} checks")
    return 0


if __name__ == "__main__":
    sys.exit(main())
