# FAILURES

Numbered registry of the failures each prompt rule exists to close.

**Primary function: deletion protection.** These prompts are long and will
eventually be audited for bloat â€” by a person or by a model doing a context pass.
Without a traceable reason, a rule that looks fussy gets cut, and the failure it
prevented returns silently. Every rule should carry a marker; every marker should
resolve here.

**Two prefixes, and the difference matters:**

- **FAIL-** â€” closes a failure OBSERVED IN A RUN. Strong claim to survive an audit.
Deleting one is a bet that a documented failure will not recur.
- **GUARD-** â€” anticipates a plausible failure, added by reasoning. Weaker claim.
A GUARD that has never fired across many runs is a legitimate deletion candidate.

**Marker format in prompts** â€” one line, no narrative:

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

*Update when adding entries.*

| Prefix | Total | Regression case exists | Never re-observed since fix |
|---|---|---|---|
| FAIL- | 13 | 4 | 13 |
| TOOL- | 2 | 1 (TOOL-002 open) | 1 |
| GUARD- | 4 | 1 | n/a |

Four regression cases now exist: case 11 (media acquittal, built), CE-006/007 (joint
citation, built), MIX-01 (mixed control, built), and the compliance fixture set (FAIL-
CN-001, run at three burden levels).

GUARD-001 and GUARD-002 have both fired on observed runs and should be treated as FAIL-
class for deletion purposes.

Remaining thin: entries 001â€“016 have no archived originating runs and are supported by
quoted excerpts alone. TOOL-002 is open.

---

## CE â€” Claim Extraction (`1-claim-extraction.txt`)

### FAIL-CE-001 â€” Three prosecutors audited three different claims
**Observed:** design review, then confirmed across early runs where construct,
internal, and citation audits attacked the paper, the design, and the media version
respectively. The combined critique read as a demolition of "the paper" when the
strongest findings concerned a press release.
**Repair:** shared Claim Map; Field 6 names one claim; all prosecutors target it.
**Regression condition:** every prosecutor finding declares the Field 6 claim as
its target, or flags MAP GAP.
**Case:** none.

### FAIL-CE-002 â€” Field 6 selected the vague claim and lost the finding
**Observed:** cold map v1 selected the abstract's unquantified version and bundled
in a second claim. The downstream audit returned the same generic verdict as two pre-
revision runs. A map selecting the quantified version found a specific defect in the
source's own method that no other run located. **The difference was Field 6, not the
prosecutor.**
**Repair:** RULE 1 (one claim only) + RULE 2 (prefer the most precisely quantified
version).
**Regression condition:** where a source states a claim at multiple precisions,
Field 6 targets the quantified one; no parenthetical second claim.
**Case:** none.

### FAIL-CE-003 â€” Recalled downstream material entered through a parenthetical
**Observed:** a run declared "no downstream uses supplied, PROVISIONAL," then
appended an unretrieved parenthetical noting the paper was "later widely restated in
secondary literature," offered "for completeness of the map only."
**Repair:** four provenance states (SUPPLIED / RETRIEVED / RECALLED / NONE FOUND);
RECALLED gets its own labeled line, never an aside.
**Regression condition:** no downstream item appears outside a labeled provenance
state.
**Case:** none.

### FAIL-CE-004 â€” Passive Field 4 could not detect inflation at all
**Observed:** Field 4 waited for user-supplied downstream material. A user pasting
a paper has none, so inflation analysis never ran.
**Repair:** Field 4 made ACTIVE â€” search for downstream restatements.
**Note:** this fix CREATED FAIL-CE-005. A passive empty field cannot be wrong.
**Regression condition:** Field 4 reports searches run, not "none supplied."
**Case:** none.

### FAIL-CE-005 â€” Active Field 4 built a misattributed inflation chain
**Observed:** the first active run recorded an assessment report's
"warmest decade of the millennium" as downstream inflation of a paper that terminates
six centuries back and calls millennial reconstruction future work. That claim rests on
a successor paper. The error would have propagated into Field 5 and every prosecutor. A
counter-audit caught it three stages later.
**Repair:** ATTRIBUTION CHECK â€” could the audited source alone support this?
Scope arithmetic. ATTRIBUTED ELSEWHERE. Same-author successors are different sources.
**Regression condition:** any restatement exceeding the source's measured scope is
traced to its actual support before being recorded as inflation.
**Case:** none.

### FAIL-CE-006 â€” The attribution check exonerated the clearest laundering
**Observed:** two runs reached opposite conclusions on the same restatement. One
reasoned that the claim rests on a successor and recorded ATTRIBUTED ELSEWHERE â€” no
inflation. The other retrieved the citing sentence and found the claim asserted with the
AUDITED paper cited for it. **The rule as written cleared the exact behavior the stage
exists to detect**, because it stopped at "who supports it" without asking "who is cited
for it."
**Repair:** MISATTRIBUTED branch. Two questions, not one.
**Regression condition:** every downstream item resolves to ATTRIBUTED ELSEWHERE
or MISATTRIBUTED via the citing sentence, not via the claim.
**Case:** none.

### FAIL-CE-007 â€” MISATTRIBUTED fired on a document that disambiguates elsewhere
**Observed:** a run classified an assessment report's joint citation as
MISATTRIBUTED on the sentence alone. A later run retrieved the same report's earlier
chapter, found it explicitly distinguished the two papers' scopes, and correctly
reclassified as synthesis attribution. **Sentence-level rule, false positive against a
careful document.**
**Repair:** joint citations require a DOCUMENT-LEVEL check before classification.
**Regression condition:** no joint citation is classified MISATTRIBUTED without a
stated search of the citing document for scope disambiguation.
**Case:** none.

### FAIL-CE-008 â€” RECALLED material anchored a failure location
**Observed:** a run correctly wrote that its downstream items were "labeled
RECALLED and do not anchor failure-location classification," then assigned CITATION /
PR-MEDIA as the "primary locus of inflation" on exactly that material.
**The rule was stated in Field 4 and violated in Field 5.**
**Repair:** ANCHORING RULE at Field 5 â€” only SUPPLIED/RETRIEVED may anchor;
otherwise SUSPECTED, not established.
**Regression condition:** Field 5 lists its anchoring items with provenance states
before assigning any location.
**Case:** none.

### FAIL-CE-009 â€” Models coined authoritative-sounding verification states
**Observed:** runs produced ESTABLISHED FROM SOURCE, RECONSTRUCTION FROM SOURCE,
and CROSS-SOURCE-CONFIRMED. Each reads as authoritative; none was defined; a downstream
stage cannot tell what was actually checked.
**Repair:** closed vocabulary + no-invented-states rule. CROSS-SOURCE-CONFIRMED
ADOPTED â€” attribution checking is a genuinely distinct verification act the ladder had
no state for. The others rejected as drift.
**Regression condition:** every verification state in output appears in the compact
vocabulary.
**Case:** none.
**Note:** one coined state was a real gap, two were drift. Worth distinguishing â€”
invented vocabulary sometimes signals a missing primitive.

### FAIL-CE-010 â€” An unquoted generalization was labeled RETRIEVED and anchored
**Observed:** a run recorded "frequent restatements of the form X, often citing Y"
as RETRIEVED â€” no quotation, no locator, no named source â€” then used it to anchor a
failure location. **The anchoring rule (FAIL-CE-008) keys off a self-assigned label;
mislabeling routes around it.**
**Repair:** VERIFY THE LABEL, DO NOT TRUST IT. Quotation AND locator required
before an item may anchor; otherwise RECALLED regardless of label. Pattern claims are
not retrieved items.
**Regression condition:** every anchoring item carries a verbatim quotation and a
locator.
**Case:** none. **This is the highest-priority regression case to build** â€” it is
the most recent failure and the only one where a fix routed around another fix.
**Status:** applied, UNTESTED.

---

## CA â€” Counter-Audit (`3-counter-audit.txt`)

### FAIL-CA-001 â€” A rebutted source was promoted to top threatening finding
**Observed:** a counter-audit elevated McShane & Wyner (2011) to its most
threatening finding without checking that the source was itself heavily rebutted in the
same journal issue. **The stage ran its defense pass on the paper and never on its own
witness.**
**Repair:** SOURCE-RECEPTION GATE. A source may not anchor a verdict until its own
reception is checked. Fires symmetrically on support and opposition.
**Regression condition:** every load-bearing source carries a reception state.
**Case:** none. **Verified firing** â€” later run recorded the same source CONTESTED
and capped.

### FAIL-CA-002 â€” Section E searched the literature and never the source
**Observed:** across SEVEN runs, no output engaged the paper's own pre-emptions â€”
a clause scoping the limitation the prosecutors quoted, and a reported sensitivity test
removing the proxy class they called dominant. Section E built the paper's case entirely
from external literature.
**Why it matters:** external support NARROWS a critique; internal pre-emption can
DEFEAT it. "They did not test it" and "their test was inadequate" are different charges
with different burdens.
**Repair:** Section E0 â€” search the source before the literature. Four targets,
four EFFECT values including DEFEATED.
**Regression condition:** E0 states which sections of the source were searched.
**Case:** none. **Verified firing** â€” found every pre-emption on first run,
produced 0 DEFEATED / 2 NARROWED / 4 RECHARACTERIZED / 0 UNAFFECTED, and moved the
impact category.

---

## MB â€” Media Branch

### FAIL-MB-001 â€” The flip test was theater
**Observed:** returned "would flag the mirror? Yes" on every finding across two
runs. Zero downgrades. Answering yes is free.
**Repair:** costly flip test â€” compose the mirror AS TEXT, audit your own mirror,
forced ranking, downgrade requirement.
**Regression condition:** a written mirror passage appears in output with findings
against it.
**Case:** none.

### FAIL-MB-002 â€” The consistency check induced a wrong downgrade
**Observed:** the check found that scene-first and justification-first orderings
both construct, and concluded the sequencing finding should be downgraded. **Wrong â€”
that ordering constructs in both directions makes the outlet's choice MORE meaningful,
not less.**
**Repair:** Type A (inconsistent principle â€” downgrade) vs. Type B (symmetric
phenomenon â€” NO downgrade) split.
**Regression condition:** no downgrade is issued for a Type B observation.
**Case:** none.

### FAIL-MB-003 â€” Coherence severity scaled with finding-splitting
**Observed:** one model split headline findings into two and reached 8
same-direction findings; two others reached 5 on the same article. The 8 drove a heavier
verdict. **Severity was a function of how finely findings were divided.**
**Repair:** count LEVERS, not findings. Nine named, capped at 9/9.
**Regression condition:** coherence ratio never exceeds the lever count.
**Case:** none.

### FAIL-MB-004 â€” The strip test removed fact-sources
**Observed:** two models split PARTLY SURVIVES vs. COLLAPSES on the same article,
entirely because one stripped a mixed paraphrase-plus-quoted-fragment construction and
the other kept it. **That single choice drove severity, aggregation, and the final
verdict.**
**Repair:** strip only FRAME-CARRIERS; keep FACT-SOURCES; explicit handling of
mixed constructions.
**Regression condition:** strip test output states what was removed and kept.
**Case:** none.

### FAIL-MB-005 â€” Discretionary downgrade never fired
**Observed:** five consecutive runs at zero downgrades. One run reproduced the
mandated sentence and then argued against it in a parenthetical. Another inverted it
("is functioning" for "may not be functioning"). **A check that can be argued away is
not a check.**
**Repair:** AUTOMATIC downgrade â€” mechanical, no justification path. If the
downgrade seems wrong, fix the ranking.
**Regression condition:** every run reports which finding was downgraded.
**Case:** none. **Status:** applied, UNTESTED.

### FAIL-MB-006 â€” D2 returned CONFIRMED with no evidence
**Observed:** on the same cross-branch question, one run returned CONFIRMED having
retrieved no primary source; another returned FALSIFIED citing a specific outlet; a
third returned STILL UNRESOLVED. **Only the second and third were defensible.**
**Repair:** D2 EVIDENCE FLOOR. CONFIRMED / FALSIFIED / RECLASSIFIED / NETWORK-WIDE
each require named evidence. CONFIRMED flagged as the most dangerous value â€” absence of
contradiction is not confirmation.
**Regression condition:** every D2 resolution names its evidence.
**Case:** none.

### FAIL-MB-007 â€” Network-wide uniformity was treated as exoneration
**Observed:** a rule stated that shared behavior across outlets should downgrade
the single-piece finding. **Wrong â€” uniformity establishes the outlet is not an OUTLIER;
it does not establish the treatment is proportionate.** Every outlet can inherit the
same wire framing or blind spot.
**Repair:** RECLASSIFY, do not downgrade. Downgrade the distinctiveness claim,
keep the construction finding, record the convention separately and name its source.
**Regression condition:** no substantive finding is downgraded solely for being
network-wide.
**Case:** none.

---

## CN â€” Citation Network execution (`2-citation-network.txt`)

### FAIL-CN-001 â€” Whole required sections vanished from the output
**Observed:** a live MBH98 run used the fully-blocked prompt and produced ZERO
hits for the claim-map receipt, verification states, and the standardized finding table
â€” while the concede test fired normally and the rest of the audit read as complete. The
instructions were present in the prompt. The sections were absent from the output, with
no acknowledgement.

**Why this is its own failure class:** every other entry in this registry is
"prompt correct, reasoning wrong." This is "prompt correct, output incomplete." A
section that is silently skipped is functionally nonexistent no matter how well written,
and it makes every repair to that section unverifiable. This class must be diagnosed
before substantive repairs to the same prompt can be trusted.

**Two candidate causes, distinguished by burden:** section salience lost in a long
prompt (a compliance defect, fixable by wording and placement) versus practical output
limits (a burden defect, fixable only by cutting or staging sections). These have
opposite repairs, which is why they had to be told apart before acting.

**Repair:** OUTPUT EXECUTION CONTRACT â€” exact-heading rule, required-heading list,
N/A rule, no-silent-merging rule, COMPLETION LEDGER, COMPLETION GATE withholding the
final verdict on any omission, plus an external checker (`check-citation-network-
output.py`) so compliance is mechanically verifiable rather than self-reported.

**Regression condition:** all 25 required headings appear as unique standalone
lines in the required order; the ledger's claims match actual presence in both
directions; the gate withholds the verdict on any omission; the checker exits 0.

**Case:** `compliance/citation-network-01` (compact), `-02` (medium),
`-03` (large: 26 sources, 70 edges).

**Status:** REPAIRED AND VALIDATED at three supplied-packet burden levels.
Sections A, F, H, and J â€” the ones originally vanishing â€” performed substantive work at
the largest level, including two real hub-removal tests.

**BURDEN HYPOTHESIS FALSIFIED.** The candidate cause "too much required output to
complete" did not survive. The precommitted response to a burden failure â€” cut, merge,
or stage sections rather than reinforce the gate â€” was never triggered and remains
recorded in TODO.md for any future failure.

**SCOPE OF THE VALIDATION â€” state this wherever the repair is cited.** All three
levels used SUPPLIED packets with no open-ended retrieval. What is validated is that the
contract holds when the network is handed to the model. It is NOT validated under
retrieval, where the model must find the network itself â€” a different burden involving
search, inclusion judgment, and a much larger candidate space. "Validated at three
burden levels" must not be read as "validated."

**DO NOT PROPAGATE THIS GATE WITHOUT AN OBSERVED OMISSION.** The contract is a
FAIL-class repair for one prompt. Adding it to prompts that have never omitted a section
imposes 25 required blocks and a ledger as a GUARD-class precaution â€” weaker
justification, permanent cost, and it inflates exactly the output burden that was the
leading alternative diagnosis. If another prompt starts skipping sections, the repair is
proven and ready.

---

## TOOL â€” Checking tooling

Failures in the tools that verify prompt output. Distinct from prompt failures: a broken
checker does not produce a wrong audit, it produces FALSE CONFIDENCE in an audit, which
is worse because it removes the signal that something is wrong.

### TOOL-001 â€” The checker's own design guaranteed a false pass
**Observed:** the first `check-citation-network-output.py` tested presence with
`heading not in text` â€” a substring search over the whole document. But the COMPLETION
LEDGER enumerates all 25 required headings in its own rows. Every heading therefore
appeared in every output that contained a ledger, and the checker returned PASS on files
where every actual section was missing.

Demonstrated on a synthetic file containing a ledger and no sections: old logic reported
0 missing.

**Why it matters more than an ordinary bug:** the checker validated that the LEDGER
existed rather than that the SECTIONS did â€” exactly inverted. The ledger is the CLAIM;
the sections are the FACT; the checker's entire purpose is testing the claim against the
fact. A tool that certifies its own input passes is worse than no tool, because the
compliance gate was built precisely because self-report could not be trusted.

**Repair:** headings must match at LINE START (markdown table rows begin with `|`
and therefore cannot satisfy the check), plus bidirectional ledger cross-verification
and distinct exit codes so a run that correctly withheld its verdict is not scored the
same as one that silently omitted sections.

**Regression condition:** a fixture containing only a ledger and no sections must
FAIL. A ledger claiming `completed` for an absent section must FAIL. A ledger claiming
`omitted` for a present section must FAIL.

**Case:** `compliance/checker-fixtures/` â€” `good.txt`,
`missing-but-ledger-says-complete.txt`, `present-but-ledger-says-omitted.txt`.

**Note:** two independent reviews found this defect and reached the same repair
from different directions. That convergence is the multi-model process working on the
tooling rather than on the prompts.

### TOOL-002 â€” The checker's regression fixtures omitted the original failure
**Observed:** the first fixture set contained three cases â€” a clean run, a ledger
falsely claiming completion, and a ledger falsely claiming omission. All three test
SELF-REPORTING failures.

None tested SILENT OMISSION: sections missing, gate NOT fired, verdict issued anyway, no
`INCOMPLETE RUN` declaration. That is the observed behavior in FAIL-CN-001 and the
entire reason the execution contract exists.

**Why this is a real failure and not a gap:** the fixture set verified that the
checker catches a run that lies about itself, and did not verify that it catches a run
that says nothing. The second is the documented case; the first is hypothetical.

**Repair:** add `missing-and-verdict-issued.txt` â€” Section B absent, ledger
reporting completed, Artifact 10 issuing a full substantive verdict with no
incompleteness declaration. Expected: flagged as silent omission, distinguished from a
well-behaved incomplete run.

**Regression condition:** the fixture set covers both self-reported and silent
omission. Also currently untested: duplicate headings (uniqueness is claimed but
unexercised), incorrect ordering (`ORDER_FAIL` never fires in any fixture), and an
entirely absent ledger.

**Status:** OPEN unless the fixture has since been added.

**General principle this establishes:** a regression suite for a checking tool must
include the failure the tool was built to catch. Testing only the failures that occurred
to the fixture author tests the author's imagination, not the tool.

---

## GUARDS â€” anticipated rather than observed at time of writing

Weaker retention claim AT TIME OF WRITING. A GUARD that has never fired across many runs
is a legitimate deletion candidate.

Two have since fired on observed runs and are marked FAIL-class for deletion purposes.
The prefix records how a rule ORIGINATED, not its current standing â€” renumbering them
would lose the fact that they were reasoned into existence before the failure was seen,
which is itself worth knowing.

### GUARD-001 â€” No-assume-suppression
Low citation uptake has two explanations: the field marginalized valid work, or the
field correctly discounted work that did not survive scrutiny. Do not resolve toward
suppression without confirming the critique survived.

**Rationale:** anticipated; the toolkit's operator has priors about suppression.

**FIRED â€” observed on the large power-posing packet.** Section H traced uptake
across failed replications, preregistered nulls, a p-curve dispute, a multiverse
analysis, ecological and hormonal nulls, and later methodological criticism â€” and
concluded the network was OPEN. The run preserved the distinction the rule exists to
protect:

"the original finding weakened or failed"  â‰   "the citation network was closed"

This is the hardest case for the rule. Power posing is cartel-shaped on the surface: a
founding cluster, a same-author review assembling 33 experiments, and headline effects
that did not replicate. A naive cartel-detector finds all three and scores high. The run
scored 6/30 and identified preregistered replication, engaged critique, and outcome-
specific meta-analysis as what a HEALTHY field looks like when a finding fails.

**Retention:** GUARD-001 has now demonstrated it changes an outcome on a case
where the wrong answer was readily available. Treat as FAIL-class for deletion purposes.

### GUARD-002 â€” Empty-table / acquittal clause
"A prosecutor that never returns 'nothing of consequence here' is not measuring
anything."

**Rationale:** anticipated â€” an instrument that cannot decline to find is a
template.

**FIRED REPEATEDLY.** A claim map returned GAP TYPE "neither apparent." A
counter-audit returned no established downstream failure location. The large citation-
network run returned a healthy/low-risk classification on a literature whose headline
finding had failed.

**Retention:** treat as FAIL-class.

**STILL NOT CLOSED, though.** No RESEARCH-BRANCH run has been scored against an
expected result written BEFORE the run. The power-posing oracle was drafted after the
medium run was observed and is therefore a regression oracle â€” it tests reproducibility,
not correctness. The acquittal gap remains open and needs either a synthetic case with
the answer built in, or a target whose expected result derives from the literature
rather than from the toolkit's own output.

### GUARD-003 â€” Symmetry requirements (flip test, direction-neutral rules)
Every construction check must fire identically regardless of political valence.
**Rationale:** anticipated â€” a one-directional instrument confirms its operator's
prior.
**Fired:** partially. The flip test caught nothing until made costly (FAIL-MB-001);
whether it catches anything now is untested.

### GUARD-004 â€” "Nothing downstream corrects it" (counter-audit stage note)
Architecturally imprecise â€” the human adjudicator IS downstream. Retained because
telling the model the human can reopen the verdict licenses laziness.
**Rationale:** anticipated.
**Fired:** unmeasurable by design. **Deletion candidate on the next audit** â€” it
is the clearest case of a rule kept on reasoning alone.

---

## HOW TO ADD AN ENTRY

When a run exposes a failure:

1. Assign the next number in the relevant prefix.
2. Record what was OBSERVED â€” the actual output, quoted where possible. Not a
summary of the failure type.
3. Record the repair and the regression condition â€” what a passing run looks like.
4. Add the marker to the prompt.
5. Note whether a regression case exists. Most do not. That is the gap.

If the failure was anticipated rather than observed, use GUARD- and say so. The
distinction is the point: it determines what survives an architecture audit.
