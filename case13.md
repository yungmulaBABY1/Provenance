# Case 13 \- Citation Network: Cartel\-Shaped and Closed

## Test purpose

This is the conviction half of a paired research\-branch correctness test\.

It has the same surface features as Case 12:

- a central founding source;
- recurring founding authors;
- an author\-led review hub;
- an independent replication;
- a dissenting critique;
- several later synthesis and primary sources;
- 12 nodes and 25 selected citation edges\.

The correct result must be derived from the graph structure and claim\-use fields,
not from those surface features\.

## Claim under audit

The later literature is a functionally closed citation network that preserves the
founding claim through a review hub while excluding dissent and avoiding model
revision\.

## Source table

|ID|Role                   |Authors       |Venue                       |Claim or function                                                                |
|--|-----------------------|--------------|----------------------------|---------------------------------------------------------------------------------|
|F1|Founding study         |Avery, Blake  |Central Journal             |Broad claim: intervention improves self-report, behavior, and physiology.        |
|F2|Founding extension     |Avery, Blake  |Central Journal             |Extends the broad claim to a second outcome and applied setting.                 |
|H1|Author-led review hub  |Avery, Blake  |Central Review Journal      |Synthesizes the founding package and recommends the broad conclusion.            |
|R1|Independent replication|Chen, Diaz    |Central Journal             |Finds one self-report effect but not the behavioral or physiological package.    |
|D1|Dissenting critique    |Evans, Farah  |Peripheral Specialty Journal|Argues that the broad conclusion exceeds the evidence.                           |
|M1|Methods reanalysis     |Garcia, Holt  |Methods Journal             |Shows that the strongest result is sensitive to analytic specification.          |
|S1|Later synthesis 1      |Ibrahim, Jones|Central Review Journal      |Repeats the broad conclusion from H1 without separating outcome classes.         |
|S2|Later synthesis 2      |Kim, Lopez    |Central Journal             |Cites H1 as authority and repeats the same broad conclusion.                     |
|S3|Later synthesis 3      |Mori, Novak   |Central Review Journal      |Treats prior supportive restatements as cumulative confirmation.                 |
|S4|Later primary study    |Owens, Patel  |Central Journal             |Reports a favorable result and interprets it as support for the full package.    |
|S5|Recent review          |Quinn, Rao    |Central Review Journal      |Reviews only the supportive central branch and preserves the broad conclusion.   |
|N1|Recent primary study   |Singh, Tan    |Central Journal             |Treats the accumulated review chain as settled evidence for the original package.|

## Selected citation\-edge table

The `Load-bearing for conclusion?` field is part of the fixture\. Historical or
background citations do not count as independent evidentiary routes\.

|Source|Target|Function              |Load-bearing for conclusion?|
|------|------|----------------------|----------------------------|
|H1    |F1    |support               |yes                         |
|H1    |F2    |support               |yes                         |
|R1    |F1    |critical replication  |yes                         |
|D1    |F1    |critical              |yes                         |
|D1    |H1    |critical              |yes                         |
|M1    |F1    |critical reanalysis   |yes                         |
|M1    |H1    |critical reanalysis   |yes                         |
|S1    |H1    |claim support         |yes                         |
|S1    |F1    |historical background |no                          |
|S1    |F2    |historical background |no                          |
|S2    |H1    |claim support         |yes                         |
|S2    |S1    |supportive restatement|yes                         |
|S2    |F2    |historical background |no                          |
|S3    |H1    |claim support         |yes                         |
|S3    |S1    |supportive restatement|yes                         |
|S3    |S2    |supportive restatement|yes                         |
|S4    |H1    |claim support         |yes                         |
|S4    |S2    |supportive restatement|yes                         |
|S4    |S3    |supportive restatement|yes                         |
|S5    |H1    |claim support         |yes                         |
|S5    |S3    |supportive restatement|yes                         |
|S5    |S4    |supportive restatement|yes                         |
|N1    |H1    |claim support         |yes                         |
|N1    |S4    |supportive restatement|yes                         |
|N1    |S5    |supportive restatement|yes                         |

## Structural facts available to the auditor

- Later sources citing the dissent D1: none\.
- Removing H1 leaves no later source connected by a load\-bearing route to the
  founding or corrective evidence:
  - N1: none
  - S1: none
  - S2: none
  - S3: none
  - S4: none
  - S5: none
- Later claims repeat the broad founding package without separating outcome
  classes\.
- D1 appears only in a peripheral venue and is never cited by the later central
  branch\.
- R1 and M1 exist, but later conclusion\-carrying sources do not cite them\.
- Historical citations to F1 or F2 are explicitly marked non\-load\-bearing\.

## Execution instruction

Run the canonical citation\-network audit against only this supplied packet\.

Do not retrieve additional sources\. Treat the graph as complete for the synthetic
case\. The task is to classify the network, identify the load\-bearing structural
features, run the hub\-removal test, and apply the Concede Test\.
