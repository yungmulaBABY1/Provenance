# RESULTS  -  per-run behavior log

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
| Total runs logged | 39 | 23 research rows and 16 media rows |
| Distinct sources audited | 6 | MBH98, Donovan et al., Madison, Seattle, Ceuta, and the closed synthetic fixture |
| Runs returning "nothing of consequence" | 1 | claude-mhb-1, GAP TYPE "neither apparent" |
| Upstream findings killed downstream | 8 | see KILLS below |
| Checks that have never altered an outcome | see DORMANT | |

**OVERFIT WARNING:** 19 of 39 logged rows are one paper. MBH98 has a same-author successor, a famous controversy, and an assessment-report trail. The attribution apparatus remains heavily shaped by that case. Donovan et al. adds a second research target, while Madison, Seattle, Ceuta, and the closed fixture broaden the media branch. The next research targets should test whether the specialized fields and gates return cleanly empty outside those two paper families.

---

## KILLS  -  upstream findings killed by a downstream stage

The clearest evidence the pipeline works rather than accumulates.

| # | Finding | Killed by | How |
|---|---|---|---|
| 1 | "produced a knife" = minimizing verb choice | Coverage-network D2 | Primary source comparison  -  MPD written report says "pulled out," presser said "produced." Document dependence, not editorial choice. RECLASSIFIED. |
| 2 | Patterson foregrounded trauma framing (source-internal selection) | Coverage-network D2 | CNN reported he opened the presser that way. FALSIFIED outright. |
| 3 | Sourcing asymmetry in the Examiner brief | Genre gate (Section 0) | Format constraint  -  a 250-word breaking brief cannot carry balancing voices. Cut, not a finding. |
| 4 | Millennial claim = MBH98 downstream inflation | Claim-map attribution check, then joint-citation document check | Scope arithmetic -> MBH99. Then the document-level check kept it from swinging to false-positive MISATTRIBUTED. |
| 5 | Persistent "teen / 15-year-old" language = suspect softening | Full Language Package + update trajectory | Later coverage paired the age noun with strong agency, severe alleged conduct, ghost-gun details, first-degree assault, adult-transfer exposure, and the correct ballistic limitation. Noun-only finding killed / REFRAMED. |
| 6 | The detained teen carried the clearest role-update problem | Party enumeration + cross-party trajectory | The stronger persistence mismatch was relocated to the deceased suspected gunman remaining inside collective victim/memorial language after role differentiation. |
| 7 | New York Post BLM / occupation characterization had no evidentiary origin | Companion Retrieval + contextual-inference ladder | Expanded retrieval supplied BLM indicators, autonomous-zone self-labeling, access control, organizer participation, and governance evidence. Formal Antifa command remained unverified, so the finding was narrowed rather than simply reversed. |
| 8 | Scope-creep finding (MAJOR) - operationalization broader than Donovan's stated definition | NSF PAR instrument retrieval (R23) | Actual battery (PHGV/GARD/BGE) targets discreteness, uniformity, proportion, and strong genetic-causation claims - different items from the GESR-family set the finding assumed. The audit had inferred, not retrieved, the scale content. |

---

## DORMANT  -  checks that exist but have not yet changed an outcome

*Not evidence they are useless. Evidence they are untested.*

| Check | Runs where present | Times it changed something |
|---|---|---|
| Concede test (construct-validity) | 2 | 1  -  v3 run, E->C via NARROWS not DEFEATS |
| Concede test (citation-network) | 1 | 0 |
| Concede test (internal-validity) | 0 | n/a  -  prompt never run |
| Standardized finding table | 3 | 0  -  summary only, no verdict effect observed |
| MAP GAP / MAP DISAGREEMENT | 4 | 0  -  never fired |
| Automatic downgrade (media) | 6+ | both run-2 audits, all three fixed-packet runs, and at least one run-1 audit - all mechanical - FAIL-MB-005 |
| D2 cross-branch resolution | 1 | 2 kills (see above) |
| Reception gate | 2 | 1  -  McShane & Wyner capped CONTESTED |
| Adaptive Language-Package Triage | 0 | n/a - proposed after overproduction review; untested |

**MAP DISAGREEMENT at 0/4 is worth watching.** Either the maps were good, or the mechanism
is weak. One more run either way does not distinguish these.

---

## ACTIVE CHECKS - recently outcome-changing

| Check | Runs where present | Times it changed something |
|---|---:|---:|
| Companion Retrieval (media) | 2 | 2 - Madison verdict materially changed; Seattle recovered broader gang / city-response context |
| Label-Update Trajectory | 2 | 2 - Seattle false positive prevented; Madison same-stage divergence established |
| Full Language Package | 2 | 2 - Seattle noun-only finding killed; Madison agency/classification packages separated |
| Party Enumeration | 1 targeted follow-up | 1 - suspected perpetrator collectives added; police quotation-pair finding surfaced |
| Quotation-Pair Preservation | 1 targeted follow-up | 1 - "small groups" / "gang-related" contrast preserved |

## RUNS

### Research branch  -  MBH98

| # | Date | Stage | Prompt ver | Model | Field 6 | Verdict | Checks that fired | Notes |
|---|---|---|---|---|---|---|---|---|
| R1 | pre-session | construct | generic, pre-revision | Claude | none | C |  -  | Audited the controversy: centering, bristlecones, M&M, Wegman. Domain-concern field **model-populated**, not user-supplied. |
| R2 | pre-session | construct | tailored (climate), pre-revision | Claude | none | C |  -  | Added PSM, uncertainty budget, pseudoproxy, convergent validity, reproducibility. Same verdict. Engaged the paper's dendro robustness test  -  the only pre-revision run that did. |
| R3 | 07-30 | construct | revised + **hand-written map** | Claude | quantified 3 claim | **E** | claim map received, concede test | Found pointwise-vs-simultaneous defect. **Map was hand-written by Claude from full text  -  not a Stage 1 output.** |
| R4 | 07-30 | claim extraction | 1-claim-extraction v1 | ? | abstract claim + forcing bundled | n/a |  -  | **Field 6 wrong**: unquantified version, two claims bundled. |
| R5 | 07-30 | construct | revised + R4 cold map | ? | abstract claim | C | claim map received | Did NOT find the defect. 0 hits pointwise/simultaneous. **Confirms E came from the map, not the prosecutor.** |
| R6 | 07-30 | claim extraction | + field-6 rules | ? | quantified, one claim | n/a | RULE 1, RULE 2 | Both rules held. |
| R7 | 07-30 | construct | revised (no Block B/F) + R6 map | ? | quantified | **E** | claim map | Found the defect. But prompt lacked concede test  -  verdict overshot. |
| R8 | 07-30 | construct | **full v3** + cold map | ? | quantified | **C** | concede test, scope-loss, MAP DISAGREEMENT, finding table | Same defect, correctly scored NARROWS not DEFEATS. **Concede test is what makes E->C.** |
| R9 | 07-30 | citation-network | blocks applied | ? | quantified |  -  | concede test (J2) | **COMPLIANCE GAP**: prompt had Blocks A/B/E; output showed 0 claim-map receipt, 0 verification states, 0 finding table. Truncation or skipping  -  unresolved. |
| R10 | 07-30 | counter-audit | v3 (no E0) | ? | quantified | B  -  narrowed | G2, reception gate | G2 softened "fatal"/"invalid" -> "not demonstrated as unconditional." Reception gate capped McShane & Wyner CONTESTED. **Section E searched literature only  -  0 hits for the paper's own pre-emptions.** |
| R11 | 07-30 | counter-audit | v3.1 + **E0** | ? | quantified | C  -  softened | E0, G2, reception gate | **E0 found every pre-emption 7 prior runs missed.** 0 DEFEATED / 2 NARROWED / 4 RECHARACTERIZED / 0 UNAFFECTED. Moved impact B->C. |
| R12 | 07-30 | claim extraction | + active field 4 | ? | quantified | n/a | field 4 active | Parenthetical failure gone. **But recorded millennial claim as MBH98 downstream inflation**  -  attribution error. |
| R13 | 07-30 | claim extraction | + attribution check | Grok-ish | quantified | n/a | ATTRIBUTED ELSEWHERE x6, scope arithmetic | Caught the "Mann et al. (1998, 1999)" conflation in a retrieved source. Recorded non-inflation for 2 items  -  first map-level acquittal behavior. |
| R14 | 07-30 | claim extraction | + attribution check | Sol | quantified | n/a | MISATTRIBUTED | Retrieved IPCC TAR sentence citing MBH98 for a millennial claim -> MISATTRIBUTED. **Later reversed by R17 on fuller retrieval.** |
| R15 | 07-30 | claim extraction | + anchoring rule | Grok | quantified | n/a | anchoring rule, SUSPECTED | Correctly declined to assign MIXED: "no retrieved citing sentence found... therefore no established CITATION-layer failure location." **Fix working  -  previous run had anchored on RECALLED.** |
| R16 | 07-30 | claim extraction | + anchoring rule | Sol | quantified | n/a | CROSS-SOURCE-CONFIRMED x4 | **Reversed its own R14.** Retrieved NRC Ch.11 distinguishing the two papers' scopes -> joint citation = synthesis attribution, not misattribution. |
| R17 | 07-30 | claim extraction | + joint-citation doc check | Claude | quantified | n/a | doc-level check, NONE FOUND (precise) | **GAP TYPE: neither apparent**  -  first map-level full acquittal. Retrieved MBH99 abstract + IPCC SPM figure attribution. |
| R18 | 07-30 | claim extraction | + joint-citation doc check | Sol | quantified | n/a | doc-level check | PAPER only, no established downstream. Retrieved the decisive IPCC Ch.2 sentence attributing to Mann et al. (1999). |
| R19 | 07-30 | claim extraction | + joint-citation doc check | Grok | quantified | n/a |  -  | **MIXED  -  diverged.** Labeled an unquoted pattern generalization as RETRIEVED, then anchored failure location on it. **Loophole: anchoring rule trusts a self-assigned label.** |

### Research branch - Donovan et al. 2024 (construct-validity axis)

| # | Date | Stage | Prompt ver | Model | Field 6 | Verdict | Checks that fired | Notes |
|---|---|---|---|---|---|---|---|---|
| R20 | 08-01 | claim map + construct-validity | pre-revision (original) | unspecified / relayed | "Humane genomics education reduces unscientific genetic essentialism and thereby racism" | C | proxy leap (DEFEATS) | Baseline. Scope creep detected but filed as commentary - under-weighted. Triggered FAIL-CV-001. |
| R21 | 08-01 | claim map + construct-validity | + scope-creep own-row repair | unspecified / relayed | same | C/D hybrid | scope-creep own row; concede test NARROWS | Scope creep elevated to primary MAJOR. Operator follow-up triggered design of the construct-establishment check (FAIL-CV-002). |
| R22 | 08-02 | claim map + construct-validity | + construct-establishment check | unspecified / relayed | same | C/D hybrid | construct-establishment check; all five properties ASSERTED | **Over-fired.** Rated major/fatal off abstract-only retrieval while its own metadata admitted full text could overturn it. Triggered FAIL-CV-003. |
| R23 | 08-02 | manual retrieval check (not a prompt stage) | n/a - web verification | Claude | n/a | n/a | external verification, not a prompt mechanism | NSF PAR open-copy retrieval of predecessor-paper instruments (PHGV/GARD/BGE). Harm-in-effect and prevalence flipped ASSERTED -> ESTABLISHED-CITED. Scope-creep finding did not survive the actual instrument text. Triggered FAIL-CV-004. |

### Media branch - Madison / Corey Ruiz, Ceuta, and Seattle

| # | Stage | Prompt ver | Model(s) | Verdict / resolution | Checks that fired | Notes |
|---|---|---|---|---|---|---|
| M1 | framing | pre-fix | Grok | substantially slanted | flip test | Returned zero downgrades - the flip test was theater. |
| M2 | framing | + costly flip test | unspecified | substantially slanted | costly flip test; consistency check | Mirror written with two findings against it, but the mandated sentence was inverted and a Type B observation was wrongly downgraded. |
| M3 | framing | + Type A/B split; lever coherence | ChatGPT, Grok, Claude | substantially slanted x2; heavily constructed x1 | Type A/B split; lever coherence | Divergence traced to finding-splitting; fixed by counting capped levers rather than rows. |
| M4 | framing | + F2 frame laundering | 4 models | heavily constructed x3; one invalid run | F2; audit-integrity check; strip test | Gemini audited a hallucinated article and was discarded. The strip test split on a mixed paraphrase construction. |
| M5 | coverage-network | first run | ChatGPT, Grok, Claude | - | independence count; sample-dependence check | Independence count converged near four across three samples; clustering correctly varied with the sample. |
| M6 | coverage-network | + D2 | ChatGPT, Claude, Grok | - | D2 cross-branch resolution | D2 falsified two upstream findings. An unsupported CONFIRMED result led to the evidence floor. |
| M7 | coverage-network | own samples | DeepSeek, Grok, Sol | - | independence count; prior-source labels; automatic downgrade | Ceuta run 1. Independence count diverged 2 / 3-4 / about 5; granular runs inverted the ratio. Two of three models generated a prior. |
| M8 | coverage-network | own samples | Grok, DeepSeek | - | two-level count; corroboration cap; prior-source labels; automatic downgrade; D8 | Ceuta run 2. Grok inverted at 1.3 while DeepSeek returned 4:1 after collapsing origins. Confirms granularity dependence. |
| M9 | coverage-network | closed synthetic fixture | DeepSeek | - | two-level count; D7/D8 routing; prior-source labels; automatic downgrade | Fixed packet. L1=4, L2=3 and ratio 2.7:1 read amplified by an unstable convention. D8 missed the crossing-verb frame. |
| M10 | coverage-network | closed synthetic fixture | Grok | - | two-level count; D8; prior-source labels; automatic downgrade | Fixed packet. L1=4, L2=6 and ratio 1.3 read healthy. D8 misfiled the verbs as mostly synonym. |
| M11 | coverage-network | closed synthetic fixture | Sol | - | per-fact decomposition; D8; prior-source labels; automatic downgrade | Fixed packet. Whole-story ratio inverted, but per-fact rows recovered single-origin amplification and D8 correctly separated breach / cross. |
| M12 | coverage-network | expanded companion retrieval | ChatGPT | Post classification materially strengthened; formal Antifa control narrowed | companion retrieval; balanced hypothesis resolution; REFRAMED; context-supported inference | Bounded retrieval recovered adjacent political framing, organizer/video indicators, and event self-labeling. The original "no evidentiary origin" assessment was partly a packet artifact. |
| M13 | coverage-network | revised method, Seattle | ChatGPT | mixed: city communication failure confirmed; teen homicide implication narrowed; broad crime-policy omission only partial | companion retrieval; epistemic stages; role-label tracking; balanced hypotheses | The method supported criticism of Seattle command/communication while rejecting stronger unsupported causal claims. |
| M14 | coverage-network / language | + Label-Update Trajectory + Language Package | ChatGPT | age-softening hypothesis REFRAMED; actual persistence failure relocated to deceased suspected gunman | label trajectory; full package; update trigger; single-event limit | **False-positive prevention:** the age noun persisted, but later packages added strong agency, ghost-gun details, repeated firing, charges, and adult-transfer exposure. |
| M15 | language follow-up | + party enumeration + quotation-pair preservation | ChatGPT | same-stage abstraction finding added | party enumeration; paired quotation check; same-stage test | Preserved "small groups" / "two groups" beside "gang-related" from the same briefing. Timing could not explain the specificity difference. |
| M16 | coverage-network / language | Madison + Label-Update Trajectory + Language Package | ChatGPT | same-stage event-classification divergence confirmed | competing classifications; function-vs-structure; agency package; update timing | By July 27, substantially the same facts supported simultaneous labels including memorial, community hub, encampment, occupation, autonomous zone, and blockade. |

---

## WHAT THE LOG ALREADY SHOWS

1. **The claim map is the highest-leverage stage.** R3/R5 isolate it: same prompt, same
   paper, different field 6, verdict E vs. C. One sentence upstream decided whether a real
   defect was found.

2. **The concede test converts finding-severity into verdict-severity correctly.** R7
   (defect found, no concede test) -> E. R8 (defect found, concede test) -> C. Without it a
   single technical defect reads as a broken paper.

3. **Downstream stages do kill upstream findings**  -  8 documented. The pipeline corrects
   rather than accumulates.

4. **Retrieval depth drives most model divergence, not reasoning.** R17/R18 retrieved
   decisive sentences and converged. R19 generalized and diverged. Same prompt.

5. **Self-report is unreliable even under explicit instruction.** M2 inverted a sentence it
   was told to reproduce verbatim. M4's audit-integrity block claimed no banned phrase was
   used while the phrase appeared in the output.

6. **Live runs remain the primary source of substantive repairs, but structural review also
   catches architecture drift.** The Ceuta runs exposed FAIL-MB-008 through 010; the later
   cross-prompt review found vocabulary and ownership seams that the MEDIA-P1 harmonization
   repaired without pretending they were additional live-run failures.

7. **The whole-story coverage-network independence metric was model-dependent on identical
   input.** The fixed packet produced Level 2 counts of 3, 6, and 12-14 and flipped the
   amplification verdict from amplified (DeepSeek) to healthy (Grok) to very healthy (Sol).
   Only Sol's per-fact decomposition recovered the stable result: the load-bearing facts
   were single-origin and amplified. The Section B rewrite removes the whole-story ratio
   from verdict duty and makes per-fact origin counts mandatory; retest pending.

8. **Companion retrieval can reverse an evidentiary assessment without lowering
   the standard.** Madison moved from "no evidentiary origin" to strong BLM /
   occupation support because the relevant material was outside the literal
   packet, while formal Antifa command still failed.

9. **The correct unit for language analysis is the package over time, not the
   noun.** Seattle's persistent age label looked soft alone and mixed-to-hard
   once agency, conduct, charges, attribution, and ballistic updates were coded.

10. **Party enumeration is not clerical.** The police-language finding did not
    appear until suspected perpetrator collectives became an explicit party and
    the paired descriptions were preserved.

11. **Same-stage divergence is distinct from update failure.** Madison's event
    labels and Seattle's "small groups" / "gang-related" language diverged under
    substantially the same evidentiary conditions; timing could not explain them.

12. **A module can be substantively useful and still be too verbose.** The full
    language-package schema prevented a false positive but over-produced
    uncontested party descriptions, motivating conditional deep-dive triage.
