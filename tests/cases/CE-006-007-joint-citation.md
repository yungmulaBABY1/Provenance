# Case CE-006 / CE-007 — Joint Citation, Paired

**Closes:** FAIL-CE-006 (attribution check exonerated the clearest laundering)
and FAIL-CE-007 (MISATTRIBUTED fired on a document that disambiguates elsewhere).

**Target prompt:** `prompts/1-claim-extraction.txt`, Field 4.

**Run both. Same run, same model, both documents.** Order does not matter; run
them back to back.

---

## WHY PAIRED

Same structure, opposite correct answer.

Built separately, either can be passed by pattern-matching: a run that classifies
every joint citation as MISATTRIBUTED passes CE-007 and fails CE-006. A run that
clears every joint citation because a successor exists passes CE-006 and fails
CE-007. **Only a run that actually performs the document-level check gets both.**

A run that passes one and fails the other has not learned the rule — it has
learned a default.

---

## SHARED SETUP

Both variants use the same audited source and the same successor. Only the citing
document differs.

### The audited source

> **Okonkwo, A. & Reyes, M. (2019).** "Sensor-derived gait asymmetry in
> community-dwelling adults aged 65–74." *Journal of Applied Gerontology* 38(4),
> 511–526.
>
> Abstract excerpt: "Accelerometer-derived gait asymmetry was measured in 412
> community-dwelling adults aged 65–74 across two urban sites over 18 months.
> Asymmetry index above 4.2% was associated with a 1.9-fold increase in
> non-syncopal falls (95% CI 1.3–2.8). **We do not extend these findings beyond
> the 65–74 band; sample size above age 74 was insufficient for stratified
> analysis.**"

### The successor

> **Okonkwo, A., Reyes, M. & Halvorsen, T. (2022).** "Extending gait-asymmetry
> fall prediction to adults aged 75 and above." *Journal of Applied Gerontology*
> 41(2), 188–203.
>
> Abstract excerpt: "We extend Okonkwo & Reyes (2019) to 1,140 adults aged 75–89.
> The asymmetry–fall association persists, with a 2.4-fold increase above the 4.2%
> threshold."

**Scope arithmetic:** the 2019 paper measures ages 65–74 and explicitly declines
to extend. Any downstream claim covering 75+ requires the 2022 paper.

---

## CE-006 — Document DISAMBIGUATES elsewhere

### The citing document

> **National Falls Prevention Advisory Panel (2023), "Screening Recommendations
> for Older Adults," Section 3.**
>
> The evidence base for gait-asymmetry screening developed in two stages. The
> initial study established the association in a younger-old cohort aged 65–74
> (Okonkwo & Reyes 2019); a subsequent analysis extended it to adults aged 75 and
> above (Okonkwo et al. 2022).
>
> [...four paragraphs on implementation...]
>
> The basic conclusion of Okonkwo et al. (2019, 2022) is that sensor-derived gait
> asymmetry above 4.2% predicts elevated fall risk across the older-adult
> population. The Panel therefore recommends asymmetry screening at routine visits
> for all patients aged 65 and above.

### Expected result — CE-006

**Written before running. Do not revise after.**

- Field 4 records the "across the older-adult population" restatement as
  **RETRIEVED**, with the citing sentence quoted and located.
- Attribution check runs: could the 2019 paper alone support a claim covering
  all older adults? **No** — it measures 65–74 and declines to extend.
- Second question runs: who is cited? **Both, jointly.**
- **Document-level check runs and finds the earlier paragraph disambiguating the
  two studies' age bands.**
- Classification: **SYNTHESIS ATTRIBUTION — not MISATTRIBUTED.**
- Verification state: **CROSS-SOURCE-CONFIRMED.**
- Field 5 does **not** assign CITATION as a failure location on the basis of this
  item.

**Pass condition:** classification is synthesis attribution, AND the output states
that the document distinguishes the scopes elsewhere.

**FAIL conditions:**

1. Classified MISATTRIBUTED. *(Sentence-level rule — the FAIL-CE-007 failure.)*
2. Classified correctly but with no stated document-level search. *(Right answer,
   wrong reason — will not generalize.)*
3. Classified ATTRIBUTED ELSEWHERE without noting the joint citation. *(Missed
   that the audited source is cited at all.)*
4. Field 5 assigns a CITATION failure location on this item.

---

## CE-007 — Document does NOT disambiguate

### The citing document

Identical **except** the disambiguating paragraph is absent.

> **Regional Health Authority (2023), "Falls Screening Protocol," Section 2.**
>
> Falls remain the leading cause of injury-related hospitalization among older
> adults in the region, accounting for 31% of admissions in the 65+ cohort.
> Current screening relies on self-reported history and clinical observation,
> both of which perform poorly in ambulatory populations.
>
> Sensor-derived gait asymmetry offers an objective alternative. Okonkwo & Reyes
> (2019) demonstrated that asymmetry above 4.2% predicts elevated fall risk
> across the older-adult population, including the oldest-old, where fall
> consequences are most severe.
>
> The Authority therefore recommends asymmetry screening at routine visits for all
> patients aged 65 and above.

### Expected result — CE-007

**Written before running. Do not revise after.**

- Field 4 records the restatement as **RETRIEVED**, citing sentence quoted and
  located.
- Attribution check: could the 2019 paper support "across the older-adult
  population, including the oldest-old"? **No** — 65–74 only, explicitly declines
  to extend.
- Who is cited? **The audited source ALONE.** The successor is not cited anywhere
  in the document.
- Document-level check runs and finds **no disambiguation** — the document never
  mentions the 2022 study or the age-band limitation.
- Classification: **MISATTRIBUTED.**
- Verification state: **CROSS-SOURCE-CONFIRMED.**
- Field 5 **may** assign CITATION as a failure location on this item — it is
  RETRIEVED, quoted, and located, so it clears the anchoring rule.

**Pass condition:** classified MISATTRIBUTED, with the citing sentence quoted and
the absence of disambiguation stated.

**FAIL conditions:**

1. Classified ATTRIBUTED ELSEWHERE because a successor exists that could support
   the claim. **This is the FAIL-CE-006 failure — the loophole that exonerates
   the clearest laundering.** Most serious failure available in this case.
2. Classified SYNTHESIS ATTRIBUTION. *(No joint citation exists — the successor
   is not cited at all.)*
3. Classified correctly but with no stated document-level search.
4. Recorded without a quoted citing sentence.

---

## PAIRED SCORING

| CE-006 | CE-007 | Reading |
|---|---|---|
| Synthesis | MISATTRIBUTED | **PASS.** Document-level check is functioning. |
| MISATTRIBUTED | MISATTRIBUTED | Sentence-level default. FAIL-CE-007 unrepaired. |
| Synthesis | Synthesis / ATTRIBUTED ELSEWHERE | Successor-exists default. FAIL-CE-006 unrepaired — the more dangerous direction. |
| MISATTRIBUTED | Synthesis | Inverted. Investigate before patching; likely a case-construction error. |

**Only the first row passes.** Record both results in `tests/RESULTS.md` even when
one variant passes alone — a split result is the informative outcome.

---

## WHAT A FAILURE MEANS

**Both MISATTRIBUTED:** the document-level check is not running, or is running and
being ignored. Look at whether the output states a search of the citing document.
If it does not, the check is decorative.

**Both cleared:** the second question ("who is cited for it?") is not being asked.
The run is stopping at "who supports it," which is exactly FAIL-CE-006. Highest
severity — this direction produces false negatives on real laundering.

**Correct answers, no stated reasoning:** the run may be pattern-matching on
surface features — presence or absence of a second citation. Vary the surface
(cite the successor in an unrelated context in CE-007) and re-run.

---

## RUN LOG

| Date | Prompt ver | Model | CE-006 | CE-007 | Paired result | Notes |
|---|---|---|---|---|---|---|
| | | | | | | |

Run on at least two models. A single-model pass on a paired case is weaker than
it looks — both documents come from the same author and may share a tell.
