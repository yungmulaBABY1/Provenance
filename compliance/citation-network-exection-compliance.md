Citation-Network Execution Compliance

Purpose

This directory contains a local execution-compliance repair for
2-citation-network.txt.

The repair exists because a live citation-network audit silently omitted required
sections even though those sections were present in the prompt. The execution
contract, Completion Ledger, and checker make that failure mechanically visible.

Files

• 2-citation-network.txt — canonical citation-network audit prompt.
• check-citation-network-output.py — mechanical compliance checker.

Run:

```bash
python prompts/research-analysis/check-citation-network-output.py <audit-output.txt>
```

What the checker establishes

The checker verifies:

• every required heading appears exactly once as a standalone line;
• required headings appear in the critical order;
• the Completion Ledger contains one row per required heading;
• ledger presence, completion, and omission claims match the actual output;
• a missing required block triggers the incomplete-run declaration and withholds
the substantive verdict;
• silent omission, duplicate headings, wrong order, and absent-ledger failures
are detected.

The checker also applies a crude placeholder screen.

A placeholder-screen pass does not establish that a section is analytically
adequate. Manual substantive review remains load-bearing.

Validation boundary

The execution contract and checker passed fixed supplied-packet pilots at three
burden levels:

|Pilot  |Sources|Selected edges|Result|
|-------|------:|-------------:|------|
|Compact|4      |bounded chain |Passed|
|Medium |12     |25            |Passed|
|Large  |26     |70            |Passed|

The medium and large runs required substantive work in the sections that had
previously vanished, including bounded topology, hub-removal analysis,
critique-uptake tracing, and comparison against a healthy-network baseline.

This validates execution behavior only for fixed supplied packets up to the
tested scale.

It does not validate:

• open-ended source discovery;
• network completeness;
• source-selection judgment across a large candidate space;
• false-absence control;
• retrieval provenance;
• search-scope reporting;
• field-wide substantive correctness.

Open-ended retrieval is a separate test axis.

Interpretation of the burden result

The original omission did not recur on compact, medium, or large supplied
packets. Output burden from supplied packets up to 26 sources and 70 selected
edges is therefore not supported as the explanation for the observed failure.

This does not prove that burden can never matter. A future failure under a larger
or retrieval-heavy run should still be diagnosed before changing the prompt.

If a future realistic run fails after these passes:

• do not add stronger warning language;
• do not add another self-report layer;
• cut, merge, or stage sections if burden is the leading diagnosis.

Non-propagation rule

This is a local FAIL-class repair, not a global prompt standard.

Do not copy the execution contract, 25-block ledger, or checker pattern into
construct validity, internal validity, counter-audit, media, or other prompts
solely for architectural symmetry.

Propagation is justified only when:

1. an analogous omission failure is observed in that prompt;
2. the local repair is proportionate to the observed failure;
3. the added output burden is tested on that prompt.

A proven repair may remain available without becoming universal overhead.
