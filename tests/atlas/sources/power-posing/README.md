# Power-posing source packet (bounded excerpts)

Real-source evidence for the four-source power-posing pilot in
[compliance/PACKET.md](../../../../compliance/PACKET.md), mapped to the findings of
the archived pilot output [compliance/run-output.md](../../../../compliance/run-output.md).
The original packet and archived outputs are unchanged.

It points; you judge. Nothing here is a scientific assessment.

## What is in this directory

| File | Content |
|---|---|
| `SOURCES.json` | Per source: DOI, citation, requested and final URL, retrieval time, HTTP status, PDF SHA-256, byte count and pages, version, sections accessible, extraction tool and output hash, and each excerpt with PDF page, offsets in the extraction output and SHA-256 |
| `S2-excerpts.txt`, `S4-excerpts.txt` | Bounded excerpts only (three and four short passages), each an exact substring of the extraction output. These are the files the adapter reads |
| `source_packet.py` | Provenance tooling: `verify` re-downloads, re-hashes, re-extracts and checks that the whole extraction output is unchanged and every excerpt is at its recorded offsets (any difference exits nonzero); `build` records a new retrieval. Needs network and poppler; not part of the adapter and not run in CI |
| `ORIGINALS.json` | SHA-256 of every file under `compliance/` and `tests/cases/` at d700031 (the original packet and archived outputs), taken from git objects; the tests require them unchanged without needing git history |

The import context is [tests/atlas/power-sources.json](../../power-sources.json), its
tests are [tests/atlas/test_power_sources.py](../../test_power_sources.py), and the
committed receipt is [tests/atlas/receipts/power-sources/](../../receipts/power-sources/).

## Source coverage (retrieved 2026-10-30)

| Packet ID | Paper | Copy retrieved | Version | Accessible | Excerpts |
|---|---|---|---|---|---|
| S1 | Carney, Cuddy & Yap (2010) | none: packet link (journals.sagepub.com) returned HTTP 403 | not retrieved | nothing | none |
| S2 | Ranehill et al. (2015) | faculty.haas.berkeley.edu PDF, SHA-256 `4ae91126…1369`, 4 pages | publisher-typeset article, author-hosted | full article: introduction, Method, Results, Discussion, back matter, references. Supplemental Material not retrieved | E1 venue/DOI header; E2 opening results summary; E3 Discussion results |
| S3 | Carney, Cuddy & Yap (2015) | none: packet link (researchgate.net) returned HTTP 403 | not retrieved | nothing | none |
| S4 | Simmons & Simonsohn (2017) | faculty.haas.berkeley.edu PDF, SHA-256 `c30b8c46…1a7f`, 16 pages | accepted manuscript ("Forthcoming in Psychological Science"), not the version of record | full manuscript: introduction through Conclusion, figures, references. OSF disclosure table and code not retrieved | E1 title/status; E2 S4's description of S3; E3 question and conclusion; E4 evidential-value test |

S1 and S3 were requested once with a plain HTTP client. No browser emulation
or bot-check workaround was attempted. OpenAlex lists no open-access copy of
either. Their unavailability is kept as a limitation, not filled in.

Extraction: `pdftotext -enc UTF-8` (poppler 24.02.0), default reading-order
mode. Its quirks are kept as extracted. Examples: a soft hyphen in S2's page
range; "selfreported" and "pcurve" where a word was hyphenated across lines;
line breaks inside sentences.

## Mapping to the archived findings

Mappings follow each finding's own Evidence field, recorded per check as
`mapping_basis`. Nothing is inferred from other prose.

- **Finding 1** ("S2 reports self-reported-power replication but no hormonal or
  behavioral effects; S4 reports no evidential value …"):
  - `S2-reported-outcomes` (S2-E2, S2-E3);
  - `S4-evidential-value` (S4-E3, S4-E4).
- **Finding 2** ("Independent S2 and S4 challenges appear in Psychological
  Science; S3 substantively engages S2 and calls for direct replications"):
  - `S2-S4-venue` (S2-E1, S4-E1, metadata);
  - `S3-engages-S2` (requires S3's own text, which is unavailable);
  - `S4-describes-S3` (S4-E2: S4's words about S3, which do not stand in for S3).
- **Declared but unmapped:**
  - `S1-founding-results` (S1 unavailable);
  - `S2-methods` (the Method section exists in the retrieved PDF but was not
    retained as an excerpt).

## Three separate facts

| Fact | Where it lives | Value in this packet |
|---|---|---|
| What the historical audit asserted | `AuditFinding.native` | Kept as written, e.g. Verification state `FULL-TEXT-CONFIRMED; CONTESTED`. Findings are `QUARANTINED` because the archived pilot output predates the current grammar |
| What the adapter can read and match now | `SourceReadReceipt`, `Passage`, `source_checks`, `AuditFinding.source_eligibility` | 7/7 excerpts exact `MATCH`; S2 and S4 `PARTIAL_READ`; S1 and S3 `RETRIEVAL_FAILED`. Finding 1 `ELIGIBLE_FOR_DECLARED_CHECKS` with limitations; Finding 2 `NOT_ASSESSABLE` (S3 missing) |
| Whether a passage substantively supports the finding | `AuditFinding.assessment`, `Relationship.epistemic_status` | `UNREVIEWED` / `UNADJUDICATED`. Not decided by the adapter or by this packet |

A matching quotation shows the text is present in the retrieved copy at the
stated place. It does not show that the passage supports the finding, that the
finding is scientifically correct, or that the historical run read it.
`FULL-TEXT-CONFIRMED` remains the historical run's assertion.

## Limits

- The adapter verifies the excerpt files' bytes. The link from excerpt to PDF
  is a separate, re-runnable check (`source_packet.py verify`). It depends on
  the hosting pages keeping the same bytes, and on poppler producing the same
  extraction.
- Every content check is at most `ELIGIBLE_WITH_LIMITATIONS`. Each excerpt file
  carries a warning naming the PDF-extraction step.
- S4 is an accepted manuscript; quotations may differ from the published
  article. S2 is a publisher PDF obtained from an author's page, not from the
  publisher.
- Excerpts were chosen after reading the findings, so selection is not blind.
  No passage contradicting a finding was sought.
- Rights: only short bounded excerpts and links are kept; no full text is
  committed. Records are marked `NOT_REVIEWED_FOR_PUBLIC_RELEASE`.
