# Provenance Philosophy

It points; you judge\.

> **Status:** Reconciled repository reference, 2026-08-09. Commitments are
> separated from demonstrated capacities; implementation state lives in the
> [current-state inventory](current-state-inventory.md). Uncommitted
> off-repository philosophy notes, if later supplied, remain a separate source to
> reconcile rather than an authority over this file.

## Status and purpose

This document states the commitments behind Provenance\. It explains what the
toolkit is trying to make visible, how responsibility is divided between the
operator, the model, retrieval, and the human adjudicator, and what the toolkit
must never claim to have established\.

It is not an execution manual\. The canonical prompt files govern what a run
does; the [methodology](methodology.md) describes how the stages connect\. When an
implementation conflicts with this philosophy, the conflict should be recorded
and resolved openly rather than hidden by documentation\.

## From a failure taxonomy to a provenance discipline

Provenance grew out of The Same Four Failures, but it changes the center of
gravity\.

The earlier project organized recurring failure shapes: a proxy becoming the
construct, analytical latitude disappearing from view, a qualified finding
hardening as it travels through citations, or an accurate set of facts producing
an unsupported impression through assembly\. Those shapes remain useful\. But a
tool built only around known failures can become a template that always finds
them\.

Provenance begins one step earlier\. It asks what claim is being
evaluated, where it came from, what was actually checked, how it changed as it
moved, and which layer is responsible for any gap\. The failure taxonomy is a set
of possibilities, not a predetermined verdict\. A run that finds no consequential
failure is a successful run if the instrument genuinely had the opportunity to
find one\.

That move was not only a design preference\. It was forced by runs in which the
instrument over\-fired, aimed at the wrong layer, or silently lost a capability
after a revision\. The provenance discipline is the correction history made
general: retrieve the object before judging it, keep the claim stable, preserve
what changed, and make the instrument’s own failures auditable\.

The project is not an AI truth machine\. It is an audit sequence for producing a
more inspectable object of human judgment\.

## It points; you judge

This is not modesty language\. It describes the division of labor\.

The sequence can direct retrieval, extract claims, compare measurements with
claims, trace source chains, classify recurring failure shapes, surface
counterevidence, and mark the limits of what was checked\. It can show a human
where attention is warranted\.

It cannot decide, on its own, whether a generic category is the actual mechanism
operating in an unfamiliar field\. It cannot know which practitioner observation
is representative, which omitted variable matters most, or how much weight a
contested finding deserves in the real world\. Fluent output does not remove those
limits\.

Human adjudication is therefore not a temporary gap awaiting automation\. It is
the point at which domain knowledge, responsibility, and judgment enter\. The
sequence should hand the human a contested set with its evidence and provenance
attached, not conceal the contest behind one automatic answer\.

## Begin with an anomaly, not a verdict

Most worthwhile audits do not begin from perfect neutrality\. They begin because
someone noticed a mismatch: a result that does not resemble the phenomenon, a
headline that seems to outrun its source, an official claim repeated as if
independently confirmed, or a field model that does not survive contact with
practice\.

Pretending that prior suspicion does not exist makes the audit less transparent,
not more objective\. Provenance permits operator hypotheses, construction\-derived
leads, and retrieval\-emergent questions, but preserves where each came from\.
Origin is provenance, not evidence\.

The governing rule is:

> Operator hypotheses influence retrieval, not conclusions. Retrieval influences
> conclusions.

Every material hypothesis must be capable of being confirmed, narrowed,
reframed, rejected, or left unresolved\. Retrieval should deliberately seek what
would weaken the hypothesis as well as what would support it\. An unperformed
search is not negative evidence, and a plausible prior does not lower the
verification threshold\.

You may begin with vibes\. You may not end with vibes\.

## Two priors require two different checks

Bias is not one object\.

The **operator’s prior** is visible through introspection and procedure\. It is
caught by disclosure, hypothesis\-origin labels, balanced retrieval, symmetry,
the flip test, and the concede test\. Its characteristic danger is reaching past
the source for the conclusion the operator came to find\.

The **field’s prior** is different\. From inside a literature it does not present
as a prior at all\. It presents as established knowledge: fluent, peer\-reviewed,
and densely cited\. It is caught only by retrieval—of the construct\-establishment
literature, actual scale items or coding rules, serious contrary evidence, and
the citation context doing the inferential work\.

A model auditing an insulated field is often most fluent in exactly the dialect
that needs interrogation\. Left to complete from ambient consensus, it can repeat
the field’s premise as if that repetition were an independent check\. “Cited”
therefore does not mean “uncontested in the respect the claim requires\.” A source
may license a bounded finding while the paper or field loads substantially more
onto it\.

The operator\-side remedy is resistance to yourself\. The field\-side remedy is to
fetch what the field treats as background and inspect whether the cited evidence
actually carries the required property, scope, and use\.

## Retrieval is part of the reasoning

Most confirmation bias enters before the final paragraph\. It enters through the
search terms, source boundaries, documents not opened, versions not checked, and
primary material never retrieved\.

For that reason, retrieval is not clerical preparation for the audit\. It is part
of the audit itself\.

The operator should disclose how the corpus was assembled\. The model should not
complete an inaccessible record from memory\. Closed fixtures remain closed; live
runs state their search and access boundaries\. Material that was supplied,
retrieved, recalled, or not found must remain distinguishable because each is
allowed to support a different level of conclusion\.

Repetition is also not automatically independence\. Ten publications can carry
one evidentiary origin\. Corroboration is assessed per load\-bearing fact by
counting independent origins, not logos\. Majority treatment is a distribution,
not a verdict about accuracy\.

## Trace the claim and preserve the layer

Claims change as they travel\.

A paper can measure one quantity and describe it carefully\. A later review can
drop the scope condition\. An institutional document can cite the review rather
than the paper\. Journalism can compress the institutional claim into a headline\.
An AI summary can then restate the headline as settled background\.

An audit that attacks whichever version is easiest may identify a real mismatch
and still assign it to the wrong actor\. Provenance therefore treats failure
location as load\-bearing\. A paper should not be blamed for an inflation that
began in a citation, press release, media restatement, or model reconstruction\.
Likewise, an explicit caveat in the source does not excuse every downstream use,
but it changes where the failure lives\.

The shared object must remain stable across stages\. Where several claims are
present, the selected claim is audited and the others are deferred rather than
silently dismissed or smuggled into scope\. When a prosecutor attacks a different
claim, the result is a map gap or scope error, not an opportunity to keep the
stronger accusation\.

## Adversarial does not mean accusatory

The toolkit is adversarial because every consequential inference should meet
resistance\. That resistance applies to the source, the operator, the model, and
the audit’s own preferred explanation\.

The target is the claim and the path supporting it\. Structure is observable;
motive usually is not\. Provenance is strongest when it evaluates measurements,
analytical choices, attribution, timing, source dependence, construction, and
institutional updating\. It is weakest when it converts those observations into
claims of fraud, corruption, ideological intent, or bad faith without separate
documentary evidence\.

Not every weak proxy is laundering\. Not every dense citation cluster is a
cartel\. Not every omission is selection\. Not every lexical difference is
framing\. Not every limitation defeats a paper, and not every rebuttal is correct\.
The relevant question is whether the confidence and use of a claim exceed what
the inspected evidence can support\.

## Symmetry is part of validity

An instrument that changes standards when the actors reverse is not auditing the
source\. It is operationalizing the auditor’s preference\.

Symmetry therefore has to be procedural, not ceremonial\. Supporting and opposing
sources face the same retrieval and reception checks\. Cause, blame, role, motive,
and ideology assignments face the same evidence floor\. A mirror or flip test must
be costly enough to change or kill a finding when the rule would not survive
reversal\.

The strongest alternative reading should be stated before a prior\-sensitive
finding is finalized\. Innocent explanations do not automatically acquit a
construction, but they have to be tested\. A timing artifact, common primary
source, professional convention, genre constraint, or later update may explain a
pattern that otherwise looks like editorial choice\.

Fairness is not produced by adding a reassuring paragraph after a one\-sided
analysis\. It is produced by applying the same burdens while the finding is still
being formed\.

## An audit must be able to acquit

An instrument that returns an indictment against every target is not measuring
anything, no matter how sophisticated its output appears\.

Provenance must be able to return:

- no consequential finding;
- a narrower claim that survives;
- a mixed result in which one claim fails and another holds;
- a reframed hypothesis whose supported mechanism differs from the original;
- a reclassified finding located downstream rather than in the source;
- an unresolved result because retrieval was insufficient; or
- a finding killed by a later stage\.

These are not reluctant concessions\. They are evidence that the sequence is
doing more than accumulating objections\.

Positive examples alone cannot establish this capacity\. Negative and mixed
controls matter, with expected results written before the run\. A clean result
means the checks performed did not fire\. It does not establish that nothing was
missed\.

**Current status:** the capacity is committed and partially demonstrated, not
fully validated\. Claim extraction has returned no gap, and a paired
citation\-network fixture correctly acquitted the healthy network\. No full
research chain has yet returned clean\. The deliberate Gabarrell\-Pascuet et al\.
loneliness audit found real construct\-side problems rather than acquitting\. The
media proportionate\-negative case is built but unrun\.

## Domain knowledge is load\-bearing and bounded

Domain experts often notice the anomaly first because they can see mechanisms a
general prompt cannot: the behavior hidden by a proxy, the real\-world constraint
absent from a laboratory design, the adjacent literature a field does not know to
search, or the distinction that makes two superficially similar cases different\.

That knowledge is indispensable, but it is not self\-validating\. Practitioner
experience generates sharper hypotheses and helps interpret the categories the
sequence surfaces\. It does not, by itself, establish prevalence, causation, or
generality\. The operator should state the observation precisely, ask what would
make it unrepresentative, and retrieve evidence capable of testing it\.

The prompts are scaffolds for turning domain knowledge into inspectable claims\.
They are not substitutes for the knowledge, and the knowledge is not a shortcut
around evidence\.

## Models are executors, not authorities

No model receives trust from fluency, scale, reputation, or a permanent role in
the workflow\. Capability profiles may make one model better suited to a long
network audit and another better suited to compression or adversarial review,
but those are empirical routing choices, not epistemic credentials\.

Record the model and version used\. Compare behavior across models when the cost
is justified\. Treat a single\-model pass as limited evidence and a reproducible
failure as a strong diagnostic lead\. A model disagreement is not resolved by
choosing the answer the operator prefers; it is an instruction to inspect the
underlying evidence or execution contract\.

Models can also fail while appearing compliant\. They can skip required sections,
invent authoritative\-sounding verification labels, silently widen a claim, or
reconstruct missing material from training memory\. A finished\-looking output is
not proof of a completed run\.

The same applies to the instrument delivered to the model\. A mutable remote path
is a locator, not proof of the prompt version in context\. When two instrument
identities conflict, the mismatch is evidence; which copy is stale remains
unresolved until an independent discriminator establishes it\. Formal evidence
therefore begins with an immutable instrument identity, not confidence in a
coherent\-looking retrieval\.

## Prompts are fallible instruments

Provenance treats prompts more like software than scripture\.

A rule can prevent one observed failure and create another\. A safeguard can be
sound in prose and fail to execute\. Repetition can improve compliance until it
consumes the reasoning budget needed for the analysis itself\. None of these
properties can be settled by reading the prompt alone\.

Changes should therefore begin with observed run behavior whenever possible\.
Expected results are written before regression runs\. Fixes record the failure
that justified them, the layer they changed, and the condition that would show
the repair worked\. Passes are logged as well as failures, because a safeguard
that never changes an outcome may be length without function\.

Rules are not preserved merely because they sound prudent, and they are not
deleted merely because a newer model might infer them\. Removal requires knowing
what failure the rule prevents, whether that failure was observed or anticipated,
where the protection moves, and what regression case will detect a recurrence\.

Project maturity is established by recorded runs, controls, and corrections, not
by confidence in the architecture\.

## The correction history is part of the method

The commitments above are not a tidied origin story\. They were learned through
specific failures:

|Observed correction                                                                                                                                             |What it forced                                                                                                                                         |
|----------------------------------------------------------------------------------------------------------------------------------------------------------------|-------------------------------------------------------------------------------------------------------------------------------------------------------|
|A newly active downstream-inflation field built a false attribution chain                                                                                       |Active retrieval had to be paired with source-to-source attribution checks and exact failure-location rules.                                           |
|A severe construct finding inferred a scale’s contents from its family name; retrieving the actual items defeated the finding                                   |Operationalization must be `ITEMS-RETRIEVED`, not merely plausible from remembered instrument descriptions.                                            |
|The same fixed Ceuta packet produced materially incompatible whole-coverage origin counts across models and conventions                                         |Whole-coverage counts became descriptive; proposition-level origins now carry independence judgments.                                                  |
|A later media prompt silently dropped a prominence finding that an older prompt had preserved                                                                   |Prompt revisions require cross-version regression protection, not only spot checks for model error.                                                    |
|A citation-network output looked complete while required sections were missing                                                                                  |Execution contracts and mechanical completion checks became part of the instrument.                                                                    |
|A mutable GitHub prompt URL returned a coherent historical snapshot, after which the detected mismatch was blamed on the repository without independent evidence|Formal runs now require an instrument preflight, and a version collision must remain unresolved until a second discriminator identifies the stale side.|

The revisions also expose the model’s role\. On the same claim, prompt, and fixed
packet, different models have produced incompatible verdicts because they
silently chose different scope or granularity conventions\. The repair is not to
anoint one model\. It is to make the convention explicit, retrieve the disputed
object, and protect the behavior with a case\.

Correction history is therefore evidence about the philosophy itself\. A
commitment with no run, control, or failure record remains aspirational\.

## No composite score and no automated final judge

The sequence produces disaggregated findings because different failures have
different evidence, locations, verification states, and surviving claims\. One
number would discard that structure and create authority the underlying audit
does not possess\.

Aggregation may summarize an adjudicated set, but it must preserve uncertainty,
scope, finding disposition, and provenance\. It may not turn several provisional
signals into one confident verdict\. The human adjudicator remains responsible for
deciding what survives and what should be published\.

Voice restoration follows the same rule\. It may remove ritual hedging, false
balance, and prose that apologizes for a warranted conclusion\. It may not remove
the language carrying genuine uncertainty\. Strip the scaffold; keep the flag\.

## Public receipts make correction possible

The aim is not merely reproducibility in the sense of obtaining identical model
prose\. The aim is inspectability\.

A serious audit should preserve enough of its path for another person to see:

- the target and claim under audit;
- the corpus and retrieval boundary;
- the prompt path and immutable version identity, plus the model used;
- the source material and verification state of load\-bearing claims;
- the raw stage outputs, including findings later killed or narrowed;
- the human adjudication; and
- the correction and revision history\.

Public receipts do not guarantee correctness\. They make disagreement specific
and correction possible\. A transparent audit can still be wrong; an opaque one
cannot be meaningfully checked\.

## Honest limits

Provenance surfaces categories, not guaranteed mechanisms\. It cannot tell the
operator what it failed to retrieve, what a domain expert would have noticed, or
whether an apparently clean result reflects a sound source or an insensitive
instrument without appropriate controls\.

Its outputs inherit the limits of source access, corpus selection, model
execution, prompt design, and operator judgment\. Some questions will remain
provisional\. Some stages will be inapplicable\. Some apparent findings will die
when primary material or counterevidence is retrieved\. The toolkit should expose
those outcomes rather than smooth them into a complete story\.

The promise is narrower and more useful: Provenance makes the path from evidence
to conclusion more visible, gives competing explanations structured resistance,
and preserves enough of the record for a human to judge the result\.

## Compact commitments

1. Start wherever the anomaly appears\.
2. Make the operator prior visible and retrieve against the field prior\.
3. Search against yourself\.
4. Retrieve it or mark it provisional\.
5. Count origins, not repetitions\.
6. Keep the claim stable and locate the failure at the correct layer\.
7. Preserve what survives the critique\.
8. Treat acquittal, narrowing, and uncertainty as valid outputs\.
9. Hand the contested set to a human; do not hide it in a score\.
10. Finish with receipts\.
