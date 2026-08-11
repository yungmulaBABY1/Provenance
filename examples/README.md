Worked examples

Curated, reader-facing guided chains showing what the toolkit produces and how
outputs move between stages. This is a selective index, not a mirror of every
run. The raw evidentiary archive remains under tests/runs/; the canonical
instructions remain under prompts/.

Examples preserve what a run got wrong as well as what it got right. A clean
presentation that hides a failed expectation or broken handoff would defeat the
purpose of the repository.

Research

|Target                              |Fields                                                 |Chain                                                                                       |Why it is here                                                                                                                                      |
|------------------------------------|-------------------------------------------------------|--------------------------------------------------------------------------------------------|----------------------------------------------------------------------------------------------------------------------------------------------------|
|[Shen et al. (2016)](research/shen/)|esports; gender and performance; observational research|claim extraction → construct validity → internal validity → citation network → counter-audit|Tests MBH98-derived attribution machinery against a different citation-network shape and records the first real run of the internal-validity prompt.|

Shen et al. (2016)

The seven-file guided chain was run on 2026-08-10 with all
five instruments identity-confirmed at commit
a7ec6f2a4e93c3aed05f9fc6d2623ca629cf6467.

What it got right: internal validity found a direct, correctly hedged
contradiction between literal Field 6 and the source’s own reported significant
interactions, while preserving a narrower model-specific residual.

What it exposed: the counter-audit’s declared inputs omitted internal validity,
so the most consequential Stage 2B finding did not reach the terminal balancing
stage. The repair is registered as FAIL-CA-003; its regression case is built
but not yet run.

The pre-registered expectation that Shen had no same-author successor was
falsified by retrieval rather than rewritten after the fact. Ratan, Shen, and
Williams (2020) was correctly classified as a conceptual extension, real
misattributions were retrieved, MBH98-specific assessment/controversy fields
remained empty, and no cartel was invented.

Practitioner boundary: the chain did not independently surface game-specific
carry, boosting, AFK-progression, or similar mechanics. That limitation is
preserved in the final assessment rather than filled from operator knowledge.

Media

No complete reader-facing media chain has been curated here yet. The Ceuta raw
runs and regression fixtures remain available under tests/.
