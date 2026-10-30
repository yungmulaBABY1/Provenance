# Review of one evidence relationship: Finding 1, S2 clause

The first substantively reviewed evidence relationship in Provenance Atlas. It
points; you judge. Nothing here is human adjudication, and neither review is
independent.

## The bounded proposition

- **Finding:** Finding 1 of the archived pilot output `compliance/run-output.md`
  (SHA-256 `761895d4…`), field `Evidence`, characters [0, 80):

  > S2 reports self-reported-power replication but no hormonal or behavioral effects

  This is a verbatim clause. The finding and its mapping are unchanged.
- **Mapping:** check `S2-reported-outcomes` (`tests/atlas/power-sources.json`), passages
  `S2-E2` and `S2-E3`.
- **Source version:** `doi:10.1177/0956797614553946/version/pdf-sha256-4ae91126e56da197`.
  The PDF has SHA-256 `4ae91126…1369`; the excerpt file has SHA-256 `f38381ce…b6`.
- **Decomposition:** for review, the clause was split into three parts:
  - (a) self-reported power replicated;
  - (b) no hormonal effect;
  - (c) no behavioral effect.

  This is an explicit reviewer decomposition. It does not replace the clause.

Each review binds to all of these identities. Each passage is bound by its full
descriptor: source version, component, start and end offsets, offset unit,
interval and quotation hash. If any of them changes, the adapter marks the
review `TARGET_MISMATCH` and the run stops referencing it.

The reviews are imported as run `urn:atlas:import:power-posing-sources:3`
(`tests/atlas/power-sources-reviewed.json`).

**Re-issue.** These artifacts were first written under `atlas-evidence-review/1`,
which bound passages by quotation hash only, so a moved locator kept the review
attached. They were re-issued under `/2` with only the binding changed; each
artifact's `reissue` block names its `/1` predecessor by hash. The `/1` files are
preserved in [v1/](v1/). Neither review was repeated.

## Not reviewed

- The S4 clause of the same Evidence field.
- Every other field of Finding 1 (Concede test, Severity, Verification state,
  Status, and so on).
- Finding 2.
- Whether Finding 1 as a whole is correct.

Finding 1's `assessment` stays `UNREVIEWED`, its native labels stay as written,
and every evidence relationship stays `UNADJUDICATED`.

## Dispositions (`atlas-evidence-review/2`)

| Review | Reviewer context | Whole | (a) self-report | (b) hormones | (c) behavior |
|---|---|---|---|---|---|
| [A](F1-S2-review-A.json) | Primary implementation session | **SUPPORTS_WITH_QUALIFICATION** | SUPPORTS | SUPPORTS_WITH_QUALIFICATION | SUPPORTS_WITH_QUALIFICATION |
| [B](F1-S2-review-B.json) | Separate subagent context | **SUPPORTS** | SUPPORTS | SUPPORTS | SUPPORTS |

**Disagreement (kept, not resolved).** Both reviews find that S2 reports what
the clause says, in S2's own words, and that nothing in the article contradicts
it. They differ on whether the clause's precision losses warrant a qualified
disposition:

- "no effects" for what S2 reports as non-significant two-tailed differences;
- two hormones only;
- statistics for only one of three behavioral tasks;
- the conceptual-replication framing, and the authors' caveat that protocol
  differences may explain the nulls.

B notes that a stricter reading would give SUPPORTS_WITH_QUALIFICATION. A
applies that reading.

## Key locators (S2 PDF, pinned extraction)

All 24 of A's and 19 of B's locators are exact spans of the
`pdftotext -enc UTF-8` output (SHA-256 `afc448e6…`), with offsets and hashes in
the artifacts. `source_packet.py verify` re-checks every one against a fresh
download.

| ID | Page | Section | Role |
|---|---|---|---|
| L01 | 653 | Title | "No Effect on Hormones and Risk Tolerance" |
| L04, L05 | 653 | Opening text | Significant self-reported power; "no significant effect … on hormonal levels or in any of the three behavioral tasks" |
| L02, L08 | 653–654 | Opening text, Method | Conceptual replication; protocol differences (3-min poses, and others) |
| L06 | 653 | Method | Sample extended from 100 to 200 after looking at the first 100 |
| L09 | 654 | Results | Self-report t(193) = 2.399, p = .017, d = 0.344 |
| L10, L11, L12 | 654 | Results | Gain-domain risk p = .215; testosterone change p = .162; cortisol p = .272 (all two-tailed) |
| L13, L14 | 654 | Results | Subgroup/nonparametric analyses "similar" (supplement); other two behavioral tasks: one sentence, no statistics |
| L15, L16 | 654 | Discussion | "failed to confirm"; "did not yield behavioral effects" |
| L17, L18 | 654–655 | Discussion | Protocol differences may have omitted crucial factors; "more research is needed" |

## Examination boundary and unavailable material

- **Read:**
  - Review A read the whole article (journal pp. 653–656), not the excerpts alone.
  - Review B viewed all four pages as images and read the layout extraction in full.
- **Unavailable to both:**
  - S2's Supplemental Material: `journals.sagepub.com` returned HTTP 403, and
    `pss.sagepub.com` is outside this environment's network policy.
  - S2's OSF data and materials: `osf.io` is outside this environment's network
    policy.

  These hold the analyses behind L13, L14 and L23. No reanalysis was attempted.
- **Not examined:** S1 (Carney et al., 2010); any later correction.

## Reviewer provenance and exposure

| | Review A | Review B |
|---|---|---|
| Identity | Claude (Anthropic), primary implementation session | Claude (Anthropic), separate subagent context launched by the primary session |
| Model identifier | Not written into the repository (session policy); see the session link in the artifact | Same |
| Inputs | Re-retrieved PDF and extractions (hashes in artifact), the import, the mapping, `SOURCES.json` | Only [the prompt](F1-S2-review-B.prompt.txt), the PDF and its layout text; [final report, verbatim](F1-S2-review-B.response.txt) |
| Exposure | Full: read the archived output and its native labels, authored the excerpt selection and mapping, received B's report before writing A | The proposition text only (a clause of Finding 1); not given native labels, other fields, excerpts, mapping or A's views |
| Isolation | None | By instruction only; the subagent had tool access on the same machine and reported opening only its two inputs (self-report) |
| Independence | Not established | Not established: same model family; a fresh context is not an independent reviewer |

**Independent review remains pending.** A reviewer outside this session and
model family, ideally one with access to the Supplemental Material and the OSF
data, has not reviewed this proposition. No human adjudication has been
performed.
