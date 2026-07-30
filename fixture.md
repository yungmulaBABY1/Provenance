Paired Citation-Network Correctness Fixture

Placement

These files belong in:

tests/cases/

They are substantive research-branch cases, not execution-compliance fixtures.

Files

• 12-citation-network-cartel-shaped-healthy.md
• 13-citation-network-cartel-shaped-closed.md
• 12-13-citation-network-frozen-expected-results.md

Design

The two synthetic networks have the same surface features:

• 12 nodes;
• 25 selected edges;
• central founding sources;
• recurring founding authors;
• an author-led review hub;
• independent replication and methodological critique nodes;
• dissent;
• several later sources.

Their graph truth is opposite.

Case 12

Independent load-bearing routes survive hub removal, dissent is cited back into
the central literature, and later claims narrow by outcome class.

Expected result: healthy or open.

Case 13

All later load-bearing routes pass through the review hub, dissent is never cited
back, corrective evidence is structurally excluded, and the broad claim is
repeated without narrowing.

Expected result: closed or high-risk.

Why the pair matters

A single acquittal case can be passed by a prompt that acquits everything. A
single conviction case can be passed by a prompt that convicts everything.

The pair tests discrimination.

The expected-result file contains both positive work requirements and negative
failure conditions. This prevents a run from passing by saying only
insufficient evidence or by avoiding obvious overreach while failing to analyze
the graph.
