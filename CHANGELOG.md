# PROVENANCE — CHANGELOG

Why each rule exists: the failure it closes, and how that failure was found\.

This is NOT a diff log\. Git has the diffs\. This records the REASON, because six
months out “MISATTRIBUTED added because the rule as written exonerated the central
case, caught when two models disagreed” is worth more than a line\-level change\.

FORMAT:
&#91;date&#93; FILE — change\. Prompted by: &#91;live run / review / reasoning&#93;\. Tested: y/n

The “prompted by” field is the important one\. Across this build, every fix that
mattered came from a live run, not from reading a prompt\. Zero exceptions\. Keep
recording it so that stays checkable\.

Related: TODO\.md \(what is pending\), tests/RESULTS\.md \(what runs actually did\)\.

## Tooling

&#91;2026\-08\-09&#93; prompts/research\-analysis/check\-citation\-network\-output\.py —
the completion\-gate declaration check required an em dash; the prompt that
tells the model what to write mandates an ASCII hyphen, and contains no em
dash anywhere\. A run that followed the prompt exactly was scored
INCOMPLETE\_DECLARATION\_MISSING, and SILENT\_OMISSION where Artifact 10 was
also not withheld\. Now matches any dash or none, case\-insensitively\.
Prompted by: reading the two files against each other, NOT a live run — the
branch only fires when a required block is missing, and all three compliance
pilots passed with zero missing blocks, so it had never executed\.
Tested: y — extracted the literal from 2\-citation\-network\.txt:988 and
asserted the old pattern rejects it and the new one accepts it; re\-ran the
five committed output fixtures, all still PASS\. No committed regression case\.
See FAILURES\.md TOOL\-003\.

&#91;2026\-08\-09&#93; reference/shared\-primitives\.txt — added the SUPERSEDED banner
TODO\.md had been asking for\. While applying it: the file is not a primitives
document at all, it is a stale reflowed copy of 1\-claim\-extraction\.txt, and
the `References: shared_primitives.txt Section 1/2/3` line carried by six
prompts is dangling — those sections exist nowhere\. Banner records both\.
The six prompt\-side reference lines are NOT changed here; that edits live
prompts and should be run\-tested\.
Prompted by: review\. Tested: n/a — documentation only, nothing executes it\.

## Academic Branch

MBH98 PILOT — first end\-to\-end run of the revised construct\-validity prompt\.
THREE\-WAY RESULT:
generic \(pre\-revision\) ……… verdict C, skill\-degradation critique
domain\-tailored \(pre\-revision\) \. verdict C, same critique \+ PSM/uncertainty/
convergent\-validity/reproducibility sections
revised \+ HAND\-WRITTEN map …\.\. verdict E, found pointwise\-vs\-simultaneous
inference defect \(99\.7% claim computed from
pointwise Gaussian residuals but asserted
over the maximum of a 590\-yr correlated
series\)\. Grounded in NRC\. None of the other
runs found it\.
revised \+ COLD map \(Stage 1\) … verdict C\. Did NOT find it\. Field 6 selected
the abstract’s unquantified claim and bundled
in the forcing\-attribution claim\.
ATTRIBUTION: the E verdict came from the MAP, not the prosecutor\. Confirmed by
running Stage 1 cold — same prompt, same paper, different field 6, verdict
reverts to C\.
WHAT STAGE 1 DID DELIVER COLD: kept the audit on the source rather than the
controversy \(no centering dispute, no bristlecones, no McIntyre\-McKitrick, no
Wegman — all of which dominated both pre\-revision runs\); correctly marked
field 4 PROVISIONAL and returned “citation use cannot be assessed” rather than
asserting downstream inflation as both earlier runs did\. Rule 4 working\.
UNTESTED: the MBH99 boundary\. No downstream material supplied, so field 4 was
empty and the trap never fired\.
STILL ABSENT COLD: the “largest\-scale quantities are still skilfully resolved”
clause; the paper’s own dendro robustness test\. Same gaps as the generic run\.
FIX APPLIED: 1\-claim\-extraction\.txt field 6 — RULE 1 one claim only \(no
bundling, no parenthetical second claim\); RULE 2 prefer the most precisely
quantified version where a source states its claim at multiple levels of
precision\. Prompted by: LIVE RUN\. Tested: n
ALSO NOTED: the user did NOT populate the domain\-expert\-concern field in the
two pre\-revision runs — the model generated it from its own knowledge of MBH98\.
Implication for Tool 2: field context adds least where the paper is famous
enough that background knowledge supplies the controversy, most where it is
obscure\. Marcott 2013 is the better test\.
counter\-audit v2 — source\-reception gate, symmetric scoring, no\-assume\-
suppression, one\-level termination, self\-tilt disclosure\.
Prompted by: live MBH98 run elevating McShane & Wyner without checking its
reception\. Tested: partially \(memory\-mode run\)\.
citation\_reception\_module\.py — OpenAlex \+ Semantic Scholar reception profiles\.
Later: verification\-state field emitted mechanically\.
Prompted by: reasoning \(grounding gap\)\. Tested: branch logic only, offline\.
field diagnostic v2 — model routing dropped, Stage\-0 framing, numbering\.
Prompted by: review \+ user call\. Tested: n
shared primitives, claim extraction, prosecutor blocks, counter\-audit v3,
concede test — Prompted by: multi\-model review \+ reasoning\. Tested: n

COUNTER\-AUDIT RUN \(MBH98, v3 chain: cold map \-\> construct \-\> citation \-\> counter\)\.
WHAT WORKED: G2 fired and softened overclaim wording \(“fatal”/“invalid” \-\>
“not demonstrated as an unconditional probability”\); thesis impact B
\(narrowed\) not overturned; Section E built 7 external supporting sources with
verification states; honestly reported that no support source answers the
central construct problem\. Produced the cleanest statement of the defect in
any run: source supports \(a\) the observations clear the selected
reconstruction’s 3\-sigma envelope, does not demonstrate \(b\) that all relevant
uncertainties are included and the chance no earlier year was warmer is \~99\.7%\.
THE HOLE: Section E searched the LITERATURE, not the SOURCE\. Zero hits across
SEVEN runs for the paper’s own pre\-emptions — the clause scoping the
“marginal usefulness” limitation to spatial reconstruction, and the reported
sensitivity test withholding all dendroclimatic indicators\.
WHY IT MATTERS: external support NARROWS a critique; internal pre\-emption can
DEFEAT a finding\. “They did not test it” vs\. “their test was inadequate” are
different charges with different burdens\.
SCOPE OF DAMAGE ON THIS RUN: none — the load\-bearing finding is one MBH98 does
not pre\-empt\. Where it DID cost: both pre\-revision runs made dendro dominance
central AND missed the paper’s own dendro\-withholding test\. That is the failure
mode — publishing a critique the source already answered\.
FIX APPLIED: counter\_audit\_v3\_insertions\.txt Block 4 — new Section E0, runs
BEFORE the external support table\. Four things to search for \(scope qualifiers,
sensitivity tests, stated assumptions, acknowledged limitations\), four EFFECT
values \(DEFEATED / NARROWED / RECHARACTERIZED / UNAFFECTED\), “NONE FOUND
requires a stated search,” and a rule that a finding whose substance the source
tested may not be rated severe without engaging that test\.
Prompted by: LIVE RUN x7\. Tested: n

E0 VALIDATION RUN \(MBH98, v3\.1 fresh\) — FIRST CLEAN FULL\-CHAIN RUN\.
Chain: cold map \(field\-6 rules\) \-\> construct \-\> citation\-network \-\> counter\-audit
with Block 4 / Section E0 applied\.

```
E0 FIRED AND FOUND EVERY PRE-EMPTION SEVEN PRIOR RUNS MISSED:
  - the "largest-scale quantities remain skillful" clause scoping the
    marginal-usefulness limitation to SPATIAL reconstruction (finding 4)
  - the reported proxy-removal tests including dendroclimatic records (finding 5)
  - the "it appears" hedge on the 99.7% sentence (finding 1)
  - the explicit "1997 ... not shown" disclosure (finding 6)
  - the residual-Gaussianity / whiteness diagnostics (finding 2)
  - the seasonality acknowledgment and stated rationale (finding 3)
Listed the eight sections searched, per rule (a).

RESIDUAL COUNT: 0 DEFEATED / 2 NARROWED / 4 RECHARACTERIZED / 0 UNAFFECTED.
Neither failure mode. Did not clear anything outright; did not return
all-UNAFFECTED.

RECHARACTERIZED carried the most weight — the value added specifically for
this. Example (finding 2): "This was not undisclosed. The correct charge is:
MBH98 explicitly defined and tested a residual-variance uncertainty model, but
then used language broad enough to sound comprehensive without propagating
structural, proxy-selection, parameter, and model-choice uncertainty."

PRECISION TEST PASSED (finding 5): credited MBH98 for testing
eigenvector-selection sensitivity and proxy-class removal, while noting "they
did not identify the later centering-specific bias." Correctly separated what
the paper tested from what it did not.

E0 PRODUCED A BETTER PROSECUTION THAN IT RECEIVED:
  "MBH98 anticipated and partially tested the main proxy and validation
   problems, but its tests were not targeted to the exact joint annual-maximum
   probability implied by its 99.7% language."

TRACEABLE EFFECT ON VERDICT: impact category moved B (narrowed) -> C
(softened), with the reason stated: "E0 changes the character of four major
findings and narrows two more. This is more than a small precision
adjustment." E0 is not a section that only adds volume.

RECEPTION GATE ALSO FIRED: McShane & Wyner recorded CONTESTED and "capped as
contested" — the exact source whose unchecked promotion in an early run
motivated the gate in the first place.

STATUS: Block 4 / E0 TESTED = y.
```

FIELD 4 MADE ACTIVE \(1\-claim\-extraction\.txt\)\.
PROBLEM: field 4 waited for the user to supply downstream material\. A user
pasting a paper does not have the assessment report or the press release\.
Worse, a live run declared “no downstream uses supplied, PROVISIONAL” and then
added an unretrieved parenthetical noting the paper was “later widely restated
in secondary literature” — RECALLED material entering the map through a side
door where downstream stages read it as context\.
FIX 1: field 4 is now ACTIVE — search for downstream use\. Four provenance
states: SUPPLIED / RETRIEVED / RECALLED / NONE FOUND\. RECALLED gets its own
labeled line, never a parenthetical, and may not anchor field 5\. Inputs section
now says the user is not expected to supply this\. Rule 4 reconciled\.
RESULT: field 4 went active, parenthetical failure gone, layers labeled,
mutation named\.
BUT — MAKING IT ACTIVE MADE IT ACTIVELY WRONG\. The run recorded an assessment
report’s “warmest decade of the millennium” as a downstream restatement of a
paper that terminates six centuries back and explicitly calls millennial
reconstruction future work\. That statement rests on a SUCCESSOR paper\. The map
built a misattributed inflation chain; the error would have propagated into
field 5’s failure\-location classification and every prosecutor after it\. The
counter\-audit caught it three stages later\.
FIX 2: ATTRIBUTION CHECK on every downstream item — could the audited source,
on its own, support this restatement? If it requires a successor paper,
extension, or pooled analysis, record ATTRIBUTED ELSEWHERE, not inflation\. Test
is SCOPE ARITHMETIC: compare what the restatement asserts against what the
source measured — longer period, broader population, finer resolution means
something else is carrying it\. Plus: SAME\-AUTHOR SUCCESSORS ARE STILL DIFFERENT
SOURCES, the most common form of this error\.
FIX 3: provenance\-state discipline\. RETRIEVED requires an actual quotation and
locator — “or closely equivalent phrasings” is not a quotation, that is
RECALLED\. NONE FOUND means searched\-and\-absent, not a completeness caveat\.
Both were misused in the same run\.
Prompted by: LIVE RUN\. Tested: n
NOTE: this is the clearest instance yet of a fix creating a new failure mode\.
Passive field 4 could not be wrong because it was empty\. Worth watching for
elsewhere\.

## Media Branch

&#91;2026\-08\-09&#93; prompts/media\-analysis/2\-coverage\-network\.txt —
whole\-coverage Level 1 / Level 2 source counts and pieces / Level 2 are now
descriptive only; amplification/corroboration is determined proposition by
proposition using per\-fact origin counts, origin completeness, proposition\-
specific source authority, contestability, attribution behavior, and
apparent\-corroboration risk\. This closes the dangerous inference path in
FAIL\-MB\-008/009 without pretending the Level\-2 count itself became
reproducible\.
Prompted by: LIVE CEUTA RUNS on identical input — whole\-coverage Level\-2
counts and ratios changed solely with counting convention and inverted the
source\-independence verdict\.
Tested: y — integrated RC2 Ceuta rerun preserved proposition\-level
classifications while Level 2 again landed around 25\. FAIL\-MB\-008 remains
DEFUSED, NOT CLOSED; FAIL\-MB\-009 repair exercised\.

&#91;2026\-08\-09&#93; prompts/media\-analysis/2\-coverage\-network\.txt \+
prompts/media\-analysis/2\-framing\-construction\.txt —
consolidated event classification / causal\-role analysis into shared
MEDIA\-P1 ownership: event classification, cause, role/status, blame,
remedy, and leadership/policy, with epistemic states where relevant\. D8 is
subordinate to the shared path rather than independently deciding whether a
frame\-carrying formulation is “synonym only\.”
Prompted by: LIVE CEUTA FIXTURE DIVERGENCE — DeepSeek/Grok and Sol routed
the same wording object differently — followed by cross\-prompt harmonization
review\.
Tested: y for shared\-path execution\. Later FAIL\-MB\-018 now sits upstream and
determines whether wording\-derived material enters MEDIA\-P1 at all; this
narrows FAIL\-MB\-010’s old disposition without erasing its observed failure\.

&#91;2026\-08\-09&#93; prompts/media\-analysis/2\-coverage\-network\.txt —
added PROMINENCE\-PACKAGING as a finding type separate from cross\-piece
SELECTION\. Added FULL\-TEXT evidence floor, packaging provenance
CHOSEN/INHERITED/MIXED/UNKNOWN, FULL/PARTIAL/NONE packet inverse,
fact\-timing/version innocent explanation, D2 branch ownership, and explicit
source\-chain / D\-ROLE type ownership\.
Prompted by: REGRESSION DIFF / LIVE\-RUN ARCHAEOLOGY — CN\_677 contained a
valid gross\-scale vs aftermath prominence finding that Revised and RC2
silently lost even though both still developed the constituent evidence\.
See FAIL\-MB\-017\.
Tested: y — integrated Ceuta rerun restored a MODERATE
`prominence-packaging` finding, with PACKET INVERSE FULL and cross\-piece
availability NOT APPLICABLE\.

&#91;2026\-08\-09&#93; prompts/media\-analysis/2\-coverage\-network\.txt —
added the SEMANTIC EQUIVALENCE AND EARNEDNESS GATE before all analysis
triggered by lexical/formulation variance\. Added same\-stage/referent
comparability, explicit decomposition of added semantic predicates,
NON\-CIRCULAR support for earned specificity, register\-variance stop,
material\-outlier requirement, and outlet\-permutation/valence symmetry\.
VERB\-AS\-TRACE is canonicalized and applies only to surviving wording\-derived
outliers; D\-ROLE’s independent substantive scan remains intact\.
Prompted by: REPEATED LIVE/FIXTURE BEHAVIOR — CN\_677, Revised, and RC2 all
regenerated substantially the same low\-severity `pour / breach / cross / enter` object despite growing downstream machinery — then adversarial review
exposed circular earnedness and over\-broad jurisdiction\. See FAIL\-MB\-018\.
Tested: y — integrated Ceuta rerun removed the wording\-only standardized
finding, reduced full language\-package expansions from 3 to 2, preserved
independent cause/blame analysis, and PASSed the 017\+018 interaction check\.

```
SIDE EFFECT OBSERVED: FAIL-MB-005's mandatory automatic downgrade had
previously landed on the event-language finding. Once FAIL-MB-018 removed
that finding before forced ranking, the downgrade moved to France 24
blame-routing, changing that finding MODERATE -> MINOR. This is a mechanical
cross-rule interaction, not discretionary severity drift and not a new fix.
```

&#91;2026\-08\-09&#93; tests/cases/ — added two self\-contained media regression cases
containing the exact original eight\-piece synthetic Ceuta packet verbatim:
`ceuta-prominence-regression` \(FAIL\-MB\-017\) and
`ceuta-semantic-equivalence` \(FAIL\-MB\-018\)\. The former protects the restored
prominence object; the latter protects the semantic\-entry procedure rather
than answer\-coding whether any particular word must be bucketed\. Both state
localized failure meanings\.
Prompted by: FAIL\-MB\-017/018 regression closure and the suite rule that a
durable case must preserve its actual test material\.
Tested: y — the integrated 2026\-08\-09 rerun passes both case invariants and
the joint interaction check\. General capability remains unproven; these are
fixed regression objects\.

MAINTENANCE NOTE — NOT A PROMPT CHANGE:

```
Runtime benchmarking changed the optimization rationale. Do not record
future null suppression, conditional gating, or cardinality reduction as
"speed fixes" merely because they shorten the prompt. Current evidence
supports this order:

  validity repairs / reruns
  -> interaction check
  -> canonicalize genuine duplicate rules
  -> null-output suppression for readability
  -> objective conditional execution gates
  -> re-measure D-ROLE burden
  -> cardinality reduction only if still warranted
  -> substantive deletion last, after prompt archaeology and
     original-fixture regression testing.

The objective is now lowest drift + clearest output + least unnecessary
execution while preserving protections earned from observed failures.
```

REPOSITORY SYNC NOTE:

```
These entries describe the integrated RC2 artifact used for the tested
reruns. The supplied integration diff is based on
`2-coverage-network_RC2_consolidated_candidate.txt`, not the shorter
canonical repository prompt. Canonical prompt synchronization remains
pending and must not be performed as a blind patch.
```

framing\_construction\_audit\_media\.txt created\.
Prompted by: user’s framing analysis of a police\-shooting article\. Tested: y

- timing test, flip test\. Prompted by: reasoning\. Tested: y
- genre gate, version tracking, availability matrix, severity caps\.
  Prompted by: review\. Tested: y
  flip test made costly \(write the mirror as text, audit your own mirror\)\.
  Prompted by: LIVE RUN — flip test returned zero downgrades, was performing
  the check not doing it\. Tested: y
- Section F2 quote function / frame laundering\.
  Prompted by: user observation that quotes were carrying the frame\. Tested: y
- F2 Step 5 source\-internal selection, then the professional\-norm cap\.
  Prompted by: user observation, then reasoning about crisis\-comms doctrine\.
  Tested: y — and the cap killed the finding on a later run, correctly\.
- H\.6 contested\-predicate ratification\.
  Prompted by: user observation about the Tony Robinson reference\. Tested: y
  strip test corrected to remove frame\-carriers only, not all quotes\.
  Prompted by: LIVE RUN — two models split PARTLY SURVIVES vs COLLAPSES on a
  mixed paraphrase\-plus\-quoted\-fragment construction\. Tested: y
  Step 3 consistency check split into Type A / Type B\.
  Prompted by: LIVE RUN — a symmetric phenomenon was misclassified as an
  inconsistent principle and induced a bad downgrade\. Tested: y
  coherence counts LEVERS not findings\.
  Prompted by: LIVE RUN — one model split headline findings and reached 8,
  driving a heavier verdict than two models at 5\. Tested: y
  mirror\-function rule \(mirror the function, not the content\)\.
  Prompted by: LIVE RUN — a mirror flipped what a prior subject did rather than
  what the prior case proved\. Tested: n
  narrative flags / causal bridges / atmospheric cues module, then generalized
  beyond crime, then 12 corrections from review, then merged into both prompts\.
  Prompted by: user observation \+ review\. Tested: y \(post\-merge run\)
  coverage\_network\_source\_chain\_audit\.txt created; \+ D2 cross\-branch resolution\.
  Prompted by: reasoning — the branches weren’t talking\. Tested: y, and D2
  falsified two upstream findings on first use\.
  automatic downgrade replaces discretionary\.
  Prompted by: LIVE RUNS — five consecutive runs at zero downgrades, with the
  model reproducing the mandated sentence then arguing against it\. Tested: n
  D2 evidence floor; retrieval\-depth disclosure\.
  Prompted by: LIVE RUNS — one model returned CONFIRMED with no primary source
  while another returned FALSIFIED with one\. Tested: n

WHAT THE LIVE RUNS ACTUALLY CHANGED — worth noting, since it is the argument for
running before building:

- flip test was theater until a run proved it
- strip test was ambiguous until two models split on it
- consistency check induced a wrong downgrade until a run showed it
- coherence counting was gameable until runs diverged on it
- the verb finding died as document dependence
- the source\-ordering finding was falsified outright
- the Taser finding hardened across eight outlets
  None of that was reachable by reasoning about the prompts\.
