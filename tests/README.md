# tests/

Regression cases for the audit prompts.

Not for people running audits. For checking that a prompt change did not break
something that used to work.

---

## Why this exists

The prompts are long and heavily patched. A rule added to fix one failure can
silently disable another. That happened repeatedly during the build:

- A consistency check meant to catch inconsistent principles induced a **wrong
  downgrade** by misclassifying a symmetric phenomenon.
- Making claim-extraction's field 4 active — a genuine improvement — made it
  **actively wrong**, because a passive empty field cannot misattribute anything.
- An attribution rule written to prevent false inflation findings **exonerated
  the clearest instance of citation laundering** in the test case.

None were visible from reading the prompt. All surfaced from runs. That is what
these cases are for.

---

## Structure

```
tests/
├── README.md      this file
├── cases/         one file per regression case
└── RESULTS.md     per-run behavior log
```

**`cases/`** — synthetic material engineered so one mechanism is unambiguous,
paired with the expected result written *before* running.

**`RESULTS.md`** — what runs actually did. Which checks fired, what they changed,
what got killed downstream. Different question, different file.

---

## What a case needs

Three parts. All three are required.

**1. The material.** Synthetic, 200–400 words for a single-piece case. Plausible
enough that the prompt engages seriously, engineered so exactly **one** mechanism
is unambiguous. If two mechanisms are in play, a failure will not tell you which
check misfired.

**2. The expected result, written before running.** This is the whole point.
Written after, you will rationalize whatever came out. State the required outputs
and the fail conditions explicitly.

**3. What a failure means** — localized to a specific check. "Fail on the strip
test" should point at frame-carrier over-identification, not at "something is
wrong."

---

## The discipline

**Expected results are written first.** Non-negotiable. A case whose expected
result was written after the run is not a test, it is a description.

**Run on at least two models.** A single-model pass is weak evidence. A
single-model fail is strong.

**The pass condition is usually the derived rating, not zero findings.** A careful
reader will find small things in almost any material. Demanding zero observations
makes a case unpassable and therefore useless.

**Log every run in `RESULTS.md`**, including passes. A check that has never once
altered an outcome across twenty runs is length without function — but you only
learn that if passes are recorded too.

---

## Running a case

1. Open the case file. Read the expected result **before** running anything.
2. Paste the target prompt, then the case material.
3. Run. Compare against the expected result and the fail conditions.
4. Record in `RESULTS.md`: date, case, prompt version, model, pass/fail, and which
   checks fired.
5. On a fail — do not immediately patch. Check whether the case is wrong first. A
   sloppy case produces false failures, and a false failure sends you fixing a
   prompt that was fine.

---

## Case status

| # | Case | Branch | Built | Priority |
|---|---|---|---|---|
| 11 | Proportionate article, clean result | media, single-piece | ✅ | **highest** |
| 01 | Omission vs. de-emphasis | media, single-piece | | high |
| 03 | Amplification vs. independent corroboration | media, network | | high |
| 04 | Timing artifact vs. editorial selection | media, single-piece | | high |
| 02 | Synonym variance vs. causal-context loss | media, single-piece | | |
| 05 | Network convention vs. outlet-specific divergence | media, network | | |
| 06 | Appositional classification | media, single-piece | | |
| 07 | Denominator / baseline switching | media, network | | |
| 08 | Established vs. attributed cause | media, single-piece | | |
| 09 | Mirror symmetry | media, single-piece | | |
| 10 | Narrative-flag omission and over-activation | media, single-piece | | |

**Case 11 is the priority** and was built first. Every other case tests whether
the instrument *detects* something. Case 11 tests whether it can *decline to*.
If it fails, the others are testing a machine that cannot say no, and their passes
mean less than they appear to.

**Cases 3, 5, and 7 test the network branch** and need multiple articles plus a
primary source. Substantially more expensive to write.

**The research branch has no cases yet.** Nothing has been run through
construct-validity, internal-validity, or the counter-audit on material that
should come back sound. That is the same gap case 11 closes for media, and it is
open.

---

## Writing new cases

Do not write all of them in one sitting. A good synthetic article is real work,
and eleven produced at once will mostly be sloppy. Sloppy cases are worse than no
cases — a false failure costs more than a missing test.

Build the next case when a check has been changed and you want to know what else
moved.
