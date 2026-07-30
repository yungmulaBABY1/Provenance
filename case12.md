Case 12 - Citation Network: Cartel-Shaped but Healthy

Test purpose

This is the acquittal half of a paired research-branch correctness test.

It has the same surface features as Case 13:

• a central founding source;
• recurring founding authors;
• an author-led review hub;
• an independent replication;
• a dissenting critique;
• several later synthesis and primary sources;
• 12 nodes and 25 selected citation edges.

The correct result must be derived from the graph structure and claim-use fields,
not from those surface features.

Claim under audit

The later literature is a functionally closed citation network that preserves the
founding claim through a review hub while excluding dissent and avoiding model
revision.

Source table

|ID|Role                   |Authors       |Venue                 |Claim or function                                                                                                   |
|--|-----------------------|--------------|----------------------|--------------------------------------------------------------------------------------------------------------------|
|F1|Founding study         |Avery, Blake  |Central Journal       |Broad claim: intervention improves self-report, behavior, and physiology.                                           |
|F2|Founding extension     |Avery, Blake  |Central Journal       |Extends the broad claim to a second outcome and applied setting.                                                    |
|H1|Author-led review hub  |Avery, Blake  |Central Review Journal|Synthesizes the founding package and recommends the broad conclusion.                                               |
|R1|Independent replication|Chen, Diaz    |Central Journal       |Finds one self-report effect but not the behavioral or physiological package.                                       |
|D1|Dissenting critique    |Evans, Farah  |Central Journal       |Argues that the broad conclusion exceeds the evidence.                                                              |
|M1|Methods reanalysis     |Garcia, Holt  |Methods Journal       |Shows that the strongest result is sensitive to analytic specification.                                             |
|S1|Later synthesis 1      |Ibrahim, Jones|Central Review Journal|Concludes that only the self-report outcome is supported; behavioral and physiological claims are not.              |
|S2|Later synthesis 2      |Kim, Lopez    |Central Journal       |Separates self-report from behavior and rejects the broad applied claim.                                            |
|S3|Later synthesis 3      |Mori, Novak   |Central Review Journal|Treats the review hub as historical background and narrows the conclusion using replication and reanalysis evidence.|
|S4|Later primary study    |Owens, Patel  |Central Journal       |Directly tests the behavioral outcome and reports a null result.                                                    |
|S5|Recent review          |Quinn, Rao    |Central Review Journal|Reviews the mixed network and preserves the narrower outcome-specific conclusion.                                   |
|N1|Recent primary study   |Singh, Tan    |Central Journal       |Finds a small self-report effect but no behavioral effect and cites the independent replication branch.             |

Selected citation-edge table

The Load-bearing for conclusion? field is part of the fixture. Historical or
background citations do not count as independent evidentiary routes.

|Source|Target|Function            |Load-bearing for conclusion?|
|------|------|--------------------|----------------------------|
|H1    |F1    |support             |yes                         |
|H1    |F2    |support             |yes                         |
|R1    |F1    |critical replication|yes                         |
|D1    |F1    |critical            |yes                         |
|D1    |H1    |critical            |yes                         |
|M1    |F1    |critical reanalysis |yes                         |
|M1    |H1    |critical reanalysis |yes                         |
|S1    |F1    |support/background  |yes                         |
|S1    |R1    |narrowing evidence  |yes                         |
|S1    |D1    |engages dissent     |yes                         |
|S2    |F2    |support/background  |yes                         |
|S2    |R1    |narrowing evidence  |yes                         |
|S2    |D1    |engages dissent     |yes                         |
|S3    |H1    |review background   |no                          |
|S3    |R1    |narrowing evidence  |yes                         |
|S3    |M1    |methods correction  |yes                         |
|S4    |F1    |direct test target  |yes                         |
|S4    |D1    |engages dissent     |yes                         |
|S4    |M1    |methods correction  |yes                         |
|S5    |S1    |later synthesis     |yes                         |
|S5    |S2    |later synthesis     |yes                         |
|S5    |D1    |engages dissent     |yes                         |
|N1    |S3    |later evidence      |yes                         |
|N1    |S4    |later evidence      |yes                         |
|N1    |R1    |replication branch  |yes                         |

Structural facts available to the auditor

• Later sources citing the dissent D1: S1, S2, S4, S5.
• Removing H1 leaves every later source connected by at least one load-bearing
route to independent evidence:
  • N1: D1, F1, M1, R1
  • S1: D1, F1, R1
  • S2: D1, F1, F2, R1
  • S3: F1, M1, R1
  • S4: D1, F1, M1
  • S5: D1, F1, F2, R1
• Later claims explicitly separate self-report, behavioral, and physiological
outcomes.
• D1 appears in a central venue and is cited by later central sources.
• R1 and M1 provide independent corrective routes that do not depend on H1.

Execution instruction

Run the canonical citation-network audit against only this supplied packet.

Do not retrieve additional sources. Treat the graph as complete for the synthetic
case. The task is to classify the network, identify the load-bearing structural
features, run the hub-removal test, and apply the Concede Test.
