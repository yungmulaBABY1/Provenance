# FAILURES

Numbered registry of the failures each prompt rule exists to close.

**Primary function: deletion protection.** These prompts are long and will
eventually be audited for bloat — by a person or by a model doing a context pass.
Without a traceable reason, a rule that looks fussy gets cut, and the failure it
prevented returns silently. Every rule should carry a marker; every marker should
resolve here.

**Two prefixes, and the difference matters:**

- **FAIL-** — closes a failure OBSERVED IN A RUN. Strong claim to survive an audit.
  Deleting one is a bet that a documented failure will not recur.
- **GUARD-** — anticipates a plausible failure, added by reasoning. Weaker claim.
  A GUARD that has never fired across many runs is a legitimate deletion candidate.

**Marker format in prompts** — one line, no narrative:

```
   [FAIL-CE-004]
```

Full record lives here. Do not restate it in the prompt.

**Deletion standard.** Before cutting any rule, answer:

1. Which FAIL/GUARD does it close?
2. Was that failure OBSERVED, or anticipated?
3. Where does the protection move if this is removed?
4. Which regression case proves it still holds?

An observed failure with no regression case and no replacement is not deletable.

---

## STATUS SUMMARY

| Prefix | Total | Regression case exists | Never re-observed since fix |
|---|---|---|---|
| FAIL- | 12 | 1 | 12 |
| GUARD- | 4 | 0 | n/a |

**Only one regression case exists** (case 11). Every other entry is protected by
the changelog narrative alone. That is the main weakness of this registry right
now — see tests/README.md.

---

## CE — Claim Extraction (`1-claim-extraction.txt`)

### FAIL-CE-001 — Three prosecutors audited three different claims
**Observed:** design review, then confirmed across early runs where construct,
internal, and citation audits attacked the paper, the design, and the media
version respectively. The combined critique read as a demolition of "the paper"
when the strongest findings concerned a press release.
**Repair:** shared Claim Map; Field 6 names one claim; all prosecutors target it.
**Regression condition:** every prosecutor finding declares the Field 6 claim as
its target, or flags MAP GAP.
**Case:** none.

### FAIL-CE-002 — Field 6 selected the vague claim and lost the finding
**Observed:** cold map v1 selected the abstract's unquantified version and bundled
in a second claim. The downstream audit returned the same generic verdict as two
pre-revision runs. A map selecting the quantified version found a specific defect
in the source's own method that no other run located. **The difference was Field 6,
not the prosecutor.**
**Repair:** RULE 1 (one claim only) + RULE 2 (prefer the most precisely quantified
version).
**Regression condition:** where a source states a claim at multiple precisions,
Field 6 targets the quantified one; no parenthetical second claim.
**Case:** none.

### FAIL-CE-003 — Recalled downstream material entered through a parenthetical
**Observed:** a run declared "no downstream uses supplied, PROVISIONAL," then
appended an unretrieved parenthetical noting the paper was "later widely restated
in secondary literature," offered "for completeness of the map only."
**Repair:** four provenance states (SUPPLIED / RETRIEVED / RECALLED / NONE FOUND);
RECALLED gets its own labeled line, never an aside.
**Regression condition:** no downstream item appears outside a labeled provenance
state.
**Case:** none.

### FAIL-CE-004 — Passive Field 4 could not detect inflation at all
**Observed:** Field 4 waited for user-supplied downstream material. A user pasting
a paper has none, so inflation analysis never ran.
**Repair:** Field 4 made ACTIVE — search for downstream restatements.
**Note:** this fix CREATED FAIL-CE-005. A passive empty field cannot be wrong.
**Regression condition:** Field 4 reports searches run, not "none supplied."
**Case:** none.

### FAIL-CE-005 — Active Field 4 built a misattributed inflation chain
**Observed:** the first active run recorded an assessment report's
"warmest decade of the millennium" as downstream inflation of a paper that
terminates six centuries back and calls millennial reconstruction future work.
That claim rests on a successor paper. The error would have propagated into Field
5 and every prosecutor. A counter-audit caught it three stages later.
**Repair:** ATTRIBUTION CHECK — could the audited source alone support this?
Scope arithmetic. ATTRIBUTED ELSEWHERE. Same-author successors are different
sources.
**Regression condition:** any restatement exceeding the source's measured scope is
traced to its actual support before being recorded as inflation.
**Case:** none.

### FAIL-CE-006 — The attribution check exonerated the clearest laundering
**Observed:** two runs reached opposite conclusions on the same restatement. One
reasoned that the claim rests on a successor and recorded ATTRIBUTED ELSEWHERE —
no inflation. The other retrieved the citing sentence and found the claim asserted
with the AUDITED paper cited for it. **The rule as written cleared the exact
behavior the stage exists to detect**, because it stopped at "who supports it"
without asking "who is cited for it."
**Repair:** MISATTRIBUTED branch. Two questions, not one.
**Regression condition:** every downstream item resolves to ATTRIBUTED ELSEWHERE
or MISATTRIBUTED via the citing sentence, not via the claim.
**Case:** none.

### FAIL-CE-007 — MISATTRIBUTED fired on a document that disambiguates elsewhere
**Observed:** a run classified an assessment report's joint citation as
MISATTRIBUTED on the sentence alone. A later run retrieved the same report's
earlier chapter, found it explicitly distinguished the two papers' scopes, and
correctly reclassified as synthesis attribution. **Sentence-level rule, false
positive against a careful document.**
**Repair:** joint citations require a DOCUMENT-LEVEL check before classification.
**Regression condition:** no joint citation is classified MISATTRIBUTED without a
stated search of the citing document for scope disambiguation.
**Case:** none.

### FAIL-CE-008 — RECALLED material anchored a failure location
**Observed:** a run correctly wrote that its downstream items were "labeled
RECALLED and do not anchor failure-location classification," then assigned
CITATION / PR-MEDIA as the "primary locus of inflation" on exactly that material.
**The rule was stated in Field 4 and violated in Field 5.**
**Repair:** ANCHORING RULE at Field 5 — only SUPPLIED/RETRIEVED may anchor;
otherwise SUSPECTED, not established.
**Regression condition:** Field 5 lists its anchoring items with provenance states
before assigning any location.
**Case:** none.

### FAIL-CE-009 — Models coined authoritative-sounding verification states
**Observed:** runs produced ESTABLISHED FROM SOURCE, RECONSTRUCTION FROM SOURCE,
and CROSS-SOURCE-CONFIRMED. Each reads as authoritative; none was defined; a
downstream stage cannot tell what was actually checked.
**Repair:** closed vocabulary + no-invented-states rule. CROSS-SOURCE-CONFIRMED
ADOPTED — attribution checking is a genuinely distinct verification act the ladder
had no state for. The others rejected as drift.
**Regression condition:** every verification state in output appears in the compact
vocabulary.
**Case:** none.
**Note:** one coined state was a real gap, two were drift. Worth distinguishing —
invented vocabulary sometimes signals a missing primitive.

### FAIL-CE-010 — An unquoted generalization was labeled RETRIEVED and anchored
**Observed:** a run recorded "frequent restatements of the form X, often citing Y"
as RETRIEVED — no quotation, no locator, no named source — then used it to anchor
a failure location. **The anchoring rule (FAIL-CE-008) keys off a self-assigned
label; mislabeling routes around it.**
**Repair:** VERIFY THE LABEL, DO NOT TRUST IT. Quotation AND locator required
before an item may anchor; otherwise RECALLED regardless of label. Pattern claims
are not retrieved items.
**Regression condition:** every anchoring item carries a verbatim quotation and a
locator.
**Case:** none. **This is the highest-priority regression case to build** — it is
the most recent failure and the only one where a fix routed around another fix.
**Status:** applied, UNTESTED.

---

## CA — Counter-Audit (`3-counter-audit.txt`)

### FAIL-CA-001 — A rebutted source was promoted to top threatening finding
**Observed:** a counter-audit elevated McShane & Wyner (2011) to its most
threatening finding without checking that the source was itself heavily rebutted
in the same journal issue. **The stage ran its defense pass on the paper and never
on its own witness.**
**Repair:** SOURCE-RECEPTION GATE. A source may not anchor a verdict until its own
reception is checked. Fires symmetrically on support and opposition.
**Regression condition:** every load-bearing source carries a reception state.
**Case:** none. **Verified firing** — later run recorded the same source CONTESTED
and capped.

### FAIL-CA-002 — Section E searched the literature and never the source
**Observed:** across SEVEN runs, no output engaged the paper's own pre-emptions —
a clause scoping the limitation the prosecutors quoted, and a reported sensitivity
test removing the proxy class they called dominant. Section E built the paper's
case entirely from external literature.
**Why it matters:** external support NARROWS a critique; internal pre-emption can
DEFEAT it. "They did not test it" and "their test was inadequate" are different
charges with different burdens.
**Repair:** Section E0 — search the source before the literature. Four targets,
four EFFECT values including DEFEATED.
**Regression condition:** E0 states which sections of the source were searched.
**Case:** none. **Verified firing** — found every pre-emption on first run,
produced 0 DEFEATED / 2 NARROWED / 4 RECHARACTERIZED / 0 UNAFFECTED, and moved the
impact category.

---

## MB — Media Branch

### FAIL-MB-001 — The flip test was theater
**Observed:** returned "would flag the mirror? Yes" on every finding across two
runs. Zero downgrades. Answering yes is free.
**Repair:** costly flip test — compose the mirror AS TEXT, audit your own mirror,
forced ranking, downgrade requirement.
**Regression condition:** a written mirror passage appears in output with findings
against it.
**Case:** none.

### FAIL-MB-002 — The consistency check induced a wrong downgrade
**Observed:** the check found that scene-first and justification-first orderings
both construct, and concluded the sequencing finding should be downgraded. **Wrong
— that ordering constructs in both directions makes the outlet's choice MORE
meaningful, not less.**
**Repair:** Type A (inconsistent principle — downgrade) vs. Type B (symmetric
phenomenon — NO downgrade) split.
**Regression condition:** no downgrade is issued for a Type B observation.
**Case:** none.

### FAIL-MB-003 — Coherence severity scaled with finding-splitting
**Observed:** one model split headline findings into two and reached 8
same-direction findings; two others reached 5 on the same article. The 8 drove a
heavier verdict. **Severity was a function of how finely findings were divided.**
**Repair:** count LEVERS, not findings. Nine named, capped at 9/9.
**Regression condition:** coherence ratio never exceeds the lever count.
**Case:** none.

### FAIL-MB-004 — The strip test removed fact-sources
**Observed:** two models split PARTLY SURVIVES vs. COLLAPSES on the same article,
entirely because one stripped a mixed paraphrase-plus-quoted-fragment construction
and the other kept it. **That single choice drove severity, aggregation, and the
final verdict.**
**Repair:** strip only FRAME-CARRIERS; keep FACT-SOURCES; explicit handling of
mixed constructions.
**Regression condition:** strip test output states what was removed and kept.
**Case:** none.

### FAIL-MB-005 — Discretionary downgrade never fired
**Observed:** five consecutive runs at zero downgrades. One run reproduced the
mandated sentence and then argued against it in a parenthetical. Another inverted
it ("is functioning" for "may not be functioning"). **A check that can be argued
away is not a check.**
**Repair:** AUTOMATIC downgrade — mechanical, no justification path. If the
downgrade seems wrong, fix the ranking.
**Regression condition:** every run reports which finding was downgraded.
**Case:** none. **Status:** applied, UNTESTED.

### FAIL-MB-006 — D2 returned CONFIRMED with no evidence
**Observed:** on the same cross-branch question, one run returned CONFIRMED having
retrieved no primary source; another returned FALSIFIED citing a specific outlet;
a third returned STILL UNRESOLVED. **Only the second and third were defensible.**
**Repair:** D2 EVIDENCE FLOOR. CONFIRMED / FALSIFIED / RECLASSIFIED / NETWORK-WIDE
each require named evidence. CONFIRMED flagged as the most dangerous value —
absence of contradiction is not confirmation.
**Regression condition:** every D2 resolution names its evidence.
**Case:** none.

### FAIL-MB-007 — Network-wide uniformity was treated as exoneration
**Observed:** a rule stated that shared behavior across outlets should downgrade
the single-piece finding. **Wrong — uniformity establishes the outlet is not an
OUTLIER; it does not establish the treatment is proportionate.** Every outlet can
inherit the same wire framing or blind spot.
**Repair:** RECLASSIFY, do not downgrade. Downgrade the distinctiveness claim,
keep the construction finding, record the convention separately and name its
source.
**Regression condition:** no substantive finding is downgraded solely for being
network-wide.
**Case:** none.

---

## GUARDS — anticipated, not observed

Weaker retention claim. A GUARD that has never fired across many runs is a
legitimate deletion candidate.

### GUARD-001 — No-assume-suppression
Low citation uptake has two explanations: the field marginalized valid work, or
the field correctly discounted rebutted work. Do not resolve toward suppression
without confirming the critique survived.
**Rationale:** anticipated; the toolkit's operator has priors about suppression.
**Fired:** not yet observed either way.

### GUARD-002 — Empty-table / acquittal clause
"A prosecutor that never returns 'nothing of consequence here' is not measuring
anything."
**Rationale:** anticipated — an instrument that cannot decline to find is a
template.
**Fired:** YES. One map returned GAP TYPE "neither apparent"; one counter-audit
returned no established downstream failure location.

### GUARD-003 — Symmetry requirements (flip test, direction-neutral rules)
Every construction check must fire identically regardless of political valence.
**Rationale:** anticipated — a one-directional instrument confirms its operator's
prior.
**Fired:** partially. The flip test caught nothing until made costly (FAIL-MB-001);
whether it catches anything now is untested.

### GUARD-004 — "Nothing downstream corrects it" (counter-audit stage note)
Architecturally imprecise — the human adjudicator IS downstream. Retained because
telling the model the human can reopen the verdict licenses laziness.
**Rationale:** anticipated.
**Fired:** unmeasurable by design. **Deletion candidate on the next audit** — it
is the clearest case of a rule kept on reasoning alone.

---

## HOW TO ADD AN ENTRY

When a run exposes a failure:

1. Assign the next number in the relevant prefix.
2. Record what was OBSERVED — the actual output, quoted where possible. Not a
   summary of the failure type.
3. Record the repair and the regression condition — what a passing run looks like.
4. Add the marker to the prompt.
5. Note whether a regression case exists. Most do not. That is the gap.

If the failure was anticipated rather than observed, use GUARD- and say so. The
distinction is the point: it determines what survives an architecture audit.
