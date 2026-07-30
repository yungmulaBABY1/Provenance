# Paired Citation-Network Correctness Test - Results

## Overall result

**PASS - the prompt discriminated between the paired synthetic networks.**

- Case 12: acquitted as healthy for graph-structural reasons.
- Case 13: convicted as functionally closed for graph-structural reasons.
- Mechanical checker: Case 12 exit `0`; Case 13 exit `0`.
- Neither run used an insufficient-evidence escape.

## Why the pair passed

The verdict did not turn on a single surface heuristic.

Case 12 contained peripheral, lightly cited dissent and recurring authors, but the
audit found independent routes through F1, F2, R1, and M1, a surviving graph after
H1 removal, substantive D1 use by S2, and outcome-specific narrowing.

Case 13 contained centrally published dissent, one later dissent citation, and
several founding-paper citations, but the audit classified those uses correctly:
the dissent citation was dismissive, the founding citations were historical, no
later source used R1 or M1, and H1 removal collapsed every evidentiary path.

## Case 12 scoring

| Requirement | Result |
|---|---|
| Correct verdict | PASS - healthy citation network; functional closure rejected. |
| Citation-function classification | PASS - historical, direct, substantive, and brief/perfunctory uses distinguished. |
| Independent-route analysis | PASS - all six later nodes retain non-H1 evidentiary routes. |
| H1 hub-removal result | PASS - network and narrowed conclusion survive. |
| Dissent-uptake quality | PASS - S2 substantive; S4 brief and not overstated. |
| Claim-narrowing result | PASS - S2-S5 and N1 separate outcomes. |
| Concede Test | PASS - closure claim defeated; local S1 risk narrowed. |
| No under-work escape | PASS - full classification and graph analysis completed. |

## Case 13 scoring

| Requirement | Result |
|---|---|
| Correct verdict | PASS - functionally closed citation network. |
| Citation-function classification | PASS - historical and ceremonial citations not counted as evidence. |
| Independent-route analysis | PASS - no later independent evidentiary route remains. |
| H1 hub-removal result | PASS - all later load-bearing connectivity collapses. |
| Dissent-uptake quality | PASS - one central citation correctly classified as dismissive/non-corrective. |
| Claim-narrowing result | PASS - no outcome-specific narrowing found. |
| Concede Test | PASS - closure findings survive. |
| No under-work escape | PASS - full classification and graph analysis completed. |

## Pair-level oracle check

| Pair requirement | Result |
|---|---|
| Case 12 acquitted for correct structural reasons | PASS |
| Case 13 convicted for correct structural reasons | PASS |
| Citation presence distinguished from citation function | PASS |
| H1 hub removal performed in both | PASS |
| Correct claim-mutation pattern identified in both | PASS |
| No single dissent/venue/citation-count heuristic decided the pair | PASS |
| Both execution contracts mechanically complete | PASS |

## Interpretation

This closes the previously open research-branch correctness gap for the synthetic
paired fixture.

It establishes that the current citation-network prompt can both acquit and
convict when surface cartel indicators are held broadly constant and the
evidentiary path structure changes.

It does not validate open-ended retrieval or real-world field correctness.
