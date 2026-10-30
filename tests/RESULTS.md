# RESULTS  -  per-run behavior log

The CHANGELOG records **fixes**: what broke and what closed it. This records **behavior**:
which checks fired, what they changed, what got killed.

After enough runs this answers questions no single run can:

- Which checks have never once altered a verdict? (length without function)
- Which fire on every run? (probably miscalibrated)
- How often does a downstream stage kill an upstream finding? (the pipeline working)
- Does the instrument ever return “nothing of consequence”? (can it acquit)

**One row per run.** Add as you go. Do not backfill from memory  -  if a run’s detail is not
recorded, mark it UNKNOWN rather than reconstructing it.

## Atlas software validation — separate from research audit runs

The first deterministic adapter slice is recorded in
[atlas/validation.json](atlas/validation.json), with pre-implementation expectations
in [atlas/EXPECTED.txt](atlas/EXPECTED.txt). These checks import existing archived
outputs and mutate software fixtures; they do not execute a new model audit or
change the research/media run tallies below. See
[the implementation scope](../docs/atlas/README.md) for source-access and review limits.

---

## SUMMARY TALLIES

*Update when adding runs. These are the numbers that matter.*

|Metric                                   |Count      |Notes                                                                           |
|-----------------------------------------|-----------|--------------------------------------------------------------------------------|
|Total runs logged                        |54         |35 research rows and 19 media rows                                              |
|Distinct sources audited                 |10         |MBH98, Donovan et al., Gabarrell-Pascuet et al., Shen et al., Galor & Özak, ISIS-2, Madison, Seattle, Ceuta, and the closed synthetic fixture|
|Runs returning “nothing of consequence”  |2          |claude-mhb-1, GAP TYPE “neither apparent”; ISIS-2 construct-validity calibration, Verdict A|
|Upstream findings killed downstream      |10         |see KILLS below                                                                 |
|Checks that have never altered an outcome|see DORMANT|                                                                                |

**OVERFIT WARNING, UPDATED:** 19 of 54 logged rows remain one paper. MBH98 has a same-author successor, a famous controversy, and an assessment-report trail, so the attribution apparatus remains heavily shaped by that case. Research coverage now also includes Donovan et al., Gabarrell-Pascuet et al., Shen et al., Galor & Özak, and ISIS-2 across genomics education, psychology, game studies, economics, and cardiology. The media branch includes Madison, Seattle, Ceuta, and the closed synthetic fixture. Source breadth is materially better; run concentration and the number of genuinely clean calibration targets remain the live overfit risks. Internal-validity and citation-network still have thin cross-target coverage: their few executions remain concentrated in MBH98/Shen/Galor-Özak territory, which is worth watching as those checks see more use.

---

## KILLS  -  upstream findings killed by a downstream stage

The clearest evidence the pipeline works rather than accumulates.

|#|Finding                                                                                  |Killed by                                                      |How                                                                                                                                                                                                                                             |
|-|-----------------------------------------------------------------------------------------|---------------------------------------------------------------|------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
|1|“produced a knife” = minimizing verb choice                                              |Coverage-network D2                                            |Primary source comparison  -  MPD written report says “pulled out,” presser said “produced.” Document dependence, not editorial choice. RECLASSIFIED.                                                                                           |
|2|Patterson foregrounded trauma framing (source-internal selection)                        |Coverage-network D2                                            |CNN reported he opened the presser that way. FALSIFIED outright.                                                                                                                                                                                |
|3|Sourcing asymmetry in the Examiner brief                                                 |Genre gate (Section 0)                                         |Format constraint  -  a 250-word breaking brief cannot carry balancing voices. Cut, not a finding.                                                                                                                                              |
|4|Millennial claim = MBH98 downstream inflation                                            |Claim-map attribution check, then joint-citation document check|Scope arithmetic -> MBH99. Then the document-level check kept it from swinging to false-positive MISATTRIBUTED.                                                                                                                                 |
|5|Persistent “teen / 15-year-old” language = suspect softening                             |Full Language Package + update trajectory                      |Later coverage paired the age noun with strong agency, severe alleged conduct, ghost-gun details, first-degree assault, adult-transfer exposure, and the correct ballistic limitation. Noun-only finding killed / REFRAMED.                     |
|6|The detained teen carried the clearest role-update problem                               |Party enumeration + cross-party trajectory                     |The stronger persistence mismatch was relocated to the deceased suspected gunman remaining inside collective victim/memorial language after role differentiation.                                                                               |
|7|New York Post BLM / occupation characterization had no evidentiary origin                |Companion Retrieval + contextual-inference ladder              |Expanded retrieval supplied BLM indicators, autonomous-zone self-labeling, access control, organizer participation, and governance evidence. Formal Antifa command remained unverified, so the finding was narrowed rather than simply reversed.|
|8|Scope-creep finding (MAJOR) - operationalization broader than Donovan’s stated definition|NSF PAR instrument retrieval (R23)                             |Actual battery (PHGV/GARD/BGE) targets discreteness, uniformity, proportion, and strong genetic-causation claims - different items from the GESR-family set the finding assumed. The audit had inferred, not retrieved, the scale content.      |
|9|Auditor prediction that the operationalization was COEXTENSIVE|Item retrieval (Sol run, R24)|The pre-run oracle reasoned that dimensional correspondence (Weiss two-factor definition ↔ DJGLS two-subscale instrument) settled the def-op question without needing item wordings. Retrieved items show 5 of 6 emotional-subscale items exceed the stated definition. Same mechanism as FAIL-CV-004, committed by the auditor rather than the audit.|
|10|Construct-validity's NARROWS finding as the load-bearing account of Shen Field 6|Internal-validity IV-1, once consumed by counter-audit|IV-1 found that the paper's own tables contained significant sex-interaction coefficients despite Field 6's “no significant” wording. The construct-validity finding survives as a narrower proxy critique, but it ceased to be the decisive lever.|

Do not increment KILLS for FAIL-MB-018 merely because a finding present in an
older prompt version disappears under the repaired instrument. The KILLS table
tracks within-run pipeline correction; the FAIL-MB-018 change is a
revision/regression comparison and is recorded in M19 instead.

---

## DORMANT  -  checks that exist but have not yet changed an outcome

*Not evidence they are useless. Evidence they are untested.*

|Check                            |Runs where present|Times it changed something                                                                                                                        |
|---------------------------------|------------------|--------------------------------------------------------------------------------------------------------------------------------------------------|
|Concede test (construct-validity)|2                 |1  -  v3 run, E->C via NARROWS not DEFEATS                                                                                                        |
|Concede test (citation-network)  |1                 |0                                                                                                                                                 |
|Concede test (internal-validity) |4                 |3  -  Shen's IV-1 defeated Field 6 directly; the Galor-Özak contaminated/clean pair changed the letter grade (D vs. C) on identical evidence depending on context, exposing FAIL-IV-001|
|Standardized finding table       |3                 |0  -  summary only, no verdict effect observed                                                                                                    |
|MAP GAP / MAP DISAGREEMENT       |5                 |1  -  Shen: internal-validity found a paper-layer failure within advancement itself that the claim map had not anticipated                        |
|Automatic downgrade (media)      |7+                |both run-2 audits, all three original fixed-packet runs, at least one run-1 audit, and the integrated 017/018 rerun — all mechanical — FAIL-MB-005|
|D2 cross-branch resolution       |1                 |2 kills (see above)                                                                                                                               |
|Reception gate                   |2                 |1  -  McShane & Wyner capped CONTESTED                                                                                                            |
|Adaptive Language-Package Triage |0                 |n/a - proposed after overproduction review; untested                                                                                              |

**MAP DISAGREEMENT has now fired once in 5 runs.** Shen shows the mechanism can
recover a paper-layer failure the claim map did not anticipate. More targets are
still needed to distinguish useful selectivity from target-specific luck.

---

## ACTIVE CHECKS - recently outcome-changing

|Check                                |Runs where present           |Times it changed something                                                                                                                                  |
|-------------------------------------|----------------------------:|-----------------------------------------------------------------------------------------------------------------------------------------------------------:|
|Companion Retrieval (media)          |2                            |2 - Madison verdict materially changed; Seattle recovered broader gang / city-response context                                                              |
|Label-Update Trajectory              |2                            |2 - Seattle false positive prevented; Madison same-stage divergence established                                                                             |
|Full Language Package                |2                            |2 - Seattle noun-only finding killed; Madison agency/classification packages separated                                                                      |
|Party Enumeration                    |1 targeted follow-up         |1 - suspected perpetrator collectives added; police quotation-pair finding surfaced                                                                         |
|Quotation-Pair Preservation          |1 targeted follow-up         |1 - “small groups” / “gang-related” contrast preserved                                                                                                      |
|Proposition-Level Source Independence|3 recent Ceuta runs          |3 — kept whole-coverage Level 2 descriptive and moved amplification/corroboration judgment to per-fact origin structure despite continued granularity spread|
|Prominence / Packaging               |1 integrated regression rerun|1 — restored the older gross-scale vs return/aftermath finding that Revised/RC2 had silently lost                                                           |
|Semantic Equivalence / Earnedness    |1 integrated regression rerun|1 — removed the wording-only event-language finding and prevented one unnecessary full language-package expansion                                           |

Adaptive Language-Package Triage remains UNTESTED. The reduction from three full
language-package expansions to two in M19 is caused by FAIL-MB-018’s upstream
semantic gate, not by FAIL-MB-016.

## RUNS

### Research branch  -  MBH98

|#  |Date       |Stage           |Prompt ver                      |Model   |Field 6                         |Verdict       |Checks that fired                                        |Notes                                                                                                                                                                                                     |
|---|-----------|----------------|--------------------------------|--------|--------------------------------|--------------|---------------------------------------------------------|----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
|R1 |pre-session|construct       |generic, pre-revision           |Claude  |none                            |C             |-                                                        |Audited the controversy: centering, bristlecones, M&M, Wegman. Domain-concern field **model-populated**, not user-supplied.                                                                               |
|R2 |pre-session|construct       |tailored (climate), pre-revision|Claude  |none                            |C             |-                                                        |Added PSM, uncertainty budget, pseudoproxy, convergent validity, reproducibility. Same verdict. Engaged the paper’s dendro robustness test  -  the only pre-revision run that did.                        |
|R3 |07-30      |construct       |revised + **hand-written map**  |Claude  |quantified 3 claim              |**E**         |claim map received, concede test                         |Found pointwise-vs-simultaneous defect. **Map was hand-written by Claude from full text  -  not a Stage 1 output.**                                                                                       |
|R4 |07-30      |claim extraction|1-claim-extraction v1           |?       |abstract claim + forcing bundled|n/a           |-                                                        |**Field 6 wrong**: unquantified version, two claims bundled.                                                                                                                                              |
|R5 |07-30      |construct       |revised + R4 cold map           |?       |abstract claim                  |C             |claim map received                                       |Did NOT find the defect. 0 hits pointwise/simultaneous. **Confirms E came from the map, not the prosecutor.**                                                                                             |
|R6 |07-30      |claim extraction|+ field-6 rules                 |?       |quantified, one claim           |n/a           |RULE 1, RULE 2                                           |Both rules held.                                                                                                                                                                                          |
|R7 |07-30      |construct       |revised (no Block B/F) + R6 map |?       |quantified                      |**E**         |claim map                                                |Found the defect. But prompt lacked concede test  -  verdict overshot.                                                                                                                                    |
|R8 |07-30      |construct       |**full v3** + cold map          |?       |quantified                      |**C**         |concede test, scope-loss, MAP DISAGREEMENT, finding table|Same defect, correctly scored NARROWS not DEFEATS. **Concede test is what makes E->C.**                                                                                                                   |
|R9 |07-30      |citation-network|blocks applied                  |?       |quantified                      |-             |concede test (J2)                                        |**COMPLIANCE GAP**: prompt had Blocks A/B/E; output showed 0 claim-map receipt, 0 verification states, 0 finding table. Truncation or skipping  -  unresolved.                                            |
|R10|07-30      |counter-audit   |v3 (no E0)                      |?       |quantified                      |B  -  narrowed|G2, reception gate                                       |G2 softened “fatal”/“invalid” -> “not demonstrated as unconditional.” Reception gate capped McShane & Wyner CONTESTED. **Section E searched literature only  -  0 hits for the paper’s own pre-emptions.**|
|R11|07-30      |counter-audit   |v3.1 + **E0**                   |?       |quantified                      |C  -  softened|E0, G2, reception gate                                   |**E0 found every pre-emption 7 prior runs missed.** 0 DEFEATED / 2 NARROWED / 4 RECHARACTERIZED / 0 UNAFFECTED. Moved impact B->C.                                                                        |
|R12|07-30      |claim extraction|+ active field 4                |?       |quantified                      |n/a           |field 4 active                                           |Parenthetical failure gone. **But recorded millennial claim as MBH98 downstream inflation**  -  attribution error.                                                                                        |
|R13|07-30      |claim extraction|+ attribution check             |Grok-ish|quantified                      |n/a           |ATTRIBUTED ELSEWHERE x6, scope arithmetic                |Caught the “Mann et al. (1998, 1999)” conflation in a retrieved source. Recorded non-inflation for 2 items  -  first map-level acquittal behavior.                                                        |
|R14|07-30      |claim extraction|+ attribution check             |Sol     |quantified                      |n/a           |MISATTRIBUTED                                            |Retrieved IPCC TAR sentence citing MBH98 for a millennial claim -> MISATTRIBUTED. **Later reversed by R17 on fuller retrieval.**                                                                          |
|R15|07-30      |claim extraction|+ anchoring rule                |Grok    |quantified                      |n/a           |anchoring rule, SUSPECTED                                |Correctly declined to assign MIXED: “no retrieved citing sentence found… therefore no established CITATION-layer failure location.” **Fix working  -  previous run had anchored on RECALLED.**            |
|R16|07-30      |claim extraction|+ anchoring rule                |Sol     |quantified                      |n/a           |CROSS-SOURCE-CONFIRMED x4                                |**Reversed its own R14.** Retrieved NRC Ch.11 distinguishing the two papers’ scopes -> joint citation = synthesis attribution, not misattribution.                                                        |
|R17|07-30      |claim extraction|+ joint-citation doc check      |Claude  |quantified                      |n/a           |doc-level check, NONE FOUND (precise)                    |**GAP TYPE: neither apparent**  -  first map-level full acquittal. Retrieved MBH99 abstract + IPCC SPM figure attribution.                                                                                |
|R18|07-30      |claim extraction|+ joint-citation doc check      |Sol     |quantified                      |n/a           |doc-level check                                          |PAPER only, no established downstream. Retrieved the decisive IPCC Ch.2 sentence attributing to Mann et al. (1999).                                                                                       |
|R19|07-30      |claim extraction|+ joint-citation doc check      |Grok    |quantified                      |n/a           |-                                                        |**MIXED  -  diverged.** Labeled an unquoted pattern generalization as RETRIEVED, then anchored failure location on it. **Loophole: anchoring rule trusts a self-assigned label.**                         |

### Research branch - Donovan et al. 2024 (construct-validity axis)

|#  |Date |Stage                                      |Prompt ver                     |Model                |Field 6                                                                                 |Verdict   |Checks that fired                                          |Notes                                                                                                                                                                                                                                    |
|---|-----|-------------------------------------------|-------------------------------|---------------------|----------------------------------------------------------------------------------------|----------|-----------------------------------------------------------|-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
|R20|08-01|claim map + construct-validity             |pre-revision (original)        |unspecified / relayed|“Humane genomics education reduces unscientific genetic essentialism and thereby racism”|C         |proxy leap (DEFEATS)                                       |Baseline. Scope creep detected but filed as commentary - under-weighted. Triggered FAIL-CV-001.                                                                                                                                          |
|R21|08-01|claim map + construct-validity             |+ scope-creep own-row repair   |unspecified / relayed|same                                                                                    |C/D hybrid|scope-creep own row; concede test NARROWS                  |Scope creep elevated to primary MAJOR. Operator follow-up triggered design of the construct-establishment check (FAIL-CV-002).                                                                                                           |
|R22|08-02|claim map + construct-validity             |+ construct-establishment check|unspecified / relayed|same                                                                                    |C/D hybrid|construct-establishment check; all five properties ASSERTED|**Over-fired.** Rated major/fatal off abstract-only retrieval while its own metadata admitted full text could overturn it. Triggered FAIL-CV-003.                                                                                        |
|R23|08-02|manual retrieval check (not a prompt stage)|n/a - web verification         |Claude               |n/a                                                                                     |n/a       |external verification, not a prompt mechanism              |NSF PAR open-copy retrieval of predecessor-paper instruments (PHGV/GARD/BGE). Harm-in-effect and prevalence flipped ASSERTED -> ESTABLISHED-CITED. Scope-creep finding did not survive the actual instrument text. Triggered FAIL-CV-004.|

### Research branch - Gabarrell-Pascuet et al. 2024 (loneliness)

|#|Date|Stage|Prompt ver|Model|Field 6|Verdict|Checks that fired|Notes|
|---|---|---|---|---|---|---|---|---|
|R24|08-08|claim map + construct-validity|commit 955c1d9|Sol|Quantified temporal claim: emotional loneliness -0.84 on 0-6 (2.62→1.78, p<0.01)|USEFUL-FOR-NARROWER; no DEFEATS; residual C|def-op ITEMS-RETRIEVED → **broader** (scope creep); proxy (content/keying confound); omitted confound; ignored adjacent literature; citation laundering ×2 (CROSS-SOURCE-CONFIRMED)|Retrieved all 11 DJGLS items + Spanish psychometrics (Tomás 2017) + 2026 Czech replication. Found 5 of 6 “emotional” items exceed the paper's attachment/intimacy definition, AND that the emotional facet is perfectly confounded with negative keying. Declined to double-count Findings 1–2 as independent levers.|
|R25|08-08|claim map + construct-validity|commit 955c1d9 (TRUNCATED — see TOOL-005)|Claude|same claim, same Rule 2 selection|INVALID as causal claim; residual C; 1 DEFEATS + 2 material narrowings|DEFEATS on absent counterfactual; F4 power-vs-outcome finding|Sharpest finding was F4: sample size powered for ≥1.7-unit difference (SD 2.33, consistent with the 0–11 global score); the reported significant result is 0.84 on the 0–6 emotional subscale, one of seven outcome families, no multiplicity adjustment, no pre-specified primary endpoint. Construct-establishment returned mostly UNKNOWN — citations read as citations, not fetched (honest per [P1]). **Discovered FAIL-CV-005:** the two models selected the same Field 6 claim under the same rule but assigned incompatible DEFEATS/NARROWS dispositions to a missing counterfactual—an unsettled scope convention, not an evidential disagreement.|

### Research branch - Shen et al. 2016

|#|Date|Stage|Prompt ver|Model|Field 6|Verdict|Checks that fired|Notes|
|---|---|---|---|---|---|---|---|---|
|R26|UNKNOWN|claim extraction|1-claim-extraction.txt|UNKNOWN|“no significant gender-based performance disparity”|n/a|overfit check; preregistration|Expectations were preregistered before retrieval. One prediction was FALSIFIED: a same-author successor, Ratan, Shen & Williams 2020, existed contrary to the preregistered assumption and was reported rather than silently revised.|
|R27|UNKNOWN|construct-validity|2-construct-validity.txt|UNKNOWN|same|NARROWS|definition-operationalization check|Found advancement-speed-as-performance proxy gap; correctly narrowed rather than defeated because advancement remains a real but bounded performance dimension.|
|R28|UNKNOWN|internal-validity|2-internal-validity.txt|UNKNOWN|same|**DEFEATS (IV-1)**|first-ever run of this prompt; MAP GAP|IV-1 found that Field 6's “no significant” wording was contradicted by significant sex-interaction coefficients (p<.001) in both studies. The output correctly hedged that clustering is not independence and power to reject is not equivalence. This was the chain's most decisive finding.|
|R29|UNKNOWN|citation-network|2-citation-network.txt|UNKNOWN|same|n/a|MISATTRIBUTED ×3|Dong, Rogstad, and Hébert-Ratté were flagged MISATTRIBUTED. The 2020 same-author successor was correctly classified as conceptual extension, not attribution repair; the MBH98-shaped attribution check returned non-empty but unstrained results.|
|R30|UNKNOWN|counter-audit|3-counter-audit.txt (pre-CA-003)|UNKNOWN|same|(incomplete)|G2; E0|**Discovered FAIL-CA-003.** Declared inputs omitted internal-validity despite the stage-role note naming it as one of the three prosecutors. IV-1 never reached the counter-audit.|
|R31|UNKNOWN|counter-audit rerun|3-counter-audit.txt v3 (post-fix)|UNKNOWN|same|Category F — Mixed|G2; E0; internal-validity coverage line; operator leads 1–4|CA-003 fix confirmed: “SUPPLIED AND CONSUMED — IV-1 through IV-5”; the verdict moved as a direct consequence. Four operator-supplied leads were included: power-leveling, AFK time, activity-composition/Simpson's-paradox structure, and citation-network, the last unexercised by design. **Discovered FAIL-CA-004:** E0 initially credited an untested directional defense as RECHARACTERIZED; DIRECTIONALLY-CONTESTED was added and regression-confirmed on a second rerun (recorded SHA-256 prefix `2043a538...`).|

### Research branch - Galor & Özak 2016

|#|Date|Stage|Prompt ver|Model|Field 6|Verdict|Checks that fired|Notes|
|---|---|---|---|---|---|---|---|---|
|R32|UNKNOWN|construct-validity|2-construct-validity.txt|UNKNOWN|pre-industrial yield → persistent long-term-orientation effect via cultural selection|DEFEATS (residual grade C)|construct-establishment (FORM/DOMAIN gap)|Ran in degraded standalone mode: no claim map was supplied, so the self-generated map was marked PROVISIONAL and cross-stage alignment remained unresolved. Hofstede LTO was found broader or orthogonal to the paper's stated definition of time preference.|
|R33|UNKNOWN|internal-validity — CONTAMINATED|2-internal-validity.txt (pre-IV-P1)|UNKNOWN|same|**D**|none — gap exposed by this run|Construct-validity output was visible in ambient context but not formally supplied. A PROVISIONAL/RECEPTION-CONFIRMED-only coding-error allegation entered “DEFEATS finding(s).” Paired with R34 to discover FAIL-IV-001 and FAIL-IV-002.|
|R34|UNKNOWN|internal-validity — CLEAN|2-internal-validity.txt (pre-IV-P1)|UNKNOWN|same|**C**|none|Same underlying evidence as R33, but construct-validity output was absent. The run correctly declined to place the same allegation under DEFEATS. R33 vs. R34 is the real A/B control behind FAIL-IV-001/002, not a discrepancy to reconcile.|

### Research branch - ISIS-2 1988 calibration audit

|#|Date|Stage|Prompt ver|Model|Field 6|Verdict|Checks that fired|Notes|
|---|---|---|---|---|---|---|---|---|
|R35|UNKNOWN|construct-validity|2-construct-validity.txt (pre-source-preflight)|UNKNOWN|aspirin/streptokinase reduce vascular mortality in suspected acute MI|**A — valid evidence**|none — gap exposed by this run|Deliberately clean calibration target: direct mortality endpoint and no genuine proxy problem. NSTEMI downstream inflation was flagged and the 10-year follow-up was scoped as UK-only after year 5. **Zero verification-state declarations appeared anywhere in the output.** Independent checking found 4 of 5 quoted figures exact; the stated combination effect of “~40%” was compatible with rounding the reported 42% ± 5, but the output did not disclose whether it was retrieved or recalled. **Discovered FAIL-CV-008:** the existing retrieval gate constrained convictions but not acquittals.|

### Media branch - Madison / Corey Ruiz, Ceuta, and Seattle

|#  |Stage                      |Prompt ver                                          |Model(s)             |Verdict / resolution                                                                                                                                 |Checks that fired                                                                                                                                                                |Notes                                                                                                                                                                                                                                                                                                                                                                                                                   |
|---|---------------------------|----------------------------------------------------|---------------------|-----------------------------------------------------------------------------------------------------------------------------------------------------|---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
|M1 |framing                    |pre-fix                                             |Grok                 |substantially slanted                                                                                                                                |flip test                                                                                                                                                                        |Returned zero downgrades - the flip test was theater.                                                                                                                                                                                                                                                                                                                                                                   |
|M2 |framing                    |+ costly flip test                                  |unspecified          |substantially slanted                                                                                                                                |costly flip test; consistency check                                                                                                                                              |Mirror written with two findings against it, but the mandated sentence was inverted and a Type B observation was wrongly downgraded.                                                                                                                                                                                                                                                                                    |
|M3 |framing                    |+ Type A/B split; lever coherence                   |ChatGPT, Grok, Claude|substantially slanted x2; heavily constructed x1                                                                                                     |Type A/B split; lever coherence                                                                                                                                                  |Divergence traced to finding-splitting; fixed by counting capped levers rather than rows.                                                                                                                                                                                                                                                                                                                               |
|M4 |framing                    |+ F2 frame laundering                               |4 models             |heavily constructed x3; one invalid run                                                                                                              |F2; audit-integrity check; strip test                                                                                                                                            |Gemini audited a hallucinated article and was discarded. The strip test split on a mixed paraphrase construction.                                                                                                                                                                                                                                                                                                       |
|M5 |coverage-network           |first run                                           |ChatGPT, Grok, Claude|-                                                                                                                                                    |independence count; sample-dependence check                                                                                                                                      |Independence count converged near four across three samples; clustering correctly varied with the sample.                                                                                                                                                                                                                                                                                                               |
|M6 |coverage-network           |+ D2                                                |ChatGPT, Claude, Grok|-                                                                                                                                                    |D2 cross-branch resolution                                                                                                                                                       |D2 falsified two upstream findings. An unsupported CONFIRMED result led to the evidence floor.                                                                                                                                                                                                                                                                                                                          |
|M7 |coverage-network           |own samples                                         |DeepSeek, Grok, Sol  |-                                                                                                                                                    |independence count; prior-source labels; automatic downgrade                                                                                                                     |Ceuta run 1. Independence count diverged 2 / 3-4 / about 5; granular runs inverted the ratio. Two of three models generated a prior.                                                                                                                                                                                                                                                                                    |
|M8 |coverage-network           |own samples                                         |Grok, DeepSeek       |-                                                                                                                                                    |two-level count; corroboration cap; prior-source labels; automatic downgrade; D8                                                                                                 |Ceuta run 2. Grok inverted at 1.3 while DeepSeek returned 4:1 after collapsing origins. Confirms granularity dependence.                                                                                                                                                                                                                                                                                                |
|M9 |coverage-network           |closed synthetic fixture                            |DeepSeek             |-                                                                                                                                                    |two-level count; D7/D8 routing; prior-source labels; automatic downgrade                                                                                                         |Fixed packet. L1=4, L2=3 and ratio 2.7:1 read amplified by an unstable convention. D8 missed the crossing-verb frame.                                                                                                                                                                                                                                                                                                   |
|M10|coverage-network           |closed synthetic fixture                            |Grok                 |-                                                                                                                                                    |two-level count; D8; prior-source labels; automatic downgrade                                                                                                                    |Fixed packet. L1=4, L2=6 and ratio 1.3 read healthy. D8 misfiled the verbs as mostly synonym.                                                                                                                                                                                                                                                                                                                           |
|M11|coverage-network           |closed synthetic fixture                            |Sol                  |-                                                                                                                                                    |per-fact decomposition; D8; prior-source labels; automatic downgrade                                                                                                             |Fixed packet. Whole-story ratio inverted, but per-fact rows recovered single-origin amplification and D8 correctly separated breach / cross.                                                                                                                                                                                                                                                                            |
|M12|coverage-network           |expanded companion retrieval                        |ChatGPT              |Post classification materially strengthened; formal Antifa control narrowed                                                                          |companion retrieval; balanced hypothesis resolution; REFRAMED; context-supported inference                                                                                       |Bounded retrieval recovered adjacent political framing, organizer/video indicators, and event self-labeling. The original “no evidentiary origin” assessment was partly a packet artifact.                                                                                                                                                                                                                              |
|M13|coverage-network           |revised method, Seattle                             |ChatGPT              |mixed: city communication failure confirmed; teen homicide implication narrowed; broad crime-policy omission only partial                            |companion retrieval; epistemic stages; role-label tracking; balanced hypotheses                                                                                                  |The method supported criticism of Seattle command/communication while rejecting stronger unsupported causal claims.                                                                                                                                                                                                                                                                                                     |
|M14|coverage-network / language|+ Label-Update Trajectory + Language Package        |ChatGPT              |age-softening hypothesis REFRAMED; actual persistence failure relocated to deceased suspected gunman                                                 |label trajectory; full package; update trigger; single-event limit                                                                                                               |**False-positive prevention:** the age noun persisted, but later packages added strong agency, ghost-gun details, repeated firing, charges, and adult-transfer exposure.                                                                                                                                                                                                                                                |
|M15|language follow-up         |+ party enumeration + quotation-pair preservation   |ChatGPT              |same-stage abstraction finding added                                                                                                                 |party enumeration; paired quotation check; same-stage test                                                                                                                       |Preserved “small groups” / “two groups” beside “gang-related” from the same briefing. Timing could not explain the specificity difference.                                                                                                                                                                                                                                                                              |
|M16|coverage-network / language|Madison + Label-Update Trajectory + Language Package|ChatGPT              |same-stage event-classification divergence confirmed                                                                                                 |competing classifications; function-vs-structure; agency package; update timing                                                                                                  |By July 27, substantially the same facts supported simultaneous labels including memorial, community hub, encampment, occupation, autonomous zone, and blockade.                                                                                                                                                                                                                                                        |
|M17|coverage-network           |revised Ceuta prompt / per-fact source-chain rewrite|ChatGPT              |10 standardized findings; proposition-level source judgments stable; old prominence object still absent                                              |per-fact source decomposition; D-ROLE; language trajectory; automatic downgrade                                                                                                  |Closed eight-piece fixture. Whole-coverage Level 2 remained granularity-sensitive (about 25 under this convention) but descriptive only. Per-fact rows carried the load-bearing source-chain result. The old gross-vs-aftermath prominence finding was still not restored.                                                                                                                                              |
|M18|coverage-network           |RC2 consolidated candidate                          |ChatGPT              |10 standardized findings; source-chain taxonomy and ownership precision improved; prominence still absent; wording-only event-language MINOR remained|origin-completeness taxonomy; source-dependent interpretation / claim-amplification split; party enumeration; same-stage classification; language trajectory; automatic downgrade|RC2 improved source-chain and ownership discipline without changing finding count. It still failed the historical prominence regression and still allowed `pour / breach / cross / enter` to survive as a low-severity standardized language object.                                                                                                                                                                    |
|M19|coverage-network           |RC2 + FAIL-MB-017 + FAIL-MB-018 integrated          |ChatGPT              |10 standardized findings; FAIL-MB-017 PASS; FAIL-MB-018 PASS; 017+018 interaction PASS                                                               |prominence-packaging; semantic equivalence / earnedness; proposition-level source chain; D-ROLE independent scan; automatic downgrade                                            |Composition changed with net count 0: old event-language MINOR removed; prominence-packaging MODERATE restored. France 24 blame-routing retained but moved MODERATE -> MINOR because FAIL-MB-005’s mandatory downgrade cascaded to the new rank #1. Full language-package expansions fell 3 -> 2. Level 2 was about 25: FAIL-MB-008 remains DEFUSED, NOT CLOSED. This regression rerun is not a clean runtime benchmark.|

#### M19 interaction and revision evidence

- **FAIL-MB-017 standalone:** PASS. The standardized table restores the
  gross-scale vs. aftermath placement object as `prominence-packaging`, marks
  cross-piece availability NOT APPLICABLE, states the packet inverse, records
  packaging provenance, and leaves the 60,000 attribution object with
  SOURCE-CHAIN / CLAIM AMPLIFICATION.
- **FAIL-MB-018 procedural:** PASS. Semantic normalization precedes
  wording-triggered expansion; no event-language finding survives merely because
  `pour / breach / cross / enter` differ; independent non-lexical D-ROLE
  cause/blame analysis remains active.
- **Joint interaction:** PASS. The prominence finding rests on gross scale,
  return/reversal context, and casualty/denominator placement—not lexical
  variance. No unrelated standardized finding disappears.
- **Finding-table delta:** 10 -> 10. The old event-language MINOR finding is
  removed and a prominence-packaging MODERATE finding is added.
- **Language-execution delta:** full package expansions fall from 3 to 2;
  migrants/crossers is no longer triggered. This is an observed execution
  reduction, not a runtime claim.
- **Downgrade cascade:** FAIL-MB-005 still requires one automatic downgrade.
  Removing the former rank-1 event-language finding re-ranks the survivors, so
  France 24’s blame-routing finding becomes rank 1 and receives the mechanical
  MODERATE -> MINOR downgrade. This is a cross-rule interaction, not
  discretionary severity drift.

---

## WHAT THE LOG ALREADY SHOWS

1. **The claim map is the highest-leverage stage.** R3/R5 isolate it: same prompt, same
   paper, different field 6, verdict E vs. C. One sentence upstream decided whether a real
   defect was found.
2. **The concede test converts finding-severity into verdict-severity correctly.** R7
   (defect found, no concede test) -> E. R8 (defect found, concede test) -> C. Without it a
   single technical defect reads as a broken paper.
3. **Downstream stages do kill upstream findings**  -  10 documented. The pipeline corrects
   rather than accumulates.
4. **Retrieval depth drives most model divergence, not reasoning.** R17/R18 retrieved
   decisive sentences and converged. R19 generalized and diverged. Same prompt.
5. **Self-report is unreliable even under explicit instruction.** M2 inverted a sentence it
   was told to reproduce verbatim. M4’s audit-integrity block claimed no banned phrase was
   used while the phrase appeared in the output.
6. **Live runs remain the primary source of substantive repairs, but structural review also**
   **catches architecture drift.** The Ceuta runs exposed FAIL-MB-008 through 010; the later
   cross-prompt review found vocabulary and ownership seams that the MEDIA-P1 harmonization
   repaired without pretending they were additional live-run failures.
7. **The whole-story coverage-network independence metric remains**
   **convention-dependent, but it no longer owns the verdict.** The original fixed
   packet produced Level-2 counts of 3, 6, and 12–14; later revised/RC2 executions
   produced approximately 25 (and another RC2 implementation produced a nearby
   but different granular total). This confirms FAIL-MB-008’s measurement spread
   is still live. The per-fact rewrite is now exercised, however: disputed
   propositions retain their proposition-level origin classification even while
   the whole-coverage count moves. FAIL-MB-008 is therefore DEFUSED, NOT CLOSED;
   FAIL-MB-009’s dangerous ratio/inference failure is repaired and exercised.
8. **Companion retrieval can reverse an evidentiary assessment without lowering**
   **the standard.** Madison moved from “no evidentiary origin” to strong BLM /
   occupation support because the relevant material was outside the literal
   packet, while formal Antifa command still failed.
9. **The correct unit for language analysis is the package over time, not the**
   **noun.** Seattle’s persistent age label looked soft alone and mixed-to-hard
   once agency, conduct, charges, attribution, and ballistic updates were coded.
10. **Party enumeration is not clerical.** The police-language finding did not
    appear until suspected perpetrator collectives became an explicit party and
    the paired descriptions were preserved.
11. **Same-stage divergence is distinct from update failure.** Madison’s event
    labels and Seattle’s “small groups” / “gang-related” language diverged under
    substantially the same evidentiary conditions; timing could not explain them.
12. **A module can be substantively useful and still be too verbose.** The full
    language-package schema prevented a false positive but over-produced
    uncontested party descriptions, motivating conditional deep-dive triage.
13. **Selection and prominence are different evidentiary objects.** A
    cross-piece availability gate can correctly police omission while silently
    destroying a within-piece placement finding. The integrated Ceuta rerun
    restored the older gross-scale vs return/aftermath object only after
    PROMINENCE-PACKAGING received its own table, provenance, inverse test, and
    evidence rules.
14. **Lexical difference is not a valid candidate unit by itself.** On the same
    Ceuta packet, increasingly elaborate prompt versions repeatedly regenerated a
    low-severity `pour / breach / cross / enter` finding. Moving semantic
    equivalence, predicate decomposition, and non-circular earnedness upstream
    removed that object without suppressing independent D-ROLE cause/blame
    differences.
15. **Repairs interact through mechanical rules even when neither repair is**
    **wrong.** Removing the old event-language finding changed the forced ranking
    used by FAIL-MB-005. The mandatory automatic downgrade therefore moved to
    France 24’s blame-routing finding, changing it MODERATE -> MINOR. This was
    neither predicted by FAIL-MB-017 nor FAIL-MB-018 and is a genuine
    cross-rule side effect worth preserving.
16. **Prompt length alone is a weak runtime predictor on the fixed corpus.**
    Original CN runs commonly landed around 6–9 minutes while RC2 runs ranged
    from roughly 7.5 minutes to nearly 20 minutes. The integrated validity repair
    also reduced one full language expansion without being designed as a speed
    optimization. Optimization should therefore be justified primarily by drift
    reduction, output clarity, or an identified execution-cardinality mechanism,
    not by prompt size alone.

17. **The retrieve-don't-infer failure is executor-agnostic.** It has now been
    observed in the audit (FAIL-CV-003/004), in a prompt-review model, and in
    the auditor writing the pre-run oracle for this test. Dimensional or
    structural correspondence is not a substitute for item retrieval.

18. **Selective non-firing and a clean substantive acquittal are now both
    demonstrated, but the acquittal exposed a provenance gap.** The Sol run
    declined on construct-establishment (not triggered), P2 (VOID),
    level-of-analysis, ecological validity, weak/fatal proxy, premise
    laundering, intervention ratchet, institutional gap, and motive claim, and
    refused to double-count two findings sharing one mechanism. ISIS-2 then
    returned Verdict A on a deliberately clean calibration target. That result
    was substantively differentiated, not blanket praise, but its complete lack
    of retrieval-basis declarations made verified accuracy indistinguishable
    from confident recall and triggered FAIL-CV-008. The same asymmetry appeared
    independently in the review of Rigor.me: “ran successfully” was presented
    without a visible distinction between genuine execution and confident
    narration filling a gap. That recurrence makes this a general provenance
    pattern, not an ISIS-2-specific defect.

19. **Cross-stage independence is an evidentiary control, not an orchestration
    preference.** The Galor-Özak contaminated/clean pair held the underlying
    evidence constant and changed only whether an unsupplied sibling output was
    visible in ambient context. The result moved from C to D, while provisional
    evidence crossed into DEFEATS only in the contaminated condition. That is a
    real control pair for FAIL-IV-001/002.

20. **Declared input coverage must establish consumption, not mere presence.**
    Shen's first counter-audit named the three-prosecutor architecture but
    omitted the decisive internal-validity finding. After the coverage repair
    explicitly recorded IV-1 through IV-5 as supplied and consumed, the verdict
    moved for a traceable reason. This is the observed case behind FAIL-CA-003.

### Regression case note

Two durable Ceuta cases now exist with the exact original synthetic packet
embedded verbatim:

- `ceuta-prominence-regression` — FAIL-MB-017
- `ceuta-semantic-equivalence` — FAIL-MB-018

They are regression fixtures for known objects, not proof of general media-branch
capability. The 017+018 interaction invariant remains: no prominence finding may
rest on a formulation difference already normalized by the semantic gate.
