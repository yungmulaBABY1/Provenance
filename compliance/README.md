# Citation-Network Compliance Pilots

This folder contains the evidence and evaluation records for three supplied-packet
compliance pilots of the citation-network audit.

The pilots tested a specific observed failure: required sections were present in
the prompt but silently disappeared from a completed audit. The repair adds an
execution contract, a Completion Ledger, and a mechanical checker that detects
missing sections, false ledger claims, wrong ordering, duplicate headings, absent
ledgers, and verdicts issued after silent omissions.

The updated prompt files are intentionally not stored here. The canonical
citation-network prompt belongs in:

`prompts/research-analysis/2-citation-network.txt`

The canonical checker belongs in:

`prompts/research-analysis/check-citation-network-output.py`

## Results

| Pilot | Packet | Intended test | Result |
|---|---:|---|---|
| Pilot 01 | 4 sources | Compact execution and gate behavior | Passed |
| Pilot 02 | 12 sources / 25 selected edges | Medium burden; genuine work in Sections A, F, and J | Passed |
| Pilot 03 | 26 sources / 70 selected edges | Large supplied-packet burden; genuine work in Sections A, F, H, and J | Passed |

All three runs completed every required heading, preserved the required order,
passed the ledger cross-check, and issued Artifact 10 only after the completion
gate passed.

## Validation boundary

These pilots validate the execution repair only for **fixed supplied packets up
to 26 sources and 70 selected citation edges**.

They do not validate:

- open-ended source discovery;
- network completeness;
- source-selection judgment across a large candidate space;
- false-absence control;
- retrieval provenance;
- search-scope reporting;
- field-wide substantive correctness.

Open-ended retrieval is a separate test axis.

The substantive power-posing verdicts are observations unless an expected result
was independently specified before the run. The pilots primarily test execution
compliance, not whether every substantive conclusion is correct.

## Pilot 01 - Compact supplied packet

A four-source power-posing chain:

1. original experiment;
2. large failed-or-narrowing replication;
3. author-led review;
4. methodological p-curve critique.

The packet was deliberately small so omitted headings or failed gate behavior
could not plausibly be blamed on output burden.

### Files

- [`citation-network-compliance-pilot-01-source-packet.txt`](citation-network-compliance-pilot-01-source-packet.txt)  
  Fixed four-source packet and bounded execution instructions.

- [`citation-network-compliance-pilot-01-audit.txt`](citation-network-compliance-pilot-01-audit.txt)  
  Complete citation-network audit produced from the packet.

- [`citation-network-compliance-pilot-01-checker-report.txt`](citation-network-compliance-pilot-01-checker-report.txt)  
  Mechanical heading, order, ledger, and gate report.

- [`citation-network-compliance-pilot-01-evaluation.md`](citation-network-compliance-pilot-01-evaluation.md)  
  Manual evaluation of substantive section completion, N/A versus PROVISIONAL
  use, present-but-empty risk, and bounded self-limitation.

## Pilot 02 - Medium supplied packet

A 12-source, 25-edge power-posing network designed to exercise the sections that
could not be meaningfully tested by the compact packet.

The run had to perform:

- a real bounded topology analysis in Section A;
- an early-review hub-removal test in Section F;
- an explicit healthy-network comparator in Section J.

### Files

- [`citation-network-compliance-pilot-02-requirements.md`](citation-network-compliance-pilot-02-requirements.md)  
  Precommitted size, burden, and interpretation requirements.

- [`citation-network-compliance-pilot-02-source-packet.txt`](citation-network-compliance-pilot-02-source-packet.txt)  
  Fixed 12-source packet, 25 selected citation edges, claim map, graph metrics,
  hub-removal input, and comparator input.

- [`citation-network-compliance-pilot-02-audit.txt`](citation-network-compliance-pilot-02-audit.txt)  
  Complete medium citation-network audit.

- [`citation-network-compliance-pilot-02-checker-report.txt`](citation-network-compliance-pilot-02-checker-report.txt)  
  Mechanical execution-compliance result.

- [`citation-network-compliance-pilot-02-evaluation.md`](citation-network-compliance-pilot-02-evaluation.md)  
  Manual review of Sections A, F, and J, section substance, bounded scope, and
  compliance interpretation.

## Pilot 03 - Large supplied packet

A 26-source, 70-edge power-posing network designed to isolate output and
analytical burden while keeping retrieval closed.

The run had to perform:

- bounded topology, density, centrality, and cluster analysis in Section A;
- two hub-removal tests in Section F;
- multi-generation critique-uptake tracing in Section H;
- a real healthy-network comparison in Section J;
- a nontrivial citation spine and network map.

### Files

- [`citation-network-pilot-03-large-supplied-requirements.md`](citation-network-pilot-03-large-supplied-requirements.md)  
  Precommitted large-packet requirements and failure interpretation.

- [`citation-network-compliance-pilot-03-source-packet.txt`](citation-network-compliance-pilot-03-source-packet.txt)  
  Fixed 26-source packet, 70 selected edges, graph metrics, two hub-removal
  inputs, and comparator branches.

- [`citation-network-compliance-pilot-03-audit.txt`](citation-network-compliance-pilot-03-audit.txt)  
  Complete large citation-network audit.

- [`citation-network-compliance-pilot-03-checker-report.txt`](citation-network-compliance-pilot-03-checker-report.txt)  
  Mechanical compliance result for the large run.

- [`citation-network-compliance-pilot-03-evaluation.md`](citation-network-compliance-pilot-03-evaluation.md)  
  Manual assessment of section survival and substantive completion under the
  largest supplied-packet burden.

## Checker behavior

Run the canonical checker with:

```bash
python prompts/research-analysis/check-citation-network-output.py <audit-output.txt>
```

The checker verifies:

- all required headings appear exactly once as standalone lines;
- Artifact 9 precedes the Completion Ledger;
- the Completion Ledger precedes Artifact 10;
- Artifact 10 precedes the standardized finding table;
- every ledger row matches actual heading presence;
- a ledger cannot falsely report an absent section as completed;
- a ledger cannot falsely report a present section as omitted;
- required omissions trigger the incomplete-run declaration;
- Artifact 10 is withheld after a failed completion gate;
- silent omissions, duplicates, wrong order, and absent ledgers are detected.

The word-count check is only a **placeholder screen**. A section that clears it
may still be analytically inadequate. Manual review remains load-bearing.

## What the three-rung ladder established

The original silent omission did not recur at compact, medium, or large
supplied-packet scale.

This means supplied-packet burden through 26 sources and 70 selected edges is not
supported as the explanation for the observed failure. It does not prove that
burden can never matter, especially during open-ended retrieval.

The gate is therefore a validated local repair for the citation-network prompt,
within the stated supplied-packet boundary.

## Non-propagation rule

This gate is a **FAIL-class repair for an observed failure in one prompt**.

Do not copy the 25-block execution contract, Completion Ledger, or checker into
other audit prompts merely for architectural symmetry. Use it elsewhere only
after an analogous omission is observed and the local cost is tested.

A proven repair can remain available without becoming permanent overhead across
the entire audit system.
