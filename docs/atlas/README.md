# Atlas deterministic audit adapter — P0 slice

This is an offline Python implementation of one bounded Atlas import path. It
turns an existing Provenance citation-network output and an explicit provenance
sidecar into inspectable records, source eligibility checks, and reproducible
execution receipts. It points; you judge.

It does not execute research audits, retrieve papers, grade scientific truth,
resolve disputes, approve publication, or implement Research/Media interfaces.
No canonical prompt or existing fixture is changed. The parser is intentionally
strict; unsupported formatting is diagnosed, never repaired by a model.

## Run it

Python 3.11+; standard library only. From the repository root:

```bash
python tests/test-citation-network-checker.py
python -m unittest discover -s tests/atlas -p 'test_*.py' -v

python -m atlas import tests/atlas/power-control.json \
  --out .atlas/power --ledger .atlas/ledger.sqlite
python -m atlas replay .atlas/power/manifest.json .atlas/power/records.jsonl

python -m atlas import tests/atlas/shen-known-bad.json \
  --out .atlas/shen --ledger .atlas/ledger.sqlite
# Expected exit 1: known-bad output is retained as QUARANTINED.

python -m atlas export .atlas/ledger.sqlite .atlas/all.jsonl
python -m atlas restore .atlas/all.jsonl .atlas/restored.sqlite
python -m atlas export .atlas/restored.sqlite .atlas/restored.jsonl
```

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

The experimental namespace is `atlas-adapter/0.1`. It does **not** claim migration
compatibility with the proposed `atlas-core/0.1` or `atlas-decision/0.1` contracts.
Those contracts' Claim, ClaimInstance and EvidenceAssessment distinctions remain
design requirements. No generic finding here replaces those future objects.

The executable minimum contract is [contract.py](../../atlas/contract.py).
Import examples are [power-control.json](../../tests/atlas/power-control.json)
and [shen-known-bad.json](../../tests/atlas/shen-known-bad.json).
Required fields, types, reference resolution, duplicate IDs and receipts are
validated. Unknown extra metadata is retained in the exact input context.

| Record | Identity and function |
|---|---|
| Work | Explicit DOI or caller-assigned stable ID; no automatic entity resolution |
| SourceVersion | Explicit edition/assignment and confidence; never a download hash |
| SourceReadReceipt | Run-scoped byte hash, source/version IDs, declared and extracted components, warnings, failed components, per-check eligibility and self-hash |
| Passage | Source version + component + half-open Unicode offsets + bounded quote/hash; run-scoped verification receipt |
| CorpusScope | Declared input boundary, selection, retrieval log and native source-lock assertions |
| AuditRun | Exact UTF-8 raw output, hash, native scorecard, parse/checker state, exposure and source gates |
| AuditFinding | Original native fields/labels and source-output line anchors, mapped checks, unreviewed disposition |
| Relationship | Explicit import mapping from finding to cited passage; never automatic evidentiary support |
| ReviewDecision | Unverified imported review artifact and declared target hash; no automatic human or independent-review credit |
| RunManifest | Base commit, prompt/checker/source hashes, adapter code hashes, exact context, environment, checker report and record-set hash |

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
exact SHA-256 pins. Escaping paths/symlinks, changed source bytes and changed
checker/prompt files fail closed. The executable checker path is fixed in code.
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

Normalization `nfkc-whitespace/1` applies Unicode NFKC and collapses whitespace.
It does not dehyphenate, translate, fuzzy-match or relocate. Matching requires the
declared component and exact offsets. Normalized quote and expected hash must
match actual source bytes after decoding. A MATCH proves that span correspondence
only; source edition confidence and scientific adequacy remain separate.

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

Canonical JSON uses sorted keys, compact separators, UTF-8 and no NaN/Infinity;
JSONL records are sorted by ID. This is this profile's serializer, not an RFC 8785
implementation. Receipts pin the Python and Unicode versions. Replay requires
matching input bytes, adapter code/baseline and environment; a changed environment
or implementation requires a new receipt. Replay reruns the deterministic import,
not the historical model investigation.

Full papers are not copied into records. Explicit passage quotes and the complete
raw audit output can still contain restricted material. All resulting records are
local/unreviewed; there is no public release service or licensing determination.
The flags are metadata, not implemented multi-user access control.

## Validation and independent review

[EXPECTED.txt](../../tests/atlas/EXPECTED.txt) was written before implementation.
[test_adapter.py](../../tests/atlas/test_adapter.py) exercises the pre-existing
positive, known-bad and review fixtures, plus deterministic mutations and
synthetic source checks. These are developer-authored contract tests and known
regressions, not held-out evaluations or independent scientific validation.

The available earlier Shen counter-audit references the earlier citation output.
Its hash does not match the revised known-bad fixture. The import records
TARGET_MISMATCH; it cannot confer counter-audit credit. Even matching a declared
target hash would only establish that mapping, not genuine independence or that
the reviewer actually inspected the target. Unknown historical details stay UNKNOWN.

See [REVIEW_HANDOFF.txt](REVIEW_HANDOFF.txt) for the independent reviewer task and
[validation.json](../../tests/atlas/validation.json) for locally executed results.
CI is configured; a workflow file alone is not evidence of a hosted CI pass.

Next: independent adversarial code review of this pinned slice, then a rights-cleared
real source packet with reviewable component/anchor mappings and a separately
attributed counter-audit. Broader instrument adapters, persistent shared services,
API ingestion, claims/adjudication schemas, and Research/Media interfaces remain
proposed work.
