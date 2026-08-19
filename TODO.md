# TOOLKIT — TODO & STATE
Last updated: after MBH98 full-chain validation + claim-extraction hardening

## REPO — github.com/yungmulaBABY1/Provenance

LIVE:
  prompts/0-field-diagnostic.txt
  prompts/1-claim-extraction.txt
  prompts/5-voice-restoration.txt
  prompts/research-analysis/2-construct-validity.txt
  prompts/research-analysis/2-internal-validity.txt
  prompts/research-analysis/2-citation-network.txt
  prompts/research-analysis/3-counter-audit.txt
  prompts/media-analysis/2-framing-construction.txt
  prompts/media-analysis/2-coverage-network.txt
  reference/shared-primitives.txt
  reference/narrative-flags-module.txt
  tools/citation_reception_module.py
  deferred/1-field-context-generator.txt
  README.md

MISSING — create:
[ ] 4-synthesis.txt          NEW PROMPT, does not exist yet. Compression step
                             between human adjudication and voice restoration.
                             Needs: aggregation rule (derived not asserted),
                             directional coherence, concede-test results,
                             provisional flags preserved, no composite score.
                             Most of this ports from the media prompts.
                             BUILD AFTER the research branch has run once —
                             easier to design when you can see what it compresses.
[ ] CHANGELOG.md             root — trim from the reconstruction below
[ ] LICENSE                  root
[x] reference/philosophy.md  first repo-grounded draft
[ ] Reconcile reference/philosophy.md with toolkit_philosophy_notes.md if/when
    that source document is supplied.
[x] reference/methodology.md first repo-grounded draft
[ ] deferred/ROADMAP.md      future-plans section of the philosophy notes
[ ] examples/                structure decided, see below

EXAMPLES STRUCTURE — decided:
  examples/
  ├── README.md                        ← field index lives here, NOT in folders
  ├── research-analysis/
  │   └── <target>/
  │       ├── README.md                ← what the run got right AND wrong
  │       ├── 2-construct-validity.md
  │       └── 3-counter-audit.md
  └── media-analysis/
      └── <target>/
          ├── README.md
          ├── 2-framing-construction.md
          └── 2-coverage-network.md

  Branch at top (already a real distinction). Target folder = the unit people
  want. Audit files numbered to match the prompts. Field browsing goes in the
  index, not the tree — a study can appear under two fields in an index, only
  one folder. Add folder taxonomy when the index stops scaling (~15 examples).

  PER-EXAMPLE README MUST INCLUDE:
    - the practitioner caveat where it applies (esports findings came from having
      done the thing, not from the prompts)
    - what the run got WRONG. The MBH counter-audit elevating McShane & Wyner
      without checking its reception is more instructive than a clean run.

README STILL NEEDS — from philosophy notes:
[ ] "it points, you judge" framing; cut the overclaim register
[ ] "How this toolkit stays honest" section — safeguards mapped to the AI failure
    each addresses
[ ] two entry points; field diagnostic is an ON-RAMP not a gate
[ ] the three stage-2 research prompts are INDEPENDENT — no dependencies, any
    order, run one or all three
[ ] human adjudication sits between 3- and 4- and has no file (by design)
[ ] media-analysis has no 3-counter-audit — balancing is internal to those two
    prompts. State it as a decision, not an omission.
[ ] reproducibility literature as rationale (SCORE, calibrated)
[ ] reviewer/editor framing — strongest use is the non-conflicted judge
[ ] limitations: surfaces categories not mechanisms; can't tell you what it missed

## DOCUMENTATION RECONCILIATION — before methodology / README are canonical

[ ] FIELD DIAGNOSTIC: choose one status and align all copies. The live prompt calls
    Stage 0 a feasibility / self-calibration gate with go/no-go routing; this TODO
    and the webapp methodology call it an on-ramp rather than a gate.

[ ] MEDIA CLAIM MAP: decide whether claim extraction is a shared media stage or an
    optional input to single-piece framing only. The webapp places it in both
    branches; `1-claim-extraction.txt` describes three research prosecutors;
    framing accepts an optional map; coverage-network does not consume one.

[ ] SHARED PRIMITIVES: resolve the six dangling prompt references before a
    methodology document links or names a canonical shared layer. The stale file
    and the available options are documented below under NOTE ON SHARED PRIMITIVES.

[ ] WEBAPP DOCUMENTATION: decide whether the hardcoded Philosophy, Methodology,
    Vocabulary, and Limitations copy is generated from repository Markdown or
    intentionally maintained as a second copy. Do not allow it to become an
    unmarked competing source of truth.

[ ] HYPOTHESIS ARCHITECTURE: the architecture note requires origin-labelled
    hypotheses plus explicit confirming and disconfirming retrieval. The live
    media prompts currently implement prior declaration, inverse evidence, and
    flip tests, but not the full Investigation Register described in the note.
    Decide where that protocol executes before documenting it as implemented.

[ ] FINDING-SCHEMA DRIFT: construct validity uses `Finding disposition`;
    internal validity and citation network use `Status`; the media tables have
    no equivalent shared column. Decide whether this is intentional branch
    specialization or vocabulary drift before defining one cross-branch schema.

## STATE OF PLAY

Both branches now have run-tested chains. See tests/RESULTS.md for per-run
behavior and CHANGELOG.md for why each rule exists.

MEDIA BRANCH — mature
  2-framing-construction ....... 7 runs, 4 models, self-corrected 3x
  2-coverage-network ........... 3 runs, 3 models, falsified 2 upstream findings

RESEARCH BRANCH — chain validated end to end on ONE paper
  Full chain run: cold map -> construct -> citation-network -> counter-audit,
  on MBH98, across 4 models. E0 verified firing. Reception gate verified firing.
  Concede test verified changing a verdict (E -> C).

  2-internal-validity has now been run twice on Galor & Özak (2016). The paired
  runs exposed verification-gated severity and ambient sibling-input failures;
  FAIL-IV-001/002 are applied and await the controlled regression rerun.

WHAT THE VALIDATION DOES NOT COVER
  12 of 14 logged runs are one paper. MBH98 has a same-author successor, a famous
  controversy, and an assessment-report trail — the entire attribution apparatus
  exists because MBH99 exists. Most sources have none of that. Next source should
  test whether those fields come back EMPTY cleanly rather than straining to fill.

  No research-branch run on material that should come back SOUND. Case 11 covers
  this for media; the research branch has no equivalent. Until it does, every
  finding is consistent with both a working instrument and a template.

## PROMPT STATE — three states, not two

All insertion blocks are applied. What remains is verification and a small
number of late fixes whose application status is unconfirmed.

APPLIED + TESTED
  1-claim-extraction.txt ........ heavily revised, 8 fixes, tested across ~10 runs
                                  and 3 models. See below for the fix list.
  2-construct-validity.txt ...... full chain, blocks A/B/C/F all fired
  2-citation-network.txt ........ Block F (J2 concede test) fired on MBH98.
                                  A/B/E present in prompt but did NOT render in
                                  the run output — see compliance gap below.
  3-counter-audit.txt ........... Blocks 1/2/3/4 applied; E0 verified firing

APPLIED, UNTESTED
  2-internal-validity.txt ....... Blocks A/B/D/F + D2 forking-paths + reception
                                  hook all present. FAIL-IV-001/002 applied after
                                  paired Galor–Özak runs; regression pending.

UNVERIFIED
  5-voice-restoration.txt ....... carve-out application not confirmed
  0-field-diagnostic.txt ........ replaced wholesale, never run

CLAIM-EXTRACTION FIX LIST — all applied, all run-tested unless noted
  1. Field-6 RULE 1 (one claim only) + RULE 2 (prefer quantified version)
  2. Field 4 made ACTIVE — search for downstream use rather than waiting
  3. Four provenance states: SUPPLIED / RETRIEVED / RECALLED / NONE FOUND
  4. Parenthetical failure named and banned
  5. Attribution check + ATTRIBUTED ELSEWHERE + scope arithmetic
  6. MISATTRIBUTED branch (closes the exoneration loophole)
  7. Field-specific provisional rule (fields 4/5/6, not blanket)
  8. Anchoring rule at field 5 — only SUPPLIED/RETRIEVED may anchor
  9. CROSS-SOURCE-CONFIRMED adopted; no-invented-states rule
 10. Joint-citation document-level check (prevents false-positive MISATTRIBUTED)
 11. Claim inventory before field 6 — applied, UNTESTED
 12. Label verification at anchoring — applied, UNTESTED. A run labeled an
     unquoted pattern generalization RETRIEVED and anchored on it; this
     requires a quotation AND locator before an item may anchor.

ALL INSERTION BLOCKS AND FIXES ARE APPLIED. Nothing is pending on the prompts.

Recently applied, UNTESTED — these have not yet been through a run:
  - Claim inventory before field 6 (1-claim-extraction)
  - Label verification at the anchoring step (1-claim-extraction)
  - CROSS-SOURCE-CONFIRMED + no-invented-states in the compact vocabulary blocks
  - Model-routing block removed from 2-citation-network
  - Voice-restoration carve-out

  The first two matter most on the next run. The claim inventory is new
  behavior; label verification closes the loophole where a run labeled an
  unquoted pattern generalization RETRIEVED and anchored a failure location on it.

NOTE ON SHARED PRIMITIVES: the compact copies inside each prompt are what
actually runs; reference/shared-primitives.txt is documentation nobody loads.
Edits must go to the prompts.

[x] Header saying so — APPLIED, matching the narrative-flags module.

  Two things surfaced while applying it, both worse than "nobody loads it":

  1. Despite the filename the file is NOT a primitives document. It is an older
     reflowed copy of 1-claim-extraction.txt — same title, same WHY THIS STAGE
     EXISTS structure, same field 1-6 table. It is a stale duplicate of a live
     prompt, not reference material.

  2. The `References: shared_primitives.txt Section 1 / 2 / 3` line at the top of
     six prompts is DANGLING. Sections 1, 2 and 3 do not exist in that file or
     anywhere else. The file's own header even carries the reference, pointing at
     itself.

[ ] Decide what to do about the six dangling reference lines. Options: point them
    at the COMPACT VOCABULARY block in the prompt that carries them, or delete the
    line. Not done here — it edits six live prompts and every prompt edit should
    be run-tested, which this has not been.

[ ] Consider deleting reference/shared-primitives.txt outright. It is now banner-
    marked, but a stale copy of a live prompt is a standing invitation to read the
    wrong version. Apply the deletion standard before cutting.

COMPLIANCE GAP OBSERVED
  The MBH98 citation-network run used the fully-blocked prompt but produced zero
  hits for claim-map receipt, verification states, and the standardized finding
  table, while the concede test fired normally. Finding table is the last section
  so truncation is plausible; the claim-map receipt sits near the top and is not
  explained by truncation. WATCH ON NEXT RUN: is this truncation or section-
  skipping? If skipping, the blocks need stronger placement or a compliance
  checklist at the top of the output.

  NOTE: this is a NEW failure category — prompt correct, output incomplete.
  Distinct from "block not applied." Track separately.

INTERNAL-VALIDITY CHECKER LIMIT — DECLARED INDEPENDENCE IS SELF-REPORT

  [ ] When an internal-validity checker is built, verify the sibling-input
      receipt and Section J branch mechanically. If the output declares
      `INDEPENDENCE STATUS: INDEPENDENT` but contains construct/proxy-specific
      terminology matching a supplied list of known sibling-output terms, emit
      `NEEDS-HUMAN-REVIEW` with matched terms and line numbers. This is a lexical
      inconsistency flag, not proof of contamination. Do not use an LLM quality
      judge and do not return a silent PASS.

## NEXT — in order

The apply-then-run sequence is complete for the research branch. What follows is
validation on new material, not construction.

1. SHEN, FULL CHAIN. map -> construct -> internal -> citation -> counter-audit.
   Chosen because you know the answer AND you know the toolkit will miss it —
   the fishing and carry mechanisms came from having played, not from a prompt.

   What this tests that MBH98 could not:
     - Does the toolkit produce the generic scaffold (wrong population, weak
       proxy, level-of-analysis) and correctly signal something is missing,
       rather than reading as complete? This is the honest-limitation claim in
       philosophy.md, tested where you can see both what it found and what it
       could not reach.
     - OVERFIT CHECK: Shen has no same-author successor, no assessment trail.
       MISATTRIBUTED / ATTRIBUTED ELSEWHERE / joint-citation disambiguation
       should all come back EMPTY. If the map strains to fill them, the MBH98
       overfit is showing.
     - First run of 2-internal-validity, ever.
     - Does the claim inventory (new, untested) produce useful secondaries?
     - Does label verification fire? Watch for any item labeled RETRIEVED
       without a quotation and locator — it should be downgraded to RECALLED
       and barred from anchoring.

2. LOG IT IN tests/RESULTS.md. Which checks fired, what changed, what was killed.
   Including passes — a check that never alters an outcome across twenty runs is
   length without function, but only if passes are recorded.

3. RESOLVE THE COMPLIANCE GAP. The citation-network run had blocks present and
   absent from output. Truncation or section-skipping? Never followed up, and it
   blocks the multi-claim scope grant (see below) — do not add scope to a stage
   that skips sections.

4. CASE 11 on the media branch. Built, never run. Tests whether the instrument
   can decline to find.

5. Voice restoration, field diagnostic, field-context generator — all still
   unverified, all lower priority than the above.

RATIONALE: every real improvement so far came from a live run surfacing something
unpredicted. Zero exceptions across 14 logged runs. More prompt-reading will not
produce the next fix.

## MULTI-CLAIM SCOPE — staged, do NOT batch

PROBLEM: a source can make several inflatable claims. Field 6 selects one; every
stage is locked to it. The other claims are invisible to the whole sequence.
Citation-network is the stage most under-powered by this — its natural job is
mapping travel across literature, assessment, PR, and media, and it is currently
constrained to one sentence.

STAGE 1 — DONE
[x] Claim inventory added to 1-claim-extraction.txt. Numbered claims, one sentence
    each, quantified or not, why each might be inflated, which was selected and
    why. Unselected = DEFERRED, not dismissed.
    This alone answers "which claims are suspect." Costs nothing downstream —
    every stage still targets field 6.

STAGE 2 — ONLY IF THE INVENTORY SHOWS SECONDARIES THAT MATTER
    Do not build these preemptively. Run the inventory first; if deferred claims
    turn out to be live, then:

[ ] 2-citation-network.txt — scope grant. MUST audit the primary claim's travel;
    MAY additionally audit claims enumerated in the map's inventory; MAY NOT
    substitute or expand its own scope. Every finding declares its claim ID.
    NOTE ON WORDING: do NOT grant "the selected claim and closely related
    restatements." "Closely related" is undefined and elastic — a prosecutor
    looking for inflation will stretch it to whatever is most inflated. That is
    the drift the shared-object rule exists to prevent, reintroduced as a scope
    grant. The map enumerates; the prosecutor does not.

[ ] Standardized finding table (all prosecutors) — "Target claim" column takes a
    CLAIM ID, not "field 6." The column currently assumes one claim exists. This
    is the structural point where standardization limits multi-claim work.

[ ] Counter-audit G2 — MUST be updated with the scope grant or it breaks. G2 asks
    "did the prosecution attack the strongest version, or the easiest downstream
    exaggeration?" and compares findings against field 6. If citation-network is
    legitimately auditing C2/C3, G2 will flag every one of those as off-target —
    the drift check firing on sanctioned breadth. Fix: G2 checks each finding
    against ITS DECLARED target claim, not against field 6 globally. It can then
    still catch real drift (a claim ID matching nothing in the inventory, or a C1
    finding that actually attacks C2).

OPTION 2 — SEPARATE MAP PER CLAIM: not a mode the user selects.
    The user does not know upfront which claims warrant a full run; that is what
    the audit is for. Sequence: first pass inventories and defers; citation-network
    reports whether any deferred claim travelled badly; THAT is the signal to run
    the sequence again with a different field 6. Informed, not guessed.
    No sequence change required — just run it again with a new primary. Keeps the
    paste-and-run path intact: one pass, one claim audited properly, others
    inventoried and flagged.

CAUTION: the scope grant expands what citation-network can do, and citation-network
is the prompt with the observed compliance gap (blocks present in prompt, absent
from output — see COMPLIANCE GAP OBSERVED above). Measure that before adding scope
to it.

## REGRESSION TEST SUITE — tests/

Structure:
  tests/
  ├── README.md          how to run, what each case proves
  ├── cases/             one file per case
  └── RESULTS.md         prompt version, model, date, pass/fail per case

Each case needs THREE parts:
  1. the synthetic article (200-400 words, ONE mechanism unambiguous)
  2. the EXPECTED RESULT, written BEFORE running
  3. what a failure means, localized to a specific check

The expected result written in advance is the whole point. Written after, you
will rationalize whatever came out.

BUILT:
[x] 11 — proportionate article, clean result  (test-case-11-proportionate.md)
       THE PRIORITY. Tests whether the instrument can decline to find. Never
       demonstrated. If this fails, the other ten test a machine that cannot say
       no, and their passes mean less than they appear to.

BUILD NEXT — the mechanisms with the most patch history, likeliest to have drifted:
[ ] 01 — omission vs. de-emphasis
[ ] 03 — amplification vs. independent corroboration   (network branch)
[ ] 04 — timing artifact vs. editorial selection

BUILD LATER:
[ ] 02 — synonym variance vs. causal-context loss
[ ] 05 — network-wide convention vs. outlet-specific divergence  (network)
[ ] 06 — appositional classification
[ ] 07 — denominator / baseline switching                        (network)
[ ] 08 — established vs. attributed cause
[ ] 09 — mirror symmetry
[ ] 10 — narrative-flag omission and over-activation

COST NOTE: cases 3, 5, 7 test the network branch and need MULTIPLE articles plus
a primary source. Substantially more expensive to write than single-piece cases.

WRITING NOTE: a good synthetic article is real work — plausible enough that the
prompt engages seriously, engineered so exactly ONE mechanism is unambiguous.
Eleven written in one sitting will mostly be sloppy, and a sloppy case is worse
than none: a false failure sends you fixing a prompt that was fine.

## ARCHITECTURE AUDIT — not yet run

The single-piece prompt is ~1450 lines assembled from ~15 rounds of patches,
each written without full view of what came before. Needs someone reading the
whole file cold, looking for CONTRADICTION rather than gaps.

Look for:
[ ] the same rule stated twice in different words — reinforcement or drift?
    (e.g. the "noted but does not offset" ban appears in J Step 6 AND the
    integrity block)
[ ] ownership collisions — Section C owns sequencing, G owns de-emphasis, E2.2
    owns causal bridges; all three can claim the same placement choice
[ ] severity caps that conflict when two apply to one finding, with no
    precedence rule
[ ] dead instructions superseded by later additions but never removed
[ ] vocabularies restated with drift between statements
[ ] optional modules lacking explicit triggers
[ ] places automated aggregation could override human adjudication

DELETION STANDARD — for every proposed cut, require:
  1. what failure the rule prevents
  2. whether that failure was OBSERVED in a run (check the changelog)
  3. where the protection moves
  4. which regression test proves it still holds

NOTE: several rules are regression fixes added after observed failures. Do not
delete a rule solely because a newer model might infer it.

BEST DONE BY SOMEONE WHO DIDN'T WRITE IT — an author reads what they intended,
not what is there.

## OPEN QUESTIONS — unresolved, not blockers

[ ] Does the A-G / A-F verdict scale survive the concede test, or does it need
    replacing? Decidable on one run. Do not add a parallel scale before checking.

[ ] Grok's automatic downgrade — does the mechanical version actually fire? Five
    runs at zero under the discretionary version. Untested since the change.

[ ] Cap Times / CNN: do they assert the pattern frame in their own headlines,
    unattributed? Claude flagged it PROVISIONAL on snippets. If it holds on full
    text, the Examiner routing its pattern claim through a quote was MORE
    restrained than peers on the dimension it was rated MAJOR for.

[x] Re-run Stage 1 cold on MBH98 with the new field-6 rules — DONE. Field 6
    selected the quantified claim, one claim only, no forcing bundled. Both rules
    held. The defect is now found from the prompt rather than from a hand-written
    map.

[x] Does the counter-audit's Section E find the source's own pre-emptions? — WAS
    NO across seven runs; Block 4 / E0 added; now YES. See changelog.

[ ] Marcott 2013 — the better Tool 2 test. Less iconic, so model background
    supplies less of the controversy. Prior generic + tailored runs already exist
    for comparison.

[ ] Nobody has run the full pipeline on a paper that should come back CLEAN.
    Individual findings have been cleared; no paper has. This is the acquittal
    test and it is the one validation the toolkit has never had.

## DEFERRED — not v1

  Tool 2 field-context generator (built: field_context_generator_v2.txt, unrun)
  Coverage-over-time branch (drift rather than divergence — designed, not built)
  Comparative institutional audit mode
  Multi-model comparison layer
  Bidirectional resistance testing
  Agentic version
  Banked field-context library + auto-update
  README rewrite (philosophy notes are the source material)
  Repo reorganization

## FAILURE REGISTRY — markers not yet inserted

FAILURES.md is written: 12 FAIL entries, 4 GUARD entries, all back-numbered from
the changelog. The registry exists; the prompt-side markers do not.

[ ] Insert one-line markers in the prompts — e.g. [FAIL-CE-010] beside the
    label-verification rule. No narrative in the prompt; the record lives in
    FAILURES.md.
[ ] Reference IDs from CHANGELOG entries and tests/RESULTS.md rows rather than
    restating the failure.

WHY THIS MATTERS: the architecture audit (below) will ask "what failure does this
rule prevent, and was it observed?" for every proposed cut. Without markers that
requires reading the whole changelog per rule. With them it is a lookup.

THE FAIL/GUARD SPLIT IS THE POINT. An observed failure has a strong claim to
survive an audit; an anticipated one does not. GUARD-004 ("nothing downstream
corrects it") is already flagged as the clearest deletion candidate — kept on
reasoning alone, unmeasurable by design.

WEAKNESS TO NOTE: only ONE regression case exists (case 11). Every other entry is
protected by narrative alone. A rule with an observed failure, no regression case,
and no replacement is not safely deletable — but it is also not safely KEEPABLE
without evidence it still fires.

## RELATED FILES

  FAILURES.md         numbered registry: every rule traces to an observed
                      failure (FAIL-) or an anticipated one (GUARD-). Deletion
                      protection for the architecture audit.
  CHANGELOG.md        why each prompt rule exists — the failure it closes and
                      the run that exposed it
  tests/RESULTS.md    per-run behavior — which checks fired, what they changed,
                      what got killed downstream
  reference/philosophy.md   design rationale and honest limitations
