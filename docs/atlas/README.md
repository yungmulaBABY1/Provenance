# Atlas deterministic audit adapter — P0 slice

This is an offline Python implementation of one bounded Atlas import path. It
turns an existing Provenance citation-network output and an explicit provenance
sidecar into inspectable records, source eligibility checks, and reproducible
execution receipts. It points; you judge.

It does not execute research audits, retrieve papers, grade scientific truth,
resolve disputes, approve publication, or implement Research/Media interfaces.
No canonical prompt or existing fixture is changed. The parser is intentionally
strict; unsupported formatting is diagnosed, never repaired by a model.

This revision implements the requirements in the P0 review record
(R1, F1–F6, R2 and the null-results rule); see [What changed](#what-changed-in-this-revision)
and [CHANGELOG.md](CHANGELOG.md). Base commit 072fa8a was authored by Codex in a
separate session and is kept as the first commit on the branch.

## Run it

Python 3.11+; standard library only. From the repository root:

```bash
python tests/test-citation-network-checker.py
python -m unittest discover -s tests/atlas -p 'test_*.py' -v

python -m atlas import tests/atlas/power-control.json \
  --out .atlas/power --ledger .atlas/ledger.sqlite
python -m atlas replay .atlas/power/manifest.json .atlas/power/records.jsonl
python -m atlas replay .atlas/power/manifest.json .atlas/power/records.jsonl --level content

python -m atlas import tests/atlas/shen-known-bad.json \
  --out .atlas/shen --ledger .atlas/ledger.sqlite
# Expected exit 1: known-bad output is retained as QUARANTINED.
# Same for tests/atlas/case12-healthy.json and tests/atlas/case13-closed.json.

python -m atlas export .atlas/ledger.sqlite .atlas/all.jsonl
python -m atlas restore .atlas/all.jsonl .atlas/restored.sqlite
python -m atlas export .atlas/restored.sqlite .atlas/restored.jsonl

# Committed receipts (what CI replays):
python -m atlas replay tests/atlas/receipts/power-control/manifest.json \
  tests/atlas/receipts/power-control/records.jsonl --level content
```

`restore` prints which runs had their native records re-derived
(`native_projection_verified`) and which could not be
(`native_projection_unverified`). `import` prints any notices, such as
`VALIDATION_BASELINE_DIFFERS_FROM_WORKING_TREE`.

Exit 0 means successful import, possibly PASS-WITH-REVIEW. Exit 1 means imported
native output fails mechanical checks and is quarantined. Exit 2 means a contract,
input-integrity, conflict or execution error. None means scientific correctness.

Each import writes `records.jsonl`, `manifest.json` and `SHA256SUMS`. Reusing the
same output directory with changed content is rejected. Use a new run ID and
output directory for a new import; keep earlier runs. SQLite writes are atomic
and idempotent; same ID/different canonical content produces ID_CONTENT_CONFLICT.
Filesystem export and SQLite commit are not one distributed transaction: if a
file write fails after commit, rerun the same import to recover the export.

## Verified repository baseline

Base commit: `d7000315197670a59988b2d0b58bf0cdae545fc3`.
The clone and GitHub tree API agreed on the pinned instrument/checker blobs.
Full SHA-256 and Git blob hashes are in [baseline.json](../../atlas/baseline.json).
Exact copies of the ten pinned files are vendored under
[atlas/baseline/files/](../../atlas/baseline/files/) and validation runs from those
copies, not from the working tree.

| Observed at base | Consequence |
|---|---|
| Prompts, archived runs, checker and a limited HTML prototype exist | Reuse the checker; no existing graph service to extend |
| README says 42 runs; tests/RESULTS.md says 54 | Do not use old README totals as current validation evidence |
| Inventory is at root; several links point to reference/ | Use the actual tracked file; inventory itself also contains stale path claims |
| Canonical media file is 2-coverage-network.txt | Do not assume the inventory's claimed rename exists |
| Latest commit repaired philosophy formatting | No additional philosophy edits needed |
| Existing checker regression script passes | Preserve its behavior and diagnostic report |
| tools/embed_prompts.py --check returns STALE | Pre-existing prototype parity failure; outside this slice |
| No Atlas schemas, adapter, ledger, ingestion service or graph backend found | This change implements only the bounded module described here |

The attached master v0.13 is a proposed design. Its SHA-256 is
`4a1dde73bb8c5795b4e50c96f6b01d0901bfa64f580304440a8c0fa44ddf03bd`.
This slice implements portions of A-02 identity/anchors, C-02 mutations, C-03
read eligibility, and the P0 adapter/export path. It does not mark the master
acceptance suite as passed. OnCo and other external research claims were not
revalidated or incorporated as dependencies.

## Contract and boundaries

The experimental record schema is `atlas-adapter/0.2` (import contexts remain
`atlas-adapter/0.1`). It does **not** claim migration
compatibility with the proposed `atlas-core/0.1` or `atlas-decision/0.1` contracts.
Those contracts' Claim, ClaimInstance and EvidenceAssessment distinctions remain
design requirements. No generic finding here replaces those future objects.

The executable minimum contract is [contract.py](../../atlas/contract.py).
Import examples are [power-control.json](../../tests/atlas/power-control.json),
[shen-known-bad.json](../../tests/atlas/shen-known-bad.json), and the paired case 12/13
packet fixtures [case12-healthy.json](../../tests/atlas/case12-healthy.json) and
[case13-closed.json](../../tests/atlas/case13-closed.json), ported from package B.
Required fields, types, reference resolution, duplicate IDs and receipts are
validated. Unknown extra metadata is retained in the exact input context.

| Record | Identity and function |
|---|---|
| Work | Explicit DOI or caller-assigned stable ID; no automatic entity resolution |
| SourceVersion | Explicit edition/assignment and confidence; never a download hash |
| SourceReadReceipt | Run-scoped byte hash, source/version IDs, declared and extracted components, warnings, failed components, per-check eligibility and self-hash |
| Passage | Source version + component + half-open Unicode offsets + bounded quote/hash; separate `exact_match` and `normalized_match`; run-scoped verification receipt |
| CorpusScope | Declared input boundary, selection, retrieval log and native source-lock assertions |
| AuditRun | Exact UTF-8 raw output, hash, native scorecard, parse/checker state, `producing_instrument_compliance`, exposure, source gates, `imported_null_assertion` and `adapter_source_eligibility` as separate fields, target-matched review refs and `mismatched_review_ids` |
| AuditFinding | Original native fields/labels and source-output anchors (line range plus exact character span), mapped checks, unreviewed disposition |
| Relationship | Explicit import mapping from finding to cited passage; never automatic evidentiary support |
| ReviewDecision | Unverified imported review artifact and declared target hash; no automatic human or independent-review credit. Linked from the run only when the target binding is MATCH |
| RunManifest | Base commit, prompt/checker/source hashes, adapter code hashes, parser identity, normalizer id, exact context, environment (including working-tree drift), checker report and record-set hash |

One source origin ID can be shared by many receipts; UNKNOWN is supported. Origin
IDs and exposure declarations are not independence proofs. Different model names,
matching judgments and multiple imported reviews never establish independence.

Every record has `schema_version`, `type`, `id`, and explicit `refs`. Cross-record
references resolve inside the export. Record IDs are immutable: corrections need
new IDs and a later, explicitly designed correction relation. Automatic identity
resolution, correction/adjudication workflows and federation remain unimplemented.

### Native parser profile

The pinned citation-network instrument is authoritative. This adapter structures:

- one exact `FINAL SECTION: STANDARDIZED FINDING TABLE` heading;
- `Finding N` blocks with two-column `Field | Entry` Markdown tables;
- the Artifact 8 scorecard with the existing checker fixture's dimension names;
- exact `SOURCE-LOCK ...:` lines.

Required finding fields come from the native final table. Verification states,
concede labels, failure locations, severity, status and scorecard axes are kept
separate. Native raw values survive, including invalid values. A leading native
severity or location followed by explanatory text is retained with that full text.
Semicolon-separated verification states are accepted only from the native list.
The original UTF-8 output remains byte-reconstructible in AuditRun.raw_output_text.
Source lines point into that original, not a regenerated rendering.

Rule failures against this grammar are `CURRENT_CONTRACT_MISMATCH`: they are
relative to the grammar implemented here, not to whatever instrument produced the
output. Archived outputs that predate the current grammar (the earlier 0–3 cartel
scorecard, no SOURCE-LOCK block) are quarantined with that code; their native
values are kept as written. `AuditRun.producing_instrument_compliance` is
`UNDETERMINED` unless `run.historical_instrument` is `VERIFIED` and its identity is
the baseline prompt's git blob; only then can it read `CONFORMS` or `VIOLATION`.
The parser has a name and version (`atlas-citation-network-native`, version 3),
recorded in each manifest; the version changes whenever parse output can change.

Missing/invalid/duplicate fields are diagnostics; labels are never completed from
surrounding prose. A valid enum swap can still be semantically wrong: every result
retains SEMANTIC_REVIEW_REQUIRED. Only the exact explicit null sentence
`No findings of consequence.` is supported in this first profile. Other null
wording is retained but requires a future versioned parser extension.

The current native checker runs unchanged and its full report is preserved. It
has broader textual scans than the adapter (including some quoted/fenced text).
Those scans can flag quoted vocabulary or headings; neither executes instructions.
The new tests establish parser data handling, **not** LLM prompt-injection safety.

### Source-read and anchor profile

Inputs are offline, explicitly declared relative paths beneath `--root`, with
exact SHA-256 pins. Escaping paths/symlinks and changed source bytes fail closed.
The checker and prompt come from the vendored baseline, checked on SHA-256, git
blob and byte count; a tampered vendored file fails with `BASELINE_HASH_MISMATCH`.
If a working-tree copy differs from (or is missing relative to) the vendored
baseline, import still succeeds and records
`VALIDATION_BASELINE_DIFFERS_FROM_WORKING_TREE` in the manifest's environment
block, naming each file. A modified working-tree checker is never executed.
The executable checker path is fixed in code.
Verified checker and output bytes are copied to a temporary snapshot; Python
isolated mode prevents neighboring corpus files from shadowing standard modules.
This is not an operating-system sandbox for arbitrary external executables.

Only direct UTF-8 extraction (`plain-utf8`, version `1`, empty configuration) is
eligible for physical span verification. Arbitrary OCR/PDF extraction claims
remain EXTRACTION_UNVERIFIED. Component kinds and semantic roles are **declared
by the sidecar author**, not inferred or scientifically verified by the parser.
READ_FOR_DECLARED_SCOPE means the adapter could read the supplied components; it
does not establish what the historical model read or that a complete paper was read.

Checks specify exact source/component/passage requirements. Metadata is not
methods/results evidence. Missing requirements cannot pass vacuously. Source-dependent
citation findings/null assertions require at least one content
check; mapping them only to eligible metadata checks cannot promote them. Unavailable
components block only dependent checks; unverified versions/extraction/anchors
remain pending. Warnings outside required components allow bounded eligibility
with limitations, not global completeness. No percentage-of-pages threshold exists.

Anchors record two comparisons separately. `exact_match`: the code points of
`source[start:end]` equal the quote, with no normalization. `normalized_match`:
they agree after normalizer `nfc-whitespace/2` (Unicode NFC plus whitespace
collapse). Only an exact match is displayed as `MATCH`. When only the normalized
forms agree the state is `NORMALIZED_MATCH_ONLY`, which is never presented as an
exact quotation and limits a check to `ELIGIBLE_WITH_LIMITATIONS` at best.
Otherwise the state is `MISMATCH` or `UNRESOLVABLE`. NFKC is not used: it equated
10² with 102, H₂O with H2O, ½ with 1⁄2 and µ with μ. Normalization does not
dehyphenate, translate, fuzzy-match or relocate, and −0.5 (U+2212) never matches
-0.5. Matching requires the declared component and exact offsets, and the declared
hash must agree with the quote. A MATCH proves that span correspondence only;
source edition confidence and scientific adequacy remain separate.

Historical FULL-TEXT-CONFIRMED labels are **reported native assertions**. In the
positive repository fixture import, only the packet's metadata is physically
available. Native syntax passes; source-dependent findings stay NOT ASSESSABLE.
This is intentional. A metadata-only import must not launder an old label into
a newly verified paper reading.

### Persistence and receipts

SQLite is a small local append-only ledger behind a storage-independent record
contract. Transactions serialize writers; duplicate identical records are no-ops;
conflicts roll back the whole batch. SQL triggers prohibit ordinary UPDATE/DELETE.
An administrator with filesystem access can replace/drop the database: this is
integrity checking, not tamper-proof storage or a signed transparency log.

Restore and append check every bundle before committing:

- every AuditRun and every record belonging to it must be listed by exactly one
  RunManifest (Work and SourceVersion may be shared); anything uncovered is
  `INVALID_MANIFEST_COVERAGE`;
- for each run whose recorded parser version this code supports, native
  findings, scorecard, parse issues, imported source lock, null assertion and
  output anchors are re-derived from `raw_output_text` and must match exactly,
  otherwise `NATIVE_PROJECTION_MISMATCH`;
- a run whose recorded parser version is not supported is neither rejected nor
  trusted: it is reported as `NATIVE_PROJECTION_UNVERIFIED`, with the version
  named, and is never labelled verified.

The manifest hash is unkeyed and can be recomputed by anyone; re-derivation, not
the hash, is what protects native labels.

Canonical JSON uses sorted keys, compact separators, UTF-8 and no NaN/Infinity;
JSONL records are sorted by ID. This is this profile's serializer, not an RFC 8785
implementation. Receipts pin the Python and Unicode versions. Replay reruns the
deterministic import, not the historical model investigation, at one of two levels:

- `--level strict` (default): records and manifest must be byte-identical,
  environment included;
- `--level content`: input context, declared input hashes, adapter code hashes,
  parser identity, normalizer id, baseline hashes and every record except the
  manifest's environment block must be identical; the environment delta is
  printed.

`REPLAY_MISMATCH` names the differing component(s): `input`, `records` (with
ids), `manifest`, `parser`, `normalizer`, `adapter_code`, `baseline`,
`declared_inputs`, or `environment` (strict only). CI runs content replay on every
committed receipt under `tests/atlas/receipts/`, because setup-python's '3.11'
moves between patch releases. The 072fa8a receipts in
`tests/atlas/receipts/historical-072fa8a/` are kept as historical artifacts and
cannot be replayed or restored by this version.

Full papers are not copied into records. Explicit passage quotes and the complete
raw audit output can still contain restricted material. All resulting records are
local/unreviewed; there is no public release service or licensing determination.
The flags are metadata, not implemented multi-user access control.

### Null results

An imported null assertion and the adapter's present-day source access are two
separate facts. `AuditRun.imported_null_assertion` holds the exact null sentence
(or null); `AuditRun.adapter_source_eligibility` holds per-check eligibility from
this import. No field derives a clean or acquitted state from the two, and
`paper_clean` is always false. The historical model's null assertion does not
show what that model read, and the adapter's read does not show it either.

## What changed in this revision

| Requirement | Change | New or changed state |
|---|---|---|
| R1, F1, F6 | Manifest coverage; native records re-derived on restore/append; parser identity in the manifest | `INVALID_MANIFEST_COVERAGE`, `NATIVE_PROJECTION_MISMATCH`, `NATIVE_PROJECTION_UNVERIFIED` |
| R2 | Exact versus normalized anchors; NFKC removed; normalizer `nfc-whitespace/2`; record schema 0.2 | `NORMALIZED_MATCH_ONLY` |
| F2 | Grammar failures are contract-relative; producing-instrument compliance undetermined unless verified | `CURRENT_CONTRACT_MISMATCH` replaces `INSTRUMENT_VIOLATION`; `producing_instrument_compliance` |
| F3 | Validation baseline vendored; working-tree drift reported, not fatal | `VALIDATION_BASELINE_DIFFERS_FROM_WORKING_TREE`, `BASELINE_HASH_MISMATCH` |
| F4 | Strict and content replay levels; CI content-replays committed receipts | `REPLAY_MISMATCH` names components |
| F5 | Only target-matched reviews in run refs | `mismatched_review_ids` |
| Null rule | `clean_display` and `SCOPED_NULL_ASSERTION_ONLY` removed | `imported_null_assertion`, `adapter_source_eligibility` |
| Port from package B | Case 12/13 paired packet fixtures; exact character spans on output anchors; contract inventories in [contracts/](contracts/) (documentation only) | `native_output_anchor.char_start/char_end` |
| Found during regeneration | Unknown scorecard dimension issues were emitted in hash-seed order; now sorted; parser version 3 | — |

### Limits

- No scientific audit, counter-audit or human adjudication was performed. Model
  agreement is not independence.
- Source receipts show the adapter's read, not a historical model's.
- An unsupported parser version is reported unverified, not rejected: anyone
  editing a bundle can avoid re-derivation that way, at the cost of the run
  being labelled `NATIVE_PROJECTION_UNVERIFIED`.
- Re-derivation covers native projections. Adapter-computed fields (source
  eligibility, syntax, checker report) are protected only by the unkeyed
  manifest hash; the checker is not re-run on restore.
- Historical outputs are parsed only against the current grammar; there are no
  versioned historical grammars yet, so they stay quarantined.
- Import contexts hashed under the old NFKC normalizer will show `MISMATCH` for
  passages containing compatibility characters (fail closed).
- `tools/embed_prompts.py --check` still returns STALE; this is pre-existing
  baseline debt, not addressed here.

## Real-source packet: power posing

The first real-source packet connects the four-source power-posing pilot
([compliance/PACKET.md](../../compliance/PACKET.md)) to the archived pilot output
([compliance/run-output.md](../../compliance/run-output.md)). It uses the existing
adapter and import-context format; no new runtime or record type was added.
Details, coverage and limits are in
[tests/atlas/sources/power-posing/README.md](../../tests/atlas/sources/power-posing/README.md).

- **Coverage (retrieved 2026-10-30):**
  - S2 (publisher PDF, author-hosted) and S4 (accepted manuscript) were
    retrieved and hashed; seven bounded excerpts are kept.
  - S1 and S3 returned HTTP 403 and are recorded as `RETRIEVAL_FAILED`.
- **Excerpt files:** each excerpt is an exact substring of pinned `pdftotext`
  output. The adapter reads only the committed excerpt files, so every content
  check is at most `ELIGIBLE_WITH_LIMITATIONS`. The excerpt-to-PDF link is
  re-verified separately by `source_packet.py verify`, which needs network
  access.
- **Mappings:** each archived finding maps only to the sources its own Evidence
  field names. Finding 1 is eligible for its declared checks with limitations.
  Finding 2 is `NOT_ASSESSABLE`, because S3's own text is missing; S4's
  description of S3 does not stand in for it.
- **Three separate facts:** the historical assertion (`native`, e.g.
  `FULL-TEXT-CONFIRMED`), what the adapter reads and matches now (receipts,
  anchors, eligibility), and substantive support (`assessment: UNREVIEWED`,
  relationships `UNADJUDICATED`). A matching quotation is not scientific support
  and does not show what the historical run read.
- **Controls** (`test_power_sources.py`): missing methods, failed extraction,
  changed source bytes, incorrect or reflowed quotations, unavailable sources,
  and all sources missing. Missing evidence blocks only the checks that depend
  on it, and never yields a clean state.

## Evidence-proposition reviews (`atlas-evidence-review/2`)

Adapter 0.3.0 has one versioned review kind, implemented in
[atlas/reviews.py](../../atlas/reviews.py). It reuses the existing
`ReviewDecision` record and import-context `reviews` list; the record schema
stays `atlas-adapter/0.2`, and old-style output reviews are unchanged.

- **Artifact.** A review is a JSON artifact with `schema: atlas-evidence-review/2`,
  declared in the context as `{"id", "artifact", "review_schema"}`. It records:
  - the target;
  - coverage (reviewed and not reviewed);
  - reviewer identity, kind and context;
  - time, method, hashed inputs and exposure;
  - examination boundary and unavailable material;
  - a disposition, plus one per part;
  - reasons and exact locators (offsets and hashes into the source extraction);
  - qualifications and the contrary search;
  - the strongest contrary interpretation;
  - what would change the assessment.
- **Dispositions:** `SUPPORTS`, `SUPPORTS_WITH_QUALIFICATION`, `CONTRADICTS`,
  `INSUFFICIENT_EVIDENCE`, `PENDING`. These belong to this extension. They do not
  replace native labels, do not change `AuditFinding.assessment` or
  `Relationship.epistemic_status`, and say nothing about the rest of the finding.
  Version 1 rejects any artifact claiming human adjudication, independence or a
  finding-level effect.
- **Binding.** A review targets an exact span of one native field of one finding,
  one mapped check, its passages, one source version and its input bytes. On
  import the adapter compares every identity with the run's own records:
  - `output`
  - `finding` (native-projection digest)
  - `proposition` (span text)
  - `mapping` (check digest, finding-to-check mapping, passage set)
  - `passages`: one descriptor per bound passage, compared field by field with the
    run's Passage record. A descriptor is the source version, component, start and
    end offsets, offset unit, interval and quotation hash, so a moved locator with
    an unchanged quotation still unbinds
  - `source_version`
  - `source_input`

  Any difference makes the review `TARGET_MISMATCH`, names the differing
  components and drops the review from the run's refs (it is listed under
  `mismatched_review_ids`). A changed mapping never inherits an old review.
- **Restore and append.** Integrity re-checks every evidence review:
  - the stored artifact text must hash to the artifact declared in the run's
    input context;
  - the parsed review must equal the stored fields;
  - the binding and refs are re-derived from the bundle's records.

  Any difference is rejected (`REVIEW_ARTIFACT_MISMATCH`,
  `REVIEW_BINDING_MISMATCH`).
- **Immutability.** A revised review under the same ID is `ID_CONTENT_CONFLICT`.
  Revisions and disagreements are new records; earlier ones are kept.
- **Not covered by the adapter.** It does not check that a locator's quotation
  appears in the source PDF. `tests/atlas/sources/power-posing/source_packet.py
  verify` does that, online.

The first review pair is in
[tests/atlas/reviews/power-posing/](../../tests/atlas/reviews/power-posing/README.md):
Finding 1's S2 clause, imported by
[power-sources-reviewed.json](../../tests/atlas/power-sources-reviewed.json) as run
`urn:atlas:import:power-posing-sources:3`. Run `:1` and its receipt are unchanged.

**Contract history.** `atlas-evidence-review/1` (adapter 0.2.0, PR #9 before the
fix) bound each passage by quotation hash only. Moving a passage's offsets while
keeping its quotation left the review attached. `/1` is retired:
- import and restore reject it with `UNSUPPORTED_REVIEW_SCHEMA` rather than trust it;
- its artifacts are preserved in `tests/atlas/reviews/power-posing/v1/`;
- its receipt (run `:2`) is preserved in `tests/atlas/receipts/historical-4718225/`.

## Validation and independent review

[EXPECTED.txt](../../tests/atlas/EXPECTED.txt) was written before implementation;
a dated amendment withdraws its scoped no-issue display.
[test_adapter.py](../../tests/atlas/test_adapter.py) exercises the pre-existing
positive, known-bad and review fixtures, plus deterministic mutations and
synthetic source checks. The review-record requirements have their own test
files (`test_integrity.py`, `test_anchors.py`, `test_contract_labels.py`,
`test_baseline.py`, `test_replay.py`, `test_reviews.py`, `test_paired_fixtures.py`,
`test_output_spans.py`, `test_determinism.py`). These are developer-authored contract tests and known
regressions, not held-out evaluations or independent scientific validation.

The available earlier Shen counter-audit references the earlier citation output.
Its hash does not match the revised known-bad fixture. The import records
TARGET_MISMATCH; it cannot confer counter-audit credit. Even matching a declared
target hash would only establish that mapping, not genuine independence or that
the reviewer actually inspected the target. Unknown historical details stay UNKNOWN.

See [REVIEW_HANDOFF.txt](REVIEW_HANDOFF.txt) for the independent reviewer task and
[validation.json](../../tests/atlas/validation.json) for locally executed results.
CI is configured; a workflow file alone is not evidence of a hosted CI pass.

Next: independent review of the power-posing source packet's mappings and excerpt
choice; versioned historical grammars so archived outputs can be read under their own
contract; and a separately attributed counter-audit. Broader instrument adapters, persistent shared services,
API ingestion, claims/adjudication schemas, and Research/Media interfaces remain
proposed work.
