# CONSTRUCT-VALIDITY AUDIT: CLAIM VS. MEASUREMENT

**Source title:** Reducing loneliness and depressive symptoms in older adults during the COVID-19 pandemic: A pre-post evaluation of a psychosocial online intervention
**Citation:** Gabarrell-Pascuet A, Coll-Planas L, Blancafort Alias S, Martínez Pascual R, Haro JM, Domènech-Abella J (2024). PLOS ONE 19(12):e0311883. https://doi.org/10.1371/journal.pone.0311883
**Field / debate:** loneliness and late-life mental-health intervention research; online/remote delivery of psychosocial group interventions.
**Prompt:** `prompts/research-analysis/2-construct-validity.txt` (Provenance, main)
**Upstream map:** `publichealth_01_claim_map.md` — **supplied. Full-sequence mode. Degraded standalone mode NOT invoked.**
**Run date:** 2026-08-08

---

## EXECUTION CONSTRAINTS — STATED BEFORE THE AUDIT

Three limits govern what follows. None is cured by confidence.

**1. The prompt itself was retrieved incomplete.** `2-construct-validity.txt` is 1,092 lines. It was fetched through GitHub's rendered blob view, which truncated at approximately line 1000, immediately after Section 17 and at the head of the closing `REMINDER` block. Sections 1–17 were captured in full. **Not captured:** the REMINDER block, and any specification of the final standardized finding table beyond the inline references to it. `shared_primitives.txt` was not loaded at all; only the compact copies embedded in the two prompts were used. The finding table at the end of this audit therefore uses columns assembled from the prompt's inline references and **may not match the canonical §2 schema.** Flagged for repair, not silently improvised over.

**2. Tables 1 and 2 were not retrieved.** They are rasterised images on the publisher page. Per-variable means, SDs, confidence intervals, and exact Cohen's *d* values are **not in evidence**. The only effect-size evidence available is the Results' prose statement of "medium to large." Every severity rating below that would otherwise depend on effect magnitude is calibrated accordingly and flagged.

**3. Quotation is constrained at the executor level.** One short quotation per source. It was spent in the map (Field 2b) on the Abstract's hedged results sentence, where exact wording carries the hedge. All other source content here is paraphrased with section locators. Under the map's anchoring rule this rendered three otherwise-retrieved items NOT ANCHOR-ELIGIBLE. See toolkit note T3.

---

## APPLICABLE-CHECKS NOTE

**Target document type:** academic paper — single-arm feasibility/pilot intervention study with pre-post evaluation.

**Sections that apply:** 1, 1A, 2, 3, 4, 5, 6, 7, 10, 11, 12, 13, 14, 15, 16, 17.

**Sections N/A or not runnable:**
- **Section 8 (Cross-Reanalysis Object Check) — N/A.** No independent reanalysis, replication, or critique of this source was located. There are no reanalyses in tension, so there is nothing to test for object mismatch. This is *not* a finding that the source is unchallenged.
- **Section 9 (Citation-Use Audit) — NOT ASSESSED.** No downstream citation was retrieved (map Field 4, PROVISIONAL). The classification enum is left **unassigned**. "Accurate citation" is not the output; *not checked* is.

---

## 1. CLAIM MAP (received)

Upstream map supplied; not regenerated.

- **Claim under audit (Field 6):** The BLOC online psychosocial group intervention reduced emotional loneliness in adults aged ≥65 by 0.84 points on the De Jong Gierveld emotional-loneliness subscale (0–6), *p*<0.01.
- **What was literally measured (Field 1):** within-person change in self-reported scale scores between two telephone interviews bracketing an 8-week single-arm online group intervention, in 27 enrolled / 21 post-assessed self-selected adults ≥65 in Barcelona, Oct 2021–Jan 2022; sex-adjusted two-level random-intercept mixed models.
- **Weaker defensible claim (Field 3):** scores on 2 of 7 outcome families were lower at T2 than T1 in an uncontrolled sample; the intervention was deliverable, with 81% attending ≥5 of 8 sessions; no causal attribution is available from the design.
- **Target layer:** source claim (PAPER).

**MAP DISAGREEMENT:** none. The operationalization is read the same way here as in the map.

**MAP GAP:** the paper administers the 11-item De Jong Gierveld scale (ref 36) but cites ref 37 — the paper describing the **6-item short** emotional and social scales — for the subscale scoring rule. The stated ranges (0–5 social, 0–6 emotional) are consistent with the 11-item instrument, so this is a citation-precision issue rather than a scoring error on the face of it. The map records the instrument but not this mismatch. Flagged, not silently absorbed.

---

## 1A. CONSTRUCT ESTABLISHMENT

**Section triggered.** The source escalates from efficacy to normative/causal claims about the construct in the Abstract Conclusions and the Discussion.

**Retrieval depth for this section: assessed from full text including the introduction and its reference list; no cited work was fetched.**

| Property | Claim-map status | Does the normative/causal claim depend on it? | ESTABLISHED-CITED prosecutor split | Evidence and exact inferential load | Finding disposition |
|---|---|---|---|---|---|
| PREVALENCE | ESTABLISHED-REPORTED (sample) / UNKNOWN (population) | Only for deferred claim 4 (policy escalation) | N/A — no ESTABLISHED-CITED property in this run | Sample distribution reported directly (≈60% lonely, 44% moderate, 15% severe). Population claim rests on unchecked citations and carries an unreconciled internal tension (11.9% older-adult European prevalence vs. "nearly a third" in developed countries) | PROVISIONAL for the population claim; not load-bearing for Field 6 |
| FORM | UNKNOWN | No | N/A | Internal consistency evidence sits in S2 Table, not retrieved | PROVISIONAL; not load-bearing |
| DOMAIN | ESTABLISHED-REPORTED (partial) | Yes — and it is **satisfied** | N/A | The source defines two dimensions, measures both, and locates its effect in one. Its own Discussion states plainly that social support and social loneliness did not move | **construct adequately established for this property**; no finding |
| WRONGNESS | N/A | No | N/A | No belief-falsity claim is made | **[P2] does not fire.** Not VOID — the check does not trigger at all. No wrongness or pathologization finding is available in this audit |
| HARM | UNKNOWN | **Yes — load-bearing for deferred claim 4 only** | N/A | Asserted by citation (refs 3–12, including the team's own longitudinal work). Establishment is present *as citation*; citations not checked | PROVISIONAL. **May not be load-bearing and may not be rated MAJOR or FATAL** per [P1] |

**1. Dependence.** No property is load-bearing for the **claim under audit**. Field 6 is an efficacy claim about moving a score; it does not require that loneliness be prevalent, coherently formed, or harmful. HARM is load-bearing only for deferred claim 4 (the policy escalation), which is not this audit's target. This distinction is the whole point of Field 6 discipline and is recorded rather than blurred.

**2. Retrieval cap.** Assessed from full text including introduction plus reference list; **cited works not checked**. Properties marked UNKNOWN produce a **PROVISIONAL gap, not a confirmed absence.**

**3. ESTABLISHED-CITED prosecutor split.** **Not runnable.** No property carries ESTABLISHED-CITED, because no cited work was fetched. The split has nothing to operate on. Recorded as a retrieval limit; **not** converted into a finding that the citations fail to support the load.

**4. Not-firing condition.** DOMAIN: **construct adequately established** — no finding raised. For PREVALENCE, FORM, and HARM the not-firing condition cannot be satisfied on this run's retrieval, so those remain open and PROVISIONAL rather than cleared.

**5. Concede test (section-level).** Surviving narrower statement if the construct-establishment gap were fully conceded: *the intervention moved scores on one dimension of a construct whose population prevalence and harm profile this run did not independently verify.* Field 6 survives this concession intact.

**6. Output ownership.** Canonical failure mode name: **Construct-establishment gap**. Own row in the finding table. Severity: **minor**, capped by PROVISIONAL disposition and by attaching to a deferred claim rather than to Field 6.

---

## 2. MEASUREMENT EXTRACTION

**Sample size:** 27 enrolled; 21 with post-intervention data. Drop-out 22%.
**Population:** community-dwelling adults ≥65 in Barcelona; 74% female; mean age 74.26 (66–88); 48% secondary education; 33% partnered.
**Recruitment:** primary care and senior centres; posters, pamphlets, calls, presentations. ~500 offered → 63 interested → 27 enrolled (~5%). Self-selection on an explicit desire to connect better with others.
**Instrument/proxy:** self-report questionnaires administered by telephone by two trained members of the research team — unblinded and not independent of delivery.
**Time scale:** 8 weeks; no follow-up.
**Outcome variable (Field 6):** De Jong Gierveld emotional-loneliness subscale, 0–6.
**Control variables:** sex only.
**Exclusions:** blind or deaf; self-reported cognitive impairment; effectively, anyone without internet and a device.
**Not measured:** any counterfactual; any objective social-contact measure; anything after week 8; treatment fidelity or module adherence (the design explicitly permits facilitator adaptation); a pre-specified single primary endpoint; blinded assessment; multiplicity adjustment across seven outcome families.

**Is the measured variable direct evidence of the claimed construct, or a proxy?**

Two different questions, and conflating them is the trap here.

- **Scale → construct: essentially direct, not a proxy.** Loneliness is definitionally a subjective state. Self-report on a validated dimensional scale is the criterion measure, not a stand-in for one. **The familiar "invalid proxy" attack does not land against this instrument, and this audit does not make it.** Stating that plainly is required by the symmetry rule.
- **Pre-post difference → intervention effect: this is the proxy, and it is where the failure lives.** The quantity measured is a within-person change score over 8 weeks in a single arm. The quantity claimed is the causal effect of the intervention. Nothing in the design connects them.

### DEFINITION-OPERATIONALIZATION CHECK

**Object A — loneliness instrument.**
Retrieval basis: **ITEMS-INFERRED.** Scope result: **UNKNOWN.**
No coextensive/narrower/broader classification is permitted, and **no scope-creep finding is raised against the De Jong Gierveld scale.** Inferring the scale's contents from its name or family is barred; it manufactures false scope creep.

**Object B — "completed the intervention."**
Retrieval basis: **ITEMS-RETRIEVED.** Scope result: **broader.**
Definition as used in the Abstract: 21 participants completed the intervention; 22% drop-out. Rule actually applied (Results, final paragraph): post-intervention interviews were given to the 21 who had completed **at least one session**. Specific out-of-scope inclusion: anyone attending 1 of 8 sessions counts as a completer, and the headline 22% drop-out figure is computed on that basis. The genuinely informative figure sits in the same paragraph and is not the one that reaches the Abstract: 81% attended ≥5 sessions.
**Failure mode: Definition-operationalization mismatch. Subtype: definitional scope creep.**

**Pathologization question.** Does the operationalization pathologize, penalize, or score as positive an accurate, nuanced, or empirically supported version of the phenomenon?
**No finding available.** The check requires ITEMS-RETRIEVED and Object A is ITEMS-INFERRED. Separately, [P2] does not fire at all here — the construct is a subjective state, not a belief with a truth value, so there is no sub-claim to grade as ESTABLISHED-FALSE or ESTABLISHED-ACCURATE. **Dropped, and dropped for the right reason.**

---

## 3. CLAIM VS. MEASUREMENT TABLE

| # | Measured variable | Claimed construct | Same? | Gap | Severity | Notes |
|---|---|---|---|---|---|---|
| F1 | Within-person change in emotional-loneliness subscale, T1→T2, single arm, no comparator | The intervention **reduced** emotional loneliness | No | **No counterfactual.** The change score is used as a proxy for the causal effect. Regression to the mean (participants enrolled on the basis of expressed unmet social need), spontaneous change, secular change across Oct 2021–Jan 2022 as restrictions eased, repeated-assessment reactivity, demand characteristics from unblinded in-team assessors, and non-specific group-contact effects are all unexcluded and unexcludable in this design | **major** | The source concedes the control-group absence in Limitations. The title does not. Failure is in packaging, not in method disclosure |
| F2 | Emotional subscale moved; global and social loneliness did not | "loneliness" unqualified (title, conclusions) | No | **Construct substitution.** One dimension stands in for the two-dimensional construct the source itself defines. The Discussion is accurate about this; the title is not | **moderate** | Same underlying object as the map's Move 2. Anchored on retrieved text |
| F3 | Post-interviews given to those attending ≥1 of 8 sessions | "21 participants completed the intervention (22% drop-out)" | No | **Definition-operationalization mismatch; subtype definitional scope creep.** ITEMS-RETRIEVED | **moderate** | Own row per the prompt. Bears on the deferred feasibility claim (claim 3), not on Field 6 |
| F4 | Seven outcome families tested; two significant; no multiplicity adjustment; no pre-specified single primary endpoint. Sample size computed to detect **≥1.7 units in loneliness** (assumed SD 2.33); the significant loneliness result is a **0.84-point** change on a 0–6 subscale | The intervention improves loneliness and mood | No | **The study was sized for one endpoint and reports significance on another.** The paper does not state whether the 1.7-unit target refers to the 0–11 global score or a subscale; SD 2.33 is more consistent with the global score. Either way the observed effect is well below the difference the calculation targeted, and the endpoint that reached significance is not identified in advance as the one the study was powered for | **major** | Sharpest measurable defect available from retrieved text. Independent of F1 in mechanism |
| F5 | PHQ-8 decrease of 2.30 points (0–24), baseline mild symptoms | "from mild to minimal symptomatology"; reduced burden of depression | Partly | Statistical significance read as clinical significance. Commonly cited minimal important differences for PHQ instruments are appreciably larger than 2.30 points, and a mild-symptom baseline limits available room | **moderate** | Attaches to **deferred claim 2**, not Field 6. Recorded, not anchoring. The MID comparison is RECALLED, not retrieved in this run — see Section 10 |
| F6 | PHQ-8 described as ranging 3–24 in Methods, 0–24 in Results; the instrument citation given is the PHQ-9 validation paper | — | — | Internal inconsistency in instrument description plus an imprecise instrument citation. Standard PHQ-8 range is 0–24 | **minor** | Reporting defect. Not claim-defeating. Two p-thresholds also appear for the same finding across Table 1 (raw *t*-test, *p*<0.05) and Table 2 (mixed model, *p*<0.01); the Abstract reports only the stronger |

Severity values are drawn from the standardized enum: none / minor / moderate / major / fatal-for-strong-claim. No mechanism wording appears in the Severity column.

F2 and F3 both involve definitional slippage, but they concern different objects (the construct vs. the completion rule) and are **two independent levers**, not one mechanism double-counted. F1 and F4 are likewise mechanically distinct: F1 is the absence of a counterfactual; F4 is endpoint/power mismatch and multiplicity. Both would remain if the other were fixed.

---

## 4. LEVEL-OF-ANALYSIS CHECK

**Level at which evidence was collected:** self-report scale scores, by telephone, from a self-selected, help-seeking, internet-equipped, non-cognitively-impaired convenience sample of 27 in a single city, single arm, 8 weeks, no follow-up.

**Level at which the claim is applied:**
- (a) Field 6 — efficacy of a specific intervention for older adults.
- (b) Abstract Conclusions (deferred claim 4) — population-level policy about an intervention *class* for "vulnerable population sectors."

**Assumptions required to bridge evidence level to claim level:**

| Assumption | Tested? | Status |
|---|---|---|
| Observed pre-post change equals the intervention's effect (no regression to mean, no secular trend, no reactivity) | **No** — and structurally untestable in a single-arm design | Untested premise |
| The 27 enrolled represent older adults generally | **No** — and the funnel argues against it: ~5% of those approached, all self-selecting on desire to connect, all digitally equipped | Merely implied |
| The 8-week change persists | **No** — no follow-up | Untested |
| Findings transfer to older adults without devices or digital confidence | **No** — the source concedes they do not | Acknowledged and correctly disclaimed |
| Group-format effects are attributable to the modular content rather than to contact per se | **No** — no attention control, no fidelity measure | Untested |

**Would a domain expert accept the bridge as valid?** For (a): as hypothesis-generating only — which is close to what the paper's own body says. For (b): no. A single-arm pilot with 21 post-assessed participants does not reach a claim about what interventions *can become essential* for a population sector.

---

## 5. CONFOUND AUDIT

| Confound | Domain obvious? | Controlled? | Acknowledged? | Impact if omitted |
|---|---|---|---|---|
| Regression to the mean — participants enrolled precisely because they reported unmet social need, i.e. selected on an extreme of the outcome | Yes | No | Control-group absence is acknowledged; RTM is not named | **Fatal for the strong claim** |
| Secular / pandemic-context change across Oct 2021 → Jan 2022 (restrictions easing, vaccination >95%, social life reopening) | Yes | No | No | High |
| Repeated-assessment reactivity and demand characteristics — unblinded assessors drawn from the delivering research team, telephone administration, participants reporting on an intervention they had just received and evidently enjoyed | Yes | No | Self-report bias acknowledged generically; assessor non-independence not addressed | High |
| Non-specific effects of structured group contact (attention, expectation, scheduled social time) as distinct from the intervention's modular content | Yes | No | No | High |
| Differential attrition — significantly more women dropped out post-intervention | Yes | **Partly** — models adjusted for sex; ML estimation handles missingness under MAR | Yes; it is the stated reason for the sex adjustment | Moderate |
| Seasonality — the study window spans the December holiday period, which has documented associations with both loneliness and mood | Yes | No | No | Moderate |
| Facilitator effects and treatment fidelity — the modular design explicitly permits per-group adaptation, and no fidelity measure is reported | Yes | No | No | Moderate |
| Selection at ~5% of those approached, on an explicit desire to connect | Yes | No | Partly — limitations note population characteristics may limit practical significance | Moderate |

The first four are the ones that matter. Any one of them could produce the observed 0.84-point movement without the intervention having any effect.

---

## 6. ECOLOGICAL VALIDITY CHECK

- **Does the task resemble the real-world phenomenon?** **Yes — and this is a genuine strength.** This is an actual 8-week intervention delivered to real older adults in their homes during the conditions it was designed for, not a laboratory analogue. Credit where due.
- **Does the sample resemble the population the claim is applied to?** Only partly. Digitally equipped, help-seeking, 74% female, no cognitive impairment, single city.
- **Does the time scale match the real process?** No. Late-life loneliness is chronic; measurement stops at week 8 with no follow-up.
- **Realistic pressure, incentives, constraints, selection?** Yes for delivery. No for measurement — unblinded, in-team assessment of a population that had just spent eight enjoyable weeks with the study team.
- **Is the study measuring performance, stated belief, compliance, perception, or institutional output? Are they conflated?** It measures **perception** (self-report), plus **satisfaction** (the open feedback prompt). Mild conflation: the Discussion reads the qualitative warmth and the behavioural signals (participants exchanging phone numbers, some meeting in person) as corroborating a loneliness reduction, while the two measures that would have registered objective social change — OSSS-3 social support and the social-loneliness subscale — did not move. Acceptability is doing some quiet evidential work for efficacy.

**Verdict: Ecologically valid only for a narrower claim.**

---

## 7. DECISIVE-TEST CHECK

- **What would the decisive test measure?** Between-group difference in loneliness change, intervention vs. an attention-matched control receiving equivalent online group time without the loneliness-specific modules.
- **Population:** community-dwelling adults ≥65 reporting loneliness, recruited across multiple sites, with an explicit strategy for including participants of low digital confidence.
- **Controls required:** randomisation; attention-matched comparator (to separate the content from contact per se); blinded outcome assessment by assessors independent of delivery; a single pre-registered primary endpoint; intention-to-treat analysis; pre-specified handling of attrition; ≥6-month follow-up.
- **Outcome supporting the source's claim:** a between-group difference on the pre-specified primary loneliness endpoint that exceeds the minimal important difference and persists at follow-up.
- **Outcome weakening or falsifying it:** no between-group difference, or a difference confined to the attention comparison, or a difference that does not survive follow-up.
- **Does the source run it?** **No.**
- **Does the field acknowledge the decisive test has not been run?** **Yes.** The paper explicitly calls for an RCT with a larger sample, and its own cited reviews describe the online-intervention evidence base as promising but generally weak in quality and the group-intervention health effects as inconclusive. The source is not pretending the question is settled.

**The decisive test would be: a pre-registered randomized controlled trial with an attention-matched online control, one pre-specified primary loneliness endpoint, blinded independent outcome assessment, intention-to-treat analysis, and follow-up at six months or longer.**

---

## 8. CROSS-REANALYSIS OBJECT CHECK

**N/A.** No independent reanalysis, replication, correction, or published critique of this source was located. Nothing is in tension, so no object-mismatch test can run. This is not evidence that the source is uncontested; it is evidence that nothing was found in this run.

---

## 9. CITATION-USE AUDIT

**NOT ASSESSED.** Map Field 4 is PROVISIONAL: no downstream restatement was retrieved, and no citation index was queried. The downstream-use classification enum is left **unassigned**. Accurate citation, inflation, citation laundering, premise laundering, and unsupported consensus construction are all **unchecked, not cleared.**

---

## 10. IGNORED-LITERATURE CHECK

| Ignored literature / evidence | Why it matters | Cited? | Effect of omission |
|---|---|---|---|
| Regression-to-the-mean and natural-history literature on uncontrolled pre-post designs | Determines whether the headline result is interpretable at all. The paper names the missing control group but never names the mechanism that makes its absence decisive | No | **Major evidentiary gap** |
| Minimal important difference literature for PHQ-8/PHQ-9 and for loneliness scales | Determines whether 2.30 and 0.84 points mean anything to a participant. The paper gestures at "clinical or practical significance" in Limitations without engaging any benchmark | No | **Major evidentiary gap.** *Verification note: the specific MID benchmarks are **RECALLED**, not retrieved in this run. This row may not be load-bearing. What is retrieved and anchored is the paper's own failure to engage any benchmark* |
| Reporting standards for pilot and feasibility trials, which discourage effectiveness hypothesis-testing in pilots | The paper describes itself as assessing feasibility while simultaneously stating effect hypotheses and reporting *p*-values in its title-level claim. That internal tension is retrieved from the paper itself | Not cited (a CONSORT diagram is supplied as S1 Fig) | **Major evidentiary gap.** *The guidance itself is RECALLED; the paper's internal tension between "feasibility" framing and effectiveness reporting is FULL-TEXT-CONFIRMED and is the anchored part* |
| Masi et al. 2011 meta-analytic finding that the strongest designs yield smaller loneliness effects, and that maladaptive-social-cognition approaches outperform contact-provision approaches | Bears directly on both the intervention's dual-focus design and on how a small pre-post movement should be read | Cited (ref 21) — but only for the four-way intervention taxonomy | Moderate weakness |
| Trial registration | Pilot intervention studies are ordinarily registered; none is reported, which leaves outcome and endpoint selection unverifiable | Not reported | Moderate weakness |

---

## 11. EVIDENCE-TYPE, VERIFICATION, AND FAILURE-LOCATION CHECK

| Claim or evidence item | Evidence type | Measurement role | Verification state | Failure location | Directly measured / inferred / speculative | Source audit required? |
|---|---|---|---|---|---|---|
| Emotional-loneliness subscale fell 0.84 points, *p*<0.01 | Primary empirical | Direct measure (of the score) | FULL-TEXT-CONFIRMED (prose); Table 2 not retrieved | — | Directly measured | Yes — Tables 1–2 |
| The **intervention** caused that fall | Author inference | Proxy evidence (change score for causal effect) | FULL-TEXT-CONFIRMED as a claim | **PAPER** | Inferred | No |
| Depressive symptoms fell 2.30 points, *p*<0.01 | Primary empirical | Direct measure | FULL-TEXT-CONFIRMED (prose) | — | Directly measured | Yes — Tables 1–2 |
| Effect sizes were "medium to large" | Primary empirical | Direct measure | **PROVISIONAL** — numeric *d* values sit in unretrieved Table 1 | — | Directly measured, unverified | **Yes — full PDF required** |
| Social support, social loneliness, anxiety, QoL, perceived health unchanged | Primary empirical | Direct measure | FULL-TEXT-CONFIRMED | — | Directly measured | Yes — Tables 1–2 |
| 22% drop-out / "21 completed the intervention" | Primary empirical | Direct measure under a **broader** definition | FULL-TEXT-CONFIRMED | **PAPER** | Directly measured, mis-defined | No |
| Loneliness is prevalent and harmful in older adults | Secondary synthesis, via citation | Citation-dependent premise | **PROVISIONAL** — citations not checked | Not assessed | Inferred | **Yes — reception/citation audit** |
| Online interventions for vulnerable sectors can become essential | Conceptual / policy | Conceptual claim | FULL-TEXT-CONFIRMED as a claim | **PAPER** (deferred claim 4) | Speculative | No |
| The group supplied the closeness participants' networks lacked | Author inference | Conceptual claim | FULL-TEXT-CONFIRMED as a claim | **PAPER** (deferred claim 5) | Speculative | No |
| Any downstream restatement | — | — | NONE FOUND, retrieval-limited | Not assessed | — | **Yes — citation-index query** |

- **Directly measured:** the score changes, the non-changes, attendance, drop-out.
- **Inferred:** intervention causation; population prevalence and harm.
- **Speculative:** the policy escalation; the mechanism narrative.
- **Requires audit before publication:** Tables 1–2 and S1–S2 from the PDF; a citation-index query; a source audit of refs 3–12 if deferred claim 4 is ever run.

---

## 12. INTERNAL CONSISTENCY CHECK

Re-read of this audit's own resolution language:

- Section 8 records "no reanalyses located"; Section 9 records "not assessed"; Section 10 records two rows as RECALLED. **These agree.** Nowhere does a later section treat the downstream layer or the cited literature as checked.
- Section 2 states that the scale→construct relationship is **not** a proxy failure; Section 3 (F1) and Section 14 both locate the proxy failure at change-score→causal-effect. **These agree.** No section calls the instrument invalid.
- Section 1A marks HARM as UNKNOWN and not load-bearing; Section 16 checks Construct-establishment gap at **minor** severity attached to a deferred claim. **These agree.** No section treats the construct as unestablished for the purposes of Field 6.
- Section 3 rates F1 **major**; Section 13 rates F1 **DEFEATS**; Section 14 returns **INVALID** for the causal claim with a surviving residual. **These agree** — a DEFEATS finding on the causal reading of Field 6 is compatible with a major (not fatal) severity, because a usable residual survives. Had the residual been "none," the severity would have had to read fatal-for-strong-claim.
- Section 10 rows F-MID and F-pilot-standards are flagged RECALLED and not load-bearing; **neither appears in the Section 13 concede table as a DEFEATS or in the Section 14 verdict derivation.** Confirmed consistent.

No contradictory resolution language found. One phrasing risk was caught and corrected during drafting: an earlier pass described the sample-size/endpoint mismatch (F4) as part of the "no control group" problem. It is not — it is mechanically independent and would survive the addition of a control group. It is recorded as a separate lever.

---

## 13. THE CONCEDE TEST

**Claim under audit: the BLOC intervention reduced emotional loneliness by 0.84 points on the De Jong Gierveld emotional subscale (0–6), *p*<0.01.**

| Finding | Concede test | Surviving claim if NARROWS |
|---|---|---|
| **F1** No counterfactual; change score proxies causal effect | **DEFEATS** | — |
| **F2** Construct substitution: emotional subscale → "loneliness" | **NARROWS** | The claim survives only for the emotional dimension, not for loneliness as the source defines it |
| **F4** Sized for a ≥1.7-unit difference; significance reported on a different, smaller endpoint; seven outcome families, no multiplicity adjustment, no pre-specified primary endpoint | **NARROWS** | The claim survives only as an unadjusted, post-hoc-selected result on one of seven outcome families |
| **F3** "Completed" = ≥1 session | **SURVIVES** | — (bears on the deferred feasibility claim; may not be rated major or fatal, may not anchor the verdict) |
| **F5** Statistical vs. clinical significance on PHQ-8 | **SURVIVES** for Field 6 | — (attaches to deferred claim 2) |
| **F6** PHQ-8 range inconsistency; PHQ-9 cited for PHQ-8 | **SURVIVES** | — |
| **1A** Construct-establishment gap on HARM and population PREVALENCE | **SURVIVES** for Field 6 | — (load-bearing only for deferred claim 4; PROVISIONAL, not load-bearing) |

### SCOPE-LOSS ASSESSMENT (required for every NARROWS)

| Finding | Scope-loss level | Original claim | Surviving claim | What practical or inferential work is lost? |
|---|---|---|---|---|
| F2 | **MATERIAL** | The intervention reduced loneliness | Scores fell on the emotional dimension only; the social dimension and the global score did not move | The paper's own two-dimensional framing is what makes the substitution material: the intervention was explicitly designed with a community/social arm, and the outcome that would register it did not move. The surviving claim cannot support "this addresses loneliness" |
| F4 | **MATERIAL** | A statistically significant reduction on the study's loneliness endpoint | An unadjusted result on one of seven outcome families, of a magnitude roughly half the difference the study was sized to detect | Loses the inferential protection the sample-size calculation was supposed to provide, and loses the ability to treat the *p*-value as pre-specified rather than selected |

**Verdict mapping applied.** One or more DEFEATS present (F1) → the mapping rule directs to D, E, or F.

**⚠ PROMPT DEFECT — flagged, not guessed around.** Section 13's verdict-mapping block references letters **D, E, F**, which are **defined nowhere in the retrieved prompt text**. Section 14 defines the residual usefulness grades as **A / B / C / G / none**, and Section 17 repeats that set. Either the D/E/F definitions sit in the truncated final ~92 lines, or the mapping block and the verdict object have drifted apart. **No letter was invented.** The verdict below is returned in Section 14's split-object form, which is fully specified in the retrieved text and is the format Section 17 requires. See toolkit note T2.

**Not counting findings.** The verdict below is derived from F1's DEFEATS result and from the two MATERIAL narrowings, not from the number of findings. The overlapping limitations (F3, F5, F6) are consolidated and do not contribute.

---

## 14. VERDICT

- **Claim under audit:** **INVALID** as stated — "The BLOC intervention *reduced* emotional loneliness."
- **DEFEATS finding:** F1 — the study contains no counterfactual, and the pre-post change score is used as a proxy for the intervention's causal effect.
- **Failure mechanism:** **major proxy failure.** Specifically: change-over-time proxying for causal effect. *Not* a fatal construct-validity failure — the instrument measures the construct appropriately, and the residual below is real and usable.
- **Surviving residual:** *In a single-arm, uncontrolled, unblinded sample of 27 self-selected, internet-equipped, help-seeking adults aged ≥65 in Barcelona (21 post-assessed), mean scores on the De Jong Gierveld emotional-loneliness subscale were 0.84 points lower (0–6) and PHQ-8 scores 2.30 points lower (0–24) at the post-intervention interview than at baseline (p<0.01, sex-adjusted mixed models), while global loneliness, social loneliness, social support, anxiety, quality of life, and perceived health did not change; the eight-session online group format proved deliverable to this population, with 81% attending at least five sessions and positive participant feedback.*
- **Residual usefulness grade:** **C** — useful for the stated narrower residual, invalid for the stronger claim.

**Explanation.** The instrument is appropriate and the construct is coherently defined and separately measured on both dimensions, so the usual construct-validity attack does not land here; the failure is that a single-arm change score is asked to carry a causal verb. Conceding F1 entirely, the claim that the *intervention* reduced emotional loneliness does not follow — regression to the mean alone, given enrolment selected on expressed unmet social need, could produce a movement of this size. Two further material narrowings compound it: the only loneliness dimension that moved is one of two, and the endpoint that reached significance is not the one the sample-size calculation was built around, in a seven-outcome design with no multiplicity adjustment and no pre-specified primary endpoint. What survives is not nothing — a feasibility pilot's proper job is to show that an intervention can be delivered and that outcome measures move in the hypothesised direction, and this study does both. **The failure location is the PAPER, but it is concentrated in the title and the abstract-level conclusions; the Methods, Results, Discussion, and Limitations are candid, and the Conclusions call for the RCT that would settle the question.** A critique that presents this as a paper concealing its design would be attacking a strawman and would deserve to be dismissed.

---

## 15. PAPER-SAFE WORDING

**A. Neutral summary sentence:**
A single-arm, eight-week online psychosocial group intervention delivered to 27 older adults in Barcelona was followed by lower emotional-loneliness and depressive-symptom scores among the 21 who completed post-intervention interviews, with no significant change in social support, social loneliness, anxiety, quality of life, or perceived health.

**B. Direct methodological critique:**
With no control group, no randomisation, no blinded assessment, and no pre-specified primary endpoint, the study's pre-post differences cannot be separated from regression to the mean, secular change over the study window, or assessment reactivity, and therefore cannot be attributed to the intervention.

**C. Strong adversarial version:**
The title asserts a reduction the design cannot license, and the only loneliness measure that moved was one subscale of a construct the paper itself defines as two-dimensional — on an endpoint roughly half the size of the difference the study was sized to detect, selected from seven outcome families without adjustment.

**D. Decisive-test sentence:**
A pre-registered randomised trial with an attention-matched online control, one pre-specified primary loneliness endpoint, blinded independent assessment, intention-to-treat analysis, and six-month follow-up would establish whether the intervention itself reduces loneliness.

---

## 16. FAILURE-MODE CLASSIFICATION

- [x] **Untested premise** — that an observed pre-post change reflects the intervention. Structurally untestable in this design.
- [x] **Proxy problem** — the change score proxies the causal effect.
- [ ] Weak proxy — **not checked.** The loneliness instrument is an appropriate measure of a subjective construct; the audit declines this finding.
- [ ] Fatal proxy failure — **not checked.** A usable residual survives.
- [x] **Level-of-analysis error** — a 21-participant single-city pilot supports a claim about what interventions can become essential for a population sector. *Attaches to deferred claim 4.*
- [x] **Ecological-validity failure** — time scale (8 weeks, no follow-up) and sample representativeness; valid only for a narrower claim. Delivery-side ecological validity is a strength.
- [x] **Omitted confound** — regression to the mean, secular/pandemic change, assessment reactivity and demand characteristics, non-specific group-contact effects.
- [ ] Citation laundering — **not assessed** (no downstream retrieved). Unchecked, not cleared.
- [ ] Premise laundering — **not assessed.** Unchecked, not cleared.
- [x] **Ignored adjacent literature** — RTM/natural-history, minimal-important-difference benchmarks, pilot-trial reporting standards, and the substantive findings of a meta-analysis it cites only for taxonomy. *Two of these rows are RECALLED and not load-bearing.*
- [x] **Missing decisive test** — and **acknowledged by the authors**, who call for an RCT.
- [ ] Intervention ratchet — no evidence.
- [ ] Institutional measurement gap — no evidence.
- [x] **Definition-operationalization mismatch** — "completed the intervention" operationalised as attendance at ≥1 of 8 sessions, with the headline drop-out figure computed on that basis. **Subtype: definitional scope creep.** ITEMS-RETRIEVED.
- [ ] Operationalization pathologizes an accurate or nuanced version of the construct — **[P2] does not fire.** The construct is a subjective state with no truth value, so no sub-claim is gradeable as ESTABLISHED-FALSE or ESTABLISHED-ACCURATE. Not VOID by insufficient retrieval; the check simply does not trigger. Dropped.
- [x] **Construct-establishment gap** — Property: **HARM** (and PREVALENCE at population level). Status: **UNKNOWN**. Dependence: load-bearing for deferred claim 4 only, **not** for Field 6. For WRONGNESS: no specific sub-claim exists, so no [P2] grade is assigned rather than a wholesale label being applied. Disposition **PROVISIONAL**; severity capped **minor**.
- [ ] Motive claim unsupported — this audit makes no motive claim. No inference about the authors' intent is drawn anywhere above, and the paper's candour in its Limitations is recorded as evidence against any such reading.

**Verification flags:**
- [x] **Load-bearing evidence remains PROVISIONAL** — effect sizes and confidence intervals (Tables 1–2) were not retrieved; the "medium to large" characterisation is unverified.
- [x] **Full source required** — PDF Tables 1 and 2, S1 Fig (CONSORT), S1 Table, S2 Table (Cronbach's alpha).
- [x] **Reception check required** — no citation-index query was run; downstream layer entirely unassessed.

---

## 17. FINAL OUTPUT FORMAT

- **Claim under audit status:** **INVALID**
- **DEFEATS finding(s):** F1 — no counterfactual; pre-post change score proxies the intervention's causal effect
- **Surviving residual:** in a single-arm sample of 27 (21 post-assessed) self-selected, internet-equipped adults ≥65 in Barcelona, emotional-loneliness subscale scores were 0.84 points lower and PHQ-8 scores 2.30 points lower at T2 than T1 (*p*<0.01, sex-adjusted), with five other outcome families unchanged, and the eight-session online group format proved deliverable (81% attended ≥5 sessions)
- **Residual usefulness grade:** **C**
- **Strongest defensible claim:** the intervention is deliverable online to this population and warrants a controlled trial
- **Claim being overextended:** that the intervention *reduced loneliness* — causally, and at the level of the whole construct
- **Definition-operationalization mismatch:** scope result **broader** on "completed the intervention" (ITEMS-RETRIEVED); subtype **definitional scope creep**. Loneliness instrument: **UNKNOWN** (ITEMS-INFERRED) — no finding raised
- **Construct-establishment gap:** property **HARM** (and population **PREVALENCE**); claim-map status **UNKNOWN**; dependence — deferred claim 4 only, not Field 6; ESTABLISHED-CITED split **not runnable** (no property carries that status this run)
- **Grade-before-assert outcome:** **not applicable** — no belief-falsity or pathologization claim exists to grade
- **Main proxy problem:** change-over-time standing in for causal effect
- **Main level-of-analysis problem:** a 21-participant single-city pilot supporting an intervention-class policy claim
- **Main omitted confound:** regression to the mean, in a sample selected on expressed unmet social need
- **Decisive test:** pre-registered RCT, attention-matched online control, one pre-specified primary loneliness endpoint, blinded independent assessment, ITT, ≥6-month follow-up
- **Citation-use verdict:** **not assessed** — no downstream restatement retrieved; unchecked, not cleared
- **Load-bearing finding(s):** F1 (DEFEATS); F2 and F4 (MATERIAL narrowing)
- **Concede-test result:** 1 DEFEATS, 2 MATERIAL NARROWS, 4 SURVIVES
- **Failure location:** **PAPER** — concentrated in the title and abstract-level conclusions; the body discloses the design and concedes its limits
- **Overall verdict:** the causal claim is invalid; a narrower, useful residual survives at grade C
- **Confidence level:** **Moderate**
- **What would change this assessment:** Tables 1–2 with effect sizes and confidence intervals; S2 Table internal consistency; the CONSORT diagram's actual flow; De Jong Gierveld item text (which would convert Object A from ITEMS-INFERRED to ITEMS-RETRIEVED and permit or refute a scope finding); a citation-index query for downstream use; and confirmation of whether the 1.7-unit sample-size target referred to the global scale or a subscale — that single fact would move F4 between **major** and **moderate**

---

## FINDING TABLE

*⚠ Schema caveat: the canonical standardized finding table is specified in `shared_primitives.txt` §2 and in the ~92 lines of this prompt that the GitHub blob render truncated. Neither was loaded. Columns below are assembled from the prompt's inline references and may not match the canonical schema. Do not treat this table as format-conformant.*

| # | Target claim (map Field 6) | Finding | Failure mode | Retrieval basis | Severity | Concede | Failure location | Verification state | Disposition |
|---|---|---|---|---|---|---|---|---|---|
| F1 | Intervention reduced emotional loneliness by 0.84 pts | No counterfactual; change score proxies causal effect | Proxy problem; untested premise; omitted confound | full-text | **major** | DEFEATS | PAPER | FULL-TEXT-CONFIRMED | **Load-bearing** |
| F2 | " | Emotional subscale substituted for the two-dimensional construct in title and conclusions | Construct substitution | full-text | moderate | NARROWS (MATERIAL) | PAPER | FULL-TEXT-CONFIRMED | Load-bearing |
| F4 | " | Sized for ≥1.7-unit difference; significance reported on a different, smaller endpoint; 7 outcome families, no multiplicity adjustment, no pre-specified primary | Untested premise; ignored adjacent literature | full-text | **major** | NARROWS (MATERIAL) | PAPER | FULL-TEXT-CONFIRMED | Load-bearing |
| F3 | (deferred claim 3) | "Completed the intervention" = ≥1 of 8 sessions; 22% drop-out computed on that basis | Definition-operationalization mismatch — definitional scope creep | ITEMS-RETRIEVED | moderate | SURVIVES | PAPER | FULL-TEXT-CONFIRMED | Not load-bearing |
| F5 | (deferred claim 2) | 2.30-pt PHQ-8 change read as clinically meaningful from a mild baseline | Ignored adjacent literature | full-text (paper) / RECALLED (MID benchmarks) | moderate | SURVIVES | PAPER | FULL-TEXT-CONFIRMED (paper) / PROVISIONAL (benchmarks) | Not load-bearing |
| F6 | — | PHQ-8 range stated 3–24 then 0–24; PHQ-9 validation cited for PHQ-8; two p-thresholds for one finding | — (reporting defect) | full-text | minor | SURVIVES | PAPER | FULL-TEXT-CONFIRMED | Not load-bearing |
| 1A | (deferred claim 4) | HARM and population PREVALENCE asserted by unchecked citation | Construct-establishment gap | **UNKNOWN** | minor | SURVIVES | not assessed | PROVISIONAL | **Not load-bearing per [P1]** |
| — | — | Downstream layer entirely unassessed | — | NONE FOUND, retrieval-limited | — | — | not assessed | PROVISIONAL | Reception check required |

---

## TOOLKIT NOTES — CANDIDATE REGISTRY ENTRIES

Four observations about the prompts themselves, produced by this live run. Recorded separately from the audit so they do not contaminate it.

**T1 — Operational: GitHub blob render truncates long prompts.**
`2-construct-validity.txt` (1,092 lines) truncated at ~line 1000 when fetched through the rendered blob page; the raw endpoint is robots-disallowed to automated fetchers. Any model executing this toolkit by URL will silently lose the tail of any prompt over roughly 1,000 lines — including, here, the canonical finding-table schema. Candidate mitigation: split prompts above ~900 lines, or add a line-count and a terminal sentinel string (e.g. `### END OF PROMPT — <n> lines`) so an executor can detect truncation instead of proceeding unaware. **This run only detected it because Section 17 ended mid-structure.**

**T2 — Candidate FAIL- entry: undefined verdict letters in Section 13.**
Section 13's VERDICT MAPPING directs to letters **D, E, F** for DEFEATS results. Those letters are defined nowhere in the retrieved text. Section 14 and Section 17 both specify residual usefulness grades **A / B / C / G / none**. A live run hitting a DEFEATS result therefore reaches an instruction it cannot execute. Either the definitions live in the truncated tail, or the mapping block predates the split-claim-space verdict object and was never updated when the verdict format changed. Worth checking against CHANGELOG.md — if the split object replaced an older single-letter A–G verdict, this is a leftover, and the mapping block should be rewritten to output the split object directly.

**T3 — Candidate FAIL- entry: no provenance state for "retrieved, read, quotation withheld."**
The Field 5 anchoring rule requires a quoted sentence and explicitly rejects a paraphrase. An executor operating under quotation limits — which most deployed models do — will read a source in full and still be unable to reproduce the sentence verbatim. The current vocabulary forces the item to **NOT ANCHOR-ELIGIBLE: quotation missing**, which is indistinguishable in the output from "the auditor never got the sentence." In this run that cost three retrieved, located, directly-read items their anchor eligibility, including the abstract-level escalation sentence that is arguably the paper's most inflationary line. The failure location was still established on two other items, so nothing was lost here — but on a source where the inflationary sentence is the *only* anchor, this rule would suppress a real, verified finding. Suggested repair: add an eligibility sub-state such as `ANCHOR-ELIGIBLE — LOCATOR-ONLY (verbatim withheld by executor)`, requiring the exact section locator plus a close structural description, and permitting it to anchor at capped severity. This is a genuinely new failure class from a live run rather than an anticipated one, so it belongs as **FAIL-**, not GUARD-.

**T4 — Confirmation that Field 6 Rule 2 does the work it claims.**
Rule 2 (prefer the most precisely quantified version) selected the 0.84-point subscale claim over the title's unquantified "reducing loneliness." That selection is what surfaced F4 — the mismatch between the 1.7-unit difference the study was sized to detect and the 0.84-point difference reported as significant. The unquantified version could not have produced that finding; it would have collapsed to "uncontrolled design, therefore uninterpretable," which is the generic verdict every ungoverned run reaches on a pilot study. Worth recording in tests/RESULTS.md as a positive confirmation on a new field (public health / gerontology), not just on the climate cases where the rule was originally derived.
