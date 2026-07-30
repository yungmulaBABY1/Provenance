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

## Three kinds of control

Most cases test whether the toolkit **catches** something. That is only one third
of what needs testing, and it is the third least likely to expose a template.

| Control | Tests | Built |
|---|---|---|
| **Clean positive** | a genuine defect is detected | implicitly, via live runs |
| **Proportionate negative** | a defensible source is cleared | case 11 (media only) |
| **Mixed** | some claims fail, others survive, in the same source | MIX-01 |

**The mixed case is the hardest and the most diagnostic.** It tests whether the
system separates claims rather than assigning a global good-paper / bad-paper
verdict.

It is also newly testable. Before the claim inventory, only one claim entered the
pipeline, so a mixed result was structurally impossible. Now a source where claim
A holds and claim B does not **should produce different verdicts per claim**. If it
produces one global verdict, the inventory is not doing its job — which makes this
a direct test of the multi-claim work, not a general test of nuance.

**The proportionate negative addresses the standing objection** to any adversarial
pipeline: that it will always return an indictment. It tests, in one run, whether
NEITHER APPARENT is real rather than ceremonial; whether prosecutors can return
nothing consequential; whether the concede test caps ordinary limitations; whether
the citation audit manufactures laundering from normal paraphrase; whether the
counter-audit invents opposition; and whether voice restoration sharpens a
non-finding into an accusation.

**Research branch now has a mixed case (MIX-01) but still no proportionate
negative.** A source that is simply sound, with nothing to find, has never been
run through construct-validity, internal-validity, or the counter-audit.

---

## Linkage

**Cases point up to failures. Failures do not list their cases.**

A case header names the failure IDs it closes. FAILURES.md stays stable. The
alternative — bidirectional links — means every new case requires editing the
registry too, which is the bureaucracy this structure exists to avoid.

Minimum case header:

```
Closes:      FAIL-CE-006, FAIL-CE-007
Target:      prompts/1-claim-extraction.txt, Field 4
Control:     clean positive / proportionate negative / mixed
```

---

## What belongs in FAILURES.md

Not everything. The threshold:

**Record a failure when it teaches something general, changes how a stage
operates, or explains why a seemingly redundant rule exists.**

Formatting repairs, wording tweaks, and one-off mistakes do not need permanent
entries. An exhaustive record would grow larger than the toolkit and bury the
changes that matter.

The test is the deletion question: *would someone auditing this prompt for bloat
cut this rule without knowing why it is there?* If yes, it needs an entry.

---

## Case status

Cases are derived from **FAILURES.md**. Every FAIL entry should eventually have
one; a FAIL with no case is protected by narrative alone, which means it can be
neither safely deleted nor safely kept.

Case numbering follows the failure ID.

| Case | Closes | Branch | Built | Priority |
|---|---|---|---|---|
| **CE-006 / CE-007** | joint-citation pair | claim extraction | | **build first — as a pair** |
| **CE-010** | unquoted item labeled RETRIEVED | claim extraction | | **highest single** |
| CA-002 | source self-defense (E0) | counter-audit | | high |
| MB-004 | strip test on mixed constructions | media, single-piece | | high |
| MB-003 | lever counting vs. finding-splitting | media, single-piece | | high |
| 11 (GUARD-002) | proportionate article, clean result | media, single-piece | ✅ | built |
| **MIX-01** | claim separation — C1 clears, C2 narrows, C3 fails | research, full chain | ✅ | **built — tests the claim inventory** |
| CE-002 | vague vs. quantified claim selection | claim extraction | | |
| CE-008 | RECALLED anchoring a failure location | claim extraction | | |
| MB-002 | Type A vs. Type B consistency | media, single-piece | | |
| MB-006 | D2 evidence floor | media, network | | |
| MB-007 | network-wide convention vs. outlier | media, network | | |

**Not testable:** GUARD-004 ("nothing downstream corrects it") — unmeasurable by
design. That is why it is FAILURES.md's flagged deletion candidate.

### Why CE-006 and CE-007 are built as a pair

Same structure, opposite correct answer. A citing document jointly cites two
sources for a claim only one supports.

- **CE-006** — the document **disambiguates their scopes elsewhere**.
  Pass: synthesis attribution, not misattribution.
- **CE-007** — the document **never disambiguates**.
  Pass: MISATTRIBUTED.

Built separately, either can be passed by pattern-matching on "joint citation."
Built together, only a run performing the document-level check gets both right.
This is the strongest test design available in this suite — use it wherever a rule
has a correct answer in both directions.

### Why CE-010 is the highest single priority

It is the only failure where **one fix routed around another**. The anchoring rule
(CE-008) bars RECALLED material from anchoring a failure location — but it keys
off a self-assigned label, so labeling an unquoted generalization RETRIEVED
defeats it. Most recent failure, applied, never tested.

### Note on case 11

Case 11 closes GUARD-002, not a FAIL — it tests whether the instrument can decline
to find, which was anticipated rather than observed. It remains the priority for
the media branch for that reason: every other case tests detection. **The research
branch has no acquittal case at all.**

## Writing new cases

Do not write all of them in one sitting. A good synthetic article is real work,
and eleven produced at once will mostly be sloppy. Sloppy cases are worse than no
cases — a false failure costs more than a missing test.

Build the next case when a check has been changed and you want to know what else
moved.
