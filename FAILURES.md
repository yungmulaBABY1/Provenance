# FAILURES

Numbered registry of the failures each prompt rule exists to close.

**Primary function:** deletion protection. These prompts are long and will eventually be
audited for bloat  -  by a person or by a model doing a context pass. Without a traceable
reason, a rule that looks fussy gets cut, and the failure it prevented returns silently.
Every rule should carry a marker; every marker should resolve here.

Two prefixes, and the difference matters:

- FAIL-  -  closes a failure OBSERVED IN A RUN. Strong claim to survive an audit.
Deleting one is a bet that a documented failure will not recur.
- GUARD-  -  anticipates a plausible failure, added by reasoning. Weaker claim. A GUARD
that has never fired across many runs is a legitimate deletion candidate.

Marker format in prompts  -  one line, no narrative:

```
   [FAIL-CE-004]
```

Full record lives here. Do not restate it in the prompt.

Deletion standard. Before cutting any rule, answer:

1. Which FAIL/GUARD does it close?
2. Was that failure OBSERVED, or anticipated?
3. Where does the protection move if this is removed?
4. Which regression case proves it still holds?

An observed failure with no regression case and no replacement is not deletable.

---

## STATUS SUMMARY

Update when adding entries.

|Prefix|Total|Regression case exists|Never re-observed since fix|
|------|-----|----------------------|---------------------------|
|FAIL- |46   |6                     |31                         |
|TOOL- |5    |1 (TOOL-002 open)     |2                          |
|GUARD-|8    |1                     |n/a                        |

Six regression cases now exist: case 11 (media acquittal, built), CE-006/007 (joint
citation, built), MIX-01 (mixed control, built), the compliance fixture set
(FAIL-CN-001, run at three burden levels), FAIL-MB-017 (Ceuta prominence, built), and
FAIL-MB-018 (Ceuta semantic equivalence, built).

FAIL-MB-008’s dangerous inference path is DEFUSED but its whole-coverage Level-2
count remains convention/model dependent. FAIL-MB-009’s per-fact repair has now
been exercised successfully on the integrated Ceuta rerun. FAIL-MB-010’s original
failure remains historical evidence, but its former “verb frame must survive as
framing variance” disposition is superseded by FAIL-MB-018’s semantic-equivalence
and earnedness gate. FAIL-MB-017 and FAIL-MB-018 both PASS their Ceuta regression
expectations and PASS the joint interaction check. FAIL-CV-003 and FAIL-CV-004
still lack a fresh prompt rerun. FAIL-MB-016 remains proposed and untested.
FAIL-CV-005, FAIL-CE-011, FAIL-CN-002 and TOOL-005 are proposed or open with no
repair applied at all. These eight unresolved entries are excluded from the
“Never re-observed since fix” count.

NUMBERING NOTE: the previously reserved ids are now written. TOOL-004
(instrument preflight) and FAIL-CA-003 / FAIL-CA-004 were referenced by TODO.md,
the shen run metadata and `tests/cases/` before an entry existed for them; those
entries are now present, so every id referenced in this repository resolves here.

FAIL-CN-006 was drafted as FAIL-CN-002 in the batch that introduced it. CN-002 was
already held by the stale verdict-letter-mapping entry committed to main, so the
incoming entry was renumbered rather than allowed to overwrite it. Two different
failures under one id is the one thing this registry cannot survive.

Repository sync note: the PASS evidence and “repair applied” statuses refer to
the integrated RC2 coverage-network artifact used for the 2026-08-09 rerun. The
current repository copy of prompts/media-analysis/2-coverage-network.txt does
not yet contain the FAIL-MB-017 / FAIL-MB-018 blocks. Its supplied integration
diff targets a different RC2 consolidated base, so canonical prompt
synchronization remains an explicit TODO rather than a blind patch.

GUARD-001 and GUARD-002 have both fired on observed runs and should be treated as FAIL-class
for deletion purposes.

Remaining thin: entries 001-016 have no archived originating runs and are supported by
quoted excerpts alone. TOOL-002 is open. TOOL-003 was found by inspection rather than by a
run, and has no committed regression case.

---

## CE  -  Claim Extraction (1-claim-extraction.txt)

### FAIL-CE-001  -  Three prosecutors audited three different claims

**Observed:** design review, then confirmed across early runs where construct, internal, and
citation audits attacked the paper, the design, and the media version respectively. The
combined critique read as a demolition of “the paper” when the strongest findings concerned
a press release. Repair: shared Claim Map; Field 6 names one claim; all prosecutors
target it. Regression condition: every prosecutor finding declares the Field 6 claim as
its target, or flags MAP GAP. Case: none.

### FAIL-CE-002  -  Field 6 selected the vague claim and lost the finding

**Observed:** cold map v1 selected the abstract’s unquantified version and bundled in a
second claim. The downstream audit returned the same generic verdict as two pre-revision
runs. A map selecting the quantified version found a specific defect in the source’s own
method that no other run located. The difference was Field 6, not the prosecutor.
**Repair:** RULE 1 (one claim only) + RULE 2 (prefer the most precisely quantified version).
**Regression condition:** where a source states a claim at multiple precisions, Field 6
targets the quantified one; no parenthetical second claim. Case: none.

### FAIL-CE-003  -  Recalled downstream material entered through a parenthetical

**Observed:** a run declared “no downstream uses supplied, PROVISIONAL,” then appended an
unretrieved parenthetical noting the paper was “later widely restated in secondary
literature,” offered “for completeness of the map only.” Repair: four provenance states
(SUPPLIED / RETRIEVED / RECALLED / NONE FOUND); RECALLED gets its own labeled line, never an
aside. Regression condition: no downstream item appears outside a labeled provenance
state. Case: none.

### FAIL-CE-004  -  Passive Field 4 could not detect inflation at all

**Observed:** Field 4 waited for user-supplied downstream material. A user pasting a paper
has none, so inflation analysis never ran. Repair: Field 4 made ACTIVE  -  search for
downstream restatements. Note: this fix CREATED FAIL-CE-005. A passive empty field
cannot be wrong. Regression condition: Field 4 reports searches run, not “none
supplied.” Case: none.

### FAIL-CE-005  -  Active Field 4 built a misattributed inflation chain

**Observed:** the first active run recorded an assessment report’s “warmest decade of the
millennium” as downstream inflation of a paper that terminates six centuries back and calls
millennial reconstruction future work. That claim rests on a successor paper. The error
would have propagated into Field 5 and every prosecutor. A counter-audit caught it three
stages later. Repair: ATTRIBUTION CHECK  -  could the audited source alone support this?
Scope arithmetic. ATTRIBUTED ELSEWHERE. Same-author successors are different sources.
**Regression condition:** any restatement exceeding the source’s measured scope is traced to
its actual support before being recorded as inflation. Case: none.

### FAIL-CE-006  -  The attribution check exonerated the clearest laundering

**Observed:** two runs reached opposite conclusions on the same restatement. One reasoned
that the claim rests on a successor and recorded ATTRIBUTED ELSEWHERE  - no inflation. The
other retrieved the citing sentence and found the claim asserted with the AUDITED paper
cited for it. The rule as written cleared the exact behavior the stage exists to detect,
because it stopped at “who supports it” without asking “who is cited for it.” Repair:
MISATTRIBUTED branch. Two questions, not one. Regression condition: every downstream
item resolves to ATTRIBUTED ELSEWHERE or MISATTRIBUTED via the citing sentence, not via the
claim. Case: none.

### FAIL-CE-007  -  MISATTRIBUTED fired on a document that disambiguates elsewhere

**Observed:** a run classified an assessment report’s joint citation as MISATTRIBUTED on the
sentence alone. A later run retrieved the same report’s earlier chapter, found it explicitly
distinguished the two papers’ scopes, and correctly reclassified as synthesis attribution.
Sentence-level rule, false positive against a careful document. Repair: joint
citations require a DOCUMENT-LEVEL check before classification. Regression condition: no
joint citation is classified MISATTRIBUTED without a stated search of the citing document
for scope disambiguation. Case: none.

### FAIL-CE-008  -  RECALLED material anchored a failure location

**Observed:** a run correctly wrote that its downstream items were “labeled RECALLED and do
not anchor failure-location classification,” then assigned CITATION / PR-MEDIA as the
“primary locus of inflation” on exactly that material. The rule was stated in Field 4 and
violated in Field 5. Repair: ANCHORING RULE at Field 5  -  only SUPPLIED/RETRIEVED may
anchor; otherwise SUSPECTED, not established. Regression condition: Field 5 lists its
anchoring items with provenance states before assigning any location. Case: none.

### FAIL-CE-009  -  Models coined authoritative-sounding verification states

**Observed:** runs produced ESTABLISHED FROM SOURCE, RECONSTRUCTION FROM SOURCE, and
CROSS-SOURCE-CONFIRMED. Each reads as authoritative; none was defined; a downstream stage
cannot tell what was actually checked. Repair: closed vocabulary + no-invented-states
rule. CROSS-SOURCE-CONFIRMED ADOPTED  - attribution checking is a genuinely distinct
verification act the ladder had no state for. The others rejected as drift. Regression
condition: every verification state in output appears in the compact vocabulary. Case:
none. Note: one coined state was a real gap, two were drift. Worth distinguishing  -
invented vocabulary sometimes signals a missing primitive.

### FAIL-CE-010  -  An unquoted generalization was labeled RETRIEVED and anchored

**Observed:** a run recorded “frequent restatements of the form X, often citing Y” as
RETRIEVED  -  no quotation, no locator, no named source  -  then used it to anchor a failure
location. The anchoring rule (FAIL-CE-008) keys off a self-assigned label; mislabeling
routes around it. Repair: VERIFY THE LABEL, DO NOT TRUST IT. Quotation AND locator
required before an item may anchor; otherwise RECALLED regardless of label. Pattern claims
are not retrieved items. Regression condition: every anchoring item carries a verbatim
quotation and a locator. Case: none. This is the highest-priority regression case to
build  -  it is the most recent failure and the only one where a fix routed around another
fix. Status: applied, UNTESTED.

### FAIL-CE-011  -  No provenance state for "retrieved, read, verbatim withheld"
**Observed:** in the Claude run, three items were directly read in the source but could not be
reproduced verbatim by the executor. The provenance vocabulary (SUPPLIED / RETRIEVED /
RECALLED / NONE FOUND) has no state for this, and the anchoring rule requires a quotation plus
locator, so all three lost anchor eligibility  -  including the abstract's escalation sentence.
Nothing was lost on this run because two other items anchored the finding.

**Why this matters:** on a source where the inflationary sentence is the ONLY available anchor,
this rule suppresses a finding that was genuinely verified. The failure is silent: the audit
reports no finding rather than reporting a finding it could not anchor.

**Repair (proposed):** add a state for read-but-unquotable material (e.g. RETRIEVED-UNQUOTED)
that may anchor when the executor attests direct reading and supplies a locator, with the
finding marked for verification on re-read.

**Regression condition:** a finding whose only support is directly read but unquotable material
is reported with a verification flag, not silently dropped.

**Case:** Gabarrell-Pascuet et al. 2024
(`tests/runs/reducing-loneliness/claude-construct.md`, toolkit note T3).

**Status:** proposed.


---

## CA  -  Counter-Audit (3-counter-audit.txt)

### FAIL-CA-001  -  A rebutted source was promoted to top threatening finding

**Observed:** a counter-audit elevated McShane & Wyner (2011) to its most threatening
finding without checking that the source was itself heavily rebutted in the same journal
issue. The stage ran its defense pass on the paper and never on its own witness.
**Repair:** SOURCE-RECEPTION GATE. A source may not anchor a verdict until its own reception
is checked. Fires symmetrically on support and opposition. Regression condition: every
load-bearing source carries a reception state. Case: none. Verified firing  -  later
run recorded the same source CONTESTED and capped.

### FAIL-CA-002  -  Section E searched the literature and never the source

**Observed:** across SEVEN runs, no output engaged the paper’s own pre-emptions  - a clause
scoping the limitation the prosecutors quoted, and a reported sensitivity test removing the
proxy class they called dominant. Section E built the paper’s case entirely from external
literature. Why it matters: external support NARROWS a critique; internal pre-emption
can DEFEAT it. “They did not test it” and “their test was inadequate” are different charges
with different burdens. Repair: Section E0  -  search the source before the literature.
Four targets, four EFFECT values including DEFEATED. Regression condition: E0 states
which sections of the source were searched. Case: none. Verified firing  -  found
every pre-emption on first run, produced 0 DEFEATED / 2 NARROWED / 4 RECHARACTERIZED / 0
UNAFFECTED, and moved the impact category.

### FAIL-CA-003 — Counter-audit's declared inputs omitted internal validity and orphaned its findings

**Observed:** the Shen full-chain run (2026-08-10) produced internal-validity's
first load-bearing finding: Field 6 ("no significant gender-based performance
disparity") is directly contradicted by Shen's own reported statistics — EQ2
Table 3's play-time × male interaction on non-guilded character level
(`beta=-0.008`, `p<.001`) and CR3 Table 5's new-level × male interaction
(`beta=-8.289`, `p<.001`, with the paper reporting a crossover near level 15).
The finding never reached the counter-audit. The pinned `3-counter-audit.txt`
declared only the claim map, original paper, citation-network output, and
construct-validity output as stage inputs. The run followed that contract and
explicitly flagged the omission rather than silently injecting Stage 2B.

**Why it matters:** the same prompt's STAGE-ROLE NOTE names construct-validity,
internal-validity, and citation-network together as the prosecuting stages it
exists to balance. Its formal INPUTS section contradicted that role. The defect
remained latent until internal validity produced a finding capable of defeating
or narrowing Field 6. A human adjudicating from the counter-audit's final verdict
alone would not see that the audited claim is contradicted by the source's own
tables unless they separately reread Stage 2B.

**Repair:** internal-validity is now a named input to `3-counter-audit.txt`.
Every supplied prosecutor's findings must enter both E0's source-self-defense
check and G2's finding-level target gate. Section J must disclose whether internal
validity was supplied and consumed; silence is not a valid disposition. In the
same edit pass, the vestigial "thesis paragraph or short paper" target was moved
from the primary Purpose/Input contract to a separately gated optional fidelity
check that runs only after G2 and E0.

**Regression condition:** a full-chain run where internal validity produces a
Field-6-defeating or Field-6-narrowing finding must either carry that finding into
the counter-audit's own E0/G2 output or explicitly state in the final verdict that
internal validity was not consumed. With the Shen Stage 2B output supplied, G2
must contain the Field-6 contradiction row and Section J must say `SUPPLIED AND
CONSUMED`.

**Case:** `tests/cases/case_FAIL-CA-003_shen-internal-validity-handoff.md`, using
`examples/research/shen/03_internal_validity.txt` for the finding and
`examples/research/shen/05_counter_audit.txt` / `06_handoffs_and_final_assessment.txt`
for the confirmed omission.

**Status:** OBSERVED; REPAIR APPLIED; PASS ON 2026-08-11 LEAD-SUPERSET REGRESSION.

### FAIL-CA-004 — E0 credited a source's untested directional defense as though it weakened the finding

**Observed:** in the Shen counter-audit rerun with operator leads, E0 found that
Shen et al.'s Discussion anticipated CV-7 / corrected Lead 3: the total-play-time
denominator does not measure how sampled characters divided their time between
leveling and other activities. The source offered a directional defense without
measuring activity allocation: expected gender differences in advancement
motivation would supposedly bias against parity, making observed parity more
robust. E0 classified CV-7 as RECHARACTERIZED. But the same unmeasured mechanism
permits a live opposite-direction hypothesis: concentration on the visible
leveling metric could bias toward parity and mask a difference among genuine
maximizers. Neither direction was tested with activity-allocation data in the
source.

**Why it matters:** as specified, E0 could award RECHARACTERIZED credit whenever
a source acknowledged an unmeasured variable and asserted that it cut in the
source's favor. The source's engagement may legitimately change a concealment
charge from "undisclosed" to "acknowledged but unresolved," but an untested
direction has not reduced the substantive confound. Treating acknowledgment as
directional rebuttal gives a convenience-flavored assumption evidentiary force
it did not earn.

**Repair:** added the DIRECTIONAL-DEFENSE SYMMETRY CHECK to E0 and added the
effect value DIRECTIONALLY-CONTESTED. The check distinguishes source-tested
direction, externally cited but not yet reception-checked direction, and
asserted-only direction. A same-mechanism opposite direction that remains live
under the source's own evidence blocks any E0 severity reduction.

**Regression condition (PASSED 2026-08-11):** rerunning the Shen counter-audit
with the repaired E0 returns CV-7 as DIRECTIONALLY-CONTESTED rather than
RECHARACTERIZED; states the mirror-direction hypothesis explicitly—selection or
concentration on the visible leveling metric could bias the comparison toward
parity and mask a difference among genuine maximizers; corrects any "hidden"
wording to "acknowledged but direction unresolved" where needed; and preserves
CV-7's pre-E0 severity consistently across E0, G2, G3, and the final verdict.

**Case:** `tests/cases/case_FAIL-CA-004_shen-directional-defense-symmetry.md`,
using the partial rerun artifacts under `examples/research/shen/`.

**Status:** OBSERVED; REPAIR APPLIED; REGRESSION PASS 2026-08-11. CV-7 was
`directional defense — EXTERNALLY-CITED` and `DIRECTIONALLY-CONTESTED`; its
pre-E0 moderate severity was preserved in every section that referenced it. All
four operator leads were supplied explicitly, corrected Lead 3 controlled, and
Lead 4 remained `FILED / NOT EXERCISED`. The overall `F — Mixed` category did
not change.

---

## CV - Construct Validity (research branch)

### FAIL-CV-001  -  Construct-validity audit under-weighted a definitional scope-creep mismatch

**Observed:** on the Donovan et al. (2024) genomics-education audit (“humane
genomics education reduces racism”), the construct-validity prosecutor detected
that the operationalization (broader-than-stated-definition GESR-family-style
items) diverged from the paper’s strong-discrete definition — but filed it as
secondary commentary (“the construct is contested,” “largely unaddressed”), with
no severity, no concede test, no finding-table row. It cleanly prosecuted the
racism proxy leap (DEFEATS) and let the construct mismatch fall out of the
verdict. Right finding, wrong tier.

**Why this matters:** same family as FAIL-MB-009 (a load-bearing fact buried
under a healthy-looking aggregate) — the toolkit’s recurring failure is
mis-TIERING a caught finding, not missing it.

**Repair:** definition-operationalization check (1-claim-extraction Field 1) +
Field 3 binding the defensible claim to actual items on mismatch + scope creep
as its own required severity value and mandatory own row (2-construct-validity
Sec 3/16/17).

**Regression condition:** where operationalization is broader than stated
definition, the mismatch appears as its own scored finding with a concede test,
never as a closing aside.

**Case:** Donovan et al. 2024 (corrected re-run elevates the finding to MAJOR,
concede test NARROWS).

---

### FAIL-CV-002  -  Construct-validity audit took the target construct as established

**Observed:** same Donovan audit run. Every measurement-side check (proxy,
level-of-analysis, ecological validity, decisive test) ran cleanly, but no
section prosecuted whether the target construct itself — genetic essentialism —
was established: prevalent, held in the stated strong form, wrong in specified
respects and degrees, or actually harmful in effect. The paper asserts these and
moves directly to “we reduced it”; the audit noted this was “contested” in
passing and moved on.

**Why this matters:** the construct-validity prosecutor is instrumented for the
measurement-vs-claim gap and blind to the construct-vs-world gap. FAIL-CV-001
and this are the same blind spot one level apart.

**Repair:** new CONSTRUCT ESTABLISHMENT section, upstream of measurement
extraction. Five graded properties (prevalence / form-intensity / domain /
wrongness-map / harm-in-effect), triggered only by normative/causal escalation
(a narrowly-hedged efficacy claim does not trigger it), with an explicit
not-firing condition (“construct adequately established”).

**Regression condition:** a paper making a normative/causal claim about a
construct it does not establish gets the gap scored as its own finding; a paper
that cites established characterization returns “adequately established,” not a
manufactured gap.

**Case:** Donovan et al. 2024.

---

### FAIL-CV-003  -  Construct-establishment check over-fires under thin retrieval

**Observed:** the FIRST live run of the FAIL-CV-002 repair (Donovan, abstract-only
retrieval) rated all five construct properties ASSERTED / load-bearing and
returned “construct not adequately established,” major/fatal, Status: confirmed
— while the finding table’s own columns (innocent-explanation, what-would-weaken)
stated the finding rests on unfetched full text and citations. The check
conflated “unverified under thin retrieval” with “unestablished by the paper.”

**Why this matters:** same failure the media branch’s retrieval-depth machinery
exists to prevent — a thin run and a deep run produced equally confident
verdicts. Also means the check could not acquit regardless of how well a paper
actually establishes its construct, under thin retrieval.

**Repair:** four-value status (ESTABLISHED-REPORTED / ESTABLISHED-CITED /
ASSERTED / UNKNOWN). ASSERTED requires the intro and citations to have actually
been fetched and checked; otherwise UNKNOWN. A finding resting on any UNKNOWN
property is capped PROVISIONAL, never load-bearing.

**Regression condition:** an abstract-only run returns “establishment UNKNOWN —
full text required,” not a confirmed gap.

**Case:** Donovan et al. 2024 (re-score against NSF PAR citation check flips
harm-in-effect and prevalence from ASSERTED to ESTABLISHED-CITED — confirms the
over-fire empirically, not just by design reasoning).

---

### FAIL-CV-004  -  Scope-creep finding built on inferred, not retrieved, scale items

**Observed:** the FAIL-CV-001 scope-creep finding (rated MAJOR) attributed
GESR-family items — “races may be smarter/better athletes because of genetics,”
medical utility of ancestry — to the Donovan paper. Donovan’s actual instruments
(PHGV, GARD, BGE — retrieved via the open NSF PAR copy of the predecessor paper;
OSF and Wiley were bot-blocked) target empirically-false discreteness/uniformity/
proportion beliefs and strong (>50%) genetic-causation claims. Different items
entirely. The scope-creep finding was built by inferring a scale’s contents from
its family/name, not by retrieving the scale actually used.

**Why this matters:** identical mechanism to FAIL-CV-003 (assert specifics
without retrieval) on a different check, AND it is the exact error the audit was
built to catch, committed by the auditor.

**Repair:** operationalization status (ITEMS-RETRIEVED / ITEMS-INFERRED). Scope-
creep and pathologization findings require ITEMS-RETRIEVED; ITEMS-INFERRED caps
the finding at UNKNOWN and bars it from firing.

**Regression condition:** a run working from a scale’s name/family returns
“operationalization UNKNOWN — items not retrieved,” not a scope-creep finding.

**Case:** Donovan et al. 2024 (PHGV/GARD/BGE instrument text retrieved, scope-
creep finding withdrawn).

### FAIL-CV-005  -  Verdict flips across models on an unsettled scope boundary
**Observed:** two models ran the same claim-extraction + construct-validity sequence on the
same paper, and BOTH selected the same Field 6 claim via the same Rule 2 (prefer the
quantified version)  -  the quantified temporal claim "emotional loneliness decreased by 0.84
points on a 0-6 scale." They then returned incompatible verdicts:

- Sol  -  no DEFEATS; USEFUL-FOR-NARROWER; residual grade C. Reads the missing counterfactual
  as defeating only the paper's separate CAUSAL claim, which it marks a deferred MAP GAP; the
  temporal score-change claim survives, materially narrowed.
- Claude  -  one DEFEATS; claim INVALID as a causal claim; residual grade C. Reads the pre-post
  change score as proxying the intervention effect, so the absent counterfactual defeats
  Field 6 itself.

Both readings are defensible under the prompt as written. The divergence is not evidential  -
it is a scope convention about whether a temporal Field 6 claim inherits the causal burden of
the surrounding paper.

**Why this matters:** structurally identical to FAIL-MB-009 (amplification verdict flipping
across models on a counting convention), now observed in the RESEARCH branch for the first
time. A verdict that flips on convention rather than evidence is not a verdict. It also means
the shared-object rule is under-specified in exactly the place it is supposed to be strongest.

**Repair (proposed, not written):** state explicitly whether a quantified temporal Field 6
claim carries the causal burden of the paper's framing, or whether causal identification is
always a separate deferred object. Either answer works; the prompt must pick one. If deferred,
define what promotes the deferred causal claim into scope.

**Regression condition:** two models on the same source and same Field 6 claim return the same
DEFEATS/NARROWS disposition for a missing counterfactual.

**Case:** Gabarrell-Pascuet et al. 2024 (`tests/runs/reducing-loneliness/sol-construct.txt`,
`tests/runs/reducing-loneliness/claude-construct.md`).

**Status:** repair proposed, not applied.


---

## MB  -  Media Branch

### FAIL-MB-001  -  The flip test was theater

**Observed:** returned “would flag the mirror? Yes” on every finding across two runs. Zero
downgrades. Answering yes is free. Repair: costly flip test  -  compose the mirror AS
TEXT, audit your own mirror, forced ranking, downgrade requirement. Regression
condition: a written mirror passage appears in output with findings against it. Case:
none.

### FAIL-MB-002  -  The consistency check induced a wrong downgrade

**Observed:** the check found that scene-first and justification-first orderings both
construct, and concluded the sequencing finding should be downgraded. **Wrong

- that ordering constructs in both directions makes the outlet’s choice MORE meaningful,
not less.** Repair: Type A (inconsistent principle  -  downgrade) vs. Type B
(symmetric phenomenon
- NO downgrade) split. Regression condition: no downgrade is issued for a Type B
observation. Case: none.

### FAIL-MB-003  -  Coherence severity scaled with finding-splitting

**Observed:** one model split headline findings into two and reached 8 same-direction
findings; two others reached 5 on the same article. The 8 drove a heavier verdict.
Severity was a function of how finely findings were divided. Repair: count LEVERS,
not findings. Nine named, capped at 9/9. Regression condition: coherence ratio never
exceeds the lever count. Case: none.

### FAIL-MB-004  -  The strip test removed fact-sources

**Observed:** two models split PARTLY SURVIVES vs. COLLAPSES on the same article, entirely
because one stripped a mixed paraphrase-plus-quoted-fragment construction and the other kept
it. That single choice drove severity, aggregation, and the final verdict. Repair:
strip only FRAME-CARRIERS; keep FACT-SOURCES; explicit handling of mixed constructions.
**Regression condition:** strip test output states what was removed and kept. Case:
none.

### FAIL-MB-005  -  Discretionary downgrade never fired

**Observed:** five consecutive runs at zero downgrades. One run reproduced the mandated
sentence and then argued against it in a parenthetical. Another inverted it (“is
functioning” for “may not be functioning”). A check that can be argued away is not a
check.

**Repair:** AUTOMATIC downgrade - mechanical, no justification path. If the downgrade seems
wrong, fix the ranking.

**Regression condition:** every run reports which finding was downgraded.

**Case:** none.

**Status:** TESTED. The automatic downgrade has fired at least seven times: both Ceuta
run-2 audits, all three earlier genuine fixed-packet runs (DeepSeek, Grok, Sol), the
integrated RC2 Ceuta rerun, and at least one run-1 audit. The integrated rerun also
shows that removing a former rank-1 finding mechanically moves the downgrade to the
new top-ranked survivor. The fixed-packet DeepSeek and Grok runs declared PRIOR
SOURCE: NONE; Sol declared a MODEL-GENERATED prior. The mechanism therefore fires
independently of whether a prior was supplied or generated. Five consecutive zeros
under the prior discretionary version. This closes the TODO question “does the
mechanical downgrade actually fire.”

### FAIL-MB-006  -  D2 returned CONFIRMED with no evidence

**Observed:** on the same cross-branch question, one run returned CONFIRMED having retrieved
no primary source; another returned FALSIFIED citing a specific outlet; a third returned
STILL UNRESOLVED. Only the second and third were defensible. Repair: D2 EVIDENCE
FLOOR. CONFIRMED / FALSIFIED / RECLASSIFIED / NETWORK-WIDE each require named evidence.
CONFIRMED flagged as the most dangerous value  - absence of contradiction is not
confirmation. Regression condition: every D2 resolution names its evidence. Case:
none.

### FAIL-MB-007  -  Network-wide uniformity was treated as exoneration

**Observed:** a rule stated that shared behavior across outlets should downgrade the
single-piece finding. Wrong  -  uniformity establishes the outlet is not an OUTLIER; it
does not establish the treatment is proportionate. Every outlet can inherit the same wire
framing or blind spot. Repair: RECLASSIFY, do not downgrade. Downgrade the
distinctiveness claim, keep the construction finding, record the convention separately and
name its source. Regression condition: no substantive finding is downgraded solely for
being network-wide. Case: none.

### FAIL-MB-008  -  The independence count had no defined unit

**Observed:** three models audited the same event (Ceuta, run-1) and returned 2, 3-4, and ~5
for “genuinely independent sources” - a 2.5x spread on the branch’s flagship metric.
Definitional, not analytical: one counted source TYPES, another reporting STREAMS. The
prompt named no unit.

Initial repair: two-level count in Section B (LEVEL 1 = original-reporting
organizations; LEVEL 2 = upstream origins); state the unit before any number; no bare
integer.

Initial repair was INCOMPLETE - confirmed on identical input. On the fixed eight-piece
packet, Level 1 remained stable at 3-4 while Level 2 returned 3, 6, and 12-14 across
DeepSeek, Grok, and Sol - a roughly 4.7x spread. The mechanism is visible in the outputs:
DeepSeek counted origins of the SHARED material; Sol counted ALL distinct origins. Both are
defensible under the prompt’s wording. The run-1 divergence therefore survived one level
down and was not sample-driven.

Superseding repair: the Section B per-fact rewrite demotes whole-coverage Level 1 and
Level 2 to description and moves the amplification verdict to origin counts for each
load-bearing contested fact. Per-fact counts are the stable unit: a disputed figure traced
to one government remains one origin regardless of how finely the rest of the story is
split.

**Regression condition:** models may differ in descriptive whole-coverage Level 2, but must
converge on the per-fact origin counts and may not let whole-coverage granularity flip the
amplification verdict.

**Case:** none dedicated. The exact fixed Ceuta packet is now preserved in the
FAIL-MB-017 and FAIL-MB-018 cases, and the integrated rerun exercises the per-fact
repair, but neither case treats descriptive Level-2 reproducibility as its oracle.

**Status:** DEFUSED, NOT CLOSED.

The superseding per-fact repair has now been exercised on the integrated RC2 Ceuta
rerun. The load-bearing inference is protected: whole-coverage Level 2 is explicitly
descriptive only, the whole-coverage ratio supports no amplification/corroboration
verdict, and proposition-level origin counts carry the source-independence judgment.

The underlying descriptive measurement instability remains live. On the same fixed
Ceuta packet, Level-2 counts have varied materially across models/conventions
(including approximately 6, 12-14, and approximately 25; other RC2 executions have
also produced nearby but different granular totals). The integrated rerun again
demonstrates that Level 2 is not a reproducible measurement unless the granularity
convention is made substantially more mechanical.

Current disposition: dangerous inference removed; descriptive measurement
instability remains. Do not compare Level-2 totals across runs as though they were
a stable metric.

### FAIL-MB-009  -  The two-level fix inverted the amplification ratio

Observed and reproduced on identical input. The whole-coverage ratio’s VERDICT flipped
across models auditing the same fixed eight-piece packet:

- DeepSeek: Level 1 = 4, Level 2 = 3, ratio 2.7:1 - read as amplified after collapsing to
cross-outlet shared origins.
- Grok: Level 1 = 4, Level 2 = 6, ratio 1.3 - read as healthy.
- Sol: Level 1 = 3-4, Level 2 = 12-14, ratio about 0.6 - read as very healthy before Sol
explicitly rejected the masking effect and decomposed the claims per fact.

This is not numeric wobble. The conclusion inverted solely because each model used a
different origin-splitting convention. DeepSeek’s correct-direction verdict came from
aggressive collapse, not from a stable metric. Grok printed the prompt’s assertion that
Level 2 would usually be lower directly above a Level 2 > Level 1 result, while its prose
described amplification and its ratio implied independence.

Second-order damage: every protection keyed to “low Level 2” - the
CROSS-OUTLET-CORROBORATED cap, the Section C1 caveat, and the Section H severity cap -
silently fails when whole-coverage Level 2 is large, even if every load-bearing contested
fact is single-origin.

Contradiction exposed: Level 1 counts only original reporters, often few. Level 2 counts
every upstream origin, often many. In wire-dominated coverage, Level 2 > Level 1 is
ordinary. That direction carries no amplification meaning.

**Repair:** amplification is now scoped PER load-bearing contested fact. The prompt requires
a row for each fact, prohibits pooling, re-keys corroboration and severity caps to that
fact’s independent-origin count, and demotes whole-coverage Level 1, Level 2, and pieces /
Level 2 to descriptive context. Sol supplied the existence proof: it flagged the overall
ratio as masking, then reported Vivas framing 8 / 1, the 60,000 figure 2 / 1, and
trafficking cause 5 / 1, surfacing the single-sourced figure as a major finding.

**Regression condition:** amplification is reported per contested fact; no whole-coverage
ratio is treated as a verdict; a fact single-sourced to one origin never reads as
corroborated regardless of total origin count; and models on the same packet no longer
disagree on whether that fact is amplified.

**Case:** none dedicated. The integrated Ceuta rerun exercises the per-fact repair
on the exact packet now preserved by the FAIL-MB-017 and FAIL-MB-018 cases.

**Status:** OBSERVED, REPRODUCED, REPAIR EXERCISED.

The integrated RC2 Ceuta rerun confirms the per-fact repair is functioning:
whole-coverage Level 1 / Level 2 and pieces / Level 2 remain descriptive, while
the proposition-level table independently classifies the 60,000 figure,
trafficking explanation, military deployment, and other load-bearing facts.

The continued Level-2 granularity spread does NOT flip the amplification verdict.
This closes the dangerous ratio/inference failure described here even though
FAIL-MB-008’s descriptive Level-2 measurement instability remains open.

### FAIL-MB-010  -  D8 filed frame-carrying verbs as “synonym only”

Observed and reproduced, but MODEL-DEPENDENT. The crossing verbs pour / breach / cross /
enter carry three different frames: flood (pour / stream), violation (breach), and neutral
movement (cross / enter). D8 exists to distinguish connotation from denotation.

- DeepSeek MISS: captured the verbs in the descriptor table, rated them neutral or “breach
factual,” and never routed the distinction through D8.
- Grok MISFILE: rated the cluster “mostly synonym.”
- Sol PASS: identified “breach” as presupposing a defended boundary overcome, distinguished
it from neutral cross / enter, ranked breach-vs-cross as the strongest non-synonym
variance, rated it MODERATE, and built the flip test on that frame distinction.

Two of three fixed-packet runs therefore failed, while Sol is an existence proof that the
branch can classify the language correctly. The failure is model-dependent, not universal.

What it protects: the branch must route the same category - verb frame,
synonym-vs-causal variance, and causal-context variance - into the same analytical bin
regardless of model. Registering the connotation and then dismissing it as factual is still
a miss.

**Repair:** APPLIED through the shared [MEDIA-P1] causal-role primitive.
The branch now distinguishes event classification, cause, role-and-status, blame,
remedy, and leadership/policy; applies epistemic states to cause and blame; and
treats a verb as frame-carrying when it moves an axis assignment rather than merely
sounding vivid. The rule is embedded in both framing-construction and
coverage-network, with D8 absorbed into the shared execution path.

**Regression condition:** where outlets use denotationally similar verbs carrying
different frames for the same action, the shared causal-role analysis records frame
variance rather than cosmetic synonymy; the same classification is reachable from
either media entry branch.

**Case:** none dedicated. FAIL-MB-018 now owns the disposition test on the fixed
Ceuta packet.

**Status:** original observed failure retained. Its former disposition is
superseded in part by FAIL-MB-018 and the replacement gate has been exercised on
the integrated Ceuta rerun.

Superseding disposition note (2026-08-09): FAIL-MB-018 changes the correct
entry condition for this object. The original observed failure remains valid:
models should not dismiss potentially meaningful formulations as “synonym only”
without testing what semantic assignment they add. But the repair is no longer
“every denotationally similar vivid verb must survive as frame variance.”

The Coverage Network branch now establishes semantic materiality first. A wording
difference may resolve as REGISTER VARIANCE, EARNED SPECIFICITY, or MATERIAL
OUTLIER. Only the last category proceeds as framing evidence. On the integrated
Ceuta rerun, breach / pour / cross / enter does not survive into the standardized
finding table after the FAIL-MB-018 gate.

Regression relationship: FAIL-MB-010 protects against premature dismissal;
FAIL-MB-018 now owns the disposition test that determines whether the wording
actually becomes a framing object.

Prefix note: retained as FAIL because the misclassification was observed and reproduced.
The Sol counterexample belongs in Status, not the prefix.

---

### FAIL-MB-011  -  Literal packet boundary excluded the source of the framing

**Observed:** The first Madison coverage-network run limited the packet to pieces
directly about the encampment. It therefore missed a same-cycle political-
reaction article that imported Jacob Blake / Kenosha as a moral precedent, and
it lacked companion video and organizer material relevant to the New York Post’s
BLM / Antifa characterization. The audit treated the resulting absence as a
weakness in the outlet claim. A bounded companion-retrieval rerun materially
changed the assessment: the occupation / autonomous-zone classification and BLM
alignment gained direct support, while formal Antifa organizational control
remained unestablished.

**Why this matters:** The audit can be rigorous inside its packet and still be
wrong about the coverage mechanism when the material supplying the inherited
frame sits immediately outside the literal event-keyword boundary.

**Repair:** COMPANION RETRIEVAL. Retrieve material that is linked, cited,
materially relied upon, repeatedly invoked as causal / historical / political /
moral context, or demonstrably upstream of the framing. Bound expansion by
evidentiary relevance, not outlet identity or open-ended topical similarity.

**Regression condition:** When a finding depends on an imported analogy,
classification, affiliation, or contextual claim, the output identifies and
retrieves the upstream material before resolving the finding. It does not treat
“not present in the initial packet” as “no evidentiary origin.”

**Case:** Madison encampment expanded rerun.

---

### FAIL-MB-012  -  Binary sourced / unsupported treatment erased supported contextual inference

**Observed:** The original Madison audit treated “BLM and Antifa controlled the
site” as lacking an evidentiary origin in the retrieved material. After companion
retrieval, BLM chants, flags, movement symbolism, named left-wing organizers,
autonomous-zone self-labeling, barricades, access enforcement, and reporter /
business interference supported a substantially stronger conclusion. The exact
formal-organizational claim still required narrowing, but the original binary
treatment had collapsed three different questions: ideological alignment,
tactical resemblance, and verified organizational control.

**Why this matters:** An audit that recognizes only explicit organizational
self-identification or “unsupported” can understate what converging retrieved
evidence legitimately establishes. The opposite danger is prior laundering:
general knowledge about who “usually” uses a tactic cannot substitute for
indicators in the record.

**Repair:** CONTEXT-SUPPORTED IDENTITY INFERENCE ladder:

1. verified organizational identity or control;
2. context-supported ideological alignment;
3. context-supported tactical / movement resemblance;
4. weak resemblance;
5. unsupported attribution.

Require the indicators to be observable in retrieved material and run the mirror
inference in the opposite ideological or institutional direction.

**Regression condition:** Every affiliation finding distinguishes alignment,
resemblance, and formal control; enumerates its retrieved indicators; and states
what the same standard licenses in the mirror direction.

**Case:** Madison encampment expanded rerun.

---

### FAIL-MB-013  -  Noun-only label coding produced a false softening finding

**Observed:** In the first Seattle label discussion, repeated use of “teen,”
“boy,” “juvenile suspect,” and “15-year-old suspect” appeared to support a
softening-language hypothesis. The full rerun showed that later coverage paired
the age noun with strong agency and severe conduct: “teen shooter,” repeated
firing, ghost-gun possession, first-degree assault, unlawful firearm possession,
and an adult-transfer request, while also preserving the ballistic limitation
that his gun did not kill the two bystanders. The noun alone pointed in the
opposite direction from the complete package.

**Why this matters:** A nominally soft category can coexist with hard,
agentive, legally specific treatment. Label-only coding can manufacture a
finding the surrounding language falsifies.

**Repair:** LABEL-UPDATE TRAJECTORY + LANGUAGE PACKAGE. Record headline, lede,
first reference, later labels, material-fact availability, verbs, modifiers,
agency, attribution, evaluation, update trigger, and persistence. A single-event
run may document the package but may not infer race-, ideology-, group-, or
status-based differential treatment without a matched corpus.

**Regression condition:** No softening / hardening finding is based on the noun
alone. The audit states whether the surrounding package is soft, mixed, hard, or
neutral and whether it updated when stronger facts became available.

**Case:** Bite of Seattle label-trajectory rerun.

---

### FAIL-MB-014  -  The actual role-update failure was displaced onto the wrong party

**Observed:** The initial Seattle hypothesis focused on whether age labels
softened treatment of the detained 15-year-old. The label-package rerun found
that the teen’s later package was mixed-to-hard and generally updated correctly
after charging and ballistic evidence. The clearer persistence failure concerned
the deceased 19-year-old suspected gunman, who sometimes remained inside
collective “three victims” or memorial language after role differentiation was
available.

**Why this matters:** Starting hypotheses can direct attention to the wrong
party. Without party-by-party trajectory coding, the audit may confirm the
operator’s suspected mechanism while missing the actual update failure nearby.

**Repair:** PARTY ENUMERATION before coding, followed by compressed trajectory
coding for every analytically significant actor, group, institution, counterpart,
or affected party. Expand the full package only where tension, ambiguity, or
persistence appears.

**Regression condition:** The audit enumerates all load-bearing parties and
reports which party actually carries the strongest persistence mismatch,
including when that differs from the operator hypothesis.

**Case:** Bite of Seattle label-trajectory rerun.

---

### FAIL-MB-015  -  Summarization collapsed the quotation pair that contained the finding

**Observed:** The Seattle audit retrieved the general facts that police called
the incident gang-related and discussed small groups driving shootings, but the
output summarized them separately. It did not preserve the same-briefing pairing
of “small groups” / “two groups firing at each other” with the explicit
“gang-related” classification. Once the quotations were placed together and the
suspected perpetrator collectives were coded as a party, the audit detected a
same-stage abstraction asymmetry.

**Why this matters:** Sometimes the contrast between adjacent formulations is
the evidence. Topic-level summarization can preserve every proposition while
destroying the linguistic relation the audit is meant to test.

**Repair:** QUOTATION-PAIR PRESERVATION. When adjacent or same-stage
formulations materially differ in agency, specificity, certainty, or
classification, preserve both verbatim and compare them as a pair. Preferred
neutral finding language: “reduces categorical specificity at the point of
agency assignment.”

**Regression condition:** Consequential paired formulations are quoted together
with speaker, evidentiary stage, agency assignment, specificity, plausible
functional distinction, and residual difference. They are not collapsed into a
generic “gang context” summary.

**Case:** Bite of Seattle police-briefing follow-up.

---

### FAIL-MB-016  -  Full language-package coding over-produced low-signal analysis

**Observed:** The Seattle language-package run applied the full multi-field
schema to every party. Several sections — including uncontested bystander and
frontline-officer packages — were accurate but did not alter a finding or the
verdict. The module succeeded at its primary job but generated substantially more
structured text than analytical signal.

**Why this matters:** A completeness rule can make a prompt look undecided,
increase output burden, and obscure the few parties where language is genuinely
contested. This is especially costly in a branch already vulnerable to long,
multi-section output.

**Repair:** ADAPTIVE LANGUAGE-PACKAGE TRIAGE. For every party, default to:

1. label trajectory;
2. package direction (soft / mixed / hard / neutral);
3. update behavior.

Expand to the full schema only when there is genuine soft/hard tension,
same-stage divergence, consequential persistence, ambiguity, a load-bearing
finding, or a targeted investigation lead.

**Regression condition:** A rerun preserves the Seattle false-positive
prevention and police quotation finding while materially reducing full-schema
sections that do not affect the verdict.

**Case:** Bite of Seattle label-trajectory output; repair proposed after
adversarial review.

**Status:** proposed, not yet rerun.

---

### FAIL-MB-017  -  Cross-piece availability gate suppressed within-piece prominence findings

**Observed:** CN_677 produced a MODERATE standardized finding on gross-vs-aftermath
headline asymmetry across the fixed Ceuta packet. France 24 and CBC foregrounded
the gross crossing figure while carrying return context lower in the same piece;
NYT foregrounded return while carrying the 57-death total lower in the piece.
Revised and RC2 developed all constituent evidence but emitted no corresponding
standardized finding. RC2 reported SELECTION FINDINGS: NONE.

Why it happened: Section C represented facts as Outlets reporting or
Outlets omitting. A fact present in a piece but absent from a more prominent
layer was therefore recorded as “reporting.” The within-piece placement object
was destroyed before the cross-piece availability gate could evaluate anything.
One gate was serving two different objects: cross-piece omission and within-piece
prominence.

**Why it matters:** within-piece prominence does not require counterfactual
cross-piece availability reconstruction; the piece itself establishes possession
of the fact. Source/wire provenance still matters to whether the packaging can be
attributed to the outlet, and update/version timing can supply an innocent
explanation. A newer instrument silently losing a valid finding an older version
caught is a regression regardless of the finding’s substantive weight.

**Repair:** split the objects.

- SELECTION remains cross-piece omission and retains the Availability Matrix,
mandatory availability citation, absence floor, and timing caps.
- PROMINENCE-PACKAGING becomes a separate finding type for within-piece placement.
- Require FULL-TEXT-CONFIRMED material.
- Record packaging provenance as CHOSEN / INHERITED / MIXED / UNKNOWN.
- Use FULL / PARTIAL / NONE PACKET INVERSE symmetry states.
- Apply the absence floor to an asserted NO PACKET INVERSE.
- Apply a FACT-TIMING / VERSION innocent-explanation check.
- Add D2 cross-branch ownership so a prior single-piece packaging finding is not
duplicated by Coverage Network.
- Keep source-attribution compression in SOURCE-CHAIN and causal-role reassignment
in D-ROLE.

**Regression condition:** on the standalone fixed Ceuta regression object, the
standardized finding table preserves the gross-vs-aftermath prominence object,
types it as prominence-packaging, marks cross-piece availability NOT APPLICABLE,
states the packet inverse, reports packaging provenance, and does not double-count
the 60,000 source-attribution object.

**Case:** ceuta-prominence-regression.

**Status:** REPAIR APPLIED AND REGRESSION PASS.

- FAIL-MB-017 standalone expectation: PASS.
- Joint FAIL-MB-017 + FAIL-MB-018 interaction check: PASS.
- The restored finding is MODERATE on this fixture.
- It is grounded in placement of substantive facts/dimensions, not lexical
differences.

**Fixture status:** COMPLETE. The exact original eight-piece Ceuta synthetic packet
supplied by the operator is embedded verbatim in the regression case. No reconstructed
or paraphrased packet is used.

---

### FAIL-MB-018  -  Lexical variance treated as the analytical unit before semantic materiality established

**Observed:** across CN_677, Revised, and RC2, the
pour / breach / cross / enter formulation difference repeatedly became a
standardized low-severity framing object. Later prompt versions added substantial
language-trajectory and causal-role machinery but continued to create the lexical
object first and test its materiality later.

**Why it matters:** this is a construct-validity defect, not a prompt-size defect.
The candidate unit was the word rather than the semantic assignment. Ordinary
synonyms and supported specificity could therefore propagate through expensive
downstream machinery and had to be knocked down late — or survive as a finding
without first establishing that they changed the reader’s model.

**Repair:** add the SEMANTIC EQUIVALENCE AND EARNEDNESS GATE upstream of all
analysis triggered by lexical/formulation variance.

- Preserve D-ROLE’s independent substantive six-axis scan.
- Require same actor/action/referent and materially comparable stage before
bucketing.
- Decompose any vivid/specific candidate into its added semantic predicate.
- Require non-circular independent packet support before awarding
EARNED SPECIFICITY.
- Stop REGISTER VARIANCE upstream.
- Carry forward only MATERIAL OUTLIERS that move a named substantive assignment.
- Apply outlet-permutation / valence-reversal symmetry to the bucketing decision.
- Make VERB-AS-TRACE subordinate to the gate for wording-derived candidates and
canonicalize its duplicate restatements.

**Regression condition:** no standardized event-language finding may survive
merely because outlets use different formulations. Any candidate that survives
must have a named added predicate, independent support, and a named moved
assignment. D-ROLE must remain able to discover non-lexical CAUSE / BLAME / ROLE /
REMEDY / LEADERSHIP differences independently.

**Case:** ceuta-semantic-equivalence.

**Status:** REPAIR APPLIED AND REGRESSION PASS.

- FAIL-MB-018 procedural expectations: PASS.
- Joint FAIL-MB-017 + FAIL-MB-018 interaction check: PASS.
- The prior RC2 event-language finding disappears on the Ceuta fixture.
- No unrelated standardized finding disappears.
- The migrants/crossers full language-package expansion is no longer triggered;
this is an observed execution reduction, not a runtime claim.

Unexpected side-effect — downgrade cascade: FAIL-MB-005 requires one automatic
downgrade after forced ranking. In old RC2, the event-language finding ranked first
and absorbed that downgrade. FAIL-MB-018 removes the event-language finding before
the flip test, so the surviving findings are re-ranked. France 24’s political
blame-routing finding becomes rank #1 and inherits the automatic downgrade,
moving MODERATE -> MINOR.

Neither FAIL-MB-017 nor FAIL-MB-018 predicted this. It is a genuine downstream
interaction of the existing mechanical downgrade rule, not discretionary severity
drift. Preserve it in RESULTS / revision evidence.

**Fixture status:** COMPLETE. The exact original eight-piece Ceuta synthetic packet
supplied by the operator is embedded verbatim in the regression case.

Joint interaction record

FAIL-MB-017 + FAIL-MB-018 interaction check: PASS.

Observed:

- prominence finding is grounded in placement of gross scale, return/reversal
context, and casualty/denominator detail;
- it does NOT use breach / cross / enter / pour variance as evidence;
- semantic-normalized wording does not re-enter Section H through prominence;
- real non-lexical cause/blame distinctions remain available to D-ROLE;
- no unrelated standardized finding disappears;
- finding-table count remains 10, with composition changed:
  • removed old event-language MINOR finding;
  • added prominence-packaging MODERATE finding;
  • France 24 blame-routing retained but automatically downgraded
MODERATE -> MINOR.

---

## IV — Internal Validity (`2-internal-validity.txt`)

### FAIL-IV-001 — Conditional DEFEATS from pending technical evidence entered the verdict as eligible

**Observed:** two runs of `2-internal-validity.txt` on Galor & Özak (2016), using the same
underlying evidence, produced different eligible-DEFEATS inventories and grades depending on
whether a construct-validity output was visible in ambient session context. The contaminated
run placed provisional or reception-confirmed-only coding-error and LTO-redefinition
allegations under "DEFEATS finding(s)" and returned D. The clean run reported no adequately
verified DEFEATS and returned C.

**Why it matters:** the Concede Test describes what follows if a finding is true; it does not
establish that the finding is true. The prompt lacked a separate eligibility gate, allowing a
logically defeating but technically unverified allegation to become load-bearing. Multiple
pending allegations could therefore compound into a confident adverse grade.

**Repair:** add `[IV-P1] VERIFICATION-GATED VERDICT ELIGIBILITY`; separate verification state,
technical-outcome status, conditional concede result, and verdict eligibility; restrict
Section I and adverse grade triggers to ELIGIBLE findings; retain conditional DEFEATS /
PENDING VERIFICATION findings in a separate visible inventory. Technical-outcome status now
distinguishes a retrieved third-party `INDEPENDENT-REANALYSIS-CONFIRMED` result from both this
audit's own `REPRODUCED` result and an `UNVERIFIED` allegation.

**Regression condition:** `galor-ozak-cross-prosecutor-leak`, expected items 1–3. The patched
grade and eligible-DEFEATS inventory must equal the clean control; the historical letter C is
context, not a permanently hard-coded oracle.

**Case:** Galor & Özak (2016), paired internal-validity runs. Exact run dates, filenames, and
hashes must be copied from the preserved artifacts; do not invent missing metadata.

**Status:** repair applied; paired regression rerun pending.

### FAIL-IV-002 — Ambient sibling-prosecutor output was treated as a formally supplied premise

**Observed:** in the contaminated Galor & Özak run, Section J stated that construct validity
"already showed" a specific major proxy mismatch even though no construct-validity output was
formally declared as an input. The output was merely visible because both audits occurred in
the same session. The clean run, without the sibling output in context, used appropriately
conditional language.

**Why it matters:** the three Stage-2 prosecutors are intended to be independent. Ambient
session visibility supplied an undeclared evidence path, changed the internal prosecutor's
factual premises, and contributed to a different grade. Section J's designed integration role
did not contain an input receipt or distinguish independent from integrated execution.

**Repair:** add an optional named sibling-output input; require `SIBLING-PROSECUTOR INPUT` and
`INDEPENDENCE STATUS` receipts; enforce the declared-input boundary globally; replace Section
J with separate NONE and FORMALLY SUPPLIED branches; label any supplied-sibling run
`INTEGRATED-NONINDEPENDENT`.

**Regression condition:** `galor-ozak-cross-prosecutor-leak`, expected items 4–6. A future
deterministic checker may verify receipt/form consistency and flag sibling-vocabulary matches
for human review, but cannot prove cognitive independence from a self-declaration.

**Case:** Galor & Özak (2016), paired internal-validity runs. Exact run dates, filenames, and
hashes must be copied from the preserved artifacts; do not invent missing metadata.

**Status:** repair applied; paired regression rerun pending.

**Cross-reference:** FAIL-IV-001 and FAIL-IV-002 arose from one paired-run comparison and were
applied in one edit pass. FAIL-IV-001 prevents pending technical claims from entering the
verdict even if ambient leakage recurs. FAIL-IV-002 prevents the undeclared evidence path
itself. Neither substitutes for the other.


---

## CN  -  Citation Network execution (2-citation-network.txt)

### FAIL-CN-001  -  Whole required sections vanished from the output

**Observed:** a live MBH98 run used the fully-blocked prompt and produced ZERO hits for the
claim-map receipt, verification states, and the standardized finding table  -  while the
concede test fired normally and the rest of the audit read as complete. The instructions
were present in the prompt. The sections were absent from the output, with no
acknowledgement.

Why this is its own failure class: every other entry in this registry is “prompt
correct, reasoning wrong.” This is “prompt correct, output incomplete.” A section that is
silently skipped is functionally nonexistent no matter how well written, and it makes every
repair to that section unverifiable. This class must be diagnosed before substantive repairs
to the same prompt can be trusted.

Two candidate causes, distinguished by burden: section salience lost in a long prompt (a
compliance defect, fixable by wording and placement) versus practical output limits (a
burden defect, fixable only by cutting or staging sections). These have opposite repairs,
which is why they had to be told apart before acting.

**Repair:** OUTPUT EXECUTION CONTRACT  -  exact-heading rule, required-heading list, N/A
rule, no-silent-merging rule, COMPLETION LEDGER, COMPLETION GATE withholding the final
verdict on any omission, plus an external checker (check-citation-network-output.py) so
compliance is mechanically verifiable rather than self-reported.

**Regression condition:** all 25 required headings appear as unique standalone lines in the
required order; the ledger’s claims match actual presence in both directions; the gate
withholds the verdict on any omission; the checker exits 0.

**Case:** compliance/citation-network-01 (compact), -02 (medium), -03 (large: 26
sources, 70 edges).

**Status:** REPAIRED AND VALIDATED at three supplied-packet burden levels. Sections A, F, H,
and J  -  the ones originally vanishing  -  performed substantive work at the largest level,
including two real hub-removal tests.

BURDEN HYPOTHESIS FALSIFIED. The candidate cause “too much required output to complete”
did not survive. The precommitted response to a burden failure  -  cut, merge, or stage
sections rather than reinforce the gate  -  was never triggered and remains recorded in
TODO.md for any future failure.

SCOPE OF THE VALIDATION  -  state this wherever the repair is cited. All three levels
used SUPPLIED packets with no open-ended retrieval. What is validated is that the contract
holds when the network is handed to the model. It is NOT validated under retrieval, where
the model must find the network itself  -  a different burden involving search, inclusion
judgment, and a much larger candidate space. “Validated at three burden levels” must not be
read as “validated.”

DO NOT PROPAGATE THIS GATE WITHOUT AN OBSERVED OMISSION. The contract is a FAIL-class
repair for one prompt. Adding it to prompts that have never omitted a section imposes 25
required blocks and a ledger as a GUARD-class precaution  - weaker justification, permanent
cost, and it inflates exactly the output burden that was the leading alternative diagnosis.
If another prompt starts skipping sections, the repair is proven and ready.

### FAIL-CN-002  -  Stale verdict-letter mapping in 2-construct-validity Section 13
**Observed:** Section 13's verdict mapping directs a DEFEATS result to letters D/E/F. Those
letters are defined nowhere else in the prompt; Sections 14 and 17 use the split claim-space
object (audited claim status + surviving residual + usefulness grade A/B/C/G/none). The Claude
run declined to invent a letter and returned the split object.

**Why this matters:** leftover from the pre-split verdict scale (see the verdict-notation
revision). Same class as the media drift-pass stale references. A model that trusted Section 13
would emit an undefined letter.

**Repair:** re-key Section 13 to the split claim-space object. Confirm no other section still
references the old letter scale.

**Regression condition:** grep for D/E/F verdict letters returns nothing outside the
residual-grade vocabulary.

**Case:** Gabarrell-Pascuet et al. 2024
(`tests/runs/reducing-loneliness/claude-construct.md`, toolkit note T2).

**Status:** open. NOTE: also verify against the truncation in TOOL-005  -  the mapping may be
reconciled in the unread tail.

### FAIL-CN-003  -  Adjacency preregistration locked fields but left exemplar selection post hoc

**Observed:** the Shen rerun locked adjacent fields before bibliography inspection but named
the purported canonical sources afterward, then described the result as a locked two-sided
canonical-source list.

**Why it matters:** scoring occurs on missing sources, not on field names. An auditor can choose
conveniently absent exemplars after seeing the bibliography while truthfully claiming the field
was preregistered.

**Repair:** require exactly one source-lock method: LOCKED QUERY, LOCKED SOURCES, or POST HOC.
A locked query fixes its output ex ante; locked sources are named ex ante; POST HOC sources
cannot independently anchor SCORED 2 or SCORED 3 on adjacent-field neglect.

**Regression condition:** the output states one source-lock method and its timestamp/hash;
post-inspection exemplars are labeled POST HOC and do not independently anchor a 2 or 3.

**Case:** Shen revised rerun, Finding 5.

**Status:** REPAIR APPLIED TO CANDIDATE; IAT VALIDATION PENDING.

### FAIL-CN-004  -  Field relevance was promoted to source-level adjudication

**Observed:** the Shen rerun treated several sources that define performance constructs,
support a general mechanism, or supply measurement methods as if their absence were missing
evidence capable of adjudicating a sex-linked psychomotor explanation against participation
and pipeline rivals.

**Why it matters:** a field can qualify ex ante while a particular source in it cannot change
the audited claim. Without a source-level gate, construct-defining and politically congenial
background literature can inflate adjacent-neglect severity.

**Repair:** classify each retrieved nominated source as CONSTRUCT-DEFINING,
MECHANISM-SUPPORTING, or DIRECTLY-ADJUDICATING. The direct class requires the actual result,
the explanation favored, the explanation weakened, and the precise revision required. Only
that class may independently anchor SCORED 2 or SCORED 3.

**Regression condition:** every nominated source receives the classification from its actual
contents; a 2 or 3 identifies at least one ex-ante locked, directly adjudicating source and the
specific result that forces revision.

**Case:** Shen revised rerun, Layer-B adjacent-field sources.

**Status:** REPAIR APPLIED TO CANDIDATE; IAT VALIDATION PENDING.

### FAIL-CN-005  -  Distinct dimensions reused the same evidence additively

**Observed:** adjacent-field neglect and lack of decisive tests both scored 2 from the same
missing-methods list; model non-updating substantially reused claim-mutation evidence. The
output's own finding language joined adjacent neglect and lack of decisive tests while the
aggregate counted them separately.

**Why it matters:** the dimensions are conceptually distinct and may dissociate, but distinct
labels do not create independent evidence. Additive scoring lets one omission increase both
the numerator and the apparent breadth of concern.

**Repair:** reuse the existing nesting rule with a separate AGGREGATION STATUS. Each SCORED
dimension is INDEPENDENT or NESTED under a parent. Nested rows retain disposition and ordinal
score, count as assessed for coverage, and are excluded from the aggregate numerator and
denominator. Separate scoring requires distinct evidence and inferential work.

**Regression condition:** overlapping dimensions name an evidence owner; any second dimension
either supplies independent evidence and inference or is NESTED and non-additive. The score
report gives independent and nested counts separately.

**Case:** Shen revised rerun, scorecard and Finding 3.

**Status:** REPAIR APPLIED TO CANDIDATE; IAT VALIDATION PENDING.

### FAIL-CN-006  -  Canonical verification vocabulary was replaced wholesale and the checker passed
*Filed as FAIL-CN-006, not FAIL-CN-002 as drafted: CN-002 is already held by the stale verdict-letter mapping entry above, committed to main.*

**Observed:** the 2026-08-16 Shen revised citation-network rerun emitted 71 noncanonical
authority labels: GRAPH-VERIFIED (37), CONTEXT-VERIFIED (24), SOURCE-VERIFIED (9), and
RECEPTION-VERIFIED (1). It used no canonical `*-CONFIRMED` verification state. The prompt
said not to invent states, but the checker returned PASS.

**Why it happened:** the run needed to describe values computed from retrieved graph inputs,
while every canonical verification state describes retrieval or evidentiary status. It filled
the expressive gap by replacing the vocabulary. Prose prohibition was not mechanically
enforced.

**Repair:** keep verification state and derivation separate. Add
COMPUTED-FROM-RETRIEVED as a derivation mode requiring rule, numerator, denominator, input
coverage, and the inputs' canonical verification state. The checker rejects every token
matching `*-VERIFIED` or `*-CONFIRMED` outside the whitelist and reports token, count, and line
numbers. It reports structural and content-form results separately and returns FAIL,
PASS-WITH-REVIEW: N items, or PASS; bare PASS is unavailable while a targeted review item is
pending.

**Regression condition:** the unchanged Shen output fails with all four offending tokens,
counts, and line numbers, plus the silent-band and scored-density receipt failures. Shen V1
passes the whitelist-only clean control. The complete clean fixture returns PASS, while its
locked-source variant returns PASS-WITH-REVIEW with the source-lock record extracted inline.

**Case:** `tests/test-citation-network-checker.py`, using the Shen revised
output as the dirty full fixture, Shen V1 as the clean whitelist fixture, and supplied-packet
PASS / PASS-WITH-REVIEW controls.

**Status:** REPAIR APPLIED TO CANDIDATE; IAT VALIDATION PENDING.


---

## TOOL  -  Checking tooling

Failures in the tools that verify prompt output. Distinct from prompt failures: a broken
checker does not produce a wrong audit, it produces FALSE CONFIDENCE in an audit, which is
worse because it removes the signal that something is wrong.

### TOOL-001  -  The checker’s own design guaranteed a false pass

**Observed:** the first check-citation-network-output.py tested presence with heading not in text  -  a substring search over the whole document. But the COMPLETION LEDGER
enumerates all 25 required headings in its own rows. Every heading therefore appeared in
every output that contained a ledger, and the checker returned PASS on files where every
actual section was missing.

Demonstrated on a synthetic file containing a ledger and no sections: old logic reported 0
missing.

Why it matters more than an ordinary bug: the checker validated that the LEDGER existed
rather than that the SECTIONS did  -  exactly inverted. The ledger is the CLAIM; the
sections are the FACT; the checker’s entire purpose is testing the claim against the fact. A
tool that certifies its own input passes is worse than no tool, because the compliance gate
was built precisely because self-report could not be trusted.

**Repair:** headings must match at LINE START (markdown table rows begin with | and
therefore cannot satisfy the check), plus bidirectional ledger cross-verification and
distinct exit codes so a run that correctly withheld its verdict is not scored the same as
one that silently omitted sections.

**Regression condition:** a fixture containing only a ledger and no sections must FAIL. A
ledger claiming completed for an absent section must FAIL. A ledger claiming omitted for
a present section must FAIL.

**Case:** compliance/checker-fixtures/  -  good.txt,
missing-but-ledger-says-complete.txt, present-but-ledger-says-omitted.txt.

Note: two independent reviews found this defect and reached the same repair from
different directions. That convergence is the multi-model process working on the tooling
rather than on the prompts.

### TOOL-002  -  The checker’s regression fixtures omitted the original failure

**Observed:** the first fixture set contained three cases  -  a clean run, a ledger falsely
claiming completion, and a ledger falsely claiming omission. All three test SELF-REPORTING
failures.

None tested SILENT OMISSION: sections missing, gate NOT fired, verdict issued anyway, no
INCOMPLETE RUN declaration. That is the observed behavior in FAIL-CN-001 and the entire
reason the execution contract exists.

Why this is a real failure and not a gap: the fixture set verified that the checker
catches a run that lies about itself, and did not verify that it catches a run that says
nothing. The second is the documented case; the first is hypothetical.

**Repair:** add missing-and-verdict-issued.txt  -  Section B absent, ledger reporting
completed, Artifact 10 issuing a full substantive verdict with no incompleteness
declaration. Expected: flagged as silent omission, distinguished from a well-behaved
incomplete run.

**Regression condition:** the fixture set covers both self-reported and silent omission.
Also currently untested: duplicate headings (uniqueness is claimed but unexercised),
incorrect ordering (ORDER_FAIL never fires in any fixture), and an entirely absent ledger.

**Status:** OPEN unless the fixture has since been added.

General principle this establishes: a regression suite for a checking tool must include
the failure the tool was built to catch. Testing only the failures that occurred to the
fixture author tests the author’s imagination, not the tool.

### TOOL-003  -  The completion gate could not be passed by a compliant run

**Observed:** found by reading, not by a run  -  see the status note below.
2-citation-network.txt line 988 instructs the model to write

```
INCOMPLETE RUN  -  REQUIRED SECTION OMITTED: [heading(s)].
```

with an ASCII hyphen. The file contains no em dash at any position. But
incomplete_run_declared() matched \bINCOMPLETE RUN\s+—\s+REQUIRED SECTION OMITTED\b, an
em dash. A model that followed the prompt EXACTLY therefore scored
INCOMPLETE_DECLARATION_MISSING, and, where Artifact 10 was also not withheld,
SILENT_OMISSION on top of it.

Why it went unseen: the branch only executes when a required block is missing. All three
compliance pilots passed with zero missing blocks, so the declaration path was never reached
in any logged run. The one scenario the completion gate exists for is the one scenario it
could not score correctly.

Why it matters more than an ordinary typo: it inverts the tool’s verdict on a
well-behaved run. A model that correctly detected its own omission and declared it as
instructed was scored identically to one that omitted silently  -  which is precisely the
distinction TOOL-001’s repair was built to preserve.

**Repair:** match any dash or none, with flexible surrounding whitespace, case-insensitive.
The separator carries no meaning; only the two phrases do.

**Regression condition:** the exact literal printed at 2-citation-network.txt:988, with its
placeholder filled, must satisfy incomplete_run_declared(). Em dash, en dash, colon and
no-separator variants must also satisfy it. Prose that merely contains the words
INCOMPLETE, RUN, REQUIRED SECTION and OMITTED in other arrangements must NOT.

**Case:** none committed. Verified at fix time by extracting the literal from the prompt and
asserting the old pattern rejected it and the new one accepts it, and by re-running the five
committed output fixtures  -  all still PASS.

**Status:** REPAIRED. Classed FAIL- rather than GUARD- because the defect is demonstrable
from the two files as they stood, not anticipated; but note it was found by inspection, so it
belongs to the small set of entries not sourced from a live run.

General principle this establishes: where a prompt mandates an exact string and a checker
matches it, the checker must be tested against the literal the prompt actually prints. Two
files agreeing in the author’s head is not agreement.

### TOOL-004 - Mutable remote artifact returned as an internally self-consistent stale version

**Class:** retrieval / instrument-provenance failure

**Status:** OBSERVED; REPAIR SPECIFIED; PROMPT GUARD ADDED; REGRESSION CASE NOT YET BUILT

**Observed:** A mutable GitHub URL for the canonical Coverage Network prompt was
supplied directly. Independent sessions reported successful retrieval of the
correct repository path and branch but received a historical representation of
the file rather than current `main`. The stale representation was internally
self-consistent: repository path, branch label, rendered line count, KB size,
line gutter, content, and GitHub-style metadata all agreed with one another.
Nothing inside the returned representation exposed that it was stale.

The stale prompt then produced behavior consistent with the historical
instrument. In a later review, a marker preflight correctly detected that
current expected modules were absent, but the mismatch was misattributed to the
repository itself rather than left unresolved. The reviewer asserted that
`main` contained the old prompt when the retrieval layer was the stale object.

**Instrument anchor at diagnosis time:**

- canonical path: `prompts/media-analysis/2-coverage-network.txt`
- branch: `main`
- pre-TOOL-004 prompt: 3,232 lines / 126,890 bytes
- Git blob SHA: `d5f3502fc3ab1af083c12be0a0b1440cbf2adf6f`
- marker present: `RC2 CONSOLIDATED CANDIDATE`
- marker present: `PROMINENCE AND PACKAGING [FAIL-MB-017]`
- marker present: `SEMANTIC EQUIVALENCE AND EARNEDNESS GATE [FAIL-MB-018]`

The live repository subsequently renamed the canonical file to
`prompts/media-analysis/2-network-coverage.txt`. At commit
`17fd1eca510a686b44970113552da55527515789`, the post-repair artifact is 3,340
lines / 131,417 bytes with Git blob SHA
`9380b619fd16b4212dabec28971f1c6a6b3d18b6`. This later identity does not rewrite
the diagnosis-time identity above.

**Failure mechanism:** Two distinct failures must remain separate.

1. **RETRIEVAL CURRENCY FAILURE.** A mutable remote reference can resolve to a
   stale historical representation while presenting internally coherent
   metadata for that stale snapshot. Successful retrieval and internal
   consistency therefore do not establish current repository state.
2. **VERSION-ATTRIBUTION FAILURE.** A failed identity preflight establishes only
   that the retrieved representation differs from the expected one. It does not
   establish which side is stale. In the observed review, detection worked but
   disposition failed: the mismatch was correctly detected and then incorrectly
   attributed to repository state from the same conflicting retrieval.

**Root cause:** Mutable remote identity was treated as if path + branch +
successful fetch + internally consistent metadata established currency. When a
version mismatch was detected, the same retrieval path was then used to infer
where the stale version lived.

**Repair:** Add an INSTRUMENT PREFLIGHT to formal/logged runs.

For a mutable remote prompt, record before substantive execution, where
available:

- canonical path / supplied filename;
- retrieval form;
- requested branch/ref;
- resolved commit SHA;
- blob/content hash or independently computed cryptographic hash;
- exact line count and byte count;
- discriminating version markers.

Mutable `main`, `master`, `latest`, or equivalent URLs are locators, not
immutable instrument identities. They remain acceptable for ordinary
exploratory work. Formal, logged, benchmark, regression, and fixture runs must
resolve an immutable identity before they count as evidence.

When expected identity and retrieved identity disagree, return exactly:

```
VERSION COLLISION — UNRESOLVED
```

Do not infer:

```
REPOSITORY STALE
RETRIEVAL STALE
LOCAL COPY STALE
OPERATOR COPY STALE
```

from the conflicting retrieval alone.

Attribution requires a SECOND, INDEPENDENT discriminator, such as an immutable
commit/blob lookup, repository history, a genuinely independent retrieval path,
operator-confirmed immutable identity, or an independently hashed local file.

Internal self-consistency is not an independent discriminator because a stale
snapshot can generate mutually consistent path, branch, size, line-count,
content, and rendered metadata.

**Governing rule:**

> A failed identity check proves a version mismatch, not where the mismatch lives.

**Formal-run disposition:**

- `IDENTITY CONFIRMED` -> proceed.
- `VERSION COLLISION — UNRESOLVED` -> stop before substantive execution; the run
  does not count as evidence for the instrument under test.
- No mismatch observed but immutable identity unavailable -> `INSTRUMENT VERSION
  UNVERIFIED`; exploratory use allowed, regression evidence disallowed.

**Required run-header form:**

```
INSTRUMENT PREFLIGHT: [path/file] @ commit [SHA/UNAVAILABLE] | blob/hash
[HASH/UNAVAILABLE] | [N] lines | [N] bytes | markers [017 PRESENT/ABSENT]
[018 PRESENT/ABSENT] | [IDENTITY CONFIRMED / INSTRUMENT VERSION UNVERIFIED /
VERSION COLLISION — UNRESOLVED]
```

**Regression condition:** A test with two versions of the same mutable artifact
must cause a mismatched retrieval to stop at `VERSION COLLISION — UNRESOLVED`.
The checker/model must not attribute the mismatch to repository state, retrieval
state, or a local copy until a second independent discriminator is supplied. The
fixture should include an internally self-consistent stale representation so
that ordinary within-result sanity checks all pass.

**Propagation:** This is a shared tooling rule, not a media-specific analytical
rule. The first execution copy is in Coverage Network because that is where the
failure was observed. Promote the rule to the common run launcher/router or
other shared execution layer when that layer exists; do not maintain divergent
hand-written copies indefinitely.

### TOOL-005  -  Prompt truncation via GitHub blob render was silent
*Filed as TOOL-005, not TOOL-003 as originally drafted. TOOL-003 was taken by the
completion-gate entry above, and TOOL-004 is already claimed by the instrument-preflight work
recorded in TODO.md and the shen run metadata, though no TOOL-004 entry has been written here
yet.*

**Observed:** the Claude run read `2-construct-validity.txt` through GitHub's blob view, which
truncated at ~line 1000 of 1092. The raw endpoint is robots-disallowed. The REMINDER block and
the canonical finding-table schema were lost. The truncation was noticed only because Section
17 ended mid-structure  -  i.e. by luck of where the cut landed.

**Why this matters:** a prompt executor can silently receive a partial prompt and produce a
complete-looking audit. Any section after the cut simply does not run, and nothing in the
output says so.

**Repair (proposed):** terminal sentinel line at the end of every prompt file (e.g.
`[END OF PROMPT  -  <filename>  -  <n> sections]`). An executor that does not see the sentinel
must declare the prompt incompletely retrieved and cap findings accordingly.

**Regression condition:** a truncated prompt produces an explicit incomplete-retrieval
declaration, not a silently partial audit.

**Case:** Gabarrell-Pascuet et al. 2024
(`tests/runs/reducing-loneliness/claude-construct.md`, toolkit note T1).

**Status:** proposed.


---

## GUARDS  -  anticipated rather than observed at time of writing

Weaker retention claim AT TIME OF WRITING. A GUARD that has never fired across many runs is
a legitimate deletion candidate.

Two have since fired on observed runs and are marked FAIL-class for deletion purposes. The
prefix records how a rule ORIGINATED, not its current standing  - renumbering them would
lose the fact that they were reasoned into existence before the failure was seen, which is
itself worth knowing.

### GUARD-001  -  No-assume-suppression

Low citation uptake has two explanations: the field marginalized valid work, or the field
correctly discounted work that did not survive scrutiny. Do not resolve toward suppression
without confirming the critique survived.

**Rationale:** anticipated; the toolkit’s operator has priors about suppression.

FIRED  -  observed on the large power-posing packet. Section H traced uptake across
failed replications, preregistered nulls, a p-curve dispute, a multiverse analysis,
ecological and hormonal nulls, and later methodological criticism  -  and concluded the
network was OPEN. The run preserved the distinction the rule exists to protect:

“the original finding weakened or failed”  =  “the citation network was closed”

This is the hardest case for the rule. Power posing is cartel-shaped on the surface: a
founding cluster, a same-author review assembling 33 experiments, and headline effects that
did not replicate. A naive cartel-detector finds all three and scores high. The run scored
6/30 and identified preregistered replication, engaged critique, and outcome-specific
meta-analysis as what a HEALTHY field looks like when a finding fails.

**Retention:** GUARD-001 has now demonstrated it changes an outcome on a case where the
wrong answer was readily available. Treat as FAIL-class for deletion purposes.

### GUARD-002  -  Empty-table / acquittal clause

“A prosecutor that never returns ‘nothing of consequence here’ is not measuring anything.”

**Rationale:** anticipated  -  an instrument that cannot decline to find is a template.

FIRED REPEATEDLY. A claim map returned GAP TYPE “neither apparent.” A counter-audit
returned no established downstream failure location. The large citation-network run returned
a healthy/low-risk classification on a literature whose headline finding had failed.

**Retention:** treat as FAIL-class.

STILL NOT CLOSED, though. No RESEARCH-BRANCH run has been scored against an expected
result written BEFORE the run. The power-posing oracle was drafted after the medium run was
observed and is therefore a regression oracle  -  it tests reproducibility, not correctness.
The acquittal gap remains open and needs either a synthetic case with the answer built in,
or a target whose expected result derives from the literature rather than from the toolkit’s
own output.

### GUARD-003  -  Symmetry requirements (flip test, direction-neutral rules)

Every construction check must fire identically regardless of political valence.
**Rationale:** anticipated  -  a one-directional instrument confirms its operator’s prior.
**Fired:** partially. The flip test caught nothing until made costly (FAIL-MB-001); whether
it catches anything now is untested.

### GUARD-004  -  “Nothing downstream corrects it” (counter-audit stage note)

Architecturally imprecise  -  the human adjudicator IS downstream. Retained because telling
the model the human can reopen the verdict licenses laziness. Rationale: anticipated.
**Fired:** unmeasurable by design. Deletion candidate on the next audit  -  it is the
clearest case of a rule kept on reasoning alone.

### GUARD-005  -  Self-generated priors could be systematically half-confirmable

**Rationale:** anticipated. The failure guarded against is a model writing a prior it can
safely half-confirm, looking calibrated while doing nothing. One run cannot distinguish a
genuine hypothesis from a self-serving one; a labeled series can.

**Repair:** PRIOR SOURCE field in Section E2 - SUPPLIED / MODEL-GENERATED / NONE;
MODEL-GENERATED full match declared WEAKER. Labeling, not prohibition.

Fired / working - observed repeatedly. In run-2, both models declared NONE and generated
no covert prior. On the fixed packet, DeepSeek and Grok declared NONE. Sol declared a
MODEL-GENERATED prior with six predictions and returned five MATCH plus one PARTIAL - a
near-total self-confirmation, correctly labeled. That is exactly the pattern the guard
exists to expose: the label worked, and the watched behavior appeared.

**Regression condition:** every prior-match check declares PRIOR SOURCE first;
MODEL-GENERATED matches are marked weaker; self-generated priors are tracked across runs for
systematic half-confirmation.

**Case:** none.

Open edge: the applied E2 rule weakens MODEL-GENERATED priors but does not bar one from
driving the automatic downgrade, and it does not distinguish a prior from standing knowledge
from one derived circularly from the audited coverage. Unresolved.

---

### GUARD-006  -  The scope-creep prosecutor can commit the mirror overclaim

Prosecuting scope creep requires the auditor to assert which penalized beliefs
are “accurate.” The corrected Donovan re-run lumped an established claim
(ancestry/allele-frequency medical relevance) with a contested one (group-average
cognitive genetics) under “consistent with population genetics” — the mirror
image of the paper’s own overclaim.

**Rationale:** observed-in-run (the corrected audit’s own lumping), not yet
adjudicated by the operator as a defect. Kept GUARD-class pending that call — if
confirmed a defect, upgrade to FAIL-class alongside CV-001/002.

Repair (proposed, not yet applied): grade-before-assert — grade the
penalized belief ESTABLISHED-FALSE / CONTESTED / ESTABLISHED-ACCURATE / FRINGE
before rating a pathologization finding; full severity only at the established
poles.

### GUARD-007  -  The causal-role map is the media branch’s most prior-abusable output

A blame/victim/cause map invites reading role assignments to confirm a prior
about a coverage set’s slant, more than any other media-branch output.

**Rationale:** anticipated during design of the causal-role axes (MEDIA-P1), not
observed misfiring in a run.

Guard: flip-test requirement naming the SPECIFIC assigning text (never “outlet
X is biased”); CHOSEN-only gate (inherited assignments are not attributed as
editorial choice); register-only exclusion (a verb that moves no axis is not a
finding).

### GUARD-008  -  Axis-vocabulary drift across branches makes cross-branch resolution entry-order-dependent

Before harmonization, the single-piece and coverage-network prompts used
different labels for the same causal-role concepts (e.g., coverage’s D2 asked
about CAUSE/AGENT/BLAME/VICTIM/REMEDY/LEADERSHIP while single-piece’s E2.1 spoke
a different vocabulary). A finding resolvable when coverage is the entry point
might not be when single-piece is, because the two sides emitted different axis
labels for the same object.

**Rationale:** caught by structural/architecture review (reading both prompt
files cold), not observed misfiring in a live run.

**Repair:** MEDIA-P1 — one shared six-axis vocabulary (event classification,
cause, role-and-status, blame, remedy, leadership) embedded verbatim in both
prompts’ compact copies.

---

## HOW TO ADD AN ENTRY

When a run exposes a failure:

1. Assign the next number in the relevant prefix.
2. Record what was OBSERVED  -  the actual output, quoted where possible. Not a summary of
the failure type.
3. Record the repair and the regression condition  -  what a passing run looks like.
4. Add the marker to the prompt.
5. Note whether a regression case exists. Most do not. That is the gap.

If the failure was anticipated rather than observed, use GUARD- and say so. The distinction
is the point: it determines what survives an architecture audit.
