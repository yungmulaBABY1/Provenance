#!/usr/bin/env python3
"""Build the v2-candidate citation-network instrument from the canonical v1 file.

Every edit is an exact, single-occurrence replacement or insertion against the
canonical text, so the candidate is reproducible from the v1 blob and every change
is enumerable. Run from the Provenance repository root:

    python3 -I make_candidate.py prompts/research-analysis/2-citation-network.txt \
        candidates/research-analysis/2-citation-network.v2-candidate.txt
"""
import hashlib
import sys
from pathlib import Path

V1_SHA256 = "dcb93491a0a2ef5716575b89963c2cd9031c43e52011bb549416c89421ff3262"
M = "[FAIL-CN-007]"

HEADER = f"""
-----------------------------------------------------------------
CANDIDATE VERSION — NOT CANONICAL   {M}
-----------------------------------------------------------------

INSTRUMENT VERSION: 2-citation-network v2-candidate.3

Revision 3 of the candidate (2026-11-04). This file is a proposed revision under review. It
is derived from the canonical prompts/research-analysis/2-citation-network.txt (git blob
7ac79f0da337c4d52e39e1490088d06c82a9d42b, sha256
{V1_SHA256}). It does not replace that file, is
not embedded in the webapp, and does not judge any output produced under an earlier version.
Every changed or added passage carries {M}. The change records are in
candidates/research-analysis/2-citation-network.v2-candidate.CHANGES.txt.

A run executed with this file reproduces the INSTRUMENT VERSION line above verbatim near the
top of its output and records the instrument identity in the preflight below.
"""

USE_RULE_OLD = """Do not present model-estimated citation counts as measured facts. Do not invent citation
counts. Do not invent edge lists. Do not infer that a citation is supportive unless you have
inspected the citing passage."""

USE_RULE_NEW = f"""Do not present model-estimated citation counts as measured facts. Do not invent citation
counts. Do not invent edge lists. Do not infer that a citation is supportive unless you have
inspected the citing passage.

Do not assign any citation polarity or claim-use class other than "unclear without full text"
(supportive, neutral/background, critical, perfunctory, inflated, used as premise) unless you
inspected the citing passage in a version that contains the citation. A retrieved version that
does not contain the citation is a VERSION-MISMATCH, not an inspected passage, and does not
count toward citation-context coverage.   {M}"""

VALIDATION_OLD = """It has NOT been validated for open-ended retrieval. It does not establish that a model can
discover a complete network, select the right sources from a large candidate space, avoid
false absence, or report search scope adequately. Retrieval is a separate test axis."""

VALIDATION_NEW = VALIDATION_OLD + f"""

The v2-candidate additions (SECTION A0, SECTION K0 and the passages marked {M}) have
been exercised only on constructed regression fixtures. No live run has used them. They add a
per-source ledger and an inference ledger, which raises execution burden; section omission
under burden is an observed failure of this prompt (FAIL-CN-001).   {M}"""

HEADINGS_OLD = """- PRE-AUDIT CLAIM CONFIRMATION
- SECTION A: CITATION NETWORK STRUCTURE AND CARTEL DETECTION"""
HEADINGS_NEW = f"""- PRE-AUDIT CLAIM CONFIRMATION
- SECTION A0: CORPUS REGISTER AND SOURCE ELIGIBILITY   {M}
- SECTION A: CITATION NETWORK STRUCTURE AND CARTEL DETECTION"""

HEADINGS_K_OLD = """- SECTION J2: THE CONCEDE TEST
- SECTION K: CARTEL-RISK SCORING

Required final-artifact headings:"""
HEADINGS_K_NEW = f"""- SECTION J2: THE CONCEDE TEST
- SECTION K0: EVIDENCE SUFFICIENCY LEDGER   {M}
- SECTION K: CARTEL-RISK SCORING

Required final-artifact headings:"""

A0_ANCHOR = """Before Section A, output the four claim-confirmation lines required above under the exact
heading PRE-AUDIT CLAIM CONFIRMATION.
"""

A0_TEXT = f"""
SECTION A0: CORPUS REGISTER AND SOURCE ELIGIBILITY   {M}

WHY THIS SECTION EXISTS

A corpus chosen to show how the target is cited (reception) is not a corpus chosen to show which
evidence tests the claim (adjudication). The most-cited works that cite a canonical paper are
mostly background users; studies that test the claim may cite the target rarely, or not at all.
When one corpus does both jobs, a reception sample stands in for the evidence base. Register the
corpora separately, screen every member before analysis, and let each inference use only the
corpus and the evidence that support it. Influence is not relevance.

EXECUTION ORDER

1. Fix the claim layers (map fields 1, 3 and 6) and the strongest rivals.
2. Build the candidate corpora: a RECEPTION corpus (how the target is cited, including any
   recent-behavior corpus) and an ADJUDICATION corpus (studies that test the claim layers or
   their strongest rivals, whether or not they cite the target).
3. Screen and classify every member in the eligibility ledger (Gate A) before analysis.
4. Retrieve the evidence each proposed inference needs. Prioritize direct tests and the citing
   passages the conclusions depend on. Full text is required only where the inference needs it.
5. Test every inference against Gate B in SECTION K0 before a finding or a score uses it.
6. Run Sections A–K on the inferences that pass. Keep the others visible as INSUFFICIENT or
   NOT-ASSESSED, each with what would make it sufficient.

CLAIM LAYERS AND RIVALS

Before the corpus register, define every claim layer and rival that any code in this output
uses (for example DIRECT (L3-R1)), one per line:

CLAIM LAYER: L1 — [the claim, for example map field 6 as stated]
RIVAL: R1 — [the strongest plausible rival explanation]

A layer or rival code used in a relevance value and not defined here fails the gate.   {M}

CORPUS REGISTER

For each corpus, output these labels, one per line:

CORPUS ID: [short identifier, for example RECEPTION-1, RECENT-1, ADJUDICATION-1]
CORPUS ROLE: RECEPTION / ADJUDICATION
CORPUS QUESTION: [what this corpus is for, in one sentence]
CORPUS SELECTION RULE: [database, exact query, query date, bounds, ranking, screening]
CORPUS DISCOVERY: SEARCHED — [search record] / NONE — [how members were assembled]
SELECTED ON TARGET CITATION: YES / NO
CORPUS SIZE: [number of members; equals the number of ledger rows naming this corpus]
CITATION CONTEXT COVERAGE: [corpus id] [members with Citation context INSPECTED]/[members]
RECORD QUALITY: [known problems in the records this corpus rests on: duplicate or conflated
records, records that changed between retrievals, reference lists known to be incomplete; or
"none known"]
CORPUS LOCK: [timestamp or hash of the search record] (required for an ADJUDICATION corpus with
CORPUS DISCOVERY: SEARCHED)

SEARCHED means the members came from a recorded query, including a ranked citation query
such as the top 50 works citing the target. NONE means they were assembled by hand or taken
from a supplied packet.

Register at least one ADJUDICATION corpus. If no adjudication search is run, register it with
CORPUS DISCOVERY: NONE and list the claim-testing sources already retrieved, or none (CORPUS
SIZE: 0). A NONE corpus supports statements about its named members only. It is enough only
for an audit that makes no claim about the evidence base. Any such claim (that a kind of test
is absent, the composition or independence of the evidence base, lack of decisive tests) needs
an ADJUDICATION corpus with CORPUS DISCOVERY: SEARCHED. Fix and record that search (database,
query, bounds, screening rule) and its CORPUS LOCK before screening any result. Results located
afterwards may be added only as POST HOC members, named as such in Supported inference.

KNOWN-ITEM RECALL. With the search record, before running the search, list the claim-testing
works you already know (from the claim map, earlier stages, or prior reading). After the
search, report for each SEARCHED adjudication corpus:

KNOWN-ITEM RECALL: [corpus id] [known items the search returned]/[known items] (returned: …;
not returned: …)

Known items the search did not return enter only as POST HOC members. A search that missed a
known item cannot support a LITERATURE-scope statement; "0/0" is the honest value when nothing
was known in advance.

Every coverage figure stated anywhere in the output uses the CITATION CONTEXT COVERAGE label and
equals the ledger count.   {M}

OVERLAP

A source may belong to several corpora. Record it once in the eligibility ledger with every
corpus ID. Count it once in each corpus. Its reception attributes (citation count, rank, citing
behavior) never weight its adjudication role, and its adjudication role never changes reception
counts. A source that does not cite the target may belong to an adjudication corpus; it cannot
belong to a corpus SELECTED ON TARGET CITATION. Sources retrieved outside every corpus (public
texts, critiques, locked Section E sources) take the membership OUTSIDE.

SOURCE ELIGIBILITY LEDGER (GATE A)

Output one row per source under the label SOURCE ELIGIBILITY LEDGER, before Section A:

| Source | Corpus membership | Question relevance | Relation to target | Evidence contribution | Source access | Citation context | Supported inference |

- Source: a stable short identifier first (for example N01), then the work identifier and label.
- Corpus membership: corpus IDs joined by +, or OUTSIDE.
- Question relevance: DIRECT (tests or adjudicates an audited claim layer or a strongest rival;
  name the layer, for example DIRECT (L3)) / ADJACENT (addresses the claim's subject or
  mechanism without testing it: syntheses, reviews, related questions) / BACKGROUND (uses the
  target for another question) / UNRELATED / UNKNOWN.
- Relation to target: SUPPORTS / CHALLENGES / QUALIFIES / PREMISE / MENTIONS / REUSES /
  CITES-UNINSPECTED / NOT-CITING / UNKNOWN. Join several with +.
- Evidence contribution: INDEPENDENT-DATA / SHARED-DATA / REANALYSIS / THEORY / REVIEW /
  METHOD / COMMENTARY / NONE / UNKNOWN.
- Source access: FULL-TEXT / EXCERPT / ABSTRACT / METADATA / INACCESSIBLE, with the version
  read in parentheses. EXCERPT is a retrieved citation-context passage without the full text.
- Citation context: INSPECTED / NOT-INSPECTED / VERSION-MISMATCH / NOT-APPLICABLE.
- Supported inference: what this record, as accessed, permits, in one short phrase. For an
  INSPECTED row it begins with a locator for the passage: an evidence ID (for example RD-E1), a
  page (p. 12, PDF page 44), a section (§3, section 4.2), or "reference list" when the citation
  appears only there.

Gate A rules:

- SUPPORTS, CHALLENGES, QUALIFIES, PREMISE and MENTIONS describe how the citation is used. Each
  requires Citation context INSPECTED. Without an inspected passage, use CITES-UNINSPECTED.
- INSPECTED requires FULL-TEXT or EXCERPT access to a version that contains the citation, and
  a locator in Supported inference. A passage that cannot be located again is not inspected.
- REUSES (shared data, instrument or sample) requires FULL-TEXT or ABSTRACT access.
- NOT-APPLICABLE is the Citation context of a NOT-CITING source.
- UNKNOWN is a valid value in every coded column. Never replace it with a guess to complete a
  count. A relevance or contribution code, or NOT-CITING, assigned from METADATA-only access is
  permitted when the record genuinely shows it; say so in Supported inference. The checker lists
  such rows for review.
- One row per work, not per database record. When several records are the same work (a
  working paper and its published version, or a duplicated record), give one row, list every
  record identifier in the Source cell, and count the work once. When you read a different
  version from the one the record describes, write VERSION-SUBSTITUTE: [version read] in
  Source access. The checker lists rows whose titles suggest the same work for review.   {M}
- A highly cited member can be BACKGROUND. A DIRECT test can be lightly cited or absent from the
  reception corpus. Do not let either attribute stand in for the other.
"""

Q1_OLD = """1. What are the top 50 most-cited papers on the central claim? List at least the top 10-15
   with:"""
Q1_NEW = f"""1. What are the top 50 most-cited papers on the central claim?   {M}

   State which registered corpus answers this. A corpus selected because its members cite the
   target is a RECEPTION corpus: it shows how the target is cited, not which evidence tests the
   claim. Questions about the evidence base (Section B 11-16, Section G 50, the
   lack-of-decisive-tests dimension) use the ADJUDICATION corpus registered in SECTION A0,
   which includes studies that test the claim or its strongest rivals whether or not they cite
   the target. List at least the top 10-15 reception-corpus members with:"""

Q6_OLD = """6. In the last 5 years, what are the most-cited new papers on the claim?
"""
Q6_NEW = f"""6. In the last 5 years, what are the most-cited new papers on the claim?

   If the recent corpus is selected because its members cite the target, every member cites
   the founding paper by construction. Report dependence only from what members cite beyond
   the target and from inspected citing passages; otherwise mark recent-paper dependence
   UNASSESSED.   {M}
"""

B_OLD = """For the top 50 papers, code each paper by evidence type:

- primary empirical test of the central claim
"""
B_NEW = f"""For the top 50 papers, code each paper by evidence type. Code every member of each registered
corpus the same way.   {M}

- primary empirical test of the central claim
- primary empirical study of another question (cites the target as background or premise)   {M}
"""

B16_OLD = """16. Is the network evidence-rich or citation-rich?
"""
B16_NEW = f"""16. Is the network evidence-rich or citation-rich?

Questions 11-16 describe the evidence base only when computed on an ADJUDICATION corpus with
CORPUS DISCOVERY: SEARCHED. Computed on a reception corpus, they describe the citing set; say so
in the answer, and report UNKNOWN codes in every count.   {M}
"""

C17_OLD = """17. For the top 15 papers, classify how they cite the founding cluster.
"""
C17_NEW = f"""17. For the top 15 papers, classify how they cite the founding cluster.

    Report how many of the 15 citing passages were inspected. Percentages in 18-19 use
    inspected citations only, report the uninspected count beside them, and do not extend to
    uninspected papers unless every paper was inspected or the inspected set is a prespecified
    random sample.   {M}
"""

H_OLD = """Presence of a major critique with verified non-uptake is high-information. Absence of critique"""
H_NEW = f"""UPTAKE POPULATION   {M}

Test uptake on papers for which engagement is expected: hub and dominant-cluster papers, and
citers screened as relying on the element the critique targets. A co-citation rate over all
citers is a co-citation count. Report it, but it does not show that a paper ignored a critique,
and it cannot alone carry a poor-uptake score above 0.

Presence of a major critique with verified non-uptake is high-information. Absence of critique"""

K0_ANCHOR = """-----

SECTION K: CARTEL-RISK SCORING
"""

K0_TEXT = f"""-----

SECTION K0: EVIDENCE SUFFICIENCY LEDGER   {M}

Before scoring, list every inference that a finding or a score relies on and test each one
against the evidence it needs (Gate B). Sufficiency belongs to the inference, not to the number
of full texts retrieved: reference lists can fully support a graph statement; one inspected
citing passage supports a statement about that citation; no quantity of metadata supports a
statement about how a paper used a citation.

INFERENCE CLASSES

Class | States | Minimum evidence for each member used | Widest scope
GRAPH-STRUCTURE | edges, density, degree, clustering | reference list (METADATA or better) |
    CORPUS; LITERATURE only for a corpus not selected on target citation and SEARCHED
CO-CITATION | how many works in a defined population also cite X | reference lists | POPULATION;
    co-occurrence only, never use, endorsement or engagement
DATABASE-RECORD | record identity, counts, authorship, versions | metadata | NAMED, CORPUS or
    POPULATION
COMPOSITION | shares of a corpus by a ledger code | a code for every member, UNKNOWN counted |
    CORPUS; LITERATURE only on an ADJUDICATION corpus that was SEARCHED
CITATION-USE | how a citing work uses the target | Citation context INSPECTED | WITHIN-SAMPLE;
    CORPUS only if every member was inspected or the inspected set is a PRESPECIFIED-RANDOM
    sample
ENGAGEMENT | whether a work answers, narrows or ignores a critique or rival | FULL-TEXT, and the
    member is DIRECT or ADJACENT | NAMED or WITHIN-SAMPLE; CORPUS as for CITATION-USE
RESTATEMENT | how a named text restates another | FULL-TEXT or EXCERPT of both texts | NAMED
    or CORPUS
DATA-ORIGIN | whether named studies share data, instrument or sample | FULL-TEXT or ABSTRACT |
    NAMED or CORPUS; LITERATURE only on an ADJUDICATION corpus that was SEARCHED
SOURCE-RESULT | what a named source reports or states | FULL-TEXT or ABSTRACT | NAMED or
    CORPUS
ABSENCE | that no work of a kind exists | an ADJUDICATION corpus, SEARCHED for that kind of
    work and locked before screening | LITERATURE, bounded by the search, only when every
    member is screened (no UNKNOWN relevance); otherwise WITHIN-SAMPLE over the screened
    members, with the statement giving screened/total. An absence is never stated beyond the
    search that bounds it.

Scopes: NAMED (listed sources); WITHIN-SAMPLE (the inspected members only; the statement says
so); CORPUS (every member of the named corpus); POPULATION (a citing population defined in the
statement with k/n counts; metadata classes only); LITERATURE (beyond any defined corpus).

Sampling rules: EXHAUSTIVE / PRESPECIFIED-RANDOM / PRESPECIFIED-RULE / CONVENIENCE /
NOT-APPLICABLE. A CONVENIENCE set (whatever was retrievable) supports WITHIN-SAMPLE statements
only. A random sample that loses members it cannot retrieve is no longer random: report
SAMPLE ATTRITION: [inference] [retrieved]/[sampled] beside it, keep the sample inference
INSUFFICIENT, and state anything about the retrieved members as a separate CONVENIENCE
inference.   {M}

INFERENCE LEDGER

| Inference | Class | Corpus | Claimed scope | Sampling rule | Members used | Disposition | Statement |

- Corpus: a registered corpus ID; POPULATION for population counts; — for NAMED sets that span
  corpora or use OUTSIDE sources.
- Members used: ALL; INSPECTED; SCREENED (members whose relevance is not UNKNOWN); a
  comma-separated list of ledger source identifiers; or, for POPULATION, UNSCREENED or
  SCREENED: [rule].
- Disposition: SUPPORTED / SUPPORTED-WITHIN-SAMPLE / INSUFFICIENT / NOT-ASSESSED.
- For each COMPOSITION inference, add one line:
  COMPOSITION: [inference] | [relevance or contribution or access or context] | CODE=n; ... |
  TOTAL=n
  The counts include UNKNOWN and sum to TOTAL.
- An INSUFFICIENT or NOT-ASSESSED inference stays in the ledger, and its statement says what
  would make it sufficient. It cannot carry a SCORED dimension or a confirmed or contested
  finding.
- If you withhold an inference whose evidence meets the minimum, as INSUFFICIENT or as
  NOT-ASSESSED, say why. The checker routes that inference to review instead of accepting the
  withholding silently.

DIMENSION EVIDENCE BASIS

| Scorecard dimension | Scorecard disposition | Inference IDs | Basis note |

Output the line DIMENSION CLASS MAP: cn7-map-3 above this table. One row for each of the 11
Section K dimensions, with the same disposition as Artifact 8. A SCORED row lists the
inferences its score relies on, and only those, each tagged (+) when it supports concern or
(-) when it supports no concern, for example: I03 (+), I10 (-). Also list, tagged (?), every
INSUFFICIENT or NOT-ASSESSED inference that bears on the dimension: a SCORED row with a (?)
inference is scored on a partial basis, and the checker routes it to review. An UNASSESSED,
UNINFORMATIVE or N/A row leaves Inference IDs as — and its basis note states what is missing
and what would make the dimension assessable.

A score above 0 needs at least one (+) inference of the concern classes below. A score of 0
needs at least one (-) inference of the no-concern classes: affirmative evidence of no concern,
as the hard rule in Section K requires. Every (+) and (-) inference must pass Gate B.

A zero carries the same burden as a concern. Where a concern would need a searched evidence
base, so does a zero; where a concern would need the population the dimension covers, so does a
zero. Evidence about named works supports a score in either direction only when those works are
that population, and the checker routes such scores to review.   {M}

DIMENSION CLASS MAP cn7-map-3 (dimension: concern classes / no-concern classes)

- Internal citation density: GRAPH-STRUCTURE / GRAPH-STRUCTURE.
- Founding-cluster dominance: GRAPH-STRUCTURE, CO-CITATION, DATABASE-RECORD / the same.
- Recent-paper dependence: CITATION-USE, GRAPH-STRUCTURE, CO-CITATION / the same. A graph or
  co-citation statement on a corpus selected on target citation must concern citation beyond
  the target.
- Review-hub laundering; Claim mutation: RESTATEMENT / RESTATEMENT.
- Proxy mismatch: RESTATEMENT, CITATION-USE, SOURCE-RESULT / the same.
- Lack of decisive tests: ABSENCE, SOURCE-RESULT (named tests whose results conflict, so none
  is decisive) / SOURCE-RESULT, DATA-ORIGIN (a named test that is decisive). Either direction
  needs an ADJUDICATION corpus with CORPUS DISCOVERY: SEARCHED. Every SCORED 0 goes to review:
  the checker cannot judge whether a test is decisive.
- Poor critique uptake: ENGAGEMENT, GRAPH-STRUCTURE (named dominant-cluster papers that had the
  opportunity do not cite the critique) / ENGAGEMENT. A score in either direction that rests
  only on named works goes to review: confirm they are the uptake population (Section H) and
  that every located critique was traced, or list the untraced ones (?).
- Adjacent-field neglect: ENGAGEMENT, GRAPH-STRUCTURE (named audited papers do not cite the
  locked adjudicating source) / ENGAGEMENT, SOURCE-RESULT. The same review applies: source-layer
  engagement alone does not cover later papers.
- Intervention-evidence ratchet; Model non-updating: any class; their own section gates apply.

A co-citation rate over a population is never a concern basis for poor critique uptake or
adjacent-field neglect. Listed beside a qualifying (+) inference it goes to review; alone it is
insufficient. The map is versioned: a change to any entry is a new map ID.

FINDING EVIDENCE BASIS

| Finding | Finding status | Inference IDs |

One row per standardized finding. A confirmed or contested finding lists only SUPPORTED or
SUPPORTED-WITHIN-SAMPLE inferences. A provisional finding may also list INSUFFICIENT ones.

PLACEMENT

Place SECTION A0 after PRE-AUDIT CLAIM CONFIRMATION and SECTION K0 immediately before SECTION K.
Place nothing after FINAL SECTION: STANDARDIZED FINDING TABLE and add no fields to the
standardized finding table: downstream parsers read that table strictly. Gate vocabulary
contains no token ending in -CONFIRMED or -VERIFIED; verification states keep their canonical
meanings and do not replace the Gate A values.

-----

SECTION K: CARTEL-RISK SCORING
"""

K_OLD = """Never convert UNKNOWN or another incomplete evidence state into SCORED 0. Never convert
UNINFORMATIVE into no concern. A dimension may be fully executed yet remain uninformative.
"""
K_NEW = K_OLD + f"""
A dimension may be SCORED only when SECTION K0 links it to inferences that pass Gate B. A
dimension whose only bases are INSUFFICIENT or NOT-ASSESSED is UNASSESSED. The coverage gate
counts dimensions after this step. Its 70% value is unchanged and remains PROVISIONAL. Report
coverage after Gate B; the gate checker also reports what coverage would be if each dimension
with an open review item were withdrawn, and the formal-label gate must state whether it is met
only on condition that those items resolve for the score. If coverage after Gate B is below
70%, RISK BAND reads WITHHELD, whatever the arithmetic band position. When the band is
WITHHELD, quote the arithmetic band position only beside the word WITHHELD.   {M}
"""

CONF_OLD = """repeat the DENSITY INFERENCE SCOPE and the corpus definition that bounds the claim.
"""
CONF_NEW = CONF_OLD + f"""
The confidence level states citation-context coverage for each corpus with the CITATION CONTEXT
COVERAGE label from SECTION A0.   {M}
"""

EDITS = [
    ("validation boundary", VALIDATION_OLD, VALIDATION_NEW),
    ("citation-use rule", USE_RULE_OLD, USE_RULE_NEW),
    ("heading list A0", HEADINGS_OLD, HEADINGS_NEW),
    ("heading list K0", HEADINGS_K_OLD, HEADINGS_K_NEW),
    ("section A0", A0_ANCHOR, A0_ANCHOR + A0_TEXT),
    ("question 1", Q1_OLD, Q1_NEW),
    ("question 6", Q6_OLD, Q6_NEW),
    ("section B code", B_OLD, B_NEW),
    ("section B scope", B16_OLD, B16_NEW),
    ("section C coverage", C17_OLD, C17_NEW),
    ("section H population", H_OLD, H_NEW),
    ("section K0", K0_ANCHOR, K0_TEXT),
    ("section K gate", K_OLD, K_NEW),
    ("confidence coverage", CONF_OLD, CONF_NEW),
]


def main() -> int:
    src, dst = Path(sys.argv[1]), Path(sys.argv[2])
    raw = src.read_bytes()
    if hashlib.sha256(raw).hexdigest() != V1_SHA256:
        raise SystemExit("input is not the pinned canonical v1 instrument")
    text = raw.decode("utf-8")
    title_end = text.index("NEGLECT\n") + len("NEGLECT\n")
    text = text[:title_end] + HEADER + text[title_end:]
    for name, old, new in EDITS:
        count = text.count(old)
        if count != 1:
            raise SystemExit(f"edit {name!r}: anchor found {count} times")
        text = text.replace(old, new)
    dst.write_text(text, encoding="utf-8")
    print(f"wrote {dst} sha256 {hashlib.sha256(text.encode()).hexdigest()} "
          f"lines {text.count(chr(10))} edits {len(EDITS) + 1}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
