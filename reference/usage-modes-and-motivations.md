# Modes of use, and why to use this toolkit

Companion to philosophy.md (commitments) and methodology.md (sequence). This
document describes HOW an operator chooses to run an audit, and WHY.

================================================================
PART 1 — THREE MODES OF USE
================================================================

These are not three different tools. They are three different amounts of
outside knowledge an operator brings to the same prompts, and each amount
requires a DIFFERENT discipline to stay honest. More outside knowledge is not
automatically better — it is more powerful and more dangerous at the same
time, which is why the discipline gets stricter as the mode gets richer.

They are not mutually exclusive and are commonly run in sequence: Mode 1 first
to see what the formal machinery finds unprompted, then Mode 3 leads layered
onto a rerun once a domain expert has seen where the cold run under-reached.

----------------------------------------------------------------
MODE 1 — BLANK / COLD-START
----------------------------------------------------------------

Pure formal critique. The operator supplies only the source and, where
relevant, the claim under audit. No outside knowledge of the domain, the
game, the field, or the population is injected — only what the source itself
supplies (methods, stated models, claimed constructs, stated controls).

WHAT IT IS FOR:
- Establishing whether a source can be shown to fail on its OWN terms, before
  any external argument is brought to bear. This is the strongest kind of
  finding, because it cannot be dismissed as the auditor's outside agenda.
- A first pass on any target, including ones the operator has no expertise in.
- Testing whether the toolkit's own formal machinery — proxy checks,
  construct-establishment, level-of-analysis, confound audit — catches a real
  problem WITHOUT being told where to look. This is also how the toolkit
  tests itself: a cold run that finds nothing on a paper that should have
  something wrong with it is informative about the instrument, not only about
  the paper.

THE DISCIPLINE THIS MODE REQUIRES: retrieve, don't infer. The single largest
failure mode in cold mode is the model filling a gap from fluent background
memory instead of the retrieved source — asserting what a scale "usually"
contains, or what a field "generally" believes, rather than what THIS source
actually says. [P1]'s retrieval-gate machinery exists specifically to keep
Mode 1 honest.

WHAT COLD MODE CANNOT DO: find a problem that requires knowledge outside the
source and its citation network. A cold run on Shen correctly flagged
"advancement efficiency is a proxy for performance" as a major finding, and
separately listed "player motivation and whether leveling is the player's
goal" as an unmeasured confound — but it filed that confound as one line
among several rather than developing it into the sharper compositional
argument a domain expert reached later (see Mode 3 below). The ingredient was
present; the weight was not. That gap is Mode 1's structural ceiling, not a
bug in the run.

----------------------------------------------------------------
MODE 2 — ASSUMPTION-TESTING
----------------------------------------------------------------

Systematically surfacing and pressure-testing the source's OWN stated and
implicit assumptions, without introducing new external domain knowledge. This
sits between Mode 1 and Mode 3: more directed than a cold read, but still
using nothing the source and its own literature didn't supply.

WHAT IT IS FOR:
- Turning a passive reading into an active checklist: does the design assume
  uniform intent, uniform access, uniform baseline conditions across the
  compared groups? Does "measuring X" quietly become "claiming Y" without the
  bridge being stated or tested?
- Distinguishing an assumption the source states explicitly (defensible,
  disclosed) from one it makes implicitly without acknowledgment (a genuine
  gap).

CURRENT STATUS — HONEST NOTE: this mode does not yet have dedicated
machinery of its own. Today it happens informally, distributed across the
construct-validity and internal-validity confound/proxy sections, rather than
as a single tracked pass. The Shen run's confound table entry for "player
motivation and whether leveling is the player's goal" is what Mode 2 should
produce systematically — one entry per implicit assumption, each with its own
falsifiability question — and currently produces incidentally, as one row
among several rather than a dedicated pass. A future addition worth
specifying: an assumptions register, structurally parallel to the existing
investigation register, with one entry per assumption rather than per
hypothesis.

THE DISCIPLINE THIS MODE REQUIRES: state the assumption in the SOURCE'S own
terms before critiquing it. The failure mode here is inventing an assumption
the source doesn't actually make and then attacking the invention — a straw
man dressed as rigor. An assumption worth listing must be traceable to
something the design actually does or fails to control for, not to what a
critic feels the design "must be assuming."

----------------------------------------------------------------
MODE 3 — DOMAIN-INFORMED / OPERATOR LEADS
----------------------------------------------------------------

The operator brings real outside knowledge — direct experience, domain
expertise, field-specific mechanisms — and files it as explicit, falsifiable,
origin-tagged leads for the toolkit to test, rather than asserting it as
already-established fact.

WHAT IT IS FOR:
- Reaching problems that are invisible to Mode 1 and Mode 2 because they
  require knowing something the source and its literature don't state and an
  outside reader wouldn't otherwise think to check. The Shen leads on
  power-leveling, AFK progression, tradeskill skill-ceiling, and the
  activity-composition/intent-mixture confound all came from having actually
  played the games studied — none of them are derivable from the paper's own
  text or its citation network.
- Letting a subject-matter expert contribute what they know without that
  knowledge silently becoming the audit's premise.

THE DISCIPLINE THIS MODE REQUIRES, and it is the strictest of the three: a
lead is a hypothesis under test, not evidence. Every lead is filed with an
origin tag (OPERATOR-SUPPLIED), a falsifiable retrieval question, and a
MANDATORY disconfirming search run with equal effort to the confirming
search. The most likely honest outcome for a Mode 3 lead is UNCONFIRMED — no
retrievable source settles it either way — and that is a legitimate,
expected result, not a failed lead. A lead that is asserted with high
operator confidence but never actually searched against is not stronger
evidence for being confident; it is exactly the failure this discipline
exists to prevent, and the flip test applies here directly: would the same
causal story be accepted this readily pointed in the opposite direction?

WORKED DISTINCTION, FROM THE SAME CASE: an early formulation of a Shen lead
proposed a specific sex-differentiated trait explanation (distractibility,
compulsion to level) for an observed pattern, offered with "I am sure there
are studies that corroborate this." That formulation was corrected before
filing, to a composition/mixture-model version that requires no causal story
about why groups might differ — only that they might, which is directly
testable against the paper's own unmeasured variables. The corrected version
is stronger evidence specifically because it dropped the unverified causal
claim. Domain expertise is most valuable when it identifies a testable
STRUCTURAL gap (what wasn't measured, what wasn't stratified) rather than
when it supplies a causal narrative for why the gap exists. The latter is a
second, separate claim that needs its own retrieval, not a free rider on the
former.

================================================================
PART 2 — WHY USE THIS TOOLKIT
================================================================

Not a feature list. Each of these is grounded in something the toolkit has
actually been shown to do, not a claim about what it should be able to do.

----------------------------------------------------------------
To pressure-test a claim you're skeptical of
----------------------------------------------------------------

The obvious use case, and the one every stage is built around: does the
source's measured variable actually support its claimed conclusion, does the
citation network show independent convergence or inherited repetition, does
the finding survive contact with the strongest available opposition.

----------------------------------------------------------------
To pressure-test a claim you already believe, before you commit to it
----------------------------------------------------------------
This is less obvious and arguably more valuable. The counter-audit stage
exists specifically to ask "does this survive contact with the strongest
opposing evidence" of the OPERATOR'S OWN developing argument, not only of a
target the operator distrusts. Using the toolkit only on claims you dislike
inherits your own priors with extra steps; using it on a claim you are about
to publish or act on is where it does its most useful work, because it is the
one point where a wrong answer actually costs you something.

----------------------------------------------------------------
To catch two different kinds of prior, which require opposite fixes
----------------------------------------------------------------
An operator's own motivated reasoning is caught by introspection: the flip
test, the concede test, prior-source labeling. A FIELD's ambient consensus —
a construct or finding that has been laundered through repeated citation
without independent scrutiny — is caught only by retrieval, because from
inside a field's own dialect a consensus claim does not present as a prior at
all; it presents as established knowledge. The toolkit is one of the few
places these two failure modes are treated as genuinely different problems
requiring different machinery, rather than both being waved at with "check
your bias."

----------------------------------------------------------------
To let domain expertise in without letting it take over
----------------------------------------------------------------
See Mode 3 above. A structured place to put what you actually know, that
forces it to survive a real search rather than becoming the audit's silent
premise.

----------------------------------------------------------------
To get a real critique without domain expertise
----------------------------------------------------------------
See Mode 1 above. A journalist, student, or generalist auditing a claim
outside their own field still gets formal proxy, construct, and
level-of-analysis checks that do not require them to already know the field's
specific failure modes.

----------------------------------------------------------------
To apply one standard regardless of which direction a claim points
----------------------------------------------------------------
The evidence-quality and reception-gate machinery is explicitly symmetric:
support sources and opposition sources are held to the identical bar, and the
counter-audit's SYMMETRIC-SCORING RULE requires the auditor to notice and
correct for the standing temptation to rate opposition higher merely because
finding opposition is the stage's job. This has been demonstrated across
domains that pull in different political directions — academic consensus
claims, activist claims, journalism — using the identical checks each time.
The toolkit does not have a preferred conclusion; it has a preferred standard
of evidence, applied to whichever side is making a load-bearing claim.

----------------------------------------------------------------
To build a record that survives past one conversation
----------------------------------------------------------------
FAILURES.md, CHANGELOG.md, and the regression fixtures mean a lesson learned
from one run does not have to be relearned on the next one, and a repair does
not silently break an earlier capability without a fixture catching it. This
matters most for exactly the kind of iterative, long-horizon use this
document describes — running the same target multiple times as new leads and
repairs accumulate, the way the Shen chain has been run three times now with
each pass building on what the last one found.

----------------------------------------------------------------
To end in a human decision, not a machine-generated score
----------------------------------------------------------------
Every stage preserves disaggregated findings — narrowed, reframed,
reclassified, or killed, each with its own reasoning — and hands them to a
human rather than collapsing them into a composite number. This is a
deliberate constraint, not a missing feature: several weak signals becoming
one authoritative-looking score is one of the specific risks the toolkit's
own design table names and guards against.
