# CLAIM EXTRACTION / INFLATION MAP

**Target:** Gabarrell-Pascuet A, Coll-Planas L, Blancafort Alias S, Martínez Pascual R, Haro JM, Domènech-Abella J (2024). *Reducing loneliness and depressive symptoms in older adults during the COVID-19 pandemic: A pre-post evaluation of a psychosocial online intervention.* PLOS ONE 19(12):e0311883. https://doi.org/10.1371/journal.pone.0311883

**Prompt:** `prompts/1-claim-extraction.txt` (Provenance, main)
**Run date:** 2026-08-08
**Stage:** 1 of sequence. Output feeds `prompts/research-analysis/2-construct-validity.txt` unchanged.

---

## RUN CONDITIONS — READ BEFORE USING THIS MAP

**Retrieval basis.** Full rendered HTML of the article was fetched: Abstract, Introduction, Methods (design, ethics, participants, intervention, instruments, data analysis), Results, Discussion, Strengths and limitations, Conclusions, and the full reference list.

**NOT retrieved:**
- **Table 1** (participant characteristics and T1/T2 outcome means at baseline/post) and **Table 2** (estimated means from the mixed models) are rasterised images on the publisher page. Per-variable means, SDs, confidence intervals, and the exact Cohen's *d* values are therefore **not in evidence**. The only effect-size evidence retrieved is the prose statement of "medium to large" in the Results.
- **S1 Fig** (CONSORT diagram), **S1 Table** (session contents), **S2 Table** (Cronbach's alpha).
- Item text of any instrument (De Jong Gierveld 11-item, PHQ-8, GAD-7, OSSS-3, EQ-5D-5L).
- Any cited work in the Introduction. Citations were read *as citations*; none was fetched.

**Quotation constraint (executor-level).** The executing model operates under a hard quotation limit: one short quotation per source. One quotation from the target is used, in Field 2, where exact wording carries the hedge and paraphrase would destroy it. Everywhere else, content is paraphrased with section-level locators. **This interacts with the Field 5 anchoring rule** — see the flag in Field 5 and the toolkit notes at the end.

---

## COMPACT VOCABULARY — STATES USED IN THIS RUN

Verification states used: FULL-TEXT-CONFIRMED, PROVISIONAL, NONE FOUND (Field 4 provenance), author reconstruction (Field 3).
No verification state was invented. CROSS-SOURCE-CONFIRMED is not used because no downstream item was retrieved.

---

## FIELD 1 — WHAT WAS LITERALLY MEASURED

**Verification state: FULL-TEXT-CONFIRMED** (main text; Tables 1–2 not retrieved)

**Design.** Non-controlled prospective pilot with pre-post evaluation. Single arm. No control, comparison, or waitlist group. No randomisation. No blinding. No trial registration reported.

**Setting and window.** Barcelona, Spain, October 2021 – January 2022, during the COVID-19 pandemic. The paper records the ambient conditions: masks mandatory, >95% of the older population fully vaccinated, indoor public venues restricted to the vaccinated.

**Recruitment funnel.** Primary care centres and senior centres were canvassed with posters, pamphlets, calls, and presentations. Approximately 500 individuals with the appropriate profile were given the option to participate → 63 expressed interest and were screened → 27 met criteria, consented, and enrolled (~5% of those approached) → 21 had a post-intervention interview.

**Inclusion criteria.** Age ≥65; expressing a need to connect more and better with other people; wishing to participate; having internet and computer/smartphone access.
**Exclusion criteria.** Blind or deaf; self-reported cognitive impairment.

**Sample.** N = 27. 74% female. Mean age 74.26 (range 66–88). 48% secondary education. 33% married or partnered.

**Intervention.** Groups of 6–8 participants plus 2 facilitators (all gerontologists; one a psychologist, the other a medical doctor or sociologist). Eight weekly sessions of 90–120 minutes via Zoom. Each session in two parts: (1) community approach — improving relationships with others, neighbourhood activities, socially significant activity; (2) individual approach through peer support — cognitive-behavioural techniques, positive coping, sense of purpose, reminiscence. Between-session activities assigned. Modular structure, explicitly adapted by facilitators to each group. Telephone/WhatsApp technical support available. Group allocation by schedule availability.

**Measurement mode.** Telephone interviews at T1 (pre) and T2 (post), administered by two members of the research team trained in item-based questionnaire administration. Assessors were not blinded and were not independent of the delivering team.

**Instruments.**
| Construct | Instrument | Range as stated in paper |
|---|---|---|
| Loneliness (primary outcome) | De Jong Gierveld 11-item | global 0–11 |
| — social subscale | | 0–5 |
| — emotional subscale | | 0–6 |
| Social support | OSSS-3 | 3–14 |
| Depressive symptoms | PHQ-8 | **3–24** (Methods) / **0–24** (Results) |
| Anxiety symptoms | GAD-7 | 0–21 |
| Quality of life | EQ-5D-5L descriptive (5 dimensions) | — |
| Perceived health | EQ VAS | 0–100 |
| Participant evaluation | single open-ended prompt at T2 | — |

**Analysis.** Two-level random-intercept mixed-effects linear models fitted by maximum likelihood (Stata SE 13, `mixed`), time point as within-participant repeated factor, participant ID as random factor. Unconditional models run first to justify the multilevel structure. **Models adjusted for sex**, because male/female proportions differed significantly between T1 and T2. Estimated means via `margins`. Two-sided tests, α = 0.05. Descriptives via χ² and Student's *t*; Cohen's *d* per Cohen (1988).

**Sample size calculation.** Based on a prior study with a similar profile; α 0.05, β <0.20, two-tailed, assumed SD 2.33, assumed 25% drop-out, ANOVA: minimum 20 subjects to detect a difference **≥1.7 units in loneliness** between pre and post. The paper does not state whether "loneliness" here means the 0–11 global score or a subscale.

**Time scale.** 8 weeks. No follow-up beyond the immediate post-intervention interview.

**What was not measured.**
- Any counterfactual condition.
- Any objective measure of social contact or network change (all social measures are self-report perception).
- Any outcome after week 8.
- Treatment fidelity or adherence to module content (the modular design explicitly permits facilitator variation, and no fidelity check is reported).
- A pre-specified single primary endpoint. Seven outcome families were tested; no multiplicity adjustment is reported.
- Blinded outcome assessment.

### DEFINITION–OPERATIONALIZATION CHECK [FAIL-CV-001, FAIL-CV-004]

**Object A — the central construct, loneliness.**
Definition given by the source (paraphrased; Introduction, para. 1): loneliness is the subjective feeling arising when the quantity and quality of one's social relationships fall short of what one wants; it is not the same as being alone. Following Weiss, the source treats loneliness as a two-dimensional construct with a **social** dimension (absence of a satisfying network, belonging, companionship, network size) and an **emotional** dimension (absence of an attachment figure, unachieved intimacy or confidence).

- **Operationalization retrieval basis: ITEMS-INFERRED.** The scale is named, cited, and its subscale scoring ranges are given, but the item text was not retrieved in this run.
- **Operationalization scope result: UNKNOWN.** Per [P1], ITEMS-INFERRED bars any coextensive/narrower/broader classification. **No scope-creep finding may be raised against the loneliness instrument in this run.**

**Object B — "completed the intervention."**
- Definition as used: the Abstract states that 21 participants completed the intervention, giving a 22% drop-out rate.
- Actual rule (Results, final para.): the post-intervention interview was administered to the 21 participants **who had completed at least one session**.
- **Operationalization retrieval basis: ITEMS-RETRIEVED.** The inclusion rule is stated in fetched text.
- **Operationalization scope result: broader.**
- Out-of-scope inclusion: participants attending as few as 1 of 8 sessions are counted as completers, and the 22% figure is computed on that basis. The informative attendance figure appears in the same paragraph: 81% attended ≥5 sessions.
- Record: **Definition-operationalization mismatch. Subtype: definitional scope creep.**
- MAP CONTENT, not a verdict.

### CONSTRUCT-ESTABLISHMENT CHECK [FAIL-CV-002, FAIL-CV-003]

**Trigger status: TRIGGERED.** The source escalates beyond a narrow efficacy claim in two places: the Abstract Conclusions (online interventions targeting vulnerable population sectors *can become essential* to lessen the pandemic's collateral consequences on social behaviour and mental health) and the Discussion (peer-support groups *might help* to reduce the burden of depression among older adults and its economic costs).

**Retrieval depth for this section: assessed from full text including the introduction; cited works NOT checked.**

| Property | Status | Basis |
|---|---|---|
| PREVALENCE | **ESTABLISHED-REPORTED** (study sample) / **UNKNOWN** (target population) | Discussion reports ~60% of the sample reporting loneliness, 44% moderate (de Jong 3–8), 15% severe (9–11). Population figures in the Introduction rest on citations that were not checked. Note an unresolved tension the source carries without comment: it cites European prevalence of 11.9% in older adults alongside a claim of nearly a third of individuals in developed countries. |
| FORM | **UNKNOWN** | Subscale scores are reported for the sample (emotional > social at baseline), but internal-consistency evidence sits in S2 Table, which was not retrieved. |
| DOMAIN | **ESTABLISHED-REPORTED** (partial, sample level) | The source explicitly separates social and emotional dimensions, reports both, and locates its effect in the emotional dimension only. |
| WRONGNESS | **N/A** | The construct is a subjective state, not a belief the source rates false. No wrongness claim is made. **[P2] not triggered; no grade assigned; strength gate not applicable.** |
| HARM | **UNKNOWN** | The Introduction asserts loneliness→mortality, morbidity, cognitive decline, impaired function/QoL, anxiety and depression, citing refs 3–12 including the team's own longitudinal work. Establishment is *present by citation*; the citations were not checked. Per [P1] the fallback is UNKNOWN, and any finding resting on it is PROVISIONAL and may not be load-bearing. |

**Handoff note to the prosecutor:** no property in this map carries ESTABLISHED-CITED, so the ESTABLISHED-CITED contested/uncontested split has **nothing to operate on** in this run. That is a retrieval limit, not a finding of absence. Do not convert it into one.

### PUBLICATION STATUS

Corrigendum / correction / retraction / expression of concern: **no notice displayed** on the publisher article page as fetched 2026-08-08. A Crossmark widget is present but was not queried; PubMed record was seen in search results without a correction flag. Recorded as: **no correction visible; not exhaustively checked.**

---

## FIELD 2 — STRONGEST CLAIM THE SOURCE ITSELF MAKES

**Verification state: FULL-TEXT-CONFIRMED**

The source states its claim at three different strengths in three different places. All three are recorded, per the rule requiring both hedged and unhedged versions where they differ.

**(a) Title — unhedged, causal.**
*Reducing loneliness and depressive symptoms in older adults during the COVID-19 pandemic: A pre-post evaluation of a psychosocial online intervention.*
The gerund asserts the reduction as accomplished and attributes it to the intervention. The subtitle discloses the design.

**(b) Abstract, Results — hedged, temporal, non-causal.**
Statistically significant (*p*<0.01) <q>decreases in emotional loneliness and depressive symptoms were observed following the intervention</q>.
This is the source's own careful formulation: *observed following*, not *caused by*. The hedge is preserved here exactly, per Rule 3.

**(c) Abstract, Conclusions — broad, modal, and not about this study's data.**
Interventions that overcome social-distancing restrictions via online tools and target vulnerable population sectors can become essential to lessen the pandemic's collateral consequences on social behaviour and mental health. (Paraphrased; Abstract/Conclusions.)
This sentence makes no reference to the study's sample, effect, or design. It is a general statement about an intervention class.

**(d) Conclusions section — intermediate.** Describes the study as having tested a promising online tool to reduce emotional loneliness and depressive symptoms, with high attendance and low drop-out, and states that an RCT on a larger sample is needed.

**Prominence asymmetry, established from the paper alone:** the body of the paper is careful — the Limitations section concedes the absence of a control group, the small sample, the preliminary status of the results, possible limits on clinical or practical significance, exclusion of the non-digital, and self-report bias. The title and the Abstract Conclusions do not carry any of that.

---

## FIELD 3 — WEAKER DEFENSIBLE CLAIM THE EVIDENCE ACTUALLY SUPPORTS

**Verification state: author reconstruction from Field 1**

In a single-arm, uncontrolled, unblinded sample of 27 self-selected, internet-equipped, help-seeking adults aged ≥65 recruited in Barcelona between October 2021 and January 2022 — of whom 21 provided post-intervention data — mean scores were lower at the post-intervention interview than at baseline on two of seven outcome families: the emotional-loneliness subscale (by 0.84 points on 0–6) and PHQ-8 depressive symptoms (by 2.30 points on 0–24), both *p*<0.01 in sex-adjusted mixed models. Global loneliness, social loneliness, social support, anxiety symptoms, quality of life, and perceived health did not change significantly. The intervention was deliverable online to this population: 81% attended at least 5 of 8 sessions, and participant feedback was positive.

Because the design contains no counterfactual, no randomisation, no blinding, no follow-up, and no pre-specified single primary endpoint, these differences cannot be separated from regression to the mean, spontaneous change, secular change in the pandemic context across the study window, repeated-assessment reactivity, demand characteristics arising from unblinded in-team assessors, non-specific effects of group contact, or differential attrition.

### ITEM TRACKING [FAIL-CV-001]

A definition-operationalization mismatch exists for **Object B** and its rule is ITEMS-RETRIEVED, so this field tracks the actual rule: *completion* means attendance at ≥1 of 8 sessions, and the 22% drop-out figure is computed on that definition.

For **Object A** and all other instruments the basis is ITEMS-INFERRED, so the **item-level defensible claim is UNKNOWN pending item retrieval**. Nothing in this field should be read as a claim about what the scale items do or do not capture.

---

## FIELD 4 — BROADER CLAIM ATTACHED DOWNSTREAM

**FIELD 4 STATUS: PROVISIONAL**

**Provenance state: NONE FOUND — retrieval-limited.**

Searches run in this session:
1. `"Breaking Loneliness, Opening Community" BLOC older adults intervention`
2. `Gabarrell-Pascuet 2024 PLOS ONE loneliness online intervention cited by`

Neither returned a downstream restatement of this source. Search 2 returned the article record itself, the PubMed record, an author profile listing, and PubMed "similar articles" panels in which this paper appears as a *related item* — not as a citation carrying a claim. One Catalan-language institutional article on intergenerational activities cites a different Gabarrell-Pascuet paper (2023), not this one.

**SUPPLIED items: none.** The operator supplied the target URL and the two prompts, with no downstream material and no framing claim. The claim-that-prompted-the-audit field is therefore empty; the map runs on the source's own claims.

**RECALLED items: none.** No downstream restatement of this paper is being reported from memory. This is stated explicitly rather than left implicit, and no parenthetical about "wide restatement in the literature" is being appended.

**Which limitation this reflects.** **Absence of retrieval capability, not established absence of downstream use.** No citation index was queried — no Scopus, Web of Science, Google Scholar, Dimensions, or PubMed cited-by. No Catalan- or Spanish-language institutional press-release search was completed beyond the two queries above. The paper is ~20 months old and is a small feasibility pilot, so low citation is plausible, but plausibility is not a retrieval.

**Attribution check:** not run. No downstream item exists to run it on. MISATTRIBUTED, ATTRIBUTED ELSEWHERE, and SYNTHESIS ATTRIBUTION are all **unassigned**, not cleared.

### FIELD-SPECIFIC PROVISIONAL ASSIGNMENT

- **Field 4 — PROVISIONAL.** Cannot distinguish "no downstream use exists" from "not retrieved."
- **Field 5 — PARTIALLY PROVISIONAL.** The downstream component is provisional. The within-source component (prominence asymmetry between title/abstract-conclusions and the body) is established from the paper alone and is **not** provisional.
- **Field 6 — NOT PROVISIONAL.** It targets the source's own claim and needs no downstream material.

---

## FIELD 5 — WHERE THE INFLATION BEGINS

### REQUIRED ANCHORING TABLE

| Item | Provenance state | Quotation present? | Locator present? | Attribution cross-source-confirmed? | Anchor eligibility |
|---|---|---|---|---|---|
| Title, as published | RETRIEVED | yes (title as identifier) | yes — PLOS ONE 19(12):e0311883, article page | N/A | **ELIGIBLE** |
| Abstract/Results sentence on observed decreases | RETRIEVED | yes (12-word quotation, Field 2b) | yes — Abstract, Results | N/A | **ELIGIBLE** |
| Abstract/Conclusions escalation sentence | RETRIEVED | **no — quotation withheld by executor constraint** | yes — Abstract, Conclusions | N/A | **NOT ELIGIBLE — quotation missing.** Retained in Field 2 as context; does not anchor Field 5. |
| Discussion mechanism passage (group supplied closeness absent from existing networks) | RETRIEVED | no — paraphrased | yes — Discussion, para. 3 | N/A | **NOT ELIGIBLE — quotation missing.** Context only. |
| Limitations section concessions | RETRIEVED | no — paraphrased | yes — Strengths and limitations | N/A | **NOT ELIGIBLE — quotation missing.** Context only; counts *against* a harsher classification, not for one. |
| Any downstream restatement | NONE FOUND | — | — | — | none exist to rate |

Provenance is preserved on every row. No item was relabelled RECALLED for failing the sufficiency check.

### 5A — WITHIN-SOURCE INFLATION POINT

**Established. Verification state: FULL-TEXT-CONFIRMED. Failure location: PAPER.**

Three distinct moves, each anchored on the two eligible items:

**Move 1 — inferential upgrade.**
"Decreases were observed following the intervention" (Abstract/Results) → "Reducing loneliness and depressive symptoms" (Title).
Association-in-time becomes reduction-by-intervention. The design supplies no counterfactual from which the second could follow.

**Move 2 — construct substitution.**
"The emotional-loneliness subscale decreased; global and social loneliness did not" (Results; Discussion states plainly that no significant change occurred in social support or social loneliness) → "loneliness" unqualified (Title; Conclusions).
One dimension of a construct the paper itself defines as two-dimensional stands in for the whole.

**Move 3 — scope escalation.**
Result in 21 completers from one city → online interventions for vulnerable population sectors *can become essential* to lessen the pandemic's collateral consequences on social behaviour and mental health (Abstract/Conclusions).
The sentence contains no reference to the study's sample, effect size, or design. Note: this move is recorded as *context* only, because its anchoring item is not quotation-eligible under this run's constraint. The move is visible; the anchor is not formally sufficient.

**Where it is not.** The Limitations section names the control-group absence, the small sample, the preliminary status, and possible limits on clinical significance; the Conclusions call for an RCT. The inflation is located in **packaging — title and abstract-level conclusions — not in the paper's own account of its methods or its self-assessment.** Do not classify this as a paper that hides its design.

### 5B — DOWNSTREAM INFLATION POINT

**Not established. Not assessed.**

No downstream layer is assigned. Under the SUSPECTED wording rule: no layer is even marked SUSPECTED, because no anchor-eligible or recalled downstream item exists in either direction. What would settle it: a citation-index query (Scopus / Web of Science / Google Scholar / PubMed cited-by) for works citing DOI 10.1371/journal.pone.0311883, plus a Catalan/Spanish institutional press-release search for Sant Joan de Déu, UVic-UCC, and CIBERSAM.

---

## CLAIM INVENTORY

| Claim | Quantified? | Why it might be inflated downstream | Selected for Field 6? |
|---|---|---|---|
| 1. The intervention reduced emotional loneliness by 0.84 points (0–6), *p*<0.01 | **Yes** | Title generalises a subscale to "loneliness"; no control group; the number is small relative to the difference the study was sized to detect | **YES** |
| 2. The intervention reduced depressive symptoms by 2.30 points on PHQ-8 (0–24), *p*<0.01 | Yes | Same causal gap; statistical significance may be read as clinical significance; the source itself flags limited practical significance | Deferred |
| 3. The intervention is feasible and acceptable (22% drop-out, 81% attended ≥5 sessions, positive feedback) | Partly | "Completed" is defined as ≥1 session; acceptability may be read as efficacy | Deferred |
| 4. Online interventions targeting vulnerable sectors can become essential to lessen the pandemic's mental-health consequences | No | General policy claim untethered from the study's data; the most portable sentence in the paper | Deferred |
| 5. Emotional loneliness fell because the group supplied closeness and emotional support their existing networks did not | No | A mechanism asserted post hoc, consistent with but not tested by the data | Deferred |
| 6. Female over-representation reflects a closing digital gender gap | No | Post-hoc explanation of a sampling feature | Deferred |

**Selection rationale for Field 6.** Rule 2 requires the most precisely quantified version where one exists. Claims 1 and 2 are both quantified; claim 1 is selected over claim 2 because loneliness is the paper's stated **primary** outcome, the title's construct-level assertion attaches to it, and the subscale/whole-construct substitution is demonstrable against retrieved text rather than arguable. Claims 3–6 are **DEFERRED, not dismissed** — a second run of the sequence audits them. Claim 4 in particular is the one most likely to travel, and should be run.

---

## FIELD 6 — CLAIM UNDER AUDIT

**The BLOC online psychosocial group intervention reduced emotional loneliness in adults aged ≥65, by 0.84 points on the De Jong Gierveld emotional-loneliness subscale (0–6), *p*<0.01.**

One claim only. Target layer: **source claim (PAPER)**. This is the source's own claim, so findings about it are findings about the source document. Not provisional.

---

## REQUIRED OUTPUT TABLE

| Field | Content | Verification state |
|---|---|---|
| 1. Literally measured | Single-arm pre-post, N=27 (21 post), ≥65, Barcelona, Oct 2021–Jan 2022; 8 weekly Zoom group sessions; telephone self-report on De Jong Gierveld 11-item, OSSS-3, PHQ-8, GAD-7, EQ-5D-5L/VAS; sex-adjusted two-level mixed models | FULL-TEXT-CONFIRMED (Tables 1–2 not retrieved) |
| 2. Source's strongest claim | Title asserts reduction causally; Abstract/Results states decreases *observed following*; Abstract/Conclusions escalates to intervention-class policy | FULL-TEXT-CONFIRMED |
| 3. Weaker defensible claim | Scores on 2 of 7 outcome families were lower at T2 than T1 in this uncontrolled sample; intervention was deliverable with 81% attending ≥5 sessions; no causal attribution available | author reconstruction from Field 1 |
| 4. Downstream claim | None retrieved | NONE FOUND — retrieval-limited; PROVISIONAL |
| 5A. Within-source inflation + failure location | Hedged result → causal title; subscale → "loneliness"; N=27 pilot → intervention-class policy. **PAPER** | FULL-TEXT-CONFIRMED |
| 5B. Downstream inflation + failure location | Not assessed; no layer assigned or suspected | PROVISIONAL |
| 6. Claim under audit | The intervention reduced emotional loneliness by 0.84 points (0–6), *p*<0.01 | FULL-TEXT-CONFIRMED |

## REQUIRED CONSTRUCT-SIDE HANDOFF SUB-SCHEMA

| Check | Object | Retrieval status / basis | Result | Verification state | Evidence |
|---|---|---|---|---|---|
| Construct establishment | PREVALENCE | ESTABLISHED-REPORTED (sample) / UNKNOWN (population) | ~60% of sample reporting loneliness, 44% moderate, 15% severe; population figures rest on unchecked citations and carry an unreconciled 11.9% vs. "nearly a third" tension | FULL-TEXT-CONFIRMED (sample) / PROVISIONAL (population) | Discussion, para. 3; Introduction, para. 2 |
| Construct establishment | FORM | UNKNOWN | Subscale distribution reported; internal consistency sits in unretrieved S2 Table | PROVISIONAL | Results; S2 Table not retrieved |
| Construct establishment | DOMAIN | ESTABLISHED-REPORTED (partial) | Two dimensions explicitly separated, both measured, effect located in the emotional dimension only | FULL-TEXT-CONFIRMED | Introduction para. 1; Results; Discussion |
| Construct establishment | WRONGNESS | N/A | No belief-falsity claim is made about the construct | N/A | — |
| Construct establishment | HARM | UNKNOWN | Asserted by citation (refs 3–12); citations not checked. Load-bearing for deferred claim 4, **not** for Field 6 | PROVISIONAL | Introduction, paras. 2–4 |
| Definition-operationalization | De Jong Gierveld 11-item (loneliness) | ITEMS-INFERRED | UNKNOWN | PROVISIONAL | Instruments section names scale and ranges; items not retrieved |
| Definition-operationalization | "completed the intervention" | ITEMS-RETRIEVED | **broader** — subtype: definitional scope creep | FULL-TEXT-CONFIRMED | Abstract vs. Results final para. (≥1 session) |
| Grade-before-assert | — | — | **not triggered** | N/A | No wrongness or pathologization claim exists. **[P2] strength: not applicable** (not VOID — the check does not fire at all) |

---

## SUMMARY LINES

- **CLAIM UNDER AUDIT:** The BLOC online psychosocial group intervention reduced emotional loneliness in adults aged ≥65 by 0.84 points on the De Jong Gierveld emotional subscale (0–6), *p*<0.01.
- **WITHIN-SOURCE FAILURE LOCATION:** paper — FULL-TEXT-CONFIRMED.
- **DOWNSTREAM FAILURE LOCATION:** not assessed — NONE FOUND, retrieval-limited, PROVISIONAL.
- **GAP TYPE:** source overclaims (in title and abstract-level conclusions, not in body); downstream not assessed.
- **MAP CONFIDENCE:** moderate. Raised by: Tables 1–2 from the PDF (means, SDs, CIs, exact Cohen's *d*), S1 Fig CONSORT, S2 Table alphas, De Jong Gierveld item text, and a citation-index query for downstream use.

---

## HANDOFF

This map goes to the prosecutor unchanged. The prosecutor audits **Field 6 only**. Deferred claims 2–6 require separate runs. Two constraints travel with the map and must not be silently discarded downstream:

1. All instrument-level operationalization is **ITEMS-INFERRED → UNKNOWN**. No scope-creep or pathologization finding may be raised against any scale in this run.
2. All construct properties are either sample-level ESTABLISHED-REPORTED or **UNKNOWN**. **No property carries ESTABLISHED-CITED**, so the prosecutor's contested/uncontested split has nothing to operate on. That is a retrieval limit and must not be converted into a finding of absence.
