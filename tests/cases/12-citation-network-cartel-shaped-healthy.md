# Case 12 - Citation Network: Cartel-Shaped but Healthy

## Test purpose

This is the acquittal half of a paired research-branch correctness test.

It shares the same surface features as Case 13:

- 12 nodes and 25 citations;
- central founding sources;
- recurring founding authors;
- an author-led review hub;
- an independent replication;
- a dissenting critique;
- a methods reanalysis;
- several later synthesis and primary sources.

The correct result must be derived from citation function, path structure, hub
removal, dissent uptake, and claim mutation.

## Claim under audit

The later literature is a functionally closed citation network that preserves the
founding claim through a review hub while excluding dissent and avoiding model
revision.

## Source table

| ID | Role | Authors | Venue | Claim or function |
|---|---|---|---|---|
| F1 | Founding study | Avery, Blake | Central Journal | Reports a broad package: self-report, behavior, and physiology. |
| F2 | Founding extension | Avery, Blake | Central Journal | Extends the broad package to an applied setting. |
| H1 | Author-led review hub | Avery, Blake | Central Review Journal | Synthesizes F1 and F2 and recommends the broad conclusion. |
| R1 | Independent replication | Chen, Diaz | Central Journal | Replicates only the self-report effect; behavioral and physiological results are null. |
| D1 | Dissenting critique | Evans, Farah | Peripheral Specialty Journal | Argues that the broad conclusion exceeds the evidence. |
| M1 | Methods reanalysis | Garcia, Holt | Methods Journal | Shows the strongest result is analytically fragile. |
| S1 | Later synthesis 1 | Avery, Ibrahim | Central Review Journal | Still uses broad language, but cites direct evidence as well as H1. |
| S2 | Later synthesis 2 | Kim, Lopez | Central Journal | Separates self-report from behavior and physiology. |
| S3 | Later synthesis 3 | Mori, Novak | Central Review Journal | Treats H1 as historical context and relies on R1 and M1 for the narrowed conclusion. |
| S4 | Later primary study | Owens, Patel | Central Journal | Directly tests behavior and reports a null result. |
| S5 | Recent review | Quinn, Rao | Central Review Journal | Reviews the mixed record and preserves only the narrower self-report claim. |
| N1 | Recent primary study | Singh, Tan | Central Journal | Reports a small self-report effect and no behavioral effect. |

## Citation-use table

No edge is pre-labeled `load-bearing` or `background`. Infer evidentiary weight
from how each citing source uses the cited source.

| Citing source | Cited source | How the citation is used |
|---|---|---|
| H1 | F1 | Uses as direct evidence for the broad claim. |
| H1 | F2 | Uses as direct evidence for the applied extension. |
| R1 | F1 | Direct replication target; reports partial failure. |
| D1 | F1 | Directly challenges the breadth of the founding inference. |
| D1 | H1 | Critiques the review's aggregation and conclusion. |
| M1 | F1 | Reanalyzes the original result and finds specification sensitivity. |
| M1 | H1 | Challenges the review's treatment of analytic robustness. |
| S1 | H1 | Uses as a broad synthesis source. |
| S1 | F1 | Uses the founding study as direct evidence, not merely history. |
| S1 | R1 | Uses the replication to qualify behavior and physiology. |
| S2 | F2 | Uses the extension as direct evidence for the self-report component only. |
| S2 | R1 | Uses the replication as evidence against the full package. |
| S2 | D1 | Engages the critique and narrows the conclusion. |
| S3 | H1 | Cites as historical background and field context. |
| S3 | R1 | Uses as direct evidence for the narrowed claim. |
| S3 | M1 | Uses as a methodological constraint on the original effect. |
| S4 | F1 | Uses as the direct target for a behavioral test. |
| S4 | M1 | Uses the reanalysis to justify a stricter design. |
| S4 | D1 | Mentions the critique briefly while motivating the test. |
| S5 | S1 | Uses as one synthesis input. |
| S5 | S2 | Uses as the main outcome-specific synthesis. |
| S5 | R1 | Uses as direct corrective evidence. |
| N1 | S3 | Uses the narrowed synthesis as background. |
| N1 | S4 | Uses the behavioral null as direct evidence. |
| N1 | R1 | Uses the independent replication as direct evidence. |

## Important constraints

- D1 is cited by only two later sources, and one citation is brief.
- D1 appears in a peripheral venue.
- S1 still uses broad language and includes a recurring founding author.
- These facts are not dispositive.
- The graph is complete for this synthetic case.

## Execution instruction

Run the canonical citation-network audit against only this supplied packet.

Do not retrieve additional sources. Determine which citations carry evidentiary
weight, perform the H1 hub-removal test, trace dissent uptake, evaluate claim
narrowing, and issue a bounded classification.
