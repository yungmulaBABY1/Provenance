# Historical receipts from commit 072fa8a

These files are kept as historical artifacts. They are copied unchanged from
package A (`Atlas_P0_Review/receipts/`) and were not regenerated or edited.

- `power/`: import of `tests/atlas/power-control.json`
- `shen/`: import of `tests/atlas/shen-known-bad.json`
- `all.jsonl`: export of a ledger holding both runs

They were produced by the earlier adapter code at commit 072fa8a (adapter
0.1.0, record schema `atlas-adapter/0.1`, normalizer `nfkc-whitespace/1`) on
**CPython 3.12.14, Unicode 15.0.0**. The validation record that accompanied them
is `tests/atlas/validation.json` as of 072fa8a (`git show 072fa8a:tests/atlas/validation.json`).

## They cannot be replayed or restored by this version

This version cannot strict-replay them. It cannot content-replay or restore them
either:

- the record schema is now `atlas-adapter/0.2`, so every record is rejected
  with `UNSUPPORTED_RECORD`;
- their manifests record no parser identity, so native labels could not be
  re-derived even if the schema were accepted;
- they used NFKC matching, which this version removed, and the `clean_display`
  and `INSTRUMENT_VIOLATION` labels, which it replaced.

Running `python -m atlas replay ... --level content` or `python -m atlas restore`
on them exits 2 with `UNSUPPORTED_RECORD`. CI's receipt replay step skips this
directory. Current receipts are in the sibling fixture directories.

## Integrity

`power/SHA256SUMS` and `shen/SHA256SUMS` are package A's own files. Package A's
top-level `SHA256SUMS` also pinned these files:

```
c1e7bf6d2a61883cdd54a57a71a2b7df4950964602682601d998026358bcfe71  all.jsonl
27d38d5d772b3a3c5a84773b100d1dc94fb2b93c51a1b5238245de3224a6aba3  power/manifest.json
e3cc97fa9e02b9782ed28fc6c3689c49a91d93c75ca039fcf941323323ce7c41  power/records.jsonl
403d901174e682e68c8619cf9a2d395d3e00c13560860099b538dedac82c0df4  shen/manifest.json
8cc00c4cfe024dd8fd2c03c5252bacce71511995749e5adc17b3ac1a9646b726  shen/records.jsonl
```
