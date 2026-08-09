# Architecture Note: Evidence Flow, Source of Truth, and Open Decisions

## Status and scope

This note records the operating architecture of Provenance as of 2026\-08\-09\. It
is a design constraint for prompt changes and interface experiments, not an
execution artifact\. The files under `prompts/` execute; this note explains what
must remain true across them\.

The workflow is evidence\-led and human\-adjudicated\. It may surface patterns, but
it does not turn a model output, citation distribution, or coverage majority into
a factual verdict\. There is no composite score\.

Implementation state and validation state are independent\. A prompt can be
canonical but untested\. A repair can be tested on a candidate artifact but not
yet synchronized into the canonical prompt\. The
[current\-state inventory](current-state-inventory.md) records both\.

## Hypothesis handling

A hypothesis is a retrieval aid, not a conclusion\.

- Record an operator\-supplied hypothesis as **operator\-originated**\.
- Record a lead created by a prior audit or extractor as **construction\-audit**
  **emergent**\.
- Record a lead first exposed by retrieval as **retrieval\-emergent**\.
- Origin is provenance, not evidence\. A lead becomes a finding only through
  retrieved, attributable material that survives the applicable gates\.
- Search deliberately for evidence that supports and weakens each material lead\.
  Record the search boundary on both sides; an unperformed search is not negative
  evidence\.
- Bound emergent leads to inconsistencies or dependencies already inside the
  audit object\. The register must not become a recursive scope\-expansion engine\.
- Apply the flip/mirror guard to prior\-sensitive assignments such as cause,
  blame, role, ideology, and motive\.

Hypothesis resolution and finding\-level counterfactuals are different axes\.
Hypotheses may be `CONFIRMED`, `PARTIALLY CONFIRMED`, `REFRAMED`, `NOT CONFIRMED`,
or `INSUFFICIENT EVIDENCE`\. A prosecutor finding separately faces the concede
test: `SURVIVES`, `NARROWS`, or `DEFEATS`\.

The complete resolution vocabulary is tested in Madison/Seattle and present in
the integrated RC2 artifact, but it is not yet fully synchronized into the
canonical media prompts\.

## Retrieval discipline

### Corpus and source boundary

State how the corpus was selected\. An outlet set assembled from sources the
operator already distrusts cannot support an unqualified distributional
conclusion\.

For media, retrieve full text or substantial excerpts, exact publication date
and time, byline, attribution, and update/correction information\. If an
institution has both a written release and a spoken briefing, retrieve both when
available; inherited wording may explain apparent editorial divergence\.

A closed synthetic fixture is a closed corpus: do not browse or supplement it\. A
live audit must label unretrieved material provisional rather than completing the
record from memory\.

### Operator prior and field prior

The operator’s prior and the field’s prior require different checks\.

- The **operator prior** is exposed through disclosure, origin tagging, symmetry,
  balanced retrieval, and the concede test\.
- The **field prior** appears as fluent, cited, peer\-reviewed background\. It is
  exposed only by retrieving the construct\-establishment literature, actual
  instrument or coding rules, contrary evidence, and citation context\.

“Cited” therefore does not mean “uncontested in the respect the claim requires\.”
Model fluency in a field’s dominant dialect is not an independent backstop\.

### What counts as corroboration

Independence is evaluated per load\-bearing fact, not by counting outlets\.

- Count reporting organizations and upstream information origins separately;
  both totals are descriptive\.
- For every contested or load\-bearing fact, identify the pieces asserting it and
  the independent origins supporting that fact\.
- Multiple outlets repeating one wire, release, briefing, or ministry figure are
  amplification, not corroboration\.
- Apply `CROSS-OUTLET-CORROBORATED` only when that fact has at least two
  independent origins, and state the count\.
- Keep source\-chain status separate from substantive verification\.
  `CHAIN-CONFIRMED`, `CHAIN-INFERRED`, and `CHAIN-PROVISIONAL` describe
  dependence; they do not establish the underlying fact\.

### Timing, placement, and editorial choice

Cross\-piece omission and within\-piece placement are different analytical
objects\.

- A **selection** finding requires evidence that the omitted fact was available
  before publication\. Unknown availability caps the finding at provisional; a
  later fact is a timing artifact\.
- A **prominence\-packaging** finding concerns placement of a fact already present
  in a full\-text\-confirmed piece\. Cross\-piece availability is not applicable, but
  packaging provenance, version timing, and packet\-inverse symmetry still apply\.

One gate must not serve two objects with different evidentiary preconditions\.
When it does, the object with the weaker precondition is liable to disappear
before evaluation\. `FAIL-MB-017` is the demonstrated media case; construct
establishment versus definition/operationalization is the analogous research
shape\.

Any claim about an **outlet choice** must consult whether wording, packaging,
source selection, or assignment was `CHOSEN`, `INHERITED`, `MIXED`, or `UNKNOWN`\.
This coupling has recurred in prominence and semantic/language analysis\. It
remains a logged promotion candidate rather than a shared primitive until a
third independent recurrence or dedicated harmonization review\.

## Canonical sources and generated copies

Canonical prompt files are the source of truth\. Generated or embedded copies
must identify their canonical path, snapshot/checksum, and state that the
repository copy wins on conflict\.

Self\-contained shipped prompts may duplicate shared text\. The avoidable bug is
duplication in authored sources with no parity mechanism\. The preferred target
is one canonical authored primitive, a build step that emits self\-contained
prompt copies, and a parity check against the built artifacts\.

The webapp is a sandbox prototype, not a supported application or an execution
surface\. Its prompt payload follows the generated\-copy rule and currently passes
the parity check\. Its separately authored documentation and run summaries remain
noncanonical presentation copies\.

## Runtime and simplification

Prompt size did not behave as a dominant runtime predictor in the fixed\-fixture
measurements across an approximately 3\.5× size range\. That observation does not
prove prompt size is irrelevant, and it is not a general runtime benchmark\. It
does remove speed alone as a sufficient justification for deleting safeguards\.

Prefer, in order: validity repair, interaction regression, canonicalization of
genuine duplicates, null suppression for readability, objective conditional
gates, remeasurement, and only then substantive deletion\. Drift reduction and
output readability remain valid reasons to simplify\.

## Decisions and current disposition

1. **Multi\-claim citation\-network scope — open\.** The research sequence remains
   single\-claim by default\. Any future scope grant must be limited to
   inventory\-enumerated claim IDs, update all handoffs and finding tables, and
   follow retrieval\-compliance validation\.
2. **Citation\-network execution compliance — locally resolved, boundary open\.**
   The completion contract and checker passed supplied packets at 4, 12, and 26
   sources, through 70 selected edges\. Open\-ended retrieval remains unvalidated\.
   `TOOL-002` also remains open because the checker fixtures do not reproduce the
   original silent\-omission/gate\-failure/verdict\-issued behavior\.
3. **Shared primitives — open\.** Six live prompt headers point to nonexistent
   sections in the bannered, superseded `reference/shared-primitives.txt`\. Decide
   whether to delete or redirect those references, then choose a canonical
   authored\-source and parity strategy before deleting the stale file\.
4. **Acquittal validation — partially demonstrated\.** Claim extraction has
   returned no gap, and the healthy paired citation\-network case was acquitted
   for structural reasons\. No full research chain has returned clean\. The media
   proportionate\-negative case is built but unrun\.
5. **Media counter\-audit — explicit design decision\.** Balancing remains internal
   to the two media prompts\. Add a separate Stage 3 only after observed evidence
   that the internal guards are insufficient\.
6. **Coverage over time — deferred\.** Treat trajectory/drift as a separate branch
   with its own sampling, timing, and update rules\.
7. **Verdict scale — derivation resolved, notation still open\.** Do not add a new
   parallel scale\. The concede test derives the existing result\. Construct and
   internal\-validity prompts already represent the output as audited\-claim status
   plus surviving residual\. Harmonization remains incomplete, and the
   `residual: none` path has not appeared in a run\.
8. **Architecture audit — partially discharged\.** Drift and duplication reviews
   were run on both prompt pairs and followed by targeted parity fixes\. The cold
   whole\-file deletion pass against the deletion standard remains undone\.
9. **Media RC2 synchronization — open\.** The integrated `FAIL-MB-017/018`
   artifact passed its standalone and joint expectations\. The repository’s
   shorter coverage prompt is a different base and must not be replaced or
   patched blindly\.

## Regression protection status

|Case or fixture                |State                                          |What it establishes                                                       |
|-------------------------------|-----------------------------------------------|--------------------------------------------------------------------------|
|Case 11, proportionate article |Built, never run                               |Media clean-result capacity if it passes                                  |
|CE-006/007 joint citation      |Built, no logged run                           |Opposite attribution outcomes under a document-level disambiguation change|
|MIX-01                         |Built, no logged run                           |Per-claim separation inside one research target                           |
|Citation cases 12/13           |Run and passed as a pair                       |Citation-network acquittal versus closure under matched surface indicators|
|`FAIL-CN-001` compliance pilots|Run and passed at three supplied-packet burdens|Output-contract survival, not open-retrieval correctness                  |
|`FAIL-MB-017`                  |Complete fixture; integrated RC2 pass          |Later revisions must not silently suppress within-piece prominence        |
|`FAIL-MB-018`                  |Complete fixture; integrated RC2 pass          |Wording alone cannot become a framing finding before semantic materiality |
|`ceuta-prominence-d2-ownership`|Specified, not built                           |Cross-branch ownership with a supplied prior packaging finding            |

The two Ceuta cases are the first repository protection specifically aimed at
silent capability suppression by a later prompt revision, rather than only at a
model producing the wrong answer\.

## Change rule

Drive prompt changes from observed run behavior when possible, then validate on
a targeted case or live rerun\. Record what fired, what changed, and what was
killed in `tests/RESULTS.md`; use `FAILURES.md` and `CHANGELOG.md` to distinguish
observed failures from precautionary guards\.

Before removing a rule, identify the failure it prevents, whether that failure
was observed, where the protection moves, and which case will detect recurrence\.
Do not delete a rule merely because a newer model might infer it\.
