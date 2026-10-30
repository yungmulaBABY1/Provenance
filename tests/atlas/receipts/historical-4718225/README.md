# Historical receipts from PR #9 at 4718225

These are the six receipts that were current on the PR #9 branch at commit
4718225, before the locator-binding fix. They were moved here unchanged, byte
for byte (`git mv`):

- `case12-healthy/`, `case13-closed/`, `power-control/`, `power-sources/`, `shen-known-bad/`
- `power-sources-reviewed/`: run `urn:atlas:import:power-posing-sources:2`,
  holding the two F1-S2 reviews under the retired contract `atlas-evidence-review/1`

They were produced by adapter 0.2.0 on CPython 3.11.17, with record schema
`atlas-adapter/0.2`, parser version 3 and normalizer `nfc-whitespace/2`.

## Why `/1` was retired

Version 1 bound each reviewed passage by quotation hash only. Moving a passage's
start and end offsets while keeping its quotation turned the passage into
`MISMATCH` but left both reviews attached as `MATCH`, so a changed evidence
mapping inherited an old review. Version 2 binds a full passage descriptor:
source version, component, start, end, offset unit, interval and quotation hash.

## What works with adapter 0.3.0

| Receipt | `restore` | Replay (strict or content) |
|---|---|---|
| The five receipts without reviews | Accepted; native records re-derived and verified | Fails on `adapter_code` |
| `power-sources-reviewed/` (run `:2`) | **Rejected**: `UNSUPPORTED_REVIEW_SCHEMA: atlas-evidence-review/1`. A `/1` binding cannot show that a locator is unchanged, so it is refused rather than trusted | Fails |

The `/1` review artifacts themselves are preserved at
`tests/atlas/reviews/power-posing/v1/`. The current reviewed import is run `:3`,
which re-issues the same reviews under `/2`. CI's receipt replay step skips
`historical-*` directories.
