CITATION-NETWORK v2-CANDIDATE GATES — REGRESSION FIXTURES
FAIL-CN-007 (candidate; not canonical)

What these are
--------------
Inputs for candidates/research-analysis/check-citation-network-v2-gates.py, run by
tests/test-citation-network-v2-gates.py. They test the candidate SECTION A0 (corpus register
and source eligibility, Gate A) and SECTION K0 (evidence sufficiency, Gate B).

Classification (MAP-15): every fixture here is a TUNED REGRESSION or a hand-written CONTROL.
The Acemoglu fixtures were built around the failure they test. None is a held-out case, none
is an unadjudicated ordinary paper, and none comes from a live run of the candidate. Passing
them shows the checker behaves as designed on these inputs; it does not validate the candidate.

Files
-----
acemoglu-as-run-transcribed.txt   expected FAIL, 12 gate failures
    The Acemoglu Stage-2c run's own declarations, re-expressed in the candidate ledger
    format by mechanical rules, with nothing repaired. It is a test input, not a re-grade of
    the run: the run was produced under the canonical v1 instrument, and the candidate's gates
    do not judge v1 outputs (the checker returns NOT_APPLICABLE for them).

acemoglu-repaired.txt             expected PASS-WITH-REVIEW, 3 items
    The same evidence re-ledgered to comply with the candidate. Repairs R1-R10 are listed in
    the file header and in build_acemoglu_fixtures.py. Nothing new was retrieved.

acemoglu-structural-control.txt   expected PASS, 0 items (clean control)
    A structural question that metadata answers (internal density of the top-50 citing
    corpus; reliability of single-database records). Every source is at METADATA access, no
    citing passage is read, and the gates raise nothing.

overlap-synthetic.txt             expected PASS (hand-written, invented records)
    Sources in both corpora, an adjudication-only source that does not cite the target, and
    a lightly cited direct test absent from the reception corpus.

power-posing-v2-blocks.txt        interaction fixture blocks
    Inserted at test time into a temporary copy of
    tests/cases/citation-network-checker/complete-clean-control.md (unchanged; pinned by the
    Atlas baseline). The test confirms the v1 checker's result and the Atlas native parser's
    findings are unchanged by the v2 blocks, and records the candidate's result on that
    v1-era control: FAIL, two SCORED_WITHOUT_BASIS (see "Observed on the v1 control").

build_acemoglu_fixtures.py        builds the three Acemoglu fixtures
    Input: examples/research/acemoglu-colonial-origins/citation-network/02c_citation_network.md
    on Provenance-Atlas branch audit/acemoglu-colonial-origins (branch head b6d7869 when
    built), git blob 0c23beed0c914bea21b09c3094b33e976561f601, sha256
    884887fe5a7b98d77921fbc31b488c7c9b7dc8406eb60340e4d5881436f3016c. The script refuses any
    other input, reads it as data, and never executes it. Run with python3 -I.

Build receipt (2026-11-04, Python 3.13 and 3.11 identical):
    acemoglu-as-run-transcribed.txt  sha256 fb667acbd4fa4977ea9b4b2cfcbd7c2036d32bf9fb99d462b9274adfb4014d72
    acemoglu-repaired.txt            sha256 4a0ec7017cf364286cc263ea5a4edb2f159742ceb44c07167aa290ee94c167aa
    acemoglu-structural-control.txt  sha256 1c94bb475dd96237e0ac77fd8f42c29dd51ca4b5a68a70d20b5068ffea612e5c
Set CN7_02C_PATH to the input file to make the test rebuild all three and compare bytes. CI
does not fetch the Atlas branch, so CI skips the rebuild and checks the committed files.

What the as-run transcription catches, with the run's own lines
---------------------------------------------------------------
02c line numbers refer to the pinned blob above.

  COVERAGE_MISMATCH        Verdict: citing passages for 13 of 50 top citers (line 686).
                           N13 and N16 retrieved versions do not contain the citation
                           (line 131). Inspected: 11/50; 10 of the top 15.
  USE_WITHOUT_CONTEXT      N11 polarity "used as premise", "same as N05 assumed, not
                           verified" (line 411); the run's own rule codes polarity only where
                           the passage was retrieved (line 126).
  REUSE_WITHOUT_ACCESS     N31 coded as reusing the AJR instrument from a LOCATED record
                           (line 94), then counted among shared-data re-estimates (line 56).
  ADJUDICATION_CORPUS_MISSING  One reception corpus (line 24) answered evidence-base
                           questions; the run disclosed the substitution (line 38).
  INFERENCE_OVERCLAIMED x5 I05 recent citation use from 0/25 passages (lines 132, 142, 467);
                           I12 literature-wide absence of instrument-independent tests with no
                           search for them (lines 472, 667); I14 includes unread N31; I15
                           literature-wide data-origin narrowing from the reception corpus
                           (line 56); I18 polarity sample includes N11.
  SCORED_ON_INSUFFICIENT x2  Recent-paper dependence (I05); lack of decisive tests (I12, I14).
  FINDING_ON_INSUFFICIENT  Finding 2 (I14, I15).

What survives, unchanged in the repaired fixture: density inside the corpus (I01), the
database conflation (I02), co-citation and authorship counts (I03, I04, I07, I11, I17), the
hub restatement and construct-broadening comparisons (I06, I08, I09), the source-layer
engagement with rivals (I10, I20), cluster engagement with Albouy (I16), the within-sample
polarity of the 10 read top-15 passages (I18), the citing-set composition (I19), and all seven
standardized findings (Finding 2 scoped to the four named re-estimates). Eight of ten
applicable dimensions stay SCORED; recent-paper dependence becomes UNASSESSED; lack of decisive
tests keeps SCORED 1 on two named-source statements (I13) and the named data-origin result
(I14).

Contestable transcription decisions
-----------------------------------
A reviewer should check these first; each changes what the as-run fixture fails on.
  1. I15 scope LITERATURE. The run's Finding 2 and line 56 generalise from "the top 50" to
     independent confirmation of L3. A reader could take them as scoped to the corpus; then
     I15 would be CORPUS-scope and pass, and Finding 2 would fail only on I14 (N31).
  2. Declared dispositions. The run declared none. Every inference an as-run score or confirmed
     finding relied on is transcribed as SUPPORTED, because the run used it as sufficient.
  3. Relevance codes come from keyword rules over the run's Section B text (rules in the
     build script). 14 of 50 reception rows fall to UNKNOWN because the run's text gives no
     relevance word; this affects the I19 composition only.
  4. R4 recodes one relevance value (N42 to DIRECT (L3)) on the run's own description (lines
     105, 221). It is the only judgment added in the repair.

Observed on the v1 control
--------------------------
The canonical v1 clean control (complete-clean-control.md) scores recent-paper dependence
SCORED 0 on "Supplied packet only" and adjacent-field neglect SCORED 0 on "No neglect
established in packet". The v1 instrument's hard rule (line 1215 of the canonical prompt) says
lack of retrieved evidence of concern is not enough for SCORED 0; the v1 checker does not
enforce it and passes the file. The candidate gates fail exactly those two rows. Recorded
here as an interaction, not as a re-grade of the v1 fixture, which is unchanged.

Known limits of the checker
---------------------------
- It cannot verify that a passage marked INSPECTED exists or contains the citation. Changing
  VERSION-MISMATCH to INSPECTED and the coverage line to match passes. Passage anchors (Atlas)
  are the intended enforcement point; not implemented here.
- It cannot verify that a code is correct, that a sample was random, or that a search was
  adequate. Those reach a reviewer as review items or not at all.
- The dimension-to-class requirements are a design judgment (see the CHANGES file, CN7-R7).
