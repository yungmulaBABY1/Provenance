# Test Cases

## Failure\-response rule

A failing run does not automatically prove the prompt is wrong\.

Before patching a prompt:

1. inspect the case packet for unintended structural features;
2. verify the expected\-result oracle against the packet;
3. check whether the run identified a genuine feature the designer failed to
   anticipate;
4. distinguish prompt failure, model failure, checker failure, and fixture failure\.

If the case or oracle is wrong, repair the fixture rather than training the prompt
to ignore valid evidence\.

## Paired citation\-network correctness fixture

Cases 12 and 13 are paired substantive tests\.

They hold surface cartel indicators broadly constant while reversing the
evidentiary path structure\. They must be scored together; a default\-acquit or
default\-convict system fails the pair\.

## Galor–Özak cross-prosecutor-leak fixture

`case_FAIL-IV-001-002_galor-ozak-cross-prosecutor-leak.txt` contains the locked,
relative oracle for FAIL-IV-001/002. Its prompt repair is applied, but the case is
not yet executable: the preserved clean and contaminated outputs still need to be
copied in with exact filenames, hashes, byte counts, and run dates. Do not replace
those missing identities with reconstructed text or plausible placeholder data.

## Citation-network checker regression fixtures

`citation-network-checker/` contains four controls used by
`tests/test-citation-network-checker.py`:

- `shen-revised-known-bad.txt`: the unchanged dirty Shen revised output;
- `shen-v1-whitelist-clean.txt`: a canonical-vocabulary clean control;
- `complete-clean-control.md`: full deterministic PASS control; and
- `locked-source-review-control.md`: deterministic PASS-WITH-REVIEW control.

The harness is self-contained and must not reference scratch-workspace paths.
It tests structure and content form only; source-lock truth, adjudicative source
classification, and nesting ownership remain targeted human-review questions.

## Media coverage\-network regression fixtures

The Ceuta media cases use the same exact eight\-piece synthetic packet, embedded
verbatim in each case so the test material cannot drift through an external
reference\.

### [`ceuta-prominence-regression`](case_FAIL-MB-017_ceuta-prominence-regression.md)[ — FAIL\-MB\-017](case_FAIL-MB-017_ceuta-prominence-regression.md)

Protects a historical capability that later prompt versions silently lost:
within\-piece headline/lede/body prominence must remain analytically distinct from
cross\-piece omission/availability\.

Standalone mode\. No prior single\-piece audit is supplied\.

The case requires the gross\-scale vs return/aftermath prominence object to
survive as `prominence-packaging`, with packet\-inverse symmetry, packaging
provenance, and cross\-piece availability marked NOT APPLICABLE\.

### [`ceuta-semantic-equivalence`](case_FAIL-MB-018_ceuta-semantic-equivalence.md)[ — FAIL\-MB\-018](case_FAIL-MB-018_ceuta-semantic-equivalence.md)

Protects the entry condition for wording\-derived analysis\.

The oracle is PROCEDURAL rather than answer\-coded: wording may become framing
evidence only after same\-stage/referent comparison, added\-predicate
decomposition, non\-circular earnedness, and a named moved assignment\.

The historical Ceuta event\-language finding is expected to disappear, but that
specific answer is not a hard invariant if a future run independently supports a
material semantic outlier\.

### Pair interaction

Run these cases together after changes touching language, prominence, selection,
D\-ROLE ownership, or source inheritance\.

A passing pair must satisfy both:

1. semantic/register wording already resolved by the semantic gate does not
   re\-enter Section H through prominence; and
2. genuine prominence based on placement of distinct substantive
   facts/dimensions survives semantic normalization\.

These are regression fixtures for known failure objects\. They do not establish
general media\-branch correctness\.

A separate `ceuta-prominence-d2-ownership` case remains to be built with a
supplied prior single\-piece packaging finding\.
