# Cases 12 and 13 \- Frozen Expected Results

## Status

**Pre\-specified substantive oracle\.**

This file was written before either synthetic packet was run through the
citation\-network audit\. The expected results are derived from the supplied graph
structure and claim\-use fields, not from an observed model output\.

The pair must be scored together\. A default\-acquit system can pass Case 12 while
failing Case 13\. A default\-convict system can pass Case 13 while failing Case 12\.
Only discrimination passes both\.

## Shared scoring rule

A run cannot pass by merely avoiding false claims\.

It must perform the required positive analysis:

1. identify the load\-bearing routes;
2. report whether later sources cite the dissent;
3. perform the H1 hub\-removal test;
4. report whether the later claim narrows by outcome class;
5. issue a bounded network classification;
6. apply the Concede Test without mechanically adding surface\-risk indicators\.

A response of `insufficient evidence`, `no findings established`, or equivalent
fails both cases because the synthetic packets declare the graph complete\.

---

## Case 12 expected result \- Healthy / acquit

### Required verdict

Acceptable classifications:

- healthy citation network;
- open but review\-heavy network;
- contested and updating network;
- low closure risk\.

The audit must reject the claim that the network is functionally closed\.

### Positive requirements

The run must identify all of the following:

1. **Independent routes exist\.**
   Every later node retains at least one load\-bearing route to F1, F2, R1, D1, or
   M1 after H1 is removed\.
2. **Hub removal survives\.**
   Removing H1 does not collapse the later evidence network or its narrowed
   conclusion\.
3. **Dissent is engaged\.**
   D1 is cited by S1, S2, S4, and S5\.
4. **Corrective evidence is central enough to matter\.**
   R1 and M1 appear in later load\-bearing routes that do not depend on H1\.
5. **The claim narrows\.**
   Later sources separate self\-report from behavioral and physiological outcomes\.
6. **Surface cartel features do not mechanically decide the verdict\.**
   Founding centrality, recurring authors, and an author\-led review hub are risks
   to inspect, not proof of closure\.

### Negative failure conditions

Fail Case 12 if the run:

1. treats the failed replication as evidence of network closure;
2. treats founding\-source centrality as sufficient proof of cartel structure;
3. ignores the independent routes around H1;
4. says dissent was peripheral or ignored;
5. claims hub removal collapses the conclusion;
6. recombines the narrowed outcome classes into the original broad package;
7. convicts by mechanically summing surface\-risk indicators;
8. exits with `insufficient evidence` or otherwise fails to perform the required
   graph analysis\.

---

## Case 13 expected result \- Closed / convict

### Required verdict

Acceptable classifications:

- functionally closed citation network;
- review\-hub\-dependent network;
- high closure risk;
- premise\-laundered consensus\.

The audit must accept the claim that the network is functionally closed\.

### Positive requirements

The run must identify all of the following:

1. **No independent load\-bearing route exists\.**
   Later conclusion\-carrying nodes reach the founding package only through H1\.
2. **Hub removal collapses the conclusion network\.**
   Removing H1 leaves every later node without a load\-bearing route to the
   founding or corrective evidence\.
3. **Dissent is not engaged\.**
   D1 is never cited by S1\-S5 or N1\.
4. **Corrective evidence is structurally excluded\.**
   R1 and M1 exist but are absent from later conclusion\-carrying reference paths\.
5. **No claim narrowing occurs\.**
   Later sources repeat the broad self\-report, behavioral, and physiological
   package\.
6. **Background citations do not cure dependence\.**
   Non\-load\-bearing historical citations to F1 or F2 must not be counted as
   independent evidentiary routes\.

### Negative failure conditions

Fail Case 13 if the run:

1. acquits merely because a dissenting paper exists somewhere in the packet;
2. counts non\-load\-bearing historical citations as independent support routes;
3. says the conclusion survives H1 removal;
4. claims later sources engaged R1, D1, or M1;
5. invents outcome\-specific narrowing;
6. treats central publication alone as evidence of openness;
7. returns healthy by default or exits with `insufficient evidence`;
8. refuses to classify despite the graph being declared complete\.

---

## Pair\-level pass condition

The pair passes only when:

- Case 12 is acquitted for the correct structural reasons;
- Case 13 is convicted for the correct structural reasons;
- both runs complete the same required analytical work;
- the difference in verdict follows from the edge structure, hub\-removal result,
  dissent uptake, and claim mutation \- not from superficial node labels\.

## Human scoring record

|Requirement                    |Case 12|Case 13|Notes|
|-------------------------------|-------|-------|-----|
|Correct verdict                |       |       |     |
|Independent-route analysis     |       |       |     |
|H1 hub-removal result          |       |       |     |
|Dissent-uptake result          |       |       |     |
|Claim-narrowing result         |       |       |     |
|Concede Test                   |       |       |     |
|No insufficient-evidence escape|       |       |     |
|Overall result                 |       |       |     |
