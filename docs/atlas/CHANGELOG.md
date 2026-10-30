# Atlas adapter changelog

## Unreleased — adapter 0.3.0: review binding contract `atlas-evidence-review/2`

- Reviews now bind each passage by a full descriptor: source version, component,
  start and end offsets, offset unit, interval and quotation hash. Under `/1` a
  passage moved by one character kept the same quotation hash, so it became
  `MISMATCH` while both reviews stayed `MATCH`. That gap is closed.
- `/1` is retired: import and restore reject it with `UNSUPPORTED_REVIEW_SCHEMA`.
  The `/1` artifacts are kept in `tests/atlas/reviews/power-posing/v1/`.
- The F1-S2 reviews are re-issued as `/2`. Only the binding changed; each has a
  `reissue` block naming its `/1` predecessor by hash, and neither review was
  repeated. They are imported as run `:3` (`tests/atlas/power-sources-reviewed.json`).
- Receipts:
  - the six receipts current at 4718225 moved unchanged to
    `tests/atlas/receipts/historical-4718225/`;
  - the `/1`-bound run `:2` receipt there is rejected on restore, and the
    others still restore;
  - current receipts regenerated (only manifests differ for unreviewed runs).
- New tests: a moved locator unbinds in both directions; every descriptor field
  is bound; the review stays detached after export and restore; restore rejects
  a moved locator with a kept binding; `/1` artifacts and receipts are rejected.
  Reverting to quotation-only binding fails 10 of them.

## Adapter 0.2.0 (PR #9 at 4718225, not merged): first substantively reviewed evidence relationship

- New review kind `atlas-evidence-review/1` (`atlas/reviews.py`), imported as a
  `ReviewDecision`. It is bound to an exact proposition span, finding projection,
  mapping, passages, source version and input bytes; any change gives
  `TARGET_MISMATCH` with the components named. Restore and append re-derive the
  binding and check the artifact. Record schema unchanged (`atlas-adapter/0.2`).
- Reviews of Finding 1's S2 clause (`tests/atlas/reviews/power-posing/`):
  - review A (primary session): `SUPPORTS_WITH_QUALIFICATION`;
  - review B (separate subagent context): `SUPPORTS`.

  Both are kept. Neither is independent, and neither is human adjudication.
- `tests/atlas/power-sources-reviewed.json` imports them as run `:2`.
- `source_packet.py verify` also re-checks review locators against a fresh
  extraction.
- Receipts:
  - the five receipts current at 7c55e2c moved unchanged to
    `tests/atlas/receipts/historical-7c55e2c/` (restorable, not replayable
    under 0.2.0 code);
  - current receipts regenerated (only manifests differ);
  - new receipt `power-sources-reviewed`.

## Unreleased — power-posing real-source packet

No adapter code changes; record schema, parser and normalizer unchanged.

- `tests/atlas/sources/power-posing/`: bounded excerpts from the two retrievable
  packet sources (S2 publisher PDF, S4 accepted manuscript), with retrieval and
  extraction provenance in `SOURCES.json`. S1 and S3 (HTTP 403) are recorded as
  `RETRIEVAL_FAILED`. `source_packet.py` rebuilds or re-verifies the packet
  against the live sources; it is not run in CI.
- `tests/atlas/power-sources.json`: import of the archived pilot output with
  explicit finding-to-check mappings based on each finding's Evidence field.
- `tests/atlas/test_power_sources.py`: provenance, the three separate facts, and
  controls for missing methods, failed extraction, changed bytes, incorrect
  quotations, unavailable sources; CLI import/export/restore/replay.
- `tests/atlas/receipts/power-sources/`: committed receipt, content-replayed by CI.

## Unreleased — P0 review repairs (branch `atlas/p0-adapter`)

Implements the requirements in the P0 review record (sections 5 and 6) on top
of 072fa8a. Record schema `atlas-adapter/0.2`; import contexts stay
`atlas-adapter/0.1`; parser `atlas-citation-network-native` version 3;
normalizer `nfc-whitespace/2`.

### Integrity (R1, F1, F6)
- Every AuditRun and every record belonging to it must be covered by exactly one
  RunManifest; Work and SourceVersion may be shared. Uncovered records are
  rejected with `INVALID_MANIFEST_COVERAGE`.
- RunManifest records the parser identity (name, version, SHA-256 of
  `atlas/native.py`).
- Restore and append re-derive native findings, scorecard, parse issues,
  imported source lock, null assertion and output anchors from
  `raw_output_text`; any difference is `NATIVE_PROJECTION_MISMATCH`.
- Unsupported parser versions are reported as `NATIVE_PROJECTION_UNVERIFIED`.

### Anchors (R2)
- Passages store `exact_match` and `normalized_match` separately. `MATCH` only
  when exact; `NORMALIZED_MATCH_ONLY` otherwise when normalized forms agree; it
  is a named limitation, never full eligibility.
- NFKC removed; normalizer is `nfc-whitespace/2`; record schema bumped to 0.2.

### Contract-relative labels (F2)
- Parser issue code `INSTRUMENT_VIOLATION` renamed `CURRENT_CONTRACT_MISMATCH`.
- New `AuditRun.producing_instrument_compliance`: `UNDETERMINED` unless the
  historical instrument is `VERIFIED` as the baseline prompt blob; then
  `CONFORMS` or `VIOLATION`.

### Validation baseline (F3)
- The ten pinned files are vendored under `atlas/baseline/files/` and checked
  on SHA-256, git blob and byte count (`BASELINE_HASH_MISMATCH`).
- Working-tree drift is recorded as `VALIDATION_BASELINE_DIFFERS_FROM_WORKING_TREE`
  in the manifest environment; import still succeeds.

### Replay (F4)
- `replay --level strict` (default, byte-identical) and `--level content`
  (everything except the environment block; environment delta printed).
- `REPLAY_MISMATCH` names the differing component(s).
- CI content-replays every committed receipt.

### Reviews (F5)
- AuditRun refs list only target-matched reviews; others are under
  `mismatched_review_ids`.

### Null results
- `clean_display` and `SCOPED_NULL_ASSERTION_ONLY` removed. AuditRun records
  `imported_null_assertion` and `adapter_source_eligibility` as separate facts.

### Ported from package B
- Case 12/13 paired packet fixtures (`tests/atlas/case12-healthy.json`,
  `tests/atlas/case13-closed.json`).
- Exact character spans (`char_start`, `char_end`) on finding output anchors,
  re-derived on restore.
- `docs/atlas/contracts/prompt-contracts.md` and `native-contract-excerpts.md`
  (documentation only).

### Fixed
- Issues for unknown scorecard dimension names were emitted in hash-seed order,
  so imports of affected outputs were not deterministic across processes
  (inherited from 072fa8a). They are now sorted; parser version 3.

### Receipts
- Current receipts for power-control, shen-known-bad, case12-healthy and
  case13-closed under `tests/atlas/receipts/`, built on CPython 3.11.17.
- The 072fa8a receipts are kept under `tests/atlas/receipts/historical-072fa8a/`;
  they cannot be replayed or restored by this version.

### Known baseline debt
- `tools/embed_prompts.py --check` returns STALE at the base commit; not changed.

## 0.1.0 — 072fa8a

Initial deterministic citation-network adapter (authored by Codex in a separate
session): native parser, pinned checker execution, source read receipts and
eligibility, append-only SQLite ledger, canonical JSONL export, byte-exact replay.
