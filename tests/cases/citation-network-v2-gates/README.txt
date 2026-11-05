CITATION-NETWORK v2-CANDIDATE GATES — REGRESSION FIXTURES
FAIL-CN-007 (candidate; not canonical). Candidate revision 3, dimension class map cn7-map-3.

What these are
--------------
Inputs for candidates/research-analysis/check-citation-network-v2-gates.py, run by
tests/test-citation-network-v2-gates.py. They test the candidate SECTION A0 (corpus register
and source eligibility, Gate A) and SECTION K0 (evidence sufficiency, Gate B).
tests/ablate-citation-network-v2-gates.py disables each checker rule in turn on a temporary
copy and confirms the suite fails without it.

Classification (MAP-15): every fixture here is a TUNED REGRESSION or a hand-written CONTROL.
The Acemoglu fixtures were built around the failure they test. One fixture comes from a live
run of the candidate (revision 2, on the same paper); revision 3 was designed from that run,
so it is a regression input for revision 3, not held-out evidence. None is a held-out case and
none is an unadjudicated ordinary paper. Passing them shows the checker behaves as designed on
these inputs; it does not validate the candidate.

The repaired fixture is public. It is close to an answer key for a v2 Acemoglu ledger, so a
live Acemoglu run of the candidate tests executability and burden, not whether the gates catch
errors. The live run below was made with that key public.

Files
-----
acemoglu-as-run-transcribed.txt   expected FAIL, 21 gate failures, 2 review items
    The Acemoglu Stage-2c run's own declarations, re-expressed in the candidate ledger
    format by mechanical rules, with nothing repaired. It is a test input, not a re-grade of
    the run: the run was produced under the canonical v1 instrument, and the candidate's gates
    do not judge v1 outputs (the checker returns NOT_APPLICABLE for them).

acemoglu-repaired.txt             expected PASS-WITH-REVIEW, 1 item; band WITHHELD
    The same evidence re-ledgered to comply with the candidate. Repairs R1-R18 are listed in
    the file header and in build_acemoglu_fixtures.py. Nothing new was retrieved. R18
    (revision 3) merges N05 and N11, a working paper and its Handbook chapter, into one row:
    RECEPTION-1 is 49 works, coverage 8/49.

acemoglu-structural-control.txt   expected PASS, 0 items (clean control)
    A structural question that metadata answers (internal density of the top-50 citing
    corpus; reliability of single-database records). Every source is at METADATA access, no
    citing passage is read, and the gates raise nothing.

overlap-synthetic.txt             expected PASS (hand-written, invented records)
    Sources in both corpora, an adjudication-only source that does not cite the target, a
    lightly cited direct test absent from the reception corpus, and a locked adjudication
    search. Mutations in the test cover bounded absence, the uptake classes and a band that
    meets the gate only while review items are counted.

live-v2cand2-acemoglu.txt         expected PASS-WITH-REVIEW, 9 items; band WITHHELD (the run's)
    Grok's live run of candidate revision 2 on AJR 2001: its SECTION A0, SECTION K0 and RISK
    BAND line as observed, plus only the declarations revision 3 requires, taken from the run's
    own records (rules L1-L6 in build_live_v2cand_fixture.py). Duplicate records, zeros on
    partial bases and the search's missed items are left as observed, so the revision-3 gates
    show what they make visible. Not a re-grade: the run declares revision 2 and passed
    revision 2's gates (PASS-WITH-REVIEW, 3 items); the revision-3 checker returns
    NOT_APPLICABLE for the run itself. Without the L-rule declarations the observed ledger
    fails 10 revision-3 gates (claim layers, record quality, known-item recall, sample
    attrition); the test records that as a property of the new rules.

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

build_live_v2cand_fixture.py      builds the live-run fixture
    Input: the run directory examples/research/acemoglu-colonial-origins/citation-network-
    v2cand/ on Provenance-Atlas branch audit/acemoglu-colonial-origins-v2cand (commit
    84d1800faf71788c46bb4c4e968ab3cb42d24b11). The script refuses any output other than
    02c_citation_network_v2cand2.md with sha256
    a1abbbee2b568f177913a3a7e9a89b2c04abac42d12152001d07fef4b1cd07c3 (also listed in the
    run's SHA256SUMS). The six adjudication search responses (raw/adj1_Q1-Q6.json) must match
    pinned digests taken with every abstract_inverted_index field removed, so the fixture
    rebuilds from the run as committed or after its abstracts are stripped. Everything is read
    as data; nothing from the run is executed. Run with python3 -I. Known-item recall (L4) is
    computed from the six responses: of the six claim-testing works the run's exposure
    declaration names, the search returned Rodrik et al. 2004 only. Rebuilt byte-identically
    from 84d1800 and from a40fbbb (the follow-up commit that nulls the run's 100 abstract
    fields; verified independently: only abstract fields changed, the output hash unchanged).

Build receipt (2026-11-04, Python 3.13 and 3.11 identical):
    acemoglu-as-run-transcribed.txt  sha256 47eb496a4c76d8a8f57ecd9bdd5b1d4b08dca82befe701064da3046034cadf57
    acemoglu-repaired.txt            sha256 937b8e37e5e3eaa196d535e80ab739764b797a852e95b93568849c97932bb658
    acemoglu-structural-control.txt  sha256 ebe5594883e1d96bc66dcd365b44af661305c8637b337855d3c78e564a04b4c2
    live-v2cand2-acemoglu.txt        sha256 b7ab366572f112a122c277c582c5a9113d95bf451389658ae43ec697519f5cdb
Set CN7_02C_PATH to the Stage-2c input, and CN7_LIVE_RUN_DIR to the live run directory, to
make the test rebuild the fixtures and compare bytes. CI does not fetch the Atlas branches, so
CI skips the rebuilds and checks the committed files.

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
  EVIDENCE_BASE_UNSEARCHED  Lack of decisive tests is scored with no adjudication search
                           (revision 3: a score in either direction needs one).
  DIMENSION_CLASS_MISSING x2  Adjacent-field neglect and poor critique uptake: the concern side
                           of each rests on co-citation over unscreened citers (I11, I17), while
                           the run's other evidence points the other way (I10, I16).
  FINDING_ON_INSUFFICIENT  Finding 2 (I14, I15).
  BAND_ISSUED_BELOW_GATE   The run's >20%-40% band (line 329). Declared coverage 9/10; after
                           Gate B 5/10, below the PROVISIONAL 70% gate.
  Review items             CODED_FROM_METADATA (six rows coded from records);
                           POSSIBLE_DUPLICATE_WORK (N05/N11, the Handbook chapter and its
                           working paper).

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
Revision 3 leaves the count at 5 and merges one duplicated work (R18).

Alternative the executor may take: poor critique uptake SCORED 0 on I16, if the dominant cluster
is taken as the uptake population (instrument Section H steps 3-4). It passes the gates with a
NAMED_ONLY_BASIS review item (revision 3). Coverage would then be 6/10 after Gate B, 5/10 with
the review item withdrawn; the band is still withheld.

What the live-run fixture shows under revision 3
------------------------------------------------
Coverage 8/10 after Gate B, as the run declared; 4/10 with review-pending dimensions withdrawn
(the run's own sensitivity line said 7/10). The nine review items:
  CODED_FROM_METADATA      ten ADJUDICATION-1 rows coded, or NOT-CITING, from records only;
                           the run reports that OpenAlex reference lists changed between runs.
  SEARCH_RECALL            the locked search returned 1 of 6 known claim-testing works
                           (Albouy 2012, the AJR 2012 Reply, Glaeser et al. 2004,
                           Easterly-Levine 2003 and Sachs 2003 not returned).
  POSSIBLE_DUPLICATE_WORK  nine pairs. Four are the run's own duplicate pairs in RECEPTION-1.
                           Five are in ADJUDICATION-1 and were not reported by the run; they
                           are title matches only, and at least one (ADJ02/ADJ20, 2007 and
                           2022) is probably two works.
  SAMPLE_DECLARED_RANDOM   I06 (kept INSUFFICIENT by the run after attrition).
  BY_CONSTRUCTION_RISK     recent-paper dependence on a target-selected set.
  DECISIVE_TEST_CLAIMED    lack of decisive tests SCORED 0 on one named result (I11).
  NAMED_ONLY_BASIS x2      adjacent-field neglect SCORED 0 on I19; poor critique uptake
                           SCORED 0 on I18.
  PARTIAL_BASIS            poor critique uptake SCORED 0 while I22 (Glaeser uptake) is
                           NOT-ASSESSED. The run cited I22 in the basis note; rule L6 adds the
                           (?) tag that revision 3 asks for.

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
search (EVIDENCE_BASE_UNSEARCHED under revision 3; DIMENSION_CLASS_MISSING under revision 2);
and the fixture records no page or section for any citing passage, so the three INSPECTED rows,
the citation-use inference built on them and Finding 2 fail. Poor critique uptake SCORED 0 on
one named engagement (P05) is a review item (NAMED_ONLY_BASIS). Recorded as an interaction,
not as a re-grade of the v1 fixture, which is unchanged.

Known limits of the checker
---------------------------
- It cannot verify that a passage marked INSPECTED exists, contains the citation, or sits at
  the stated locator. The locator rule makes the claim checkable later; it does not check it.
  The locator pattern is found anywhere in the Supported inference cell, not only at its start.
  Passage anchors (Atlas) are the intended enforcement point; not implemented here.
- It cannot verify that a code or a direction tag is correct, that a sample was random, that a
  search was adequate, or that a CORPUS LOCK predates screening.
- The dimension class map cn7-map-3 is a design judgment, and the one most in need of
  independent review (see the CHANGES file, CN7-R7).
- POSSIBLE_DUPLICATE_WORK matches normalised titles (and prefixes of truncated titles). It
  misses retitled versions and flags distinct works with matching title openings; review
  only. Known-item recall is computed against the list the executor declares, so an
  executor who lists nothing reports 0/0. A (?) tag is a declaration: an omitted partial
  inference is not detected.
