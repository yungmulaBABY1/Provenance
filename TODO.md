# TOOLKIT — TODO & STATE

Last updated: 2026\-08\-09 documentation and RC2 reconciliation pass\. See
`reference/current-state-inventory.md` for the verified cross\-artifact snapshot\.

## REPO — github\.com/yungmulaBABY1/Provenance

LIVE:
prompts/0\-field\-diagnostic\.txt
prompts/1\-claim\-extraction\.txt
prompts/5\-voice\-restoration\.txt
prompts/research\-analysis/2\-construct\-validity\.txt
prompts/research\-analysis/2\-internal\-validity\.txt
prompts/research\-analysis/2\-citation\-network\.txt
prompts/research\-analysis/3\-counter\-audit\.txt
prompts/media\-analysis/2\-framing\-construction\.txt
prompts/media\-analysis/2\-network\-coverage\.txt
reference/shared\-primitives\.txt
reference/narrative\-flags\-module\.txt
tools/citation\_reception\_module\.py
deferred/1\-field\-context\-generator\.txt
README\.md

MISSING — create:
&#91; &#93; 4\-synthesis\.txt          NEW PROMPT, does not exist yet\. Compression step
between human adjudication and voice restoration\.
Needs: aggregation rule \(derived not asserted\),
directional coherence, concede\-test results,
provisional flags preserved, no composite score\.
Most of this ports from the media prompts\.
BUILD AFTER the research branch has run once —
easier to design when you can see what it compresses\.
&#91;x&#93; CHANGELOG\.md             root — present and current through TOOL\-004
&#91; &#93; LICENSE                  root
&#91;x&#93; reference/philosophy\.md  reconciled repository reference
&#91;x&#93; reference/methodology\.md reconciled repository reference
&#91;x&#93; reference/architecture\-note\.md refreshed decisions and constraints
&#91;x&#93; reference/current\-state\-inventory\.md canonical/tested/duplicated/pending map
&#91; &#93; Reconcile reference/philosophy\.md with toolkit\_philosophy\_notes\.md if/when
that source document is supplied\.
&#91; &#93; deferred/ROADMAP\.md      future\-plans section of the philosophy notes
&#91; &#93; examples/                structure decided, see below

EXAMPLES STRUCTURE — decided:
examples/
├── README\.md                        ← field index lives here, NOT in folders
├── research\-analysis/
│   └── <target>/
│       ├── README\.md                ← what the run got right AND wrong
│       ├── 2\-construct\-validity\.md
│       └── 3\-counter\-audit\.md
└── media\-analysis/
└── <target>/
├── README\.md
├── 2\-framing\-construction\.md
└── 2\-coverage\-network\.md

Branch at top \(already a real distinction\)\. Target folder = the unit people
want\. Audit files numbered to match the prompts\. Field browsing goes in the
index, not the tree — a study can appear under two fields in an index, only
one folder\. Add folder taxonomy when the index stops scaling \(\~15 examples\)\.

PER\-EXAMPLE README MUST INCLUDE:
\- the practitioner caveat where it applies \(esports findings came from having
done the thing, not from the prompts\)
\- what the run got WRONG\. The MBH counter\-audit elevating McShane & Wyner
without checking its reception is more instructive than a clean run\.

README RECONCILIATION:
&#91;x&#93; “it points, you judge” framing; cut the overclaim register
&#91;x&#93; “How this toolkit stays honest” section — safeguards mapped to the AI failure
each addresses
&#91;x&#93; two entry routes documented; gate/on\-ramp terminology remains an explicit
architecture decision rather than being silently resolved in prose
&#91;x&#93; the three stage\-2 research prompts are INDEPENDENT — no dependencies, any
order, run one or all three
&#91;x&#93; human adjudication sits between 3\- and 4\- and has no file \(by design\)
&#91;x&#93; media\-analysis has no 3\-counter\-audit — balancing is internal to those two
prompts\. State it as a decision, not an omission\.
&#91; &#93; reproducibility literature as rationale \(SCORE, calibrated\)
&#91; &#93; reviewer/editor framing — strongest use is the non\-conflicted judge
&#91;x&#93; limitations: surfaces categories not mechanisms; can’t tell you what it missed

## DOCUMENTATION RECONCILIATION — before methodology / README are canonical

&#91; &#93; FIELD DIAGNOSTIC: choose one status and align all copies\. The live prompt calls
Stage 0 a feasibility / self\-calibration gate with go/no\-go routing; this TODO
and the webapp methodology call it an on\-ramp rather than a gate\.

&#91; &#93; MEDIA CLAIM MAP: decide whether claim extraction is a shared media stage or an
optional input to single\-piece framing only\. The webapp places it in both
branches; `1-claim-extraction.txt` describes three research prosecutors;
framing accepts an optional map; coverage\-network does not consume one\.

&#91; &#93; SHARED PRIMITIVES: resolve the six dangling prompt references before a
methodology document links or names a canonical shared layer\. The stale file
and the available options are documented below under NOTE ON SHARED PRIMITIVES\.

&#91;x&#93; WEBAPP PROMPT COPIES: generated payload now carries canonical paths,
checksums, byte/line counts, snapshot date, and an explicit repository\-wins rule\.
`tools/embed_prompts.py --check` currently passes\.

&#91; &#93; WEBAPP DOCUMENTATION: the sandbox prototype’s hardcoded Philosophy,
Methodology, Vocabulary, Limitations, and run\-library copy remains separately
authored\. If the prototype is promoted beyond sandbox status, generate or parity\-
check these copies; until then the repository references are authoritative\.

## STATE OF PLAY

The canonical snapshot, tested\-but\-unsynchronized work, duplication map, and
validation gaps are maintained in `reference/current-state-inventory.md`\.

- 42 runs are logged: 23 research and 19 media\.
- Research evidence remains concentrated on MBH98 and Donovan; internal validity
  has never run\.
- Proposition\-level source independence is canonical and exercised\.
- FAIL\-MB\-017/018 passed on the integrated RC2 artifact and their execution
  blocks are now canonical in `2-network-coverage.txt`\.
- TOOL\-004’s instrument preflight is canonical, but its dedicated two\-version
  collision case has not been built or run\.
- Individual stages have acquitted; no full research chain has returned clean\.
- The media proportionate\-negative case is built but unrun\.
- The webapp is an incomplete sandbox prototype, not a supported application\.

## PROMPT STATE — implementation and validation are separate

The research insertion blocks described below are applied\. The tested media RC2
integration is now canonical\. The later TOOL\-004 preflight is also canonical
but remains regression\-untested\. Do not use “implemented,” “tested,” and
“canonical” as synonyms\.

APPLIED \+ TESTED
1\-claim\-extraction\.txt ……\.\. heavily revised, 8 fixes, tested across \~10 runs
and 3 models\. See below for the fix list\.
2\-construct\-validity\.txt …… full chain, blocks A/B/C/F all fired
2\-citation\-network\.txt ……\.\. J2 concede test fired on MBH98\. The later
execution contract and checker passed three supplied\-packet pilots; open\-ended
retrieval remains unvalidated\.
3\-counter\-audit\.txt ………\.\. Blocks 1/2/3/4 applied; E0 verified firing

APPLIED, UNTESTED
2\-internal\-validity\.txt ……\. Blocks A/B/D/F \+ D2 forking\-paths \+ reception
hook all present\. Never run\.

UNVERIFIED
5\-voice\-restoration\.txt ……\. carve\-out application not confirmed
0\-field\-diagnostic\.txt ……\.\. replaced wholesale, never run

CLAIM\-EXTRACTION FIX LIST — all applied, all run\-tested unless noted

1. Field\-6 RULE 1 \(one claim only\) \+ RULE 2 \(prefer quantified version\)
2. Field 4 made ACTIVE — search for downstream use rather than waiting
3. Four provenance states: SUPPLIED / RETRIEVED / RECALLED / NONE FOUND
4. Parenthetical failure named and banned
5. Attribution check \+ ATTRIBUTED ELSEWHERE \+ scope arithmetic
6. MISATTRIBUTED branch \(closes the exoneration loophole\)
7. Field\-specific provisional rule \(fields 4/5/6, not blanket\)
8. Anchoring rule at field 5 — only SUPPLIED/RETRIEVED may anchor
9. CROSS\-SOURCE\-CONFIRMED adopted; no\-invented\-states rule
10. Joint\-citation document\-level check \(prevents false\-positive MISATTRIBUTED\)
11. Claim inventory before field 6 — applied, UNTESTED
12. Label verification at anchoring — applied, UNTESTED\. A run labeled an
    unquoted pattern generalization RETRIEVED and anchored on it; this
    requires a quotation AND locator before an item may anchor\.

All research\-branch insertion blocks and fixes described below are applied\.
The media coverage\-network RC2 repository sync is complete\.

MEDIA COVERAGE\-NETWORK RC2 / TOOL\-004 STATE

&#91;x&#93; Preserve FAIL\-MB\-017 / FAIL\-MB\-018 registry records, complete
fixture\-bearing cases, and integrated rerun evidence\.

&#91;x&#93; Synchronize the integrated FAIL\-MB\-017 / FAIL\-MB\-018 execution blocks\.
The integrated 3,232\-line artifact at Git blob
`d5f3502fc3ab1af083c12be0a0b1440cbf2adf6f` was run; current `main` carries the
same analytical blocks in `prompts/media-analysis/2-network-coverage.txt`\.

&#91;x&#93; Add TOOL\-004’s formal\-run instrument preflight to the canonical prompt\.
The current 3,340\-line / 131,417\-byte prompt has Git blob
`9380b619fd16b4212dabec28971f1c6a6b3d18b6`\.

&#91; &#93; Build and run `mutable-prompt-version-collision` before claiming the TOOL\-004
guard is exercised\. The current prompt’s presence and immutable identity prove
implementation, not regression behavior\.

&#91; &#93; Promote TOOL\-004 to a common run launcher/router when that shared execution
layer exists; do not maintain divergent prompt\-local copies indefinitely\.

Recently applied, UNTESTED — these have not yet been through a run:

- Claim inventory before field 6 \(1\-claim\-extraction\)
- Label verification at the anchoring step \(1\-claim\-extraction\)
- CROSS\-SOURCE\-CONFIRMED \+ no\-invented\-states in the compact vocabulary blocks
- Model\-routing block removed from 2\-citation\-network
- Voice\-restoration carve\-out

The first two matter most on the next run\. The claim inventory is new
behavior; label verification closes the loophole where a run labeled an
unquoted pattern generalization RETRIEVED and anchored a failure location on it\.

NOTE ON SHARED PRIMITIVES: the compact copies inside each prompt are what
actually runs; reference/shared\-primitives\.txt is documentation nobody loads\.
Edits must go to the prompts\.

&#91;x&#93; Header saying so — APPLIED, matching the narrative\-flags module\.

Two things surfaced while applying it, both worse than “nobody loads it”:

1. Despite the filename the file is NOT a primitives document\. It is an older
   reflowed copy of 1\-claim\-extraction\.txt — same title, same WHY THIS STAGE
   EXISTS structure, same field 1\-6 table\. It is a stale duplicate of a live
   prompt, not reference material\.
2. The `References: shared_primitives.txt Section 1 / 2 / 3` line at the top of
   six prompts is DANGLING\. Sections 1, 2 and 3 do not exist in that file or
   anywhere else\. The file’s own header even carries the reference, pointing at
   itself\.

&#91; &#93; Decide what to do about the six dangling reference lines\. Options: point them
at the COMPACT VOCABULARY block in the prompt that carries them, or delete the
line\. Not done here — it edits six live prompts and every prompt edit should
be run\-tested, which this has not been\.

&#91; &#93; Consider deleting reference/shared\-primitives\.txt outright\. It is now banner\-
marked, but a stale copy of a live prompt is a standing invitation to read the
wrong version\. Apply the deletion standard before cutting\.

COMPLIANCE GAP — LOCAL REPAIR VALIDATED, BOUNDARY STILL OPEN

FAIL\-CN\-001’s execution contract, Completion Ledger, and checker passed three
supplied\-packet pilots at 4, 12, and 26 sources \(through 70 selected edges\)\.
This falsified supplied\-packet burden as the explanation within that range and
closes the earlier “truncation or skipping?” diagnosis for those pilots\.

Still open:

- validation during open\-ended retrieval;
- TOOL\-002, because the checker regression fixtures do not reproduce the
  original silent omission \+ gate failure \+ verdict issued behavior; and
- substantive correctness, which the mechanical checker does not evaluate\.

## NEXT — in order

The apply\-then\-run sequence is complete for the research branch\. What follows is
validation on new material, not construction\.

1. SHEN, FULL CHAIN\. map \-\> construct \-\> internal \-\> citation \-\> counter\-audit\.
   Chosen because you know the answer AND you know the toolkit will miss it —
   the fishing and carry mechanisms came from having played, not from a prompt\.
   What this tests that MBH98 could not:

- Does the toolkit produce the generic scaffold \(wrong population, weak
  proxy, level\-of\-analysis\) and correctly signal something is missing,
  rather than reading as complete? This is the honest\-limitation claim in
  philosophy\.md, tested where you can see both what it found and what it
  could not reach\.
- OVERFIT CHECK: Shen has no same\-author successor, no assessment trail\.
  MISATTRIBUTED / ATTRIBUTED ELSEWHERE / joint\-citation disambiguation
  should all come back EMPTY\. If the map strains to fill them, the MBH98
  overfit is showing\.
- First run of 2\-internal\-validity, ever\.
- Does the claim inventory \(new, untested\) produce useful secondaries?
- Does label verification fire? Watch for any item labeled RETRIEVED
  without a quotation and locator — it should be downgraded to RECALLED
  and barred from anchoring\.

2. LOG IT IN tests/RESULTS\.md\. Which checks fired, what changed, what was killed\.
   Including passes — a check that never alters an outcome across twenty runs is
   length without function, but only if passes are recorded\.
3. TOOL\-004 REGRESSION\. Build `mutable-prompt-version-collision` and verify that
   a collision stops unresolved until a second independent discriminator exists\.
4. CASE 11 on the media branch\. Built, never run\. Tests whether the instrument
   can decline to find\.
5. CITATION RETRIEVAL \+ TOOL\-002\. Test the completion contract during retrieval
   and add a fixture for the original silent\-omission behavior\.
6. Voice restoration, field diagnostic, field\-context generator — all still
   unverified, all lower priority than the above\.

RATIONALE: every real improvement so far came from a live run surfacing something
unpredicted\. Zero exceptions across 14 logged runs\. More prompt\-reading will not
produce the next fix\.

## MULTI\-CLAIM SCOPE — staged, do NOT batch

PROBLEM: a source can make several inflatable claims\. Field 6 selects one; every
stage is locked to it\. The other claims are invisible to the whole sequence\.
Citation\-network is the stage most under\-powered by this — its natural job is
mapping travel across literature, assessment, PR, and media, and it is currently
constrained to one sentence\.

STAGE 1 — DONE
&#91;x&#93; Claim inventory added to 1\-claim\-extraction\.txt\. Numbered claims, one sentence
each, quantified or not, why each might be inflated, which was selected and
why\. Unselected = DEFERRED, not dismissed\.
This alone answers “which claims are suspect\.” Costs nothing downstream —
every stage still targets field 6\.

STAGE 2 — ONLY IF THE INVENTORY SHOWS SECONDARIES THAT MATTER
Do not build these preemptively\. Run the inventory first; if deferred claims
turn out to be live, then:

&#91; &#93; 2\-citation\-network\.txt — scope grant\. MUST audit the primary claim’s travel;
MAY additionally audit claims enumerated in the map’s inventory; MAY NOT
substitute or expand its own scope\. Every finding declares its claim ID\.
NOTE ON WORDING: do NOT grant “the selected claim and closely related
restatements\.” “Closely related” is undefined and elastic — a prosecutor
looking for inflation will stretch it to whatever is most inflated\. That is
the drift the shared\-object rule exists to prevent, reintroduced as a scope
grant\. The map enumerates; the prosecutor does not\.

&#91; &#93; Standardized finding table \(all prosecutors\) — “Target claim” column takes a
CLAIM ID, not “field 6\.” The column currently assumes one claim exists\. This
is the structural point where standardization limits multi\-claim work\.

&#91; &#93; Counter\-audit G2 — MUST be updated with the scope grant or it breaks\. G2 asks
“did the prosecution attack the strongest version, or the easiest downstream
exaggeration?” and compares findings against field 6\. If citation\-network is
legitimately auditing C2/C3, G2 will flag every one of those as off\-target —
the drift check firing on sanctioned breadth\. Fix: G2 checks each finding
against ITS DECLARED target claim, not against field 6 globally\. It can then
still catch real drift \(a claim ID matching nothing in the inventory, or a C1
finding that actually attacks C2\)\.

OPTION 2 — SEPARATE MAP PER CLAIM: not a mode the user selects\.
The user does not know upfront which claims warrant a full run; that is what
the audit is for\. Sequence: first pass inventories and defers; citation\-network
reports whether any deferred claim travelled badly; THAT is the signal to run
the sequence again with a different field 6\. Informed, not guessed\.
No sequence change required — just run it again with a new primary\. Keeps the
paste\-and\-run path intact: one pass, one claim audited properly, others
inventoried and flagged\.

CAUTION: the scope grant expands what citation\-network can do, and citation\-network
is the prompt with the observed compliance gap \(blocks present in prompt, absent
from output — see COMPLIANCE GAP OBSERVED above\)\. Measure that before adding scope
to it\.

## REGRESSION TEST SUITE — tests/

Structure:
tests/
├── README\.md          how to run, what each case proves
├── cases/             one file per case
└── RESULTS\.md         prompt version, model, date, pass/fail per case

Each case needs THREE parts:

1. the synthetic article \(200\-400 words, ONE mechanism unambiguous\)
2. the EXPECTED RESULT, written BEFORE running
3. what a failure means, localized to a specific check

The expected result written in advance is the whole point\. Written after, you
will rationalize whatever came out\.

BUILT:
&#91;x&#93; 11 — proportionate article, clean result
\(`tests/cases/11-proportionate.md`\)
THE PRIORITY\. Tests whether the instrument can decline to find\. Never
demonstrated\. If this fails, the other ten test a machine that cannot say
no, and their passes mean less than they appear to\.
&#91;x&#93; CE\-006 / CE\-007 — joint citation pair
\(`tests/cases/CE-006-007-joint-citation.md`\)\.
&#91;x&#93; MIX\-01 — mixed claim\-inventory control
\(`tests/cases/MIX-01-mixed-control.md`\)\.
&#91;x&#93; FAIL\-CN\-001 — compliance fixture set, run at three burden levels
\(`tests/cases/fixture-structural-verification.md`\)\.
&#91;x&#93; FAIL\-MB\-017 — Ceuta prominence regression
\(`tests/cases/case_FAIL-MB-017_ceuta-prominence-regression.md`\)\.
Exact eight\-piece fixture embedded; standalone and joint interaction PASS\.
&#91;x&#93; FAIL\-MB\-018 — Ceuta semantic equivalence / earnedness
\(`tests/cases/case_FAIL-MB-018_ceuta-semantic-equivalence.md`\)\.
Exact eight\-piece fixture embedded; procedural and joint interaction PASS\.

BUILD NEXT — the mechanisms with the most patch history, likeliest to have drifted:
&#91; &#93; TOOL\-004 / `mutable-prompt-version-collision` — two versions at one mutable
logical path; internally coherent stale representation; immutable current
identity supplied independently\. Expected: collision remains unresolved before
that discriminator, no stale\-side attribution is invented, and formal execution
is blocked until identity is confirmed\.
&#91; &#93; 01 — omission vs\. de\-emphasis
&#91; &#93; 03 — amplification vs\. independent corroboration   \(network branch\)
&#91; &#93; 04 — timing artifact vs\. editorial selection

BUILD LATER:
&#91; &#93; ceuta\-prominence\-d2\-ownership — supply a prior single\-piece
packaging finding and exercise cross\-branch ownership without duplication
&#91; &#93; 02 — synonym variance vs\. causal\-context loss
&#91; &#93; 05 — network\-wide convention vs\. outlet\-specific divergence  \(network\)
&#91; &#93; 06 — appositional classification
&#91; &#93; 07 — denominator / baseline switching                        \(network\)
&#91; &#93; 08 — established vs\. attributed cause
&#91; &#93; 09 — mirror symmetry
&#91; &#93; 10 — narrative\-flag omission and over\-activation

COST NOTE: cases 3, 5, 7 test the network branch and need MULTIPLE articles plus
a primary source\. Substantially more expensive to write than single\-piece cases\.

WRITING NOTE: a good synthetic article is real work — plausible enough that the
prompt engages seriously, engineered so exactly ONE mechanism is unambiguous\.
Eleven written in one sitting will mostly be sloppy, and a sloppy case is worse
than none: a false failure sends you fixing a prompt that was fine\.

## ARCHITECTURE AUDIT — parity passes complete; deletion pass pending

Cross\-prompt drift and duplication reviews have been run on the media pair and
the claim\-extraction / construct\-validity pair, followed by targeted fix passes\.
What remains is the cold whole\-file deletion review below\.

The single\-piece prompt is \~1450 lines assembled from \~15 rounds of patches,
each written without full view of what came before\. Needs someone reading the
whole file cold, looking for CONTRADICTION rather than gaps\.

Look for:
&#91; &#93; the same rule stated twice in different words — reinforcement or drift?
\(e\.g\. the “noted but does not offset” ban appears in J Step 6 AND the
integrity block\)
&#91; &#93; ownership collisions — Section C owns sequencing, G owns de\-emphasis, E2\.2
owns causal bridges; all three can claim the same placement choice
&#91; &#93; severity caps that conflict when two apply to one finding, with no
precedence rule
&#91; &#93; dead instructions superseded by later additions but never removed
&#91; &#93; vocabularies restated with drift between statements
&#91; &#93; optional modules lacking explicit triggers
&#91; &#93; places automated aggregation could override human adjudication

DELETION STANDARD — for every proposed cut, require:

1. what failure the rule prevents
2. whether that failure was OBSERVED in a run \(check the changelog\)
3. where the protection moves
4. which regression test proves it still holds

NOTE: several rules are regression fixes added after observed failures\. Do not
delete a rule solely because a newer model might infer it\.

BEST DONE BY SOMEONE WHO DIDN’T WRITE IT — an author reads what they intended,
not what is there\.

## OPEN QUESTIONS — unresolved, not blockers

&#91;x&#93; The existing verdict scale survives as a derived output; do not add a
parallel scale\. The concede test supplies the derivation rule\. Remaining work is
notation harmonization for audited claim \+ surviving residual, and a run that
exercises `residual: none`\.

&#91;x&#93; Automatic downgrade — the mechanical version fires\. It fired in the
integrated RC2 Ceuta rerun and, after FAIL\-MB\-018 removed the former rank\-1
event\-language finding, moved to France 24 blame routing \(MODERATE \-\> MINOR\)\.

&#91; &#93; Cap Times / CNN: do they assert the pattern frame in their own headlines,
unattributed? Claude flagged it PROVISIONAL on snippets\. If it holds on full
text, the Examiner routing its pattern claim through a quote was MORE
restrained than peers on the dimension it was rated MAJOR for\.

&#91;x&#93; Re\-run Stage 1 cold on MBH98 with the new field\-6 rules — DONE\. Field 6
selected the quantified claim, one claim only, no forcing bundled\. Both rules
held\. The defect is now found from the prompt rather than from a hand\-written
map\.

&#91;x&#93; Does the counter\-audit’s Section E find the source’s own pre\-emptions? — WAS
NO across seven runs; Block 4 / E0 added; now YES\. See changelog\.

&#91; &#93; Marcott 2013 — the better Tool 2 test\. Less iconic, so model background
supplies less of the controversy\. Prior generic \+ tailored runs already exist
for comparison\.

&#91; &#93; Nobody has run the full pipeline on a paper that should come back CLEAN\.
Individual findings have been cleared; no paper has\. This is the acquittal
test and it is the one validation the toolkit has never had\.

&#91; &#93; CAND\-006 construct\-side acquittal test — ATTEMPTED, NOT ACHIEVED\. The
chosen target \(Gabarrell\-Pascuet et al\. 2024\) turned out to have a genuine
construct problem: definitional scope creep plus a content/keying confound\. The
next attempt needs a target vetted at ITEM level before the run, not at
dimensional level\. NOTE: the CAND\- register itself is not in this repository
yet, so this label is pending reconciliation rather than resolvable\.

&#91; &#93; Settle the FAIL\-CV\-005 scope boundary before the next acquittal attempt\.
Two models on the same source and the same Field 6 claim returned incompatible
verdicts on a scope convention rather than on evidence\. A verdict that flips on
convention makes any acquittal result unfalsifiable\.

## DEFERRED — not v1

Tool 2 field\-context generator \(built: field\_context\_generator\_v2\.txt, unrun\)
Coverage\-over\-time branch \(drift rather than divergence — designed, not built\)
Comparative institutional audit mode
Multi\-model comparison layer
Bidirectional resistance testing
Agentic version
Banked field\-context library \+ auto\-update
README rewrite \(philosophy notes are the source material\)
Repo reorganization

## FAILURE REGISTRY — markers not yet inserted

FAILURES\.md is written: 35 FAIL entries, 4 TOOL entries, and 8 GUARD entries\.
The registry exists; the prompt\-side markers are still incomplete\.

&#91; &#93; Insert one\-line markers in the prompts — e\.g\. &#91;FAIL\-CE\-010&#93; beside the
label\-verification rule\. No narrative in the prompt; the record lives in
FAILURES\.md\.
&#91; &#93; Reference IDs from CHANGELOG entries and tests/RESULTS\.md rows rather than
restating the failure\.

WHY THIS MATTERS: the architecture audit \(below\) will ask “what failure does this
rule prevent, and was it observed?” for every proposed cut\. Without markers that
requires reading the whole changelog per rule\. With them it is a lookup\.

THE FAIL/GUARD SPLIT IS THE POINT\. An observed failure has a strong claim to
survive an audit; an anticipated one does not\. GUARD\-004 \(“nothing downstream
corrects it”\) is already flagged as the clearest deletion candidate — kept on
reasoning alone, unmeasurable by design\.

WEAKNESS TO NOTE: six canonical regression case units now exist, including the
completed FAIL\-MB\-017 and FAIL\-MB\-018 Ceuta cases\. Most registry entries are
still protected by narrative alone\. A rule with an observed failure, no regression
case, and no replacement is not safely deletable — but it is also not safely
KEEPABLE without evidence it still fires\.

## RELATED FILES

FAILURES\.md         numbered registry: every rule traces to an observed
failure \(FAIL\-\) or an anticipated one \(GUARD\-\)\. Deletion
protection for the architecture audit\.
CHANGELOG\.md        why each prompt rule exists — the failure it closes and
the run that exposed it
tests/RESULTS\.md    per\-run behavior — which checks fired, what they changed,
what got killed downstream
reference/philosophy\.md   design rationale and honest limitations
reference/methodology\.md  canonical sequence, handoffs, and evidence axes
reference/architecture\-note\.md  cross\-prompt constraints and decision status
reference/current\-state\-inventory\.md  reconciled implementation and validation map
