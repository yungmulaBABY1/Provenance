# Case 13 - Citation Network: Cartel-Shaped and Closed

## Test purpose

This is the conviction half of a paired research-branch correctness test.

It shares the same surface features as Case 12:

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
| D1 | Dissenting critique | Evans, Farah | Central Journal | Argues that the broad conclusion exceeds the evidence. |
| M1 | Methods reanalysis | Garcia, Holt | Methods Journal | Shows the strongest result is analytically fragile. |
| S1 | Later synthesis 1 | Avery, Ibrahim | Central Review Journal | Repeats the broad conclusion from H1. |
| S2 | Later synthesis 2 | Kim, Lopez | Central Journal | Treats H1 as the authoritative synthesis and repeats the broad package. |
| S3 | Later synthesis 3 | Mori, Novak | Central Review Journal | Treats supportive restatements as cumulative confirmation. |
| S4 | Later primary study | Owens, Patel | Central Journal | Reports one favorable result and generalizes it to the full package. |
| S5 | Recent review | Quinn, Rao | Central Review Journal | Reviews only the supportive central branch and preserves the broad conclusion. |
| N1 | Recent primary study | Singh, Tan | Central Journal | Treats the accumulated review chain as settled evidence. |

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
| S1 | H1 | Uses as the authoritative evidentiary synthesis. |
| S1 | F1 | Cites only to identify the historical origin of the claim. |
| S1 | F2 | Cites only as historical background. |
| S2 | H1 | Uses as the authoritative evidentiary synthesis. |
| S2 | S1 | Uses as a supportive restatement of H1. |
| S2 | F2 | Cites only to identify the historical origin of the applied extension. |
| S3 | H1 | Uses as the authoritative evidentiary synthesis. |
| S3 | S1 | Uses as cumulative supportive confirmation. |
| S3 | S2 | Uses as cumulative supportive confirmation. |
| S4 | H1 | Uses as the evidentiary basis for interpreting one favorable result. |
| S4 | S2 | Uses as supportive authority. |
| S4 | D1 | Acknowledges the critique in one sentence, dismisses it as outside scope, and does not use it to alter the claim or design. |
| S5 | H1 | Uses as the authoritative evidentiary synthesis. |
| S5 | S3 | Uses as cumulative supportive confirmation. |
| S5 | S4 | Uses as direct support for the unchanged broad package. |
| N1 | H1 | Uses as the authoritative evidentiary synthesis. |
| N1 | S4 | Uses as supportive confirmation. |
| N1 | S5 | Uses as the latest authoritative review. |

## Important constraints

- D1 is cited once by a later central source.
- D1 appears in a central venue.
- F1 and F2 receive several later citations.
- Those facts are not dispositive.
- The graph is complete for this synthetic case.

## Execution instruction

Run the canonical citation-network audit against only this supplied packet.

Do not retrieve additional sources. Determine which citations carry evidentiary
weight, perform the H1 hub-removal test, trace dissent uptake, evaluate claim
narrowing, and issue a bounded classification.
