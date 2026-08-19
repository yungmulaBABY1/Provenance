# Test Cases

## Failure-response rule

A failing run does not automatically prove the prompt is wrong.

Before patching a prompt:

1. inspect the case packet for unintended structural features;
2. verify the expected-result oracle against the packet;
3. check whether the run identified a genuine feature the designer failed to
   anticipate;
4. distinguish prompt failure, model failure, checker failure, and fixture failure.

If the case or oracle is wrong, repair the fixture rather than training the prompt
to ignore valid evidence.

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

## Paired citation-network correctness fixture

Cases 12 and 13 are paired substantive tests.

They hold surface cartel indicators broadly constant while reversing the
evidentiary path structure. They must be scored together; a default-acquit or
default-convict system fails the pair.
