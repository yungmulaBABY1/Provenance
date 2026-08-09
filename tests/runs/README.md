# tests/runs

Model outputs, kept as evidence. Nothing here is a prompt and nothing here
executes. These are the artifacts the run log in `tests/RESULTS.md` refers to.

## The two Ceuta folders are not the same thing

They sit next to each other and their names are one letter apart. Read this
before treating a file from either as evidence for the other.

**`cueta/`  -  SYNTHETIC FIXTURES.** Closed-packet coverage fixtures written to
have known structure, run to test whether the coverage-network prompt returns the
answer the fixture was built to have. Every file declares itself a fixture in its
own header. A finding here is a statement about the INSTRUMENT.

**`ceuta-live/`  -  LIVE RUNS.** Coverage-network audits of real reporting on the
July 2026 Ceuta crossing. Three models, two passes each. No fixture markers
anywhere in them, because nothing about them is engineered. A finding here is a
statement about the COVERAGE.

Keeping them apart matters more than the folder names suggest. A synthetic
fixture has a known correct answer and can therefore falsify the prompt; a live
run has no oracle and cannot. Reading a live-run finding as if it validated the
instrument, or a fixture result as if it said something about real coverage, is
the same category error in both directions.

The `cueta` spelling in the fixture folder is a misspelling of Ceuta, retained
for now because every path and filename inside it carries it. Fixing it is a
rename of the folder and its three files; nothing depends on the spelling.

## Naming

Live-run filenames follow `<model>-<target>[-N].txt`, where `N` distinguishes
repeat passes by the same model. The pass number is not a version  -  both passes
are evidence, and a later pass does not supersede an earlier one. Where two
passes disagree, that disagreement is itself the finding, and `tests/RESULTS.md`
is where it gets recorded.

## What does not belong here

Test-case specifications and their expected results live in `tests/cases/`, with
per-case run outputs under `tests/cases/runs/<date>-<case>-<model>/`. A run
output that belongs to a numbered case goes there, beside the case it exercises,
not in this directory.
