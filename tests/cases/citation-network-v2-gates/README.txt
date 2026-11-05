CITATION-NETWORK v2-CANDIDATE GATES — REGRESSION FIXTURES
FAIL-CN-007 (candidate; not canonical). Candidate revision 2, dimension class map cn7-map-2.

What these are
--------------
Inputs for candidates/research-analysis/check-citation-network-v2-gates.py, run by
tests/test-citation-network-v2-gates.py. They test the candidate SECTION A0 (corpus register
and source eligibility, Gate A) and SECTION K0 (evidence sufficiency, Gate B).
tests/ablate-citation-network-v2-gates.py disables each checker rule in turn on a temporary
copy and confirms the suite fails without it.

Classification (MAP-15): every fixture here is a TUNED REGRESSION or a hand-written CONTROL.
The Acemoglu fixtures were built around the failure they test. None is a held-out case, none
is an unadjudicated ordinary paper, and none comes from a live run of the candidate. Passing
them shows the checker behaves as designed on these inputs; it does not validate the candidate.

The repaired fixture is public. It is close to an answer key for a v2 Acemoglu ledger, so a
live Acemoglu run of the candidate tests executability and burden, not whether the gates catch
errors.

Files
-----
acemoglu-as-run-transcribed.txt   expected FAIL, 20 gate failures
    The Acemoglu Stage-2c run's own declarations, re-expressed in the candidate ledger
    format by mechanical rules, with nothing repaired. It is a test input, not a re-grade of
    the run: the run was produced under the canonical v1 instrument, and the candidate's gates
    do not judge v1 outputs (the checker returns NOT_APPLICABLE for them).

acemoglu-repaired.txt             expected PASS-WITH-REVIEW, 1 item; band WITHHELD
    The same evidence re-ledgered to comply with the candidate. Repairs R1-R17 are listed in
    the file header and in build_acemoglu_fixtures.py. Nothing new was retrieved.

acemoglu-structural-control.txt   expected PASS, 0 items (clean control)
    A structural question that metadata answers (internal density of the top-50 citing
    corpus; reliability of single-database records). Every source is at METADATA access, no
    citing passage is read, and the gates raise nothing.

overlap-synthetic.txt             expected PASS (hand-written, invented records)
    Sources in both corpora, an adjudication-only source that does not cite the target, a
    lightly cited direct test absent from the reception corpus, and a locked adjudication
    search. Mutations in the test cover bounded absence, the uptake classes and a band that
    meets the gate only while review items are counted.

power-posing-v2-blocks.txt        interaction fixture blocks
    Inserted at test time into a temporary copy of
    tests/cases/citation-network-checker/complete-clean-control.md (unchanged; pinned by the
    Atlas baseline). The test confirms the v1 checker's result and the Atlas native parser's
    findings are unchanged by the v2 blocks, and records the candidate's result on that
    v1-era control (see "Observed on the v1 control").

build_acemoglu_fixtures.py        builds the three Acemoglu fixtures
    Input: examples/research/acemoglu-colonial-origins/citation-network/02c_citation_network.md
    on Provenance-Atlas branch audit/acemoglu-colonial-origins (branch head b6d7869 when
    built), git blob 0c23beed0c914bea21b09c3094b33e976561f601, sha256
    884887fe5a7b98d77921fbc31b488c7c9b7dc8406eb60340e4d5881436f3016c. The script refuses any
    other input, reads it as data, and never executes it. Run with python3 -I. Two locators
    (R11) come from the same run's Stage 2a, 02a_internal_validity.md line 203 (blob
    05599d8ce1f83bd95c6fc91127c4b15b0c18dcd7); they are written into the script, not read.

Build receipt (2026-11-04, Python 3.13 and 3.11 identical):
    acemoglu-as-run-transcribed.txt  sha256 a8c2fb4ea3ad9ce58627fe13f95d23af8a74a0f7b935e2438e857d9b97d6e3f2
    acemoglu-repaired.txt            sha256 51199f56c9e85ad2f98d2bec83473bf6af9f4d38f140ec8478500300394a991b
    acemoglu-structural-control.txt  sha256 04e64b43fd1d3fdbc528ac7064d5f0794fc671ad3d87db00e3aa88cf4ec2614e
Set CN7_02C_PATH to the input file to make the test rebuild all three and compare bytes. CI
does not fetch the Atlas branch, so CI skips the rebuild and checks the committed files.

What the as-run transcription catches, with the run's own lines
---------------------------------------------------------------
02c line numbers refer to the pinned blob above.

  COVERAGE_MISMATCH        Verdict: citing passages for 13 of 50 top citers (line 686).
                           N13 and N16 retrieved versions do not contain the citation
                           (line 131). Read: 11/50. Locatable: 8/50.
  LOCATOR_MISSING x5       N01, N08, N09, N14 and AL are marked read with no passage locator
                           in this stage's record.
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
                           (line 56); I18 polarity sample includes N11 and unlocatable passages.
  SCORED_ON_INSUFFICIENT x2  Recent-paper dependence (I05); lack of decisive tests (I12, I14).
  DIMENSION_CLASS_MISSING x2  Adjacent-field neglect and poor critique uptake: the concern side
                           of each rests on co-citation over unscreened citers (I11, I17), while
                           the run's other evidence points the other way (I10, I16).
  FINDING_ON_INSUFFICIENT  Finding 2 (I14, I15).
  BAND_ISSUED_BELOW_GATE   The run's >20%-40% band (line 329). Declared coverage 9/10; after
                           Gate B 5/10, below the PROVISIONAL 70% gate.

What survives in the repaired fixture: density inside the corpus (I01), the database
conflation (I02), co-citation and authorship counts (I03, I04, I07, I11, I17), the hub
restatement and construct-broadening comparisons (I06, I08, I09), the source-layer engagement
with rivals (I10, I20), named statements on decisive tests (I13), cluster engagement with
Albouy (I16), the within-sample polarity of the 7 locatable top-15 passages (I18), the
citing-set composition (I19), and all seven standardized findings (Finding 2 scoped to the four
named re-estimates). Five of ten applicable dimensions stay SCORED (founding-cluster dominance,
internal density, review-hub laundering, proxy mismatch, claim mutation). Recent-paper
dependence, adjacent-field neglect, lack of decisive tests and poor critique uptake become
UNASSESSED. The band is WITHHELD.

Revision 1 of these fixtures kept 8 of 10 dimensions SCORED. Revision 2 lowers that to 5 for
three reasons, each one of the open decisions now taken: a concern score cannot rest on
co-citation alone (R13, R14); a concern score on lack of decisive tests needs an absence over a
searched adjudication corpus (R15); and an inspected passage needs a locator (R11, R12).

Alternative the executor may take: poor critique uptake SCORED 0 on I16, if the dominant cluster
is taken as the uptake population (instrument Section H steps 3-4). The test confirms that it
passes the gates. Coverage would then be 6/10, and the band is still withheld.

Contestable transcription decisions
-----------------------------------
A reviewer should check these first; each changes what the as-run fixture fails on.
  1. I15 scope LITERATURE. The run's Finding 2 and line 56 generalise from "the top 50" to
     independent confirmation of L3. A reader could take them as scoped to the corpus; then
     I15 would be CORPUS-scope and pass, and Finding 2 would fail only on I14 (N31).
  2. Declared dispositions. The run declared none. Every inference an as-run score or confirmed
     finding relied on is transcribed as SUPPORTED, because the run used it as sufficient.
  3. Direction tags. The run declared none. An inference is tagged (-) where the run's own
     disposition text presents it as cutting against the concern ("source layer affirmative",
     "formally engaged by the cluster"); otherwise (+).
  4. Relevance codes come from keyword rules over the run's Section B text (rules in the
     build script). 14 of 50 reception rows fall to UNKNOWN because the run's text gives no
     relevance word; this affects the I19 composition only.
  5. Locators come from evidence IDs in the run's Artifact 4 rows (they resolve to PDF pages in
     the run's excerpts manifest) and, for N01 and AL, from Stage 2a page ranges. N08, N09 and
     N14 have none anywhere in the run; R12 marks them NOT-INSPECTED. A reader who accepts the
     run's statement that they were read would keep them inspected and fail them on locators.
  6. R4 recodes one relevance value (N42 to DIRECT (L3)) on the run's own description (lines
     105, 221).

Observed on the v1 control
--------------------------
The canonical v1 clean control (complete-clean-control.md) passes the v1 checker. Under the
candidate gates it fails 8 checks: recent-paper dependence and adjacent-field neglect are
SCORED 0 with no evidence (the v1 hard rule at line 1215 forbids this, but the v1 checker does
not enforce it); lack of decisive tests is SCORED 2 on a named source's statement, with no
search; and the fixture records no page or section for any citing passage, so the three
INSPECTED rows, the citation-use inference built on them and Finding 2 fail. Recorded as an
interaction, not as a re-grade of the v1 fixture, which is unchanged.

Known limits of the checker
---------------------------
- It cannot verify that a passage marked INSPECTED exists, contains the citation, or sits at
  the stated locator. The locator rule makes the claim checkable later; it does not check it.
  The locator pattern is found anywhere in the Supported inference cell, not only at its start.
  Passage anchors (Atlas) are the intended enforcement point; not implemented here.
- It cannot verify that a code or a direction tag is correct, that a sample was random, that a
  search was adequate, or that a CORPUS LOCK predates screening.
- The dimension class map cn7-map-2 is a design judgment, and the one most in need of
  independent review (see the CHANGES file, CN7-R7).
