# Historical receipts from main at 7c55e2c

These are the five receipts that were current on `main` at commit 7c55e2c (after
PR #6). They were moved here unchanged, byte for byte (`git mv`), when adapter
0.2.0 added evidence-proposition reviews (`atlas-evidence-review/1`):

- `case12-healthy/`, `case13-closed/`, `power-control/`, `power-sources/`, `shen-known-bad/`

They were produced by adapter 0.1.0 on CPython 3.11.17, with record schema
`atlas-adapter/0.2`, parser version 3 and normalizer `nfc-whitespace/2`.

## What still works with this version

- `python -m atlas restore` accepts each of them. Every run's native records are
  re-derived and reported `native_projection_verified`.
- Their `SHA256SUMS` files still verify.

## What does not

- Content or strict replay fails with `REPLAY_MISMATCH (content): adapter_code`.
  Their manifests record the 0.1.0 code hashes, and replay recomputes with the
  current code.

The current receipts in the sibling directories were regenerated from the same
contexts under adapter 0.2.0. Each differs from its predecessor here only in
the RunManifest record; every other record is identical. CI's receipt replay
step skips `historical-*` directories.
