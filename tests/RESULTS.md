# RESULTS — per-run behavior log

The CHANGELOG records **fixes**: what broke and what closed it. This records **behavior**:
which checks fired, what they changed, what got killed.

After enough runs this answers questions no single run can:
- Which checks have never once altered a verdict? (length without function)
- Which fire on every run? (probably miscalibrated)
- How often does a downstream stage kill an upstream finding? (the pipeline working)
- Does the instrument ever return "nothing of consequence"? (can it acquit)

**One row per run.** Add as you go. Do not backfill from memory  -  if a run's detail is not
recorded, mark it UNKNOWN rather than reconstructing it.

---

## SUMMARY TALLIES

*Update when adding runs. These are the numbers that matter.*

| Metric | Count | Notes |
|---|---|---|
| Total runs logged | 39 | 19 research rows (MBH98), 6 Madison media rows, 2 Ceuta media rows, 12 new research rows (Shen, Galor-Özak, Gabarrell-Pascuet, ISIS-2) |
| Distinct sources audited | 7 | **overfit risk  -  see below** |
| Runs returning "nothing of consequence" | 1 | claude-mhb-1, GAP TYPE "neither apparent" |
| Upstream findings killed downstream | 4 | see KILLS below |
| Checks that have never altered an outcome | see DORMANT | |

**OVERFIT WARNING, UPDATED:** the original concentration on one research paper (MBH98,
19 of the first 27 rows) has been substantially addressed by four additional research
sources since -- Shen et al. 2016, Galor & Özak 2016, Gabarrell-Pascuet et al. 2024, and
ISIS-2 (1988) -- spanning games research, economics, psychology, and cardiology. The
MBH98-specific attribution apparatus (MISATTRIBUTED / ATTRIBUTED ELSEWHERE / joint-citation
disambiguation) was tested against Shen, a source with no comparable controversy trail, and
correctly returned non-empty but unstrained results rather than either forcing entries or
returning suspiciously clean ones. On the media side, Ceuta adds a second event beyond
Madison and reproduces three prompt defects (FAIL-MB-008/009/010) independently of the
Madison findings -- real diversification, not just a second data point on the same
mechanism. Remaining concentration risk: research-branch construct-validity work is now
tested across five sources, but internal-validity and citation-network have each only been
exercised on two (MBH98/Shen/Galor-Özak territory) -- worth watching as those checks see
more use.

---

## KILLS — upstream findings killed by a downstream stage

The clearest evidence the pipeline works rather than accumulates.

| # | Finding | Killed by | How |
|---|---|---|---|
| 1 | "produced a knife" = minimizing verb choice | Coverage-network D2 | Primary source comparison  -  MPD written report says "pulled out," presser said "produced." Document dependence, not editorial choice. RECLASSIFIED. |
| 2 | Patterson foregrounded trauma framing (source-internal selection) | Coverage-network D2 | CNN reported he opened the presser that way. FALSIFIED outright. |
| 3 | Sourcing asymmetry in the Examiner brief | Genre gate (Section 0) | Format constraint  -  a 250-word breaking brief cannot carry balancing voices. Cut, not a finding. |
| 4 | Millennial claim = MBH98 downstream inflation | Claim-map attribution check, then joint-citation document check | Scope arithmetic → MBH99. Then the document-level check kept it from swinging to false-positive MISATTRIBUTED. |
| 5 | Scope-creep finding (Donovan et al., MAJOR) attributing GESR-family items | NSF PAR instrument retrieval | Actual instruments (PHGV/GARD/BGE) target different content than assumed; the finding had been built on inferred, not retrieved, items. |
| 6 | Construct-validity's own narrower framing of Field 6 (Shen) | Internal-validity's IV-1 | Once internal-validity's statistical contradiction was actually consumed by counter-audit (FAIL-CA-003 fix), it -- not the construct-side narrowing -- became the load-bearing reason Field 6 fails. Construct-validity's finding survives as a NARROWS; it stopped being the decisive lever. |

---

## DORMANT — checks that exist but have not yet changed an outcome

*Not evidence they are useless. Evidence they are untested.*

| Check | Runs where present | Times it changed something |
|---|---|---|
| Concede test (construct-validity) | 2 | 1  -  v3 run, E→C via NARROWS not DEFEATS |
| Concede test (citation-network) | 1 | 0 |
| Concede test (internal-validity) | 4 | 3 -- Shen's IV-1 defeated Field 6 directly; the Galor-Özak contaminated/clean pair changed the letter grade (D vs. C) on identical evidence depending on context, which is itself the finding behind FAIL-IV-001 |
| Standardized finding table | 3 | 0  -  summary only, no verdict effect observed |
| MAP GAP / MAP DISAGREEMENT | 5 | 1 -- Shen: internal-validity found a paper-layer failure within advancement itself that the claim map had not anticipated |
| Automatic downgrade (media) | 4 | 2/2 run-2 + 2/3 run-1, all mechanical, run-2 with no prior  -  FAIL-MB-005 |
| D2 cross-branch resolution | 1 | 2 kills (see above) |
| Reception gate | 2 | 1  -  McShane & Wyner capped CONTESTED |

**MAP DISAGREEMENT at 0/4 is worth watching.** Either the maps were good, or the mechanism
is weak. One more run either way does not distinguish these.

---

## RUNS

### Research branch — MBH98

| # | Date | Stage | Prompt ver | Model | Field 6 | Verdict | Checks that fired | Notes |
|---|---|---|---|---|---|---|---|---|
| R1 | pre-session | construct | generic, pre-revision | Claude | none | C |  -  | Audited the controversy: centering, bristlecones, M&M, Wegman. Domain-concern field **model-populated**, not user-supplied. |
| R2 | pre-session | construct | tailored (climate), pre-revision | Claude | none | C |  -  | Added PSM, uncertainty budget, pseudoproxy, convergent validity, reproducibility. Same verdict. Engaged the paper's dendro robustness test  -  the only pre-revision run that did. |
| R3 | 07-30 | construct | revised + **hand-written map** | Claude | quantified 3σ claim | **E** | claim map received, concede test | Found pointwise-vs-simultaneous defect. **Map was hand-written by Claude from full text  -  not a Stage 1 output.** |
| R4 | 07-30 | claim extraction | 1-claim-extraction v1 | ? | abstract claim + forcing bundled | n/a |  -  | **Field 6 wrong**: unquantified version, two claims bundled. |
| R5 | 07-30 | construct | revised + R4 cold map | ? | abstract claim | C | claim map received | Did NOT find the defect. 0 hits pointwise/simultaneous. **Confirms E came from the map, not the prosecutor.** |
| R6 | 07-30 | claim extraction | + field-6 rules | ? | quantified, one claim | n/a | RULE 1, RULE 2 | Both rules held. |
| R7 | 07-30 | construct | revised (no Block B/F) + R6 map | ? | quantified | **E** | claim map | Found the defect. But prompt lacked concede test  -  verdict overshot. |
| R8 | 07-30 | construct | **full v3** + cold map | ? | quantified | **C** | concede test, scope-loss, MAP DISAGREEMENT, finding table | Same defect, correctly scored NARROWS not DEFEATS. **Concede test is what makes E→C.** |
| R9 | 07-30 | citation-network | blocks applied | ? | quantified |  -  | concede test (J2) | **COMPLIANCE GAP**: prompt had Blocks A/B/E; output showed 0 claim-map receipt, 0 verification states, 0 finding table. Truncation or skipping  -  unresolved. |
| R10 | 07-30 | counter-audit | v3 (no E0) | ? | quantified | B  -  narrowed | G2, reception gate | G2 softened "fatal"/"invalid" → "not demonstrated as unconditional." Reception gate capped McShane & Wyner CONTESTED. **Section E searched literature only  -  0 hits for the paper's own pre-emptions.** |
| R11 | 07-30 | counter-audit | v3.1 + **E0** | ? | quantified | C  -  softened | E0, G2, reception gate | **E0 found every pre-emption 7 prior runs missed.** 0 DEFEATED / 2 NARROWED / 4 RECHARACTERIZED / 0 UNAFFECTED. Moved impact B→C. |
| R12 | 07-30 | claim extraction | + active field 4 | ? | quantified | n/a | field 4 active | Parenthetical failure gone. **But recorded millennial claim as MBH98 downstream inflation**  -  attribution error. |
| R13 | 07-30 | claim extraction | + attribution check | Grok-ish | quantified | n/a | ATTRIBUTED ELSEWHERE x6, scope arithmetic | Caught the "Mann et al. (1998, 1999)" conflation in a retrieved source. Recorded non-inflation for 2 items  -  first map-level acquittal behavior. |
| R14 | 07-30 | claim extraction | + attribution check | Sol | quantified | n/a | MISATTRIBUTED | Retrieved IPCC TAR sentence citing MBH98 for a millennial claim → MISATTRIBUTED. **Later reversed by R17 on fuller retrieval.** |
| R15 | 07-30 | claim extraction | + anchoring rule | Grok | quantified | n/a | anchoring rule, SUSPECTED | Correctly declined to assign MIXED: "no retrieved citing sentence found... therefore no established CITATION-layer failure location." **Fix working  -  previous run had anchored on RECALLED.** |
| R16 | 07-30 | claim extraction | + anchoring rule | Sol | quantified | n/a | CROSS-SOURCE-CONFIRMED x4 | **Reversed its own R14.** Retrieved NRC Ch.11 distinguishing the two papers' scopes → joint citation = synthesis attribution, not misattribution. |
| R17 | 07-30 | claim extraction | + joint-citation doc check | Claude | quantified | n/a | doc-level check, NONE FOUND (precise) | **GAP TYPE: neither apparent**  -  first map-level full acquittal. Retrieved MBH99 abstract + IPCC SPM figure attribution. |
| R18 | 07-30 | claim extraction | + joint-citation doc check | Sol | quantified | n/a | doc-level check | PAPER only, no established downstream. Retrieved the decisive IPCC Ch.2 sentence attributing to Mann et al. (1999). |
| R19 | 07-30 | claim extraction | + joint-citation doc check | Grok | quantified | n/a |  -  | **MIXED  -  diverged.** Labeled an unquoted pattern generalization as RETRIEVED, then anchored failure location on it. **Loophole: anchoring rule trusts a self-assigned label.** |

### Research branch — Shen et al. (2016)

| #   | Date    | Stage             | Prompt ver                        | Model    | Field 6                                            | Verdict                    | Checks that fired                                              | Notes |
| --- | ------- | ------------------ | ---------------------------------- | -------- | --------------------------------------------------- | --------------------------- | ---------------------------------------------------------------- | ----- |
| R20 | UNKNOWN | claim extraction   | 1-claim-extraction.txt             | UNKNOWN  | "no significant gender-based performance disparity" | n/a                          | overfit check, pre-registration                                  | Pre-registered expectations written before retrieval. One prediction FALSIFIED by retrieval: a same-author successor (Ratan, Shen & Williams 2020) exists, contra the assumption Shen had none -- reported honestly rather than quietly revised. |
| R21 | UNKNOWN | construct-validity | 2-construct-validity.txt           | UNKNOWN  | as above                                             | NARROWS                     | definition-operationalization check                              | Found advancement-speed-as-performance proxy gap; correctly narrowed rather than defeated -- advancement is a real but bounded dimension. |
| R22 | UNKNOWN | internal-validity   | 2-internal-validity.txt            | UNKNOWN  | as above                                             | **DEFEATS (IV-1)**          | first-ever run of this prompt                                    | **FIRST EVER RUN of 2-internal-validity.txt.** IV-1: Field 6's "no significant" wording directly contradicted by the source's own tables -- significant sex-interaction coefficients (p<.001) in both studies. Single most decisive finding in the chain. |
| R23 | UNKNOWN | citation-network    | 2-citation-network.txt             | UNKNOWN  | as above                                             | n/a                          | MISATTRIBUTED x3                                                  | Dong, Rogstad, Hébert-Ratté flagged MISATTRIBUTED. Same-author 2020 successor correctly classified as conceptual extension, not attribution repair -- overfit check unstrained. |
| R24 | UNKNOWN | counter-audit       | 3-counter-audit.txt (pre-CA-003)   | UNKNOWN  | as above                                             | (incomplete)                | G2, E0                                                            | **Discovered FAIL-CA-003.** Declared INPUTS omitted internal-validity despite the stage-role note naming it as one of three balanced prosecutors. IV-1 never reached this stage. |
| R25 | UNKNOWN | counter-audit rerun | 3-counter-audit.txt v3 (post-fix)  | UNKNOWN  | as above                                             | Category F -- Mixed          | G2, E0, internal-validity coverage line, operator leads 1-4       | CA-003 fix confirmed: coverage line "SUPPLIED AND CONSUMED"; verdict moved as direct consequence. Also ran with 4 operator-supplied leads. **Discovered FAIL-CA-004**: E0 initially credited an untested directional defense (CV-7) as RECHARACTERIZED; DIRECTIONALLY-CONTESTED disposition added and regression-confirmed (SHA-256 `2043a538...`). |

### Research branch — Galor & Özak (2016)

| #   | Date    | Stage               | Prompt ver                | Model   | Field 6                                                          | Verdict | Checks that fired                     | Notes |
| --- | ------- | -------------------- | --------------------------- | ------- | ------------------------------------------------------------------ | -------- | ---------------------------------------- | ----- |
| R26 | UNKNOWN | construct-validity   | 2-construct-validity.txt   | UNKNOWN | pre-industrial yield -> persistent long-term-orientation effect via cultural selection | DEFEATS (residual grade C) | construct-establishment (FORM/DOMAIN gap) | Degraded standalone mode -- no claim map supplied, self-generated and marked PROVISIONAL. Hofstede LTO found broader/orthogonal to the paper's own stated definition of time preference. |
| R27 | UNKNOWN | internal-validity -- CONTAMINATED | 2-internal-validity.txt (pre-IV-P1) | UNKNOWN | as above | **D** | none (gap this run exposed) | Construct-validity's output visible in ambient session context, not formally supplied. Coding-error allegation (PROVISIONAL) entered "DEFEATS finding(s)" directly. Paired with R28 to discover FAIL-IV-001/002. |
| R28 | UNKNOWN | internal-validity -- CLEAN | 2-internal-validity.txt (pre-IV-P1) | UNKNOWN | as above | **C** | none | Same underlying evidence as R27, construct-validity's output NOT present. Correctly declined to list the same allegation under DEFEATS. **R27 vs. R28 on identical evidence is the case behind FAIL-IV-001 and FAIL-IV-002.** |

### Research branch — Gabarrell-Pascuet et al. (2024)

| #   | Date    | Stage               | Prompt ver                | Model   | Field 6                                                     | Verdict                        | Checks that fired         | Notes |
| --- | ------- | -------------------- | --------------------------- | ------- | -------------------------------------------------------------- | -------------------------------- | ---------------------------- | ----- |
| R29 | UNKNOWN | claim extraction + construct-validity | 2-construct-validity.txt | Claude (this session) | reducing loneliness / depressive symptoms via online intervention | near-acquittal -- 4 properties ESTABLISHED, 1 N/A, 1 MINOR note | [P1], [P2] | First deliberate acquittal-direction attempt this session. Genuine differentiated result, not blanket praise. **Own retrieval failure on this run**: predicted operationalization COEXTENSIVE from dimensional correspondence alone, without checking item-level content -- same mechanism as FAIL-CV-004, committed by the auditor. |
| R30 | UNKNOWN | claim extraction + construct-validity, independent rerun | 2-construct-validity.txt | UNKNOWN (second model) | as above | USEFUL-FOR-NARROWER vs. INVALID (diverged) | Rule 2 claim selection (both models, same selection) | **Discovered FAIL-CV-005.** Same Field 6 claim, same selection rule, incompatible DEFEATS/NARROWS dispositions on a missing counterfactual -- an unsettled scope convention, not an evidential disagreement. Repair not yet written; status OPEN. |

### Research branch — ISIS-2 (1988), calibration audit

| #   | Date    | Stage               | Prompt ver                | Model   | Field 6                                                   | Verdict | Checks that fired | Notes |
| --- | ------- | -------------------- | --------------------------- | ------- | ------------------------------------------------------------ | -------- | -------------------- | ----- |
| R31 | UNKNOWN | construct-validity   | 2-construct-validity.txt (pre-source-preflight) | UNKNOWN | aspirin/streptokinase reduce vascular mortality in suspected acute MI | **A -- valid evidence** | none (gap this run exposed) | Deliberately chosen calibration target -- methodologically clean paper, direct mortality endpoint. Correctly differentiated acquittal. **Zero verification-state declarations anywhere in the output.** Independent check found 4 of 5 specific figures accurate; one discrepancy (combination odds reduction stated ~40%, actual reported 42% +/- 5). **Discovered FAIL-CV-008**: [P1]'s retrieval gate caps severity for convictions, has no equivalent for acquittals. |


### Media branch — Madison / Corey Ruiz and Ceuta

| # | Stage | Prompt ver | Models | Verdict | Notes |
|---|---|---|---|---|---|
| M1 | framing | pre-fix | Grok | substantially slanted | Flip test returned zero downgrades  -  **theater**. |
| M2 | framing | + costly flip test | ? | substantially slanted | Mirror written, 2 findings against it. But **inverted the mandated sentence** ("is functioning" for "may not be functioning"). Consistency check induced a bad downgrade (Type B misread as Type A). |
| M3 | framing | + Type A/B split, lever coherence | ChatGPT, Grok, Claude | subst. slanted x2, heavily constructed x1 | Divergence traced to **finding-splitting**  -  Claude counted 8, others 5. Fixed by counting levers. |
| M4 | framing | + F2 frame laundering | 4 models | 3x heavily constructed, 1 invalid | **Gemini audited a hallucinated article**  -  cited paragraphs not in the piece. Discarded. Strip test split PARTLY/COLLAPSES on a mixed paraphrase construction. |
| M5 | coverage-network | first run | ChatGPT, Grok, Claude |  -  | **Independence count converged ~4 across 3 unrelated samples.** Strongest metric the branch produces. Clustering answer varied by sample  -  correctly flagged as sample-dependent by all three. |
| M6 | coverage-network | + D2 | ChatGPT, Claude, Grok |  -  | **D2 falsified 2 upstream findings** on first use. Grok returned CONFIRMED with no primary source  -  led to the D2 evidence floor. |
| M7 | coverage-network | current (two-level count, E2 prior labels) | DeepSeek, Grok, Sol |  -  | Ceuta run 1, unassisted. **Independence count DIVERGED 2 / 3-4 / ~5** → FAIL-MB-008; the granular runs inverted the amplification ratio (~8/7 ~= 1.14) → FAIL-MB-009. 2/3 models self-generated a prior → GUARD-005; one model's auto-downgrade fired off its self-prior. [run-1 per-model detail from handoff; confirm against transcripts before committing.] |
| M8 | coverage-network | current | Grok, DeepSeek |  -  | Ceuta run 2, unassisted (different samples: Grok 7 pieces, DeepSeek 8). **Grok: L1=4, L2=5-6, ratio 1.3  -  inversion REPRODUCED**; printed "Level 2 usually LOWER" boilerplate directly above its L2 > L1 count; prose said "amplification, not independent confirmation" while the ratio read healthy. **DeepSeek: L1=3, L2=2, ratio 4:1  -  no inversion** (collapsed origins); CROSS-OUTLET cap fired correctly. Both declared prior NONE (no self-prior recurred → GUARD-005 working); both fired the automatic downgrade MODERATE→MINOR with no prior involved → FAIL-MB-005 tested. Confirms FAIL-MB-009 is real and reproduces, conditional on Level-2 granularity (= un-closed FAIL-MB-008). **D8 language discrimination split:** Grok filed the crossing verbs (pour/breach/cross) as "synonym, mild"  -  frame-carriers misread as cosmetic (FAIL-MB-010); DeepSeek captured them in the inventory but never ran D8 on them. Neither adjudicated the flood/breach frame. |

---

## WHAT THE LOG ALREADY SHOWS

1. **The claim map is the highest-leverage stage.** R3/R5 isolate it: same prompt, same
   paper, different field 6, verdict E vs. C. One sentence upstream decided whether a real
   defect was found.

2. **The concede test converts finding-severity into verdict-severity correctly.** R7
   (defect found, no concede test) → E. R8 (defect found, concede test) → C. Without it a
   single technical defect reads as a broken paper.

3. **Downstream stages do kill upstream findings**  -  4 documented. The pipeline corrects
   rather than accumulates.

4. **Retrieval depth drives most model divergence, not reasoning.** R17/R18 retrieved
   decisive sentences and converged. R19 generalized and diverged. Same prompt.

5. **Self-report is unreliable even under explicit instruction.** M2 inverted a sentence it
   was told to reproduce verbatim. M4's audit-integrity block claimed no banned phrase was
   used while the phrase appeared in the output.

6. **Every fix that mattered came from a run, not from reading the prompt.** The Ceuta rows
   add three more observed prompt defects or incomplete repairs: FAIL-MB-008, FAIL-MB-009,
   and FAIL-MB-010.

7. **The whole-story coverage-network independence metric is not yet a stable baseline.** On
   the same Ceuta event, run-2 produced an amplification ratio of 4:1 in DeepSeek and 1.3 in
   Grok. The divergence follows Level-2 granularity, not a substantive disagreement about
   the shared official dependence. Until FAIL-MB-008 and FAIL-MB-009 are closed, the metric
   is MODEL-DEPENDENT and may not anchor a verdict.

8. **A clean acquittal is not the same claim as a demonstrated-clean acquittal.** ISIS-2
   (R31) returned Verdict A correctly -- mortality is genuinely a direct, non-proxy endpoint
   -- but did so with zero verification-state declarations anywhere in the output, and
   independent checking found one of five specific figures inaccurate. [P1]'s retrieval gate
   caps severity for convictions resting on thin retrieval; nothing equivalent existed for
   acquittals, because an empty finding table was never designed to trigger the same
   discipline (FAIL-CV-008). The same asymmetry showed up independently when reviewing an
   external reproducibility tool (Rigor.me) days later -- "ran successfully" as an unqualified
   label, no visible distinction between genuine execution and confident narration filling a
   gap. Worth treating as a general pattern, not a one-off: an instrument that only audits its
   own confidence when it convicts will look more reliable than it is.
