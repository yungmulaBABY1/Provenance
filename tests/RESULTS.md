# RESULTS — per-run behavior log

The CHANGELOG records **fixes**: what broke and what closed it.
This records **behavior**: which checks fired, what they changed, what got killed.

After enough runs this answers questions no single run can:
- Which checks have never once altered a verdict? (length without function)
- Which fire on every run? (probably miscalibrated)
- How often does a downstream stage kill an upstream finding? (the pipeline working)
- Does the instrument ever return "nothing of consequence"? (can it acquit)

**One row per run.** Add as you go. Do not backfill from memory — if a run's
detail is not recorded, mark it UNKNOWN rather than reconstructing it.

---

## SUMMARY TALLIES

*Update when adding runs. These are the numbers that matter.*

| Metric | Count | Notes |
|---|---|---|
| Total runs logged | 14 | 1 paper (MBH98), 1 article (Madison), 4 models |
| Distinct sources audited | 2 | **overfit risk — see below** |
| Runs returning "nothing of consequence" | 1 | claude-mhb-1, GAP TYPE "neither apparent" |
| Upstream findings killed downstream | 4 | see KILLS below |
| Checks that have never altered an outcome | see DORMANT | |

**OVERFIT WARNING:** 12 of 14 runs are one paper. MBH98 has a same-author
successor, a famous controversy, and an assessment-report trail. The entire
attribution apparatus (MISATTRIBUTED / ATTRIBUTED ELSEWHERE / joint-citation
disambiguation) exists because MBH99 exists. Most sources have none of that.
Next source should test whether those fields come back empty cleanly.

---

## KILLS — upstream findings killed by a downstream stage

The clearest evidence the pipeline works rather than accumulates.

| # | Finding | Killed by | How |
|---|---|---|---|
| 1 | "produced a knife" = minimizing verb choice | Coverage-network D2 | Primary source comparison — MPD written report says "pulled out," presser said "produced." Document dependence, not editorial choice. RECLASSIFIED. |
| 2 | Patterson foregrounded trauma framing (source-internal selection) | Coverage-network D2 | CNN reported he opened the presser that way. FALSIFIED outright. |
| 3 | Sourcing asymmetry in the Examiner brief | Genre gate (Section 0) | Format constraint — a 250-word breaking brief cannot carry balancing voices. Cut, not a finding. |
| 4 | Millennial claim = MBH98 downstream inflation | Claim-map attribution check, then joint-citation document check | Scope arithmetic → MBH99. Then the document-level check kept it from swinging to false-positive MISATTRIBUTED. |

---

## DORMANT — checks that exist but have not yet changed an outcome

*Not evidence they are useless. Evidence they are untested.*

| Check | Runs where present | Times it changed something |
|---|---|---|
| Concede test (construct-validity) | 2 | 1 — v3 run, E→C via NARROWS not DEFEATS |
| Concede test (citation-network) | 1 | 0 |
| Concede test (internal-validity) | 0 | n/a — prompt never run |
| Standardized finding table | 3 | 0 — summary only, no verdict effect observed |
| MAP GAP / MAP DISAGREEMENT | 4 | 0 — never fired |
| Automatic downgrade (media) | 0 | n/a — untested since replacing discretionary |
| D2 cross-branch resolution | 1 | 2 kills (see above) |
| Reception gate | 2 | 1 — McShane & Wyner capped CONTESTED |

**MAP DISAGREEMENT at 0/4 is worth watching.** Either the maps were good, or the
mechanism is weak. One more run either way does not distinguish these.

---

## RUNS

### Research branch — MBH98

| # | Date | Stage | Prompt ver | Model | Field 6 | Verdict | Checks that fired | Notes |
|---|---|---|---|---|---|---|---|---|
| R1 | pre-session | construct | generic, pre-revision | Claude | none | C | — | Audited the controversy: centering, bristlecones, M&M, Wegman. Domain-concern field **model-populated**, not user-supplied. |
| R2 | pre-session | construct | tailored (climate), pre-revision | Claude | none | C | — | Added PSM, uncertainty budget, pseudoproxy, convergent validity, reproducibility. Same verdict. Engaged the paper's dendro robustness test — the only pre-revision run that did. |
| R3 | 07-30 | construct | revised + **hand-written map** | Claude | quantified 3σ claim | **E** | claim map received, concede test | Found pointwise-vs-simultaneous defect. **Map was hand-written by Claude from full text — not a Stage 1 output.** |
| R4 | 07-30 | claim extraction | 1-claim-extraction v1 | ? | abstract claim + forcing bundled | n/a | — | **Field 6 wrong**: unquantified version, two claims bundled. |
| R5 | 07-30 | construct | revised + R4 cold map | ? | abstract claim | C | claim map received | Did NOT find the defect. 0 hits pointwise/simultaneous. **Confirms E came from the map, not the prosecutor.** |
| R6 | 07-30 | claim extraction | + field-6 rules | ? | quantified, one claim | n/a | RULE 1, RULE 2 | Both rules held. |
| R7 | 07-30 | construct | revised (no Block B/F) + R6 map | ? | quantified | **E** | claim map | Found the defect. But prompt lacked concede test — verdict overshot. |
| R8 | 07-30 | construct | **full v3** + cold map | ? | quantified | **C** | concede test, scope-loss, MAP DISAGREEMENT, finding table | Same defect, correctly scored NARROWS not DEFEATS. **Concede test is what makes E→C.** |
| R9 | 07-30 | citation-network | blocks applied | ? | quantified | — | concede test (J2) | **COMPLIANCE GAP**: prompt had Blocks A/B/E; output showed 0 claim-map receipt, 0 verification states, 0 finding table. Truncation or skipping — unresolved. |
| R10 | 07-30 | counter-audit | v3 (no E0) | ? | quantified | B — narrowed | G2, reception gate | G2 softened "fatal"/"invalid" → "not demonstrated as unconditional." Reception gate capped McShane & Wyner CONTESTED. **Section E searched literature only — 0 hits for the paper's own pre-emptions.** |
| R11 | 07-30 | counter-audit | v3.1 + **E0** | ? | quantified | C — softened | E0, G2, reception gate | **E0 found every pre-emption 7 prior runs missed.** 0 DEFEATED / 2 NARROWED / 4 RECHARACTERIZED / 0 UNAFFECTED. Moved impact B→C. |
| R12 | 07-30 | claim extraction | + active field 4 | ? | quantified | n/a | field 4 active | Parenthetical failure gone. **But recorded millennial claim as MBH98 downstream inflation** — attribution error. |
| R13 | 07-30 | claim extraction | + attribution check | Grok-ish | quantified | n/a | ATTRIBUTED ELSEWHERE ×6, scope arithmetic | Caught the "Mann et al. (1998, 1999)" conflation in a retrieved source. Recorded non-inflation for 2 items — first map-level acquittal behavior. |
| R14 | 07-30 | claim extraction | + attribution check | Sol | quantified | n/a | MISATTRIBUTED | Retrieved IPCC TAR sentence citing MBH98 for a millennial claim → MISATTRIBUTED. **Later reversed by R17 on fuller retrieval.** |
| R15 | 07-30 | claim extraction | + anchoring rule | Grok | quantified | n/a | anchoring rule, SUSPECTED | Correctly declined to assign MIXED: "no retrieved citing sentence found... therefore no established CITATION-layer failure location." **Fix working — previous run had anchored on RECALLED.** |
| R16 | 07-30 | claim extraction | + anchoring rule | Sol | quantified | n/a | CROSS-SOURCE-CONFIRMED ×4 | **Reversed its own R14.** Retrieved NRC Ch.11 distinguishing the two papers' scopes → joint citation = synthesis attribution, not misattribution. |
| R17 | 07-30 | claim extraction | + joint-citation doc check | Claude | quantified | n/a | doc-level check, NONE FOUND (precise) | **GAP TYPE: neither apparent** — first map-level full acquittal. Retrieved MBH99 abstract + IPCC SPM figure attribution. |
| R18 | 07-30 | claim extraction | + joint-citation doc check | Sol | quantified | n/a | doc-level check | PAPER only, no established downstream. Retrieved the decisive IPCC Ch.2 sentence attributing to Mann et al. (1999). |
| R19 | 07-30 | claim extraction | + joint-citation doc check | Grok | quantified | n/a | — | **MIXED — diverged.** Labeled an unquoted pattern generalization as RETRIEVED, then anchored failure location on it. **Loophole: anchoring rule trusts a self-assigned label.** |

### Media branch — Madison / Corey Ruiz

| # | Stage | Prompt ver | Models | Verdict | Notes |
|---|---|---|---|---|---|
| M1 | framing | pre-fix | Grok | substantially slanted | Flip test returned zero downgrades — **theater**. |
| M2 | framing | + costly flip test | ? | substantially slanted | Mirror written, 2 findings against it. But **inverted the mandated sentence** ("is functioning" for "may not be functioning"). Consistency check induced a bad downgrade (Type B misread as Type A). |
| M3 | framing | + Type A/B split, lever coherence | ChatGPT, Grok, Claude | subst. slanted ×2, heavily constructed ×1 | Divergence traced to **finding-splitting** — Claude counted 8, others 5. Fixed by counting levers. |
| M4 | framing | + F2 frame laundering | 4 models | 3× heavily constructed, 1 invalid | **Gemini audited a hallucinated article** — cited paragraphs not in the piece. Discarded. Strip test split PARTLY/COLLAPSES on a mixed paraphrase construction. |
| M5 | coverage-network | first run | ChatGPT, Grok, Claude | — | **Independence count converged ~4 across 3 unrelated samples.** Strongest metric the branch produces. Clustering answer varied by sample — correctly flagged as sample-dependent by all three. |
| M6 | coverage-network | + D2 | ChatGPT, Claude, Grok | — | **D2 falsified 2 upstream findings** on first use. Grok returned CONFIRMED with no primary source — led to the D2 evidence floor. |

---

## WHAT THE LOG ALREADY SHOWS

1. **The claim map is the highest-leverage stage.** R3/R5 isolate it: same prompt,
   same paper, different field 6, verdict E vs. C. One sentence upstream decided
   whether a real defect was found.

2. **The concede test converts finding-severity into verdict-severity correctly.**
   R7 (defect found, no concede test) → E. R8 (defect found, concede test) → C.
   Without it a single technical defect reads as a broken paper.

3. **Downstream stages do kill upstream findings** — 4 documented. The pipeline
   corrects rather than accumulates.

4. **Retrieval depth drives most model divergence, not reasoning.** R17/R18
   retrieved decisive sentences and converged. R19 generalized and diverged.
   Same prompt.

5. **Self-report is unreliable even under explicit instruction.** M2 inverted a
   sentence it was told to reproduce verbatim. M4's audit-integrity block claimed
   no banned phrase was used while the phrase appeared in the output.

6. **Every fix that mattered came from a run, not from reading the prompt.**
   Zero exceptions across 14 runs.
