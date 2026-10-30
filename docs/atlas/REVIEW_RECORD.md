# Atlas P0 review record

This file holds three things: the review record (revision 2) verbatim, a map
from each requirement to the commits and tests that implement it, and the
exposure of the implementation session.

## 1. Review record, revision 2 (verbatim)

Source file `Atlas_P0_Claude_Review_v2_2026-10-30.txt`, SHA-256
`443a8b5840651a068ec1e49ca3d50bd78bb0a0bddfdec9f130f0076667aa9e7b`.
The text between the fences below is byte-identical to that file. Sections 5
and 6 were the specification for this branch.

```text
PROVENANCE ATLAS — P0 ADAPTER REVIEW (CLAUDE) — REVISION 2
30 October 2026
Scope: Claude_Review_Handoff.txt + Atlas_Claude_Review_Package.zip
Status: review record and agreed implementation requirements. No changes
committed, pushed or opened as a PR by the reviewer.
Supersedes: Atlas_P0_Claude_Review_2026-10-30.txt (revision 1, retained).

REVISION 2 CHANGES
  * Section 2 (R1): the handoff's R1 reproducer changed Status to "contested",
    which was already "contested" in the fixture, so it altered nothing. R1 as
    reproduced shows only that a manifest-less record set restores. The decisive
    changed-label reproduction is F1 (Concede test).
  * Section 3 (F2) and section 7: the revision-1 probe script found archived
    outputs by filename and missed several. extra_probes.py now uses an explicit
    six-file inventory, which reproduces the reported pattern.
  * Section 6: replaced with the implementation requirements agreed with the
    second reviewer (ChatGPT), which reported reproducing F1 independently:
    restored label SURVIVES while the stored raw output says DEFEATS.

EXPOSURE DECLARATION
Reviewer read the handoff (including R1/R2 and the A-over-B recommendation)
before inspecting code. F1–F6 came from direct code reading and new probes
after that exposure; this review is not independent of the handoff's framing.

============================================================================
1. WHAT WAS VERIFIED
============================================================================
  * Package checksums: all SHA256SUMS entries OK (outer package and package A).
  * Fresh clone of github.com/yungmulaBABY1/Provenance: main HEAD is
    d7000315197670a59988b2d0b58bf0cdae545fc3 — the target base.
  * Package A bundle verified against the real clone; branch
    atlas/deterministic-audit-adapter = 072fa8a0fc7396d7eeea69bce96f731a5761002a.
    The .patch also applies cleanly to d700031.
  * atlas/baseline.json: all 10 pinned files match d700031 on SHA-256, git blob
    SHA-1 and byte count.
  * Workflow action pins are real: actions/checkout 11d5960a… = v4.4.0;
    actions/setup-python a26af69b… = v5.6.0.
  * Tests: 50/50 pass on CPython 3.11.18 (the CI version) and 3.13.18; the
    upstream checker regression passes. Package B: 26/26 pass after clean apply.
  * Receipt replay: NOT reproduced. Receipts were generated on CPython 3.12.14
    (Unicode 15.0.0), which was unavailable here. Under 3.12.3 the manifest
    differs ONLY in the environment field (see F4).

============================================================================
2. HANDOFF FINDINGS
============================================================================
R1  A manifest-less record set restores (16 records accepted). The reproducer's
    "altered Status" was a no-op (value already "contested"); see F1 for the
    changed-label case. R1 stands as a coverage gap.
R2  NFKC makes semantically different strings MATCH. Reproduced and wider than
    superscripts. Equal under NFKC, distinct under NFC:
      10² / 102   H₂O / H2O   ½ / 1⁄2   Ⅳ / IV   ℓ / l   µ / μ   ﬁt / fit
    Never equal under either: −0.5 (U+2212) vs -0.5; x⁻¹ vs x-1.
    NFC + whitespace normalization is still not an exact quotation match.

============================================================================
3. ADDITIONAL FINDINGS
============================================================================
F1  HIGH — Restore never re-derives native labels from the stored raw output.
    Probe P-a: change finding 1's Concede test DEFEATS -> SURVIVES in
    native.fields and native.labels, recompute records_before_manifest_sha256,
    restore: ACCEPTED, while the AuditRun raw_output_text in the same bundle
    still parses to DEFEATS. The manifest is an unkeyed, recomputable hash, so
    requiring one (R1) does not protect native labels.

F2  HIGH (provenance accuracy) — Historical outputs are charged with
    INSTRUMENT_VIOLATION under a contract they were never given. Probe P-e,
    explicit inventory: all 6 archived outputs are quarantined —
      compliance/run-output.md
      compliance/run-output-medium.md
      compliance/run-output-large.txt
      tests/cases/runs/2026-07-30-case-12-13-sol/12-output.md
      tests/cases/runs/2026-07-30-case-12-13-sol/13-output.md
      examples/research/shen/04_citation_network.txt
    Each shows 10–15 INSTRUMENT_VIOLATION issues, mostly "unscored dimension has
    numeric score" from the earlier 0–3 scorecard, plus missing SOURCE-LOCK
    fields that predate the source-lock block. Quarantine is correct; the
    violation label is a false statement about those runs.

F3  MEDIUM (workflow) — Appending one newline to the working-tree
    2-citation-network.txt makes every import fail (INPUT_HASH_MISMATCH). Tests
    build fixtures and CI runs on every push, so the next routine prompt patch
    fails CI.

F4  MEDIUM — Replay is byte-exact to the Python patch release. CI pins 3.11;
    receipts were built on 3.12.14; CI can never replay committed receipts.

F5  LOW — The Shen AuditRun's refs include review/earlier-shen-counter-audit,
    whose target_binding is TARGET_MISMATCH.

F6  LOW — A record covered by no manifest restores (probe P-b).

============================================================================
4. THINGS A GETS RIGHT (keep)
============================================================================
  * Checker executed from verified bytes in a temp directory with python -I.
  * Duplicate JSON keys and NaN/Infinity rejected at load.
  * SQLite append-only triggers, BEGIN IMMEDIATE, idempotent re-append,
    ID_CONTENT_CONFLICT, write-once outputs.
  * Source eligibility separate from native labels; paper_clean always false;
    metadata never satisfies a content check; non-plain extraction always
    EXTRACTION_UNVERIFIED (fail closed).
  * Byte hash labelled RUN_LOCAL_NOT_CANONICAL_IDENTITY.

============================================================================
5. CONTRACT DECISIONS (agreed)
============================================================================
1. Semicolon verification states / prefixed severity and location: store raw
   text, the projection, and the named projection rule. A PASS under one
   projection is not a PASS under a stricter grammar.
2. Evidence type: keep raw free text; publish observed values; unknown values
   stay visible; no guessed aliases.
3. Null results — B's rule: the historical null assertion and present-day
   source eligibility are separate facts. No derived clean state.
4. Historical contract failures: native values kept as written (including case
   13's SURVIVES/major pairing); labelled per requirement F2 below.

============================================================================
6. IMPLEMENTATION REQUIREMENTS (agreed with second reviewer)
============================================================================
Base: A (072fa8a). Do not ship B's runtime. Fix integrity issues together,
then port, regenerate, and open one draft PR.

R1 + F1 + F6 — INTEGRITY
  * Every AuditRun and every record belonging to it must be covered by a
    RunManifest; shared Work/SourceVersion records may be covered by more than
    one manifest. Uncovered records are rejected.
  * On restore/append, re-derive native findings, scorecard, source-lock values,
    null assertion and parse issues from raw_output_text using the parser
    version recorded in the manifest. A mismatch is rejected.
  * A recorded parser version this code does not support is not rejected and is
    not trusted: it is reported as explicitly unverified, never as verified.
  * Tests: missing manifest; uncovered record; Concede-test mutation with a
    recomputed manifest hash; unsupported parser version; valid multi-run
    export; transactional rollback.

F2 — CONTRACT-RELATIVE LABELS
  * Discrepancies against the current grammar are CURRENT_CONTRACT_MISMATCH.
  * Unknown or unverified producing instrument versions establish neither
    compliance nor violation (producing-instrument compliance: UNDETERMINED).
  * INSTRUMENT_VIOLATION only when the producing instrument is verified to be
    the contract the parser implements. Quarantine behavior is unchanged.

R2 — ANCHORS
  * Exact character match (no normalization) is distinct from normalized match
    (NFC + whitespace). Only an exact match is displayed as MATCH. A
    normalized-only match is a separate, visible state and is never presented
    as an exact quotation. NFKC is removed from matching. The normalizer is
    versioned; old receipts are kept as historical artifacts, not rewritten.

F3 — VALIDATION BASELINE
  * Resolve the immutable validation baseline independently of working-tree
    prompts, with hash checks retained. Working-tree drift is reported, not
    fatal.

F4 — REPLAY
  * Content replay compares inputs, code, parser, normalizer and substantive
    records, and reports environment differences explicitly.
  * Byte-exact strict replay is preserved.
  * Error messages name the differing component.

F5 — Only MATCH reviews appear in a run's refs; mismatched reviews are kept
     under a separate typed field.

AFTER THE REPAIRS
  * Port B's paired healthy/closed packet fixtures (cases 12 and 13), exact
    character spans for output locators, and B's contract documentation
    (prompt-contracts.md, native-contract-excerpts.md) into A as docs.
  * Regenerate manifests and receipts under the reviewed code and the CI
    interpreter; keep the 072fa8a receipts as historical artifacts.
  * Leave the existing webapp embed-parity failure as documented baseline debt.
  * Submit one implementation as a draft PR.

============================================================================
7. PROBES
============================================================================
extra_probes.py runs P-a through P-e against a checkout:
  python3 -I extra_probes.py /path/to/checkout
P-a alters Concede test (a real change). P-e uses the explicit six-file
inventory above. After the repairs, P-a and P-b must be rejected, P-c must
import with a drift warning, P-d pairs must not report MATCH, and P-e must
report CURRENT_CONTRACT_MISMATCH, never INSTRUMENT_VIOLATION.

It points; you judge.
```

## 2. Requirements to commits and tests

Commit hashes are on branch `atlas/p0-adapter`; base `072fa8a` (Codex) is the
first commit. Test files are under `tests/atlas/`. All tests pass on CPython
3.11.17 (95 tests).

| Requirement | Commit(s) | Tests |
|---|---|---|
| R1: manifest-less record set restores | `8565a18` | `test_integrity.py`: `test_missing_manifest_rejected`, `test_run_record_covered_twice_rejected`, `test_valid_multi_run_export_restores`, `test_failed_integrity_check_rolls_back_entire_append`; `test_adapter.py`: `test_conflict_rolls_back_entire_import` |
| F1: native labels not re-derived on restore | `8565a18`; output anchors added to re-derivation in `c83419b`; issue order made seed-independent in `1de873c` | `test_integrity.py`: `test_concede_mutation_with_recomputed_manifest_hash_rejected`, `test_run_level_projection_mutations_rejected`, `test_removed_finding_rejected`, `test_unsupported_parser_version_reported_unverified`; `test_output_spans.py`: `test_tampered_span_rejected_on_restore`; `test_determinism.py` (all) |
| F2: historical outputs charged with INSTRUMENT_VIOLATION | `c8f54ce` | `test_contract_labels.py` (all); `test_paired_fixtures.py`: `test_quarantined_as_current_contract_mismatch`, `test_native_labels_preserved`; `test_adapter.py`: three parser tests renamed to `CURRENT_CONTRACT_MISMATCH` |
| F3: working-tree prompt edit breaks every import | `f43df14` | `test_baseline.py` (all); `test_adapter.py`: `test_input_hash_and_executable_pin_fail_closed` |
| F4: replay byte-exact to the Python patch release | `253dc88`; receipts regenerated in `355a25a`; CI content replay in `af199c3` | `test_replay.py` (all); `test_determinism.py`: `test_import_in_one_process_restores_in_another`; CI step "Content replay of committed receipts" |
| F5: run refs a mismatched review | `d09a7aa` | `test_reviews.py` (all) |
| F6: record outside any manifest restores | `8565a18` | `test_integrity.py`: `test_uncovered_record_rejected` |
| R2: NFKC makes different strings MATCH | `f130417` | `test_anchors.py` (all); `test_adapter.py`: `test_normalizer_is_explicit_and_conservative` |
| Null rule (B's rule): two separate facts, no clean state | `80adac4` | `test_adapter.py`: `test_null_assertion_is_scoped_and_requires_evidence`, `test_absent_findings_cannot_be_null`, `test_metadata_mapping_cannot_enable_null_citation_result` |
| After repairs: port case 12/13 paired fixtures | `f1c4362` | `test_paired_fixtures.py` (all) |
| After repairs: exact character spans for output locators | `c83419b` | `test_output_spans.py` (all) |
| After repairs: B's contract documentation (docs only) | `bd8e68c` | none (byte-identical body checked with `cmp` against package B) |
| After repairs: regenerate receipts; keep 072fa8a receipts | `355a25a`, `007d735` | `tests/atlas/validation.json`; CI content replay |
| After repairs: embed-parity failure left as baseline debt | not changed | `tools/embed_prompts.py --check` still returns STALE (recorded in `validation.json`) |
| Documentation | `4d0038e` | n/a |

Found during implementation, not in the record: the parser emitted issues for
unknown scorecard dimension names in hash-seed order (inherited from 072fa8a),
so imports of outputs with renamed dimensions were not deterministic across
processes. The F1 re-derivation exposed it when the case 12/13 receipts failed
replay. Fixed in `1de873c` with the user's approval; parser version 3.

Probe results after the repairs (`extra_probes.py`, unmodified): P-a and P-b
rejected; P-c imports (the drift notice it records in the manifest is asserted
by `test_baseline.py`); P-d pairs never
equal (and `test_anchors.py` shows none reaches MATCH or NORMALIZED_MATCH_ONLY);
P-e reports CURRENT_CONTRACT_MISMATCH and no INSTRUMENT_VIOLATION.

## 3. Exposure

This implementation session saw the handoff, both packages and the review
record before writing code. In detail, before the first line of code:

- it read both review record revisions (revision 1 and revision 2, which embed
  the handoff's R1/R2 findings and its A-over-B recommendation), the procedure
  file, and `extra_probes.py`;
- it unpacked `Atlas_Claude_Review_Package.zip` (containing
  `Claude_Review_Handoff.txt`, `Review_Probes.py` and both packages), read and
  ran `Review_Probes.py`, and verified both packages' checksums;
- it read the 072fa8a code, tests and docs, including
  `docs/atlas/REVIEW_HANDOFF.txt`.

Package B's `fixtures.json`, `fixtures.py`, validation imports and contract
documents were read later, during the Stage 2 port.

The implementation is not independent of the review: it was written to the
review's requirements, by a session in the same model family (Claude) as the
reviewer. It is also not independent of 072fa8a, which it extends. No
scientific audit, counter-audit or human adjudication was performed.
