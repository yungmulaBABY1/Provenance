# FAIL\-CA\-004 — Shen directional\-defense symmetry

- Closes: `FAIL-CA-004`
- Target: `prompts/research-analysis/3-counter-audit.txt`, Section E0
- Control: positive directional\-symmetry regression
- Status: **BUILT, NOT RUN**
- Oracle fixed: 2026\-08\-11, before the repaired counter\-audit is rerun

## Failure object

The Shen partial rerun added an activity\-composition concern to construct
validity: EQ2 total character play time combines advancement\-directed play with
fishing, gathering, social, exploratory, and other activities\. The source’s
Discussion acknowledges potentially different gaming goals, then asserts that
the expected direction would bias against parity and make its parity finding
more robust\. It does not measure activity allocation or advancement\-directed
time\.

The historical E0 row correctly found the passage but classified it
`RECHARACTERIZED`\. That gave an untested, source\-favorable direction the effect
of a partial rebuttal even though the same unmeasured mechanism permits a live
opposite direction\.

This case tests E0’s classification and effect rule\. It does not ask the rerun
to rediscover CV\-7 or to establish which directional hypothesis is true\.

## Frozen evidence bundle

Run source: [`examples/research/shen/`](../../examples/research/shen/)\. The
partial rerun was completed 2026\-08\-10 with operator\-supplied leads\. It updated
claim extraction and construct validity, reused internal validity and citation
network unchanged, and then reran the counter\-audit\.

Supply these files to the repaired counter\-audit:

1. Updated claim map:
   [`01_claim_extraction_with_leads.txt`](../../examples/research/shen/01_claim_extraction_with_leads.txt)
2. Original source: Shen et al\. \(2016\), identified and access\-bounded in
   [`00_run_metadata_and_preregistration.txt`](../../examples/research/shen/00_run_metadata_and_preregistration.txt)
3. Updated construct validity:
   [`02_construct_validity_with_leads.txt`](../../examples/research/shen/02_construct_validity_with_leads.txt)
4. Existing internal validity, unchanged:
   [`03_internal_validity.txt`](../../examples/research/shen/03_internal_validity.txt)
5. Existing citation network, unchanged:
   [`04_citation_network.txt`](../../examples/research/shen/04_citation_network.txt)

The historical comparison output is
[`05_counter_audit_with_leads.txt`](../../examples/research/shen/05_counter_audit_with_leads.txt)\.

Frozen SHA\-256 identities:

|File                                  |SHA-256                                                           |
|--------------------------------------|------------------------------------------------------------------|
|`01_claim_extraction_with_leads.txt`  |`367a41394b60ecd89a07b9616c5b16c9ebcbcf2688fa52b0dba3a3de80a386f6`|
|`02_construct_validity_with_leads.txt`|`b77c116c18dd718078e0c98c780a8f24509cf3565e4224ded49261de551a3964`|
|`03_internal_validity.txt`            |`c721fac19c7e130bb38bd18d1bcf053e6b34ff229a8d98000d6e4c10f2f1e6b2`|
|`04_citation_network.txt`             |`e59149379c92a44d84720a2f28d1ab8e5a3cc719e07e07ba16b3305d6cb691bb`|
|`05_counter_audit_with_leads.txt`     |`37530657bf6ae5717d55823c331a292d6dfa6d60e4f7b176066a16cb138a1a6a`|

## Load\-bearing historical row

The historical E0 row for `CV-7 / corrected Lead 3` quotes the source asking
whether its finding could be attributed to men and women pursuing different
gaming goals\. It records that the paper directionally defended the point but
reported no activity\-share or advancement\-directed\-time analysis\. Its effect
was:

> RECHARACTERIZED — the goal-allocation issue was anticipated and directionally
> defended, not hidden. The residual charge is that the defense is not tested
> against observed activity allocation or an advancement-directed-time
> denominator.

The construct\-validity output rates the item\-specific proxy problem moderate and
nests it under the general proxy mechanism\. This case does not unnest it or
upgrade that pre\-E0 severity\.

## Expected result

A passing repaired run must satisfy all of the following:

1. CV\-7’s E0 `Type` is `directional defense — ASSERTED-ONLY`, unless the rerun
   locates source\-specific measurement not present in the frozen packet\.
2. CV\-7’s E0 `Effect` is `DIRECTIONALLY-CONTESTED`, not
   `RECHARACTERIZED`\.
3. The E0 row explicitly states the live mirror hypothesis: concentration on
   the visible leveling metric could bias toward parity and mask a difference
   among genuine maximizers\.
4. If any incoming wording calls the issue hidden or undisclosed, E0 corrects
   it to `acknowledged but direction unresolved`\.
5. The source’s untested directional assertion does not reduce CV\-7 below its
   pre\-E0 severity\. A wording correction is not counted as a severity reduction\.
6. Any external citation offered for the source’s direction is routed through
   E1 and the SOURCE\-RECEPTION GATE rather than treated as verified inside E0\.
7. Section J and E0’s residual line use the expanded five\-value effect
   vocabulary and include the CV\-7 disposition\.
8. The overall bottom\-line category is checked for movement but is not forced to
   change\. The reasoning for CV\-7 must no longer imply that the source’s untested
   directional defense weakened the substantive criticism\.

## Failure meaning

- Effect remains `RECHARACTERIZED`: the symmetry check did not fire, or the
  defense was misclassified as tested\.
- Mirror hypothesis is absent: the check fired but its output requirement was
  skipped\.
- Severity drops at E0: the no\-reduction rule was not applied\.
- Source is called silent or the issue hidden: the repair preserved severity by
  retaining an inaccurate concealment charge\.
- An external citation is treated as verified inside E0: the E0/E1 boundary was
  violated\.
- E0 is correct but Section J omits `DIRECTIONALLY-CONTESTED`: schema
  propagation is incomplete\.

Do not add a `tests/RESULTS.md` regression row until this repaired run is
actually executed\.
