# Case MIX-01 — Mixed Control, Research Branch

```
Closes:      GUARD-002 (partial), and tests the claim inventory (untested)
Target:      prompts/1-claim-extraction.txt → research-analysis chain
Control:     MIXED
```

**The hardest control and the most diagnostic.** Tests whether the system
separates claims rather than assigning a global good-paper / bad-paper verdict.

**Newly testable.** Before the claim inventory, only one claim entered the
pipeline, so a mixed result was structurally impossible. This is therefore a
direct test of the multi-claim work.

---

## WHAT IT TESTS

One source, three claims of deliberately different quality:

| Claim | Should return |
|---|---|
| **C1** — measurement claim, scoped, well-supported | SOUND / no consequential finding |
| **C2** — generalization beyond the sampled population | NARROWS, material |
| **C3** — causal claim the design cannot support | DEFEATS |

**A run that returns one verdict for "the paper" has failed**, whatever that
verdict is. The failure mode is not being too harsh or too lenient — it is
collapsing three distinguishable claims into one.

---

## THE SOURCE

Synthetic. Fictional, so no reputation leaks in.

---

> **Vasquez, R., Lindqvist, P. & Oyelaran, D. (2024).** "Break-timing patterns and
> error rates among air-traffic control trainees." *Human Factors in Transport*
> 19(3), 244–261.
>
> **Abstract.** We instrumented training consoles at three regional academies to
> record break timing and simulated-conflict error rates for 218 trainees over 14
> months. Trainees taking a break within 90 minutes of shift start showed a 22%
> lower simulated-error rate than those breaking later (95% CI 11–33%). The effect
> persisted after adjustment for shift length, time of day, and cohort. **Early
> breaks reduce error rates in controllers.** These findings indicate that
> mandating early breaks would lower operational incidents across the controller
> workforce.
>
> **Methods (excerpt).** Participants were trainees at three regional academies,
> enrolled in the 14-month basic certification programme. Mean age 24.3 (SD 3.1).
> All were in the first six months of console training. Error rate was defined as
> simulated conflicts not resolved within the scenario window, recorded
> automatically. Break timing was recorded by console logout. **Break timing was
> not assigned; trainees chose when to break.** Adjustment covariates were shift
> length, time of day, and academy cohort.
>
> **Results (excerpt).** Early-break trainees: 4.1 errors per 100 scenarios.
> Late-break trainees: 5.3 (p = 0.003). Adjustment attenuated the difference
> slightly (22%, from 23% unadjusted). We did not collect data on sleep, prior
> shift work, or caffeine intake.
>
> **Discussion (excerpt).** Our sample is restricted to trainees in early console
> training; we did not sample certified controllers, and workload profiles differ
> substantially between training and operational environments. **We note that
> break timing was self-selected, and trainees who break early may differ
> systematically from those who do not.**

---

## THE THREE CLAIMS

**C1 — measurement, scoped.** Among trainees at three academies, self-selected
early breaks were associated with a 22% lower simulated-error rate after
adjustment for three covariates.

*Defensible.* The measurement matches the claim. Scope is stated. The paper
reports the unadjusted figure, names its uncovered confounders, and flags
self-selection in the discussion.

**C2 — generalization.** "Early breaks reduce error rates **in controllers**."

*Overreaches.* The sample is trainees in the first six months of console work.
The paper's own discussion states it did not sample certified controllers and
that workload profiles differ substantially. The abstract drops that limitation.

**C3 — causal / policy.** "Mandating early breaks would lower operational
incidents across the controller workforce."

*Not supported.* Break timing was self-selected, not assigned. The paper says so.
An association under self-selection cannot support a mandate's effect, and the
outcome shifts from simulated errors to operational incidents — a construct the
study never measured.

---

## EXPECTED RESULT

**Written before running. Do not revise after.**

### Stage 1 — claim map

- **Claim inventory lists all three.** C1, C2, C3, each one sentence, quantified
  or not, with a suspicion note.
- **Field 6 selects C1** — the most precisely quantified version (22%, CI 11–33,
  p = 0.003). RULE 2.
- C2 and C3 recorded **DEFERRED, not dismissed**, with a note that C3 is the most
  suspect.
- Field 4: no downstream material exists. **NONE FOUND**, or PROVISIONAL with the
  reason stated — *no downstream use retrieved* vs. *no retrieval capability*.
- **Attribution apparatus returns empty.** No successor, no assessment trail. If
  MISATTRIBUTED, ATTRIBUTED ELSEWHERE, or joint-citation disambiguation appear at
  all, that is MBH98 overfit showing.
- Field 5, within-source: the **abstract/discussion asymmetry** — the abstract
  says "in controllers" and asserts a mandate effect; the discussion states the
  trainee limitation and the self-selection problem. That is a real within-source
  finding and should be located as PAPER.

### Stage 2 — construct validity on C1

- Findings, if any, rated **SURVIVES** under the concede test.
- Uncovered confounders (sleep, prior shift work, caffeine) are **limitations**,
  disclosed by the paper. Concede them and C1 still stands.
- **Verdict: SOUND, or the equivalent letter for "valid evidence for the claim."**
- If the run rates C1's limitations MAJOR, the concede test is not capping.

### Stage 2 — construct validity on C2 *(second run, or via inventory)*

- Population mismatch: trainees ≠ certified controllers.
- Concede test: **NARROWS**, scope-loss **MATERIAL**.
- Surviving claim: early breaks associated with lower simulated error **among
  trainees in early console training**.
- **Verdict: the "useful for a narrower claim" letter.**

### Stage 2 — construct validity / internal validity on C3

- Self-selected exposure. Outcome construct shift (simulated errors → operational
  incidents). Population mismatch compounding.
- Concede test: **DEFEATS.**
- **Verdict: invalid for the stronger claim.**

### Counter-audit

- **E0 finds the paper's own pre-emptions** and recharacterizes accordingly. The
  paper discloses self-selection, names its uncovered confounders, reports the
  unadjusted figure, and states the trainee limitation.
- Findings about C2 and C3 should come back **RECHARACTERIZED**, not DEFEATED —
  the charge is not "they concealed it" but "they disclosed it in the discussion
  and asserted past it in the abstract."
- That distinction is the point. A run that treats the limitations as hidden has
  not read the discussion.

---

## PASS CONDITION

**Three distinguishable outcomes, one per claim.** C1 clears, C2 narrows, C3 fails.

Not required: that the verdict letters match exactly. Required: that the three
claims **do not receive the same verdict**, and that the ordering is C1 > C2 > C3
in defensibility.

---

## FAIL CONDITIONS

1. **One global verdict for "the paper."** The core failure. The inventory is
   decorative, or downstream stages ignore it.

2. **C1 rated MODERATE or worse.** Disclosed limitations escalated into findings
   because the workflow expects findings. This is the template failure.

3. **C3 rated NARROWS rather than DEFEATS.** Self-selected exposure plus an
   unmeasured outcome construct cannot support a mandate effect. If that only
   narrows, the concede test is not discriminating at the top end.

4. **Inventory omits a claim**, or lists all three and Field 6 selects C3 because
   it is the most inflated. Field 6 targets the *quantified* claim (RULE 2), not
   the most attackable one.

5. **Attribution machinery fires.** MISATTRIBUTED, ATTRIBUTED ELSEWHERE, or
   joint-citation analysis on a source with no successor and no downstream trail
   is MBH98 overfit.

6. **E0 returns all UNAFFECTED.** The paper pre-empts three separate critiques in
   its own discussion. A run finding none has not searched.

7. **C2 and C3 collapsed into one finding.** They are different failures —
   population mismatch versus causal identification — and merging them hides that
   C2 survives in narrowed form while C3 does not survive at all.

---

## WHAT EACH FAILURE MEANS

**Fail 1:** the claim inventory produces a list nothing downstream consumes. Check
whether prosecutor finding tables carry a claim ID at all. This is the multi-claim
scope work in TODO.md — if the case fails here, that work is required, not
optional.

**Fail 2:** the concede test is not capping. Compare against case 11 — if both
fail, the problem is general; if only this one fails, it is specific to research
prompts, which have never been tested for acquittal.

**Fail 3:** the concede test discriminates at the bottom (SURVIVES vs. NARROWS)
but not at the top (NARROWS vs. DEFEATS). Look at whether the scope-loss
assessment's NEAR-DEFEAT tier is being used.

**Fail 5:** the map has learned MBH98's shape. This is the overfit warning in
tests/RESULTS.md, confirmed.

**Fail 6:** E0 is running as ceremony. Check whether it lists sections searched.

---

## RUN LOG

| Date | Prompt ver | Model | C1 | C2 | C3 | Separated? | Notes |
|---|---|---|---|---|---|---|---|
| | | | | | | | |

Run on at least two models.

**Note on execution:** the sequence targets one claim per run. Either run it three
times with different Field 6 selections, or run once on C1 and check that the
inventory correctly flags C2 and C3 as deferred with accurate suspicion notes.
The second is cheaper and tests the inventory directly; the first tests the full
per-claim verdict separation. Do the cheap one first.
