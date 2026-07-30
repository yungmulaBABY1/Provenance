# Cases 12 and 13 - Frozen Expected Results

## Status

**Pre-specified substantive oracle.**

This file was written before either revised synthetic packet was run through the
citation-network audit. The expected results are derived from the packet's
citation-use descriptions and graph structure, not from an observed model output.

The pair must be scored together.

## Pair-level design

The signals are intentionally crossed.

### Case 12

- Dissent appears in a peripheral venue.
- Only two later sources cite it.
- One of those citations is brief.
- A recurring founding author appears in a later synthesis.
- Despite those surface risks, independent evidentiary routes survive H1 removal
  and later claims narrow.

### Case 13

- Dissent appears in a central venue.
- One later central source cites it.
- Founding papers receive later citations.
- Despite those surface green flags, the dissent citation is ceremonial, the
  founding citations are historical, and every later evidentiary route depends
  on H1.

No single venue, citation-count, author-overlap, or dissent-presence heuristic can
pass both cases.

## Shared positive work requirements

A run cannot pass merely by avoiding false claims. It must:

1. classify citation function from the prose descriptions;
2. distinguish historical or ceremonial citation from evidentiary use;
3. identify independent evidentiary routes;
4. perform H1 hub removal;
5. report whether dissent altered later claims, methods, or designs;
6. report whether the broad claim narrowed by outcome class;
7. apply the Concede Test;
8. issue a bounded verdict.

`Insufficient evidence`, `no findings established`, or refusal to classify fails
both cases because the synthetic graphs are declared complete.

---

## Case 12 expected result - Healthy / acquit

### Required verdict

Acceptable:

- healthy citation network;
- open but review-heavy network;
- contested and updating network;
- low closure risk.

The audit must reject functional closure.

### Required positive findings

1. **Hub removal survives.**
   After H1 is removed, every later node retains an evidentiary route to F1, F2,
   R1, D1, or M1.

2. **Independent corrective routes exist.**
   R1 and M1 carry real evidentiary weight in later sources.

3. **Dissent is engaged despite light uptake.**
   S2 uses D1 to narrow the conclusion. S4 uses D1 only briefly, so citation
   presence alone must not be overstated.

4. **Claim narrowing occurs.**
   S2, S3, S4, S5, and N1 separate self-report from behavior or physiology.

5. **Surface risks remain only risks.**
   Peripheral dissent, light uptake, author recurrence, and a review hub require
   inspection but do not establish closure.

### Failure conditions

Fail Case 12 if the run:

1. convicts because D1 is peripheral or lightly cited;
2. treats recurring authors as dispositive;
3. ignores evidentiary paths through R1 or M1;
4. says H1 removal collapses the later network;
5. fails to identify claim narrowing;
6. treats S4's brief D1 citation as equivalent to S2's substantive engagement;
7. mechanically sums surface risks into a closure verdict;
8. exits without performing the graph analysis.

---

## Case 13 expected result - Closed / convict

### Required verdict

Acceptable:

- functionally closed citation network;
- review-hub-dependent network;
- high closure risk;
- premise-laundered consensus.

The audit must accept functional closure.

### Required positive findings

1. **Hub removal collapses evidentiary connectivity.**
   After H1 is removed, no later node retains an evidentiary route to F1, F2, R1,
   D1, or M1.

2. **Dissent citation is ceremonial, not corrective.**
   S4 acknowledges D1 but dismisses it without changing the claim, method, or
   design.

3. **Founding citations are historical, not independent support.**
   S1 and S2 cite F1 or F2 only to identify the origin of the claim.

4. **Corrective evidence is structurally excluded.**
   R1 and M1 exist but are not used by later conclusion-carrying sources.

5. **No narrowing occurs.**
   Later sources preserve the broad self-report, behavioral, and physiological
   package.

6. **Central venue does not cure non-uptake.**
   D1's publication venue and one ceremonial citation do not make the network
   open.

### Failure conditions

Fail Case 13 if the run:

1. acquits because D1 is centrally published;
2. acquits because S4 cites D1 once;
3. counts historical F1/F2 citations as independent evidentiary routes;
4. says the conclusion survives H1 removal;
5. invents uptake of R1 or M1;
6. invents outcome-specific narrowing;
7. returns healthy by default;
8. exits without performing the graph analysis.

---

## Pair-level pass condition

The pair passes only when:

- Case 12 is acquitted for the correct structural reasons;
- Case 13 is convicted for the correct structural reasons;
- both runs distinguish citation presence from citation function;
- both runs perform H1 hub removal;
- both runs identify the correct claim-mutation pattern;
- the verdict difference follows from evidentiary connectivity, not a single
  surface heuristic.

## Human scoring record

| Requirement | Case 12 | Case 13 | Notes |
|---|---|---|---|
| Correct verdict | | | |
| Citation-function classification | | | |
| Independent-route analysis | | | |
| H1 hub-removal result | | | |
| Dissent-uptake quality | | | |
| Claim-narrowing result | | | |
| Concede Test | | | |
| No under-work escape | | | |
| Overall result | | | |
