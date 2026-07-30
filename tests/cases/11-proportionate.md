# Case 11 — Proportionate Article, Clean Result

**Target prompt:** `prompts/media-analysis/2-framing-construction.txt`
**Tests:** whether the instrument can return no consequential finding.

---

## WHY THIS CASE EXISTS

Every other regression case tests whether the audit DETECTS something. This one
tests whether it can DECLINE to.

The prompt contains a mandatory clause: *"if you produced no findings of
consequence, say so and submit an empty table. A construction audit that never
returns 'this piece is constructed proportionately' is not measuring anything —
it is a template."*

That output has never been produced. Across seven runs and four models, on one
article, every run returned findings. That is consistent with the article being
constructed — but it is also consistent with the instrument being unable to
acquit. This case distinguishes them.

**If this case fails, the other ten are testing a machine that cannot say no,
and their passes mean less than they appear to.**

---

## THE ARTICLE

Synthetic. Constructed so that each construction lever is either neutral or
proportionate to the reported facts. Not a bland article — it reports a
contested event with a death, protest, and an official account. The point is
that a piece can cover charged material proportionately.

---

> **Council rejects zoning change after five-hour hearing**
>
> *Riverside Gazette — March 4, 2026, 11:40 p.m. Updated March 5, 8:15 a.m. to
> add the final vote tally.*
>
> The Riverside City Council voted 4–3 Tuesday night to reject a rezoning
> request that would have allowed a 60-unit apartment building on Fulton Street,
> ending a hearing that ran past 11 p.m. and drew about 90 residents.
>
> The developer, Cassner Properties, had sought to change the parcel from
> single-family to medium-density residential. Company representative Dana Oyelaran
> told the council the project would include nine units priced below market rate
> and said the firm had reduced the building from 84 units after neighborhood
> meetings in January.
>
> Twenty-two residents spoke. Fourteen opposed the change, seven supported it,
> and one asked questions without stating a position. Opponents raised traffic on
> Fulton Street, which city figures show carries about 4,200 vehicles daily, and
> the loss of mature trees on the lot. Supporters cited a city housing study
> released in November that found Riverside added 310 housing units between 2020
> and 2025 while adding roughly 2,400 residents.
>
> "We are not going to zone our way out of this by putting sixty units on a
> street built for a fraction of that," said Councilmember Ruth Pinsky, who voted
> no.
>
> Councilmember Andre Loomis, who voted yes, said the council had rejected four of
> the last six multifamily proposals. "At some point the pattern is the policy,"
> he said.
>
> City planning staff had recommended approval, citing the parcel's proximity to
> two bus lines. Planning Director Marcus Hale said the department's analysis
> assumed a traffic mitigation agreement that Cassner had offered but the council
> did not vote on separately.
>
> Cassner Properties did not say whether it would submit a revised application.
> Oyelaran said the firm would "look at the options." Pinsky said she would
> support a smaller project on the site. The council's next regular meeting is
> March 18.

---

## WHY EACH LEVER IS PROPORTIONATE

Stated in advance so a failure can be localized to a specific check.

| Lever | Treatment | Why it is not a finding |
|---|---|---|
| **Packaging** | Headline states the outcome and the hearing length. No aggravating modifiers. | "Five-hour hearing" is duration, not atmosphere. The headline's impression matches the body. |
| **Sequencing** | Outcome → developer's case → public comment → both councilmembers → staff position → next steps. | The complicating material (staff recommended approval) appears before the close, not buried. No reaction block precedes the explanation. |
| **Agency / verbs** | "voted," "sought," "told," "said," "raised," "cited." Neutral throughout for all parties. | No vivid/clinical asymmetry. No party de-agentified. |
| **Attribution** | Vote and attendance asserted. Traffic and housing figures attributed to city sources. Positions attributed to speakers. | Asserted material is directly observable; attributed material is sourced. The asymmetry tracks the evidence. |
| **Sourcing** | Developer, opponents, supporters, both sides of the council, planning staff. | Both directions represented, including the dissenting councilmember and the staff recommendation that cut against the vote. |
| **Quote function** | Pinsky and Loomis quotes are FRAME-CARRIERS. Oyelaran and Hale are FACT-SOURCES. | Frame-carrier words ≈ 40. Fact-source and outlet-voice reporting ≈ 300. Strip the two councilmember quotes and the piece still supports: a contested rezoning was rejected against staff recommendation, in a city adding residents faster than housing. **The interpretation survives the strip.** |
| **Omission** | No stated omission of an available material fact. | Traffic count, housing study, staff position, and the un-voted mitigation agreement are all present — including the last, which cuts against the council. |
| **Causal bridges** | "reduced the building from 84 units after neighborhood meetings"; "assumed a traffic mitigation agreement that Cassner had offered but the council did not vote on." | Both bridges present. The second is the one a constructed piece would drop. |
| **Baselines** | 310 units vs. 2,400 residents, 2020–2025. 4,200 vehicles daily. Four of last six proposals. | Denominators stated. Window stated. No switching. |
| **Atmospheric cues** | "ran past 11 p.m.," "about 90 residents." | Both materially relevant to a hearing story. Neither supplies aggravation. |
| **Pattern linkage** | Loomis's "four of the last six" is a pattern claim. | Attributed to a councilmember, and the underlying count is a checkable public record rather than a contested predicate about a prior case. |

---

## EXPECTED RESULT

Written before any run. Do not revise after.

**Required outputs:**

- Section 0 classifies as **news report** (not brief — it has full sourcing and
  ran with time to report).
- Section F2 Step 3 strip test: **SURVIVES.**
- Section K: **empty finding table**, with the stated no-findings sentence.
- Section L directional coherence: **no coherence finding** (fewer than 4 levers
  same-direction; ideally zero surviving findings to count).
- Section L aggregation: **PROPORTIONATE.**
- Final required statement: the **second** of the two options —
  *"No findings survived both the timing and flip tests. This piece's
  construction is defensible."*

**Tolerable:** one or two MINOR findings, if each is stated with a real innocent
explanation and none survives to aggregation. Reasonable people can find small
things. The pass condition is the **derived rating** and the **final statement**,
not zero observations.

**FAIL conditions:**

1. Overall rating above PROPORTIONATE.
2. Any finding rated MODERATE or higher.
3. A directional coherence finding.
4. Strip test returns PARTLY SURVIVES or COLLAPSES.
5. The first final-statement option is used instead of the second.
6. Findings generated from the absence of things the piece had no obligation to
   include (a resident's name, the developer's finances, a competing housing
   study). That is the template failure — manufacturing findings to fill a form.

---

## WHAT A FAILURE MEANS

**Fail on 1–3:** the aggregation and coherence rules are producing findings from
noise. The severity caps or the coherence threshold need raising.

**Fail on 4:** the strip test is over-firing. Check whether frame-carriers are
being over-identified — probably the councilmember quotes being read as
laundering rather than ordinary political reaction.

**Fail on 5 alone, with everything else passing:** the clause is present but the
model won't use it. That is a phrasing problem in the final-statement block, not
an architecture problem.

**Fail on 6:** the most serious result. The instrument mechanically generates
findings regardless of input, and every prior run's findings are suspect —
not because they were wrong, but because they cannot be distinguished from the
output of a template.

---

## RUN LOG

| Date | Prompt version | Model | Result | Notes |
|---|---|---|---|---|
| | | | | |

Run on at least two models. A single-model pass is weaker evidence than a
single-model fail is damning.
