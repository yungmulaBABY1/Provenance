# TOOLKIT — TODO & STATE
Last updated: end of build session

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
[ ] reference/philosophy.md  from toolkit_philosophy_notes.md
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

## STATE OF PLAY

TESTED AND LIVE
  framing_construction_audit_media.txt ......... 7 runs, 4 models, self-corrected 3x
  coverage_network_source_chain_audit.txt ...... 3 runs, 3 models, falsified 2 upstream findings

BUILT, NEVER RUN
  everything on the academic side. Six-plus structural additions since the last
  end-to-end run. Some will interact badly in ways only a live run reveals.

APPLIED TO REPO
  Files are in. UNKNOWN whether the insertion blocks were applied before upload
  or whether the pre-edit versions went in. VERIFY THIS FIRST — check whether
  2-construct-validity.txt contains "CONCEDE TEST" and "CLAIM MAP (received)".
  If not, the pending list below is still fully pending.

## PROMPT STATE — three states, not two

APPLIED + TESTED
  1-claim-extraction.txt ........ field-6 rules verified cold on MBH98
  2-construct-validity.txt ...... full chain, blocks A/B/C/F all fired
  2-citation-network.txt ........ Block F (J2 concede test) fired on MBH98.
                                  A/B/E present in prompt but did NOT render in
                                  the run output — see compliance gap below.
  3-counter-audit.txt ........... Blocks 1/2/3/4 applied; E0 verified firing

APPLIED, UNTESTED
  2-internal-validity.txt ....... Blocks A/B/D/F + D2 forking-paths + reception
                                  hook all present. Never run.

UNVERIFIED
  5-voice-restoration.txt ....... carve-out application not confirmed
  0-field-diagnostic.txt ........ replaced wholesale, never run

OUTSTANDING EDITS
[ ] 2-citation-network.txt — REMOVE the model routing block ("Use Grok for
    initial mapping / Claude to synthesize / ChatGPT only after"). Dated
    product-specific guidance; was stripped from the field diagnostic and missed
    here. Replace with the model-agnostic principle already used in
    0-field-diagnostic.
[ ] Confirm 5-voice-restoration carve-out is applied.

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

## PENDING — INSERTION BLOCKS NOT YET IN THE REPO PROMPTS

[ ] claim_extraction_inflation_map.txt
      NEW FILE — new shared pre-stage. Runs after target selection, before the
      three prosecutors. Produces the claim map they all receive.

[ ] shared_primitives.txt
      NEW FILE — canonical §1 verification states, §2 finding table, §3 failure
      location. Compact copies get inlined per Block A.

[ ] prosecutor_insertion_blocks.txt → construct validity
      Block A (receive claim map + compact vocab)
      Block B (standardized finding table, final section)
      Block C (Section 1 REPLACED: receive the map, don't regenerate)
      Block F (concede test, before the finding table)
      + applicable-checks note

[ ] prosecutor_insertion_blocks.txt → internal validity
      Block A, Block B, Block F
      Block D (verification state on replication claims)

[ ] prosecutor_insertion_blocks.txt → citation network
      Block A, Block B, Block F
      Block E (verification state + no-assume-suppression)

[ ] audit_prompt_additions.txt → internal validity
      SECTION D2 forking-paths / multiverse (between D and E)
      + reception-module hook in the data-honesty section
      + one added verdict question

[ ] audit_prompt_additions.txt → citation network
      reception-module confirmation rule in data-honesty

[ ] counter_audit_v3_insertions.txt → oppositional counter-audit
      Block 1 (claim map receipt, INPUTS)
      Block 2 (verification-state ladder replaces memory/retrieval labeling;
               column renames in tables A, E, G)
      Block 3 (NEW Section G2: did the prosecution attack the strongest version;
               failure-location classification; re-aiming check)
      + 2 lines in J, 1 bullet in J2
      NOTE: keep "nothing downstream corrects it" in the prompt text. Diagram only
      softens it.

[ ] voice_restoration_insertion.txt → voice restoration prompt
      pipeline-flag preserve rule (strip the scaffold, KEEP the flag)
      + one line to output Section 5

[ ] field_diagnostic_44_questions_v2.txt
      REPLACES the existing 44-question file. Model routing dropped, numbering
      fixed, Stage-0 framing added, retrieval grounding on Q4/14/15/18.

## EDIT MAP — which addition file goes where

There are 5 addition files. Each targets specific prompts. This is the lookup.

prosecutor_insertion_blocks.txt
  → 2-construct-validity.txt ... Blocks A, B, C, F + applicable-checks note
                                 (C REPLACES its Section 1 — do not keep both)
  → 2-internal-validity.txt .... Blocks A, B, D, F
  → 2-citation-network.txt ..... Blocks A, B, E, F

audit_prompt_additions.txt
  → 2-internal-validity.txt .... SECTION D2 forking-paths (between D and E),
                                 reception hook in data-honesty,
                                 +1 verdict question
  → 2-citation-network.txt ..... reception-module confirmation rule in
                                 data-honesty
  NOTE: this file also says NOT to merge the old FORKING PATHS doc's citation
  half — already covered by 2-citation-network's Sections D and G.

counter_audit_v3_insertions.txt
  → 3-counter-audit.txt ........ Block 1 (claim map receipt, INPUTS)
                                 Block 2 (verification ladder replaces
                                          memory/retrieval labeling; column
                                          renames in tables A, E, G)
                                 Block 3 (NEW Section G2, between G and H)
                                 + 2 lines in J, 1 bullet in J2
                                 KEEP "nothing downstream corrects it" verbatim

voice_restoration_insertion.txt
  → 5-voice-restoration.txt .... pipeline-flag preserve rule after the existing
                                 "Important distinction" block
                                 + 1 line to output Section 5

media_branch_post_test_fixes.txt
  → ALREADY APPLIED to both media prompts. Reference only. Do not re-apply.

WHOLE-FILE REPLACEMENTS (not insertions):
  field_diagnostic_44_questions_v2.txt → replaces 0-field-diagnostic.txt
  field_context_generator_v2.txt       → replaces deferred/1-field-context-generator.txt

VERIFY BEFORE STARTING: does 2-construct-validity.txt already contain
"CONCEDE TEST"? If yes, some edits are applied and this map is stale.
Current answer: NO — repo holds pre-edit prompts.

## ORDER OF OPERATIONS — do not batch these

1. Apply the claim map + primitives + Blocks A/B/C/F to CONSTRUCT VALIDITY only.

2. RUN IT on a paper you already know the answer to (Shen, or MBH98). One run.
   Watch specifically:
     - does the concede test demote anything, or does everything come back DEFEATS?
     - does the claim map get received, or does the prompt regenerate it anyway?
     - does the A-G verdict map cleanly onto concede results, or does it need
       replacing? (see the note at the end of Block F)
     - does the finding table crowd out the prompt's own internal tables?

3. Fix whatever that surfaces. Then apply to internal validity + citation network.

4. Run the counter-audit v3 on the output of step 2-3.
     - does G2 fire? does it ever conclude the prosecution attacked the wrong layer?
     - does the reception gate cap anything?

5. Only then: voice restoration, field diagnostic, field-context generator.

RATIONALE: every real improvement in the media branch came from a live run
surfacing something unpredicted. Applying six additions at once and then running
means you cannot tell which one caused what.

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

## RELATED FILES

  CHANGELOG.md        why each prompt rule exists — the failure it closes and
                      the run that exposed it
  tests/RESULTS.md    per-run behavior — which checks fired, what they changed,
                      what got killed downstream
  reference/philosophy.md   design rationale and honest limitations
