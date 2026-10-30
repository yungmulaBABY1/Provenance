> **Origin:** copied unchanged from package B (alternative implementation
> `atlas-citation-import/0.1`, file `prompt-contracts.md`, SHA-256 `59274ae700b686acb03f5edd6bda5616a2473ca230c31b7cb050a9c74f837c17`).
> Everything below this header is byte-for-byte the original.
>
> **Status:** documentation only. This is not a second runtime, schema or
> parser; package B's `atlas_adapter/` is not part of this repository. Paths
> such as `atlas_adapter/contract.json` and `evidence/verified-files.json`
> refer to package B and do not exist here. The runtime is `atlas/`, and the
> pinned prompts remain authoritative.

---

# Provenance prompt and fixture contracts — inspected baseline

Baseline: `d7000315197670a59988b2d0b58bf0cdae545fc3`, retrieved 2026-10-30.
All paths below are relative to that repository commit. Exact blob SHAs, byte
counts and line counts are in `evidence/verified-files.json`. Exact native
headings and table definitions, with line numbers, are in
`native-contract-excerpts.md`. That appendix is a transcription/index, not a
universal parser. The actual pinned prompt remains authoritative.

## Common boundaries, not a universal finding schema

The nine active prompts and deferred field-context generator contain TOOL-004
identity preflight. Retrieval form is `PASTED / ATTACHED / IMMUTABLE REMOTE /
MUTABLE REMOTE`. The output preflight uses `IDENTITY CONFIRMED`, `INSTRUMENT
VERSION UNVERIFIED`, or `VERSION COLLISION — UNRESOLVED`. A formal version
collision stops substantive execution; an unverified exploratory run is not
formal regression evidence. A failed hash does not identify which copy is stale.
This is currently a prompt instruction, not an enforced execution service.

The research verification vocabulary is `LOCATED`, `ABSTRACT-CONFIRMED`,
`FULL-TEXT-CONFIRMED`, `RECEPTION-CONFIRMED`, `CONTESTED`, `REBUTTED`,
`PROVISIONAL`, `CROSS-SOURCE-CONFIRMED`. `COMPUTED-FROM-RETRIEVED` is a separate
derivation label. None means human adjudication. Missing fields are not silently
converted to PROVISIONAL: Atlas `MISSING` and `INVALID_LABEL` are adapter states.

Research prosecutors share claim-map field 6 as the target, but preserve their
own contracts. Their `Concede test` is `SURVIVES / NARROWS / DEFEATS`; scope loss
is `incidental / material / near-defeat` plus the surviving claim. The native
meaning concerns the audited claim, which cannot safely be inferred from the
word alone. Paired network outputs demonstrate a historical direction mismatch.

Media evidence vocabulary is `LOCATED / FULL-TEXT-CONFIRMED /
CROSS-OUTLET-CORROBORATED / CONTESTED / PROVISIONAL`. Media reception is not
research reception. Source-chain labels `CHAIN-CONFIRMED / CHAIN-INFERRED /
CHAIN-PROVISIONAL` are another axis. Corroboration requires at least two
independent origins for the particular fact, not two outlet logos.

`reference/shared-primitives.txt` is explicitly superseded and says nothing
loads it. Its old Section 1–3 references are not executable dependencies.
Instrument-local compact blocks govern today; unifying them requires a later
parity-preserving change, not blind reuse of the old file.

## 0 — Field diagnostic

Path: `prompts/0-field-diagnostic.txt`; canonical prompt, no automated validator
found. Purpose: test field-level plausibility, operator position/access and
self-calibration before committing to the audit. Inputs are the proposed field,
problem, claimed anomaly and investigator's access/competence. It does not
consume a completed six-field claim map or produce prosecutor finding rows.

Native shape: 44 questions across A/B/C and `FINAL ASSESSMENT` with six routing
questions. Preserve these question/answer and routing objects, including
uncertainty and the human-facing self-calibration portion. Do not coerce this
into a severity/status table. Its permission to proceed is not a clean paper
assessment. A future adapter needs its own schema and fixture, not inheritance
from citation-network output.

## 1 — Claim extraction / inflation map

Path: `prompts/1-claim-extraction.txt`; canonical. Inputs: foundational source,
downstream use and the audit target. Required six native fields:

1. `WHAT WAS LITERALLY MEASURED`
2. `STRONGEST CLAIM THE SOURCE ITSELF MAKES`
3. `WEAKER DEFENSIBLE CLAIM THE EVIDENCE ACTUALLY SUPPORTS`
4. `BROADER CLAIM ATTACHED DOWNSTREAM`
5. `WHERE THE INFLATION BEGINS`
6. `WHICH CLAIM IS THIS AUDIT EVALUATING?`

The claim inventory precedes a precise selected target. Source provenance
`SUPPLIED / RETRIEVED / RECALLED / NONE FOUND` is separate from evidence
verification. Field 5 needs actual quotations/locators; downstream uncertainty
is local to affected fields, not an excuse to fabricate an inflation bridge.
Joint-citation attribution requires the two texts and whole-document context;
`MISATTRIBUTED` and `ATTRIBUTED ELSEWHERE` cannot follow from snippets alone.

[P1] separates `PREVALENCE / FORM / DOMAIN / WRONGNESS / HARM`, with
`ESTABLISHED-REPORTED / ESTABLISHED-CITED / ASSERTED / UNKNOWN`. Reading only an
introduction's claim does not establish a property; the cited literature matters.
Item access uses `ITEMS-RETRIEVED / ITEMS-INFERRED`; inferred items force UNKNOWN
scope and provisional treatment. [P2] uses `ESTABLISHED-FALSE /
GRADE-CONTESTED / FRINGE / ESTABLISHED-ACCURATE` and `STRONG / WEAK / VOID`.

Evidence: CE-006/007 joint-citation case, MBH98/Donovan/Shen examples, and later
CV failures documenting attribution and instrument-content errors. These are
archived cases/manual logs, not an implemented deterministic full claim-map
validator. No new model extraction was executed here.

## Research 2 — Construct validity

Path: `prompts/research-analysis/2-construct-validity.txt`; canonical, with later
source-preflight and P1/P2 repairs. Full mode needs source plus upstream claim
map; a self-generated map is degraded/provisional and does not establish
cross-prosecutor alignment. Source-access basis is mandatory even for a clean
result. Verify load-bearing reported numbers and operationalization items.

Native numbered sections culminate in `14. VERDICT` and `FINAL SECTION:
STANDARDIZED FINDING TABLE`. The table adds `Failure-mode subtype`, `Construct
property`, `Construct-property status`, `ESTABLISHED-CITED prosecutor split`,
`Operationalization retrieval basis`, `Operationalization scope result`,
`P2 belief grade`, `P2 strength gate`, and **`Finding disposition`**. The last
uses uppercase `CONFIRMED / CONTESTED / PROVISIONAL`, not citation's `Status`.
Operationalization scope: `coextensive / narrower / broader / UNKNOWN / N/A`.
Cited-property split: `uncontested-in-respect-required /
contested-in-respect-required / N/A`.

Verdict is a split claim-space object: `VALID / USEFUL-FOR-NARROWER / INVALID`,
exact surviving residual or `none`, and residual usefulness `A / B / C / G /
none`. A single letter erases the difference between a defeated strong claim and
a useful residual. Weak P2 caps severity at minor; VOID removes it. Provisional
evidence or inferred item scope cannot carry major/fatal findings. Null findings
still need source preflight; inability to read is not acquittal.

Evidence: Donovan operationalization retrieval killed an inferred scale-content
finding (R23/CV-004); ISIS-2 R35 exposed the clean-result source-read gap
(FAIL-CV-008). `case_FAIL-CV-008_isis2-source-preflight.txt` specifies the repaired
regression; a fresh post-repair model run was not located. The source-preflight
body currently carries the wrong `[FAIL-CV-006]` tag. Do not silently relabel the
historical record or claim the planned test passed.

## Research 2 — Internal validity

Path: `prompts/research-analysis/2-internal-validity.txt`; canonical. Inputs:
source, underlying data/code/preregistration/reception where accessible, claim
map and optional formally declared sibling outputs. Native headers:
`SIBLING-PROSECUTOR INPUT: NONE / FORMALLY SUPPLIED — identifier` and
`INDEPENDENCE STATUS: INDEPENDENT / INTEGRATED-NONINDEPENDENT`. Ambient sibling
context is excluded throughout an independent run. Merely reading a source
does not establish that a computational claim was reproduced.

Sections A–K include D2 for analytical paths, H2 for the concede test, and J for
explicit integration. [IV-P1] technical outcome is `SOURCE-DIRECT / REPRODUCED /
INDEPENDENT-REANALYSIS-CONFIRMED / ACKNOWLEDGED-CORRECTION / UNRESOLVED /
UNVERIFIED`. Verdict eligibility is separately `ELIGIBLE / PENDING VERIFICATION`.
Pending allegations cannot trigger adverse C/D/E grades. If missing evidence
prevents assessment, use F, not a clean verdict. Grades are A Strong, B
Acceptable, C Weak, D Suspect, E Invalid, F Cannot assess.

Important loss risk: the final standardized table has the familiar 15 research
fields but omits these newer technical-outcome and eligibility axes. An adapter
must preserve H2/J plus the final table. Citation's adapter is not suitable.

Evidence: Shen raw outputs; R33 contaminated and R34 clean Galor–Özak runs
document a D-versus-C difference, motivating FAIL-IV-001/002. The paired case
file exists; fresh execution of the repaired prompt is not demonstrated here.
README's claim that internal validity had never run is stale.

## Research 2 — Citation network: implemented adapter scope

Path: `prompts/research-analysis/2-citation-network.txt`; canonical current
baseline. Inputs: selected claim/map, bounded source corpus, citation contexts,
source texts and retrieval record. Degraded self-generated maps must be marked.

Native structure: `PRE-AUDIT CLAIM CONFIRMATION`, Sections A–K including J2,
Artifacts 1–9, `COMPLETION LEDGER`, `ARTIFACT 10: FINAL VERDICT`, and
`FINAL SECTION: STANDARDIZED FINDING TABLE`: 25 required headings. Missing a
required section or Artifact 1–9 prevents a substantive final verdict;
`INCOMPLETE RUN — REQUIRED SECTION OMITTED` and a withheld verdict are required.

Final table has **15** fields: Finding; Target claim; What was measured; What
was claimed; Failure mode; Severity; Concede test; Scope loss if NARROWS;
Evidence; Evidence type; Verification state; Possible innocent explanation;
What would weaken this; Failure location; Status. Severity: `none / minor /
moderate / major / fatal-for-strong-claim`. Location: `PAPER / CITATION /
PR-MEDIA / MODEL-RETRIEVAL / MIXED`. Status: lowercase `confirmed / contested /
provisional`. The contract's literal Evidence-type list and verification enums
are in `atlas_adapter/contract.json`; historical prose/combinations are not
silently aliased. No findings is a permitted explicit empty table, not an empty
parser result.

Source lock: `LOCKED QUERY / LOCKED SOURCES / POST HOC`, plus database, source
list/query, cutoff, ranking, N, deduplication and timestamp/hash. Source class:
`CONSTRUCT-DEFINING / MECHANISM-SUPPORTING / DIRECTLY-ADJUDICATING`. Dimensions
retain `SCORED / UNASSESSED / UNINFORMATIVE / N/A` and independent/nested
aggregation. Density requires its corpus and numerator/denominator/coverage
receipts. The native risk score is retained as historical data, not converted
to an Atlas credibility score.

Native formal labels: healthy citation network; normal small-field clustering;
self-referential citation cluster; citation-laundering network;
premise-laundering hub; functionally closed citation network; functional citation
cartel; insufficient evidence. These are model findings, not Atlas judgments.

Existing code: `check-citation-network-output.py` checks structural/content form
and routes judgment to review. `tests/test-citation-network-checker.py` asserts
known-bad failure, whitelist control, clean PASS and locked-source
PASS-WITH-REVIEW. Both run successfully in this inspection. Current checker
rejects archived paired cases on new content requirements while their old logs
report PASS: version drift, not a new failed model run.

## Research 3 — Counter-audit

Path: `prompts/research-analysis/3-counter-audit.txt`; canonical. Inputs include
source and claim map, **all supplied prosecutors including internal validity**,
and optional thesis/draft. It has distinct A–K sections, E0 source self-defense,
E1 external support, G2 re-aiming and J2 self-tilt disclosure. E0 runs before
external support; G2 checks strongest/defensible/downstream target and nested
findings. Scholarly reception is a prerequisite for promoting an opposing source
to load-bearing status; low uptake of a rebutted source is not suppression.

E0 disposition: `DEFEATED / NARROWED / RECHARACTERIZED / UNAFFECTED`; directional
defense requires the CA-004 gate rather than automatic recharacterization.
Final internal-validity coverage: `SUPPLIED AND CONSUMED / SUPPLIED BUT NOT RUN
THROUGH G2 / NOT SUPPLIED` plus the required caveat. Optional fidelity output:
`MATCHES VETTED FINDING / OVERSTATES / OMITS / MISCITES VERIFICATION STATE`.
Revised thesis categories A–F: strengthened, narrowed, softened, seriously
weakened, overturned, mixed. These do not map to prosecutor severity.

Evidence: Shen R30 omitted IV; R31 rerun consumed it and changed verdict
(FAIL-CA-003). CA-004 directional-defense case and raw v3/v4 files exist. This
slice records counter-audit NOT_SUPPLIED for imported network runs; importing a
different paper's counter-audit would falsely create independent review.

## Media 2 — Single-piece framing / construction

Path: `prompts/media-analysis/2-framing-construction.txt`; canonical. Inputs:
piece/full text, timing/versions, packaging surfaces and upstream sources; not
the research six-field map. Section 0 genre/format gate precedes A–L, including
E2 narrative analysis, F2 quotation checks and I2 prior-match. Genre constraints
can remove a supposed omission; timing and costly flip tests gate findings.
Independent levers, not row counts, drive construction aggregation.

Section K fields: Finding; Section; Evidence; **Media finding type**; Failure
location (if applicable); Severity; Survives timing test; Survives flip test;
Possible innocent explanation; What would weaken this; Verification state.
Severity ends in `severe`, not research's `fatal-for-strong-claim`. Type includes
`factual / construction / omission / sourcing / frame-laundering / causal-bridge /
causal-role-framing / narrative-flag / baseline / packaging / none`.
Test booleans are literal `yes / no`. Construction verdict:
`PROPORTIONATE / MILDLY SLANTED / SUBSTANTIALLY SLANTED / HEAVILY CONSTRUCTED`;
factual assessment stays separate. A null finding is reachable.

Caps: failed flip at most minor; timing-explained cannot carry verdict;
unchecked packaging at most moderate; unretrieved other-coverage allegation
provisional/minor. Prior-match requires an actual costly downgrade, not a
boilerplate symmetry statement. Evidence: Madison/Seattle/Ceuta historical runs
and MB-series failures. `11-proportionate.md` is a built clean control, not a
located completed run. No deterministic media validator was found.

## Media 2 — Coverage network

Path: `prompts/media-analysis/2-coverage-network.txt`; canonical location,
**header says RC2 CONSOLIDATED CANDIDATE**. Both statuses must be reported.
Inputs: bounded event packet, minimum three pieces (prefer five to eight),
publication/update times, upstream origins and sampling rule. Stay within a
closed packet; separately declared companion-source exceptions are not open
permission to retrieve beyond its boundary. No canonical media Stage 3 exists.

Sections A–I, plus D2 cross-branch resolution and E2 prior-match, contain source
chain, factual core, framing, clustering, flip, sample audit and finding table.
Section H fields include Finding; Section; Evidence; **Finding type**; Severity;
Survives flip test; Sample-dependent; Possible innocent explanation;
Availability row cited; What would weaken this; Verification state.
Finding type is `common-source-propagation / source-dependent-interpretation /
claim-amplification / source-chain / selection / prominence-packaging /
framing-divergence / causal-role-framing / event-classification-divergence /
language-package-divergence / clustering`.

FAIL-MB-017 separates SELECTION from PROMINENCE. A selection finding needs the
availability matrix and publication-time opportunity. A prominence finding needs
full-text possession, packaging ownership and packet-inverse symmetry; its
availability row is `NOT APPLICABLE`. Ownership: `CHOSEN / INHERITED / MIXED /
UNKNOWN`. Packet inverse: `FULL / PARTIAL / NONE` with eligible comparison scope.
Partial pieces cannot support packet-wide absence claims.

FAIL-MB-018 checks actor/action/referent/stage semantic equivalence and earned
specificity before treating lexical divergence as framing. D-ROLE causal-role
analysis remains distinct. Corroboration is counted per independent fact origin.
Convenience sample distributions remain provisional; inherited choices cannot
be attributed to outlet discretion; sample-dependent findings cannot anchor
verdicts. Timing-unavailable material is not a demonstrated omission.

Evidence: Ceuta RC2 audit and closed-fixture runs, MB-017/018 logs. The gates are
present in the live file despite README's unsynchronized note. This inspection
does not reproduce all historical model tests or establish source-packet
completeness for every media run. No media code added in P0.

## 5 — Voice restoration

Path: `prompts/5-voice-restoration.txt`; canonical editorial instrument. Input:
draft/excerpt and preserved pipeline flags. Native seven-part output: Executive
summary; Phrase inventory; Hotspot table; Stronger terminology suggestions;
Good caveats to preserve; Final voice-restoration pass; Manual review warning.
Softening severity: no meaningful problem / mild / moderate / severe. Hotspot
action: `keep / cut / rewrite / move to introduction`.

It must preserve reception-unverified, provisional, inferred/not-confirmed and
specific-versus-general scope flags. It cannot turn uncertainty into confidence
or add unsupported claims. No scientific finding table, shared-map requirement
or new evidence verification is implied. No automated voice validator or newly
executed voice regression in this work.

## Deferred and auxiliary code

`deferred/1-field-context-generator.txt` exists with TOOL-004 but is deferred,
not a live substitute for grounded claim extraction. It requires explicit
grounding/confidence and validation of inferred field context. Neither inspected
branch contains policy-specific prompts; Policy Atlas remains proposed scope.

`tools/citation_reception_module.py` is actual Python using requests, OpenAlex
and Semantic Scholar. It resolves titles using first search hits, pages cited-by
results up to a bound, takes one S2 citation page, and applies title/snippet
lexicons. Its `REBUTTED` threshold is three replies and refutation signal greater
than twice support; `CONTESTED` also has heuristic thresholds. That cannot prove
technical rebuttal validity or source identity. Full-text confirmation is never
emitted, appropriately. Network behavior was inspected but not live-validated.
This is a candidate integration requiring identity resolution, rate-limit/error
receipts, API contract tests and bounded interpretation, not a trusted Atlas
evidence oracle.

`tools/embed_prompts.py` builds webapp prompt copies. Its parity check currently
fails. The webapp is an interface sandbox, not an Atlas runner or persistence
system. Stage 4 synthesis is explicitly unbuilt. Neither prototypes, prompt
instructions nor proposed acceptance tests count as implemented services.
