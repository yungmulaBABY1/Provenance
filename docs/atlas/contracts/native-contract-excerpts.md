> **Origin:** copied unchanged from package B (alternative implementation
> `atlas-citation-import/0.1`, file `native-contract-excerpts.md`, SHA-256 `b6aa29608b2074feb3d24e24760fa1d3e49d54f513c3ffb9afbce1471f94da5e`).
> Everything below this header is byte-for-byte the original.
>
> **Status:** documentation only. This is not a second runtime, schema or
> parser; package B's `atlas_adapter/` is not part of this repository. Paths
> such as `atlas_adapter/contract.json` and `evidence/verified-files.json`
> refer to package B and do not exist here. The runtime is `atlas/`, and the
> pinned prompts remain authoritative.

---

# Native contract excerpts

Generated exact excerpts, not an executable schema. Each source is pinned in verified-files.json.

## prompts/0-field-diagnostic.txt

```text
18: PROMPT IDENTITY MARKERS
25: 1. RECORD THE INSTRUMENT ACTUALLY IN CONTEXT.
42: 2. MUTABLE-REFERENCE / CURRENCY RULE.
70: 3. VERSION-COLLISION ATTRIBUTION GATE.
97: 4. DISPOSITION.
110: 5. REQUIRED RUN-HEADER LINE.
171: HOW TO USE THIS PROMPT
202: SECTION A: DOES THE FAILURE MODE EXIST?
207: ON THE CORE CLAIM
209: 1. What is the field's central claim? State it in one sentence.
210: 2. Is this claim presented as an empirical finding, a theoretical framework, or
212: 3. What was the original study or paper that established the claim? What was the
214: 4. Has the original claim been directly replicated by independent researchers
219: 5. Does the field clearly distinguish between well-supported versions of the
222: ON EMPIRICAL STATUS
224: 6. What would it take for a researcher in this field to publish a paper that
226: 7. Has the field specified what evidence would falsify or seriously weaken its
228: 8. Has the field's main prediction been tested against a natural experiment or
230: 9. Are there adjacent fields or literatures that contradict or complicate the
233: ON THE PROXY / MEASUREMENT
235: 10. What does the field most commonly measure? Describe the primary data sources
237: 11. What construct does the field claim to be explaining or intervening on?
238: 12. Is the thing being measured the same as the construct being claimed? If not,
240: 13. What confounds are routinely present in the field's typical measurements that
242: 14. Has anyone in the field formally challenged the validity of the primary
249: ON THE CITATION NETWORK
251: 15. Name the 5-10 most-cited papers in the relevant subfield. Do they primarily
256: 16. Is there a small founding cluster of papers that later work heavily relies
259: 17. Which disciplines with relevant expertise are well-represented in the
261: 18. Are there papers that challenged the dominant view that receive little
268: ON EXTRAPOLATION
270: 19. At what population or skill level were the foundational studies conducted?
271: 20. At what population or outcome level does the field make its strongest claims?
272: 21. What assumptions are required to bridge the evidence level to the claim
274: 22. Are there contexts where the field's model predicts improvement or
277: ON THE INTERVENTION RATCHET
279: 23. What interventions or policies has the field advocated for or helped
281: 24. Which metrics improved after implementation, and which did not?
282: 25. Was the primary outcome measure independent of the intervention, or did it
284: 26. Has any version of the intervention been meaningfully rolled back or
286: 27. When interventions fail to deliver on their stated goals, what does the field
291: SECTION B: CAN THE CHALLENGE BE RUN?
296: ON YOUR DOMAIN KNOWLEDGE
298: 28. Do you have direct experience with the phenomenon the field claims to explain
300: 29. Can you identify specific, concrete cases where the field's model or
302: 30. Can you name confounds that the field routinely ignores because you have
304: 31. Can you clearly articulate the proxy or measurement problem in terms that
308: ON THE DECISIVE TEST
310: 32. What evidence would directly and decisively test the central claim at the
312: 33. Does this evidence currently exist? If not, is it collectible through a
314: 34. If the decisive test were run and came back against the field's position,
318: ON YOUR POSITION
320: 35. What do you have to lose by running this challenge (career, funding,
322: 36. What do you have to gain that is independent of career advancement?
323: 37. Are you willing to publish under your own name with transparent sourcing and
325: 38. Can you specify what evidence would cause you to revise or abandon your
330: SECTION C: CALIBRATION QUESTIONS
335: 39. Is there a version of the field's central claim that you accept as valid?
337: 40. Can you describe the strongest version of the field's argument before
339: 41. If the decisive test came back in the field's favor, would you update your
341: 42. Are there aspects of the field's work you would be willing to cite positively
344: 43. Are you primarily identifying problems with the field's methods and evidence,
347: 44. Would you be willing to publish this challenge even if it received
398: FINAL ASSESSMENT
```

## prompts/1-claim-extraction.txt

```text
1: CLAIM EXTRACTION / INFLATION MAP
18: PROMPT IDENTITY MARKERS
25: 1. RECORD THE INSTRUMENT ACTUALLY IN CONTEXT.
42: 2. MUTABLE-REFERENCE / CURRENCY RULE.
70: 3. VERSION-COLLISION ATTRIBUTION GATE.
97: 4. DISPOSITION.
110: 5. REQUIRED RUN-HEADER LINE.
132: WHY THIS STAGE EXISTS
181: COMPACT VOCABULARY
221: 1. Never report a verification state above what was actually checked.
222: 2. Evidence type and verification state are separate axes; report both.
223: 3. FULL-TEXT-CONFIRMED, RECEPTION-CONFIRMED, and CROSS-SOURCE-CONFIRMED answer different
225: 4. Field 4 provenance states describe how a downstream item entered the map; verification
237: CANONICAL CONSTRUCT PROPERTIES
263: MAP / PROSECUTOR DIVISION
290: HARD RULE
341: 1. WHAT WAS LITERALLY MEASURED
436: 2. STRONGEST CLAIM THE SOURCE ITSELF MAKES
446: 3. WEAKER DEFENSIBLE CLAIM THE EVIDENCE ACTUALLY SUPPORTS
464: 4. BROADER CLAIM ATTACHED DOWNSTREAM
733: 5. WHERE THE INFLATION BEGINS
739: 1. Its provenance state is SUPPLIED or RETRIEVED.
740: 2. It is ANCHOR-ELIGIBLE under the sufficiency check below.
773: | Item | Provenance state | Quotation present? | Locator present? | Attribution cross-source-confirmed, if applicable? | Anchor eligibility |
774: |---|---|---|---|---|---|
775: | | | yes / no | yes / no | yes / no / N/A | ELIGIBLE / NOT ELIGIBLE  -  reason |
858: | Claim | Quantified? | Why it might be inflated | Selected for Field 6? |
859: |---|---|---|---|
860: | | | | |
866: 6. WHICH CLAIM IS THIS AUDIT EVALUATING?
934: REQUIRED OUTPUT TABLE
936: | Field | Content | Verification state |
937: |---|---|---|
938: | 1. Literally measured | | |
939: | 2. Source's strongest claim | | |
940: | 3. Weaker defensible claim | | |
941: | 4. Downstream claim | | |
942: | 5A. Within-source inflation point + failure location | | |
943: | 5B. Downstream inflation point + failure location | | |
944: | 6. Claim under audit | | |
946: REQUIRED CONSTRUCT-SIDE HANDOFF SUB-SCHEMA
950: | Check | Object | Retrieval status / basis | Result | Verification state | Evidence |
951: |---|---|---|---|---|---|
952: | Construct establishment | PREVALENCE | ESTABLISHED-REPORTED / ESTABLISHED-CITED / ASSERTED / UNKNOWN | mapped content | | |
953: | Construct establishment | FORM | ESTABLISHED-REPORTED / ESTABLISHED-CITED / ASSERTED / UNKNOWN | mapped content | | |
954: | Construct establishment | DOMAIN | ESTABLISHED-REPORTED / ESTABLISHED-CITED / ASSERTED / UNKNOWN | mapped content | | |
955: | Construct establishment | WRONGNESS | ESTABLISHED-REPORTED / ESTABLISHED-CITED / ASSERTED / UNKNOWN | mapped content | | |
956: | Construct establishment | HARM | ESTABLISHED-REPORTED / ESTABLISHED-CITED / ASSERTED / UNKNOWN | mapped content | | |
957: | Definition-operationalization | instrument / scale / coding rule | ITEMS-RETRIEVED / ITEMS-INFERRED | coextensive / narrower / broader / UNKNOWN | | |
958: | Grade-before-assert | specific sub-claim | source retrieval basis | ESTABLISHED-FALSE / GRADE-CONTESTED / FRINGE / ESTABLISHED-ACCURATE | | |
979: 1. EXTRACT, DO NOT EVALUATE.
994: 3. PRESERVE THE SOURCE'S HEDGES EXACTLY IN FIELD 2.
999: 4. SEARCH FOR DOWNSTREAM USES; DO NOT INVENT THEM.
1015: 5. IF THE MAP IS AMBIGUOUS, SAY SO RATHER THAN RESOLVING IT.
```

## prompts/5-voice-restoration.txt

```text
1: VOICE RESTORATION / ANTICIPATORY COMPLIANCE AUDIT PROMPT
15: PROMPT IDENTITY MARKERS
22: 1. RECORD THE INSTRUMENT ACTUALLY IN CONTEXT.
39: 2. MUTABLE-REFERENCE / CURRENCY RULE.
67: 3. VERSION-COLLISION ATTRIBUTION GATE.
94: 4. DISPOSITION.
107: 5. REQUIRED RUN-HEADER LINE.
223: 1. Executive summary
232: 2. Phrase inventory
241: 3. Hotspot table
257: 4. Stronger terminology suggestions
268: 5. Good caveats to preserve
274: 6. Final voice-restoration pass
286: 7. Manual review warning
```

## prompts/media-analysis/2-coverage-network.txt

```text
52: PROMPT IDENTITY MARKERS
64: 1. RECORD THE INSTRUMENT ACTUALLY IN CONTEXT.
81: 2. MUTABLE-REFERENCE / CURRENCY RULE.
109: 3. VERSION-COLLISION ATTRIBUTION GATE.
136: 4. DISPOSITION.
149: 5. REQUIRED RUN-HEADER LINE.
241: REQUIRED PRIOR MAP
243: | Prior ID | Exact operator proposition | Proposition type | Quantifier / threshold | Exact coverage object | Unit of analysis | Eligible denominator rule | Retrieval question | Required evidence | Resolution |
244: |---|---|---|---|---|---|---|---|---|---|
246: PROPOSITION TYPES
248: 1. COVERAGE-DISTRIBUTION PREDICTION
252: 2. COVERAGE-CONSTRUCTION PREDICTION
256: 3. FACTUAL PREMISE
259: 4. COUNTERFACTUAL OR COMPARATOR CLAIM
263: 5. CAUSAL OR MOTIVE CLAIM
266: 6. NORMATIVE JUDGMENT
270: MANDATORY RULES
272: A. PRESERVE QUANTIFIERS
300: B. DEFINE DENOMINATOR ELIGIBILITY
315: C. DO NOT MERGE DISTINCT OBJECTS
331: D. SEPARATE COVERAGE CLAIMS FROM UNDERLYING-TRUTH CLAIMS
344: E. ALLOW ONE PRIOR TO PRODUCE MULTIPLE LEADS
364: F. PRESERVE CONDITIONAL STRUCTURE
371: G. MATCH EVIDENCE TO THE EXACT PREDICATE
388: H. TRANSLATE LOADED LANGUAGE WITHOUT WEAKENING THE PREDICTION
403: I. RESOLVE EACH PRIOR BEFORE AGGREGATING
420: | Prior ID | Exact proposition | Result | Corpus count / evidence | Qualification |
421: |---|---|---|---|---|
435: J. COUNTEREXAMPLES NARROW; THEY DO NOT AUTOMATICALLY FALSIFY
447: PRIOR-MATCH OUTPUT
473: MAPPING INTEGRITY CHECK
486: EXECUTION GATE
504: INVESTIGATION AND RESOLUTION MECHANICS
508: INVESTIGATION REGISTER AND LEAD ORIGIN
524: | Lead ID | Origin | Initial formulation | Trigger | Retrieval question | Resolution |
525: |---|---|---|---|---|---|
538: BALANCED HYPOTHESIS RETRIEVAL
553: 1. Translate the lead into one or more falsifiable retrieval questions.
554: 2. Document the search performed for evidence that would SUPPORT it.
555: 3. Document the search performed for evidence that would WEAKEN, REFRAME, or
557: 4. Apply comparable effort to both search directions.
558: 5. Do not resolve the lead until both search paths are documented.
559: 6. Searching only for confirming evidence is a procedural failure.
561: | Lead ID | Supporting search | Weakening / disconfirming search | Evidence recovered | Missing evidence |
562: |---|---|---|---|---|
572: BOUNDED EMERGENT LEADS
587: | Trigger inside current object | Why necessary | Scope boundary | Supporting search | Weakening search |
588: |---|---|---|---|---|
593: SHARED INNOCENT-EXPLANATION TEST
614: | Candidate explanation | Evidence supporting it | Evidence weakening it | Residual difference |
615: |---|---|---|---|
621: REFRAMED RESOLUTION STATE
629: 1. ORIGINAL FORMULATION
630: 2. EVIDENCE-SUPPORTED REFORMULATION
631: 3. WHAT MOVED
632: 4. WHY THE OTHER RESOLUTION STATES ARE LESS ACCURATE
642: CONFIRMED / FALSIFIED / RECLASSIFIED / NETWORK-WIDE /
651: COMPACT MEDIA PRIMITIVE
672: EVENT CLASSIFICATION
681: ROLE-AND-STATUS
685: BLAME / RESPONSIBILITY
693: LEADERSHIP / POLICY
699: EPISTEMIC LEVEL - CAUSE AND BLAME
722: VERB-AS-TRACE
747: BRANCH-SPECIFIC LAYERS
765: COMPANION RETRIEVAL
775: MECHANICAL TRIGGERS
783: JUDGMENT-REQUIRING TRIGGERS
810: | Companion item | Trigger (A-D) | Dependency in audited coverage | Retrieval result | Effect on finding |
811: |---|---|---|---|---|
817: PACKET-BOUNDARY OUTPUT
830: CONTEXT-SUPPORTED IDENTITY INFERENCE
841: INFERENCE LADDER
867: FORMAL-CONTROL EVIDENCE FLOOR
879: MANDATORY INFERENCE-PARITY CHECK
884: 1. ENUMERATE THE ORIGINAL INDICATORS
887: 2. STATE THE EXACT INFERENCE
891: 3. BUILD THE MIRROR CANDIDATE
896: 4. APPLY THE SAME LADDER
900: 5. EXPLAIN ANY DIFFERENT RESOLUTION
905: 6. REMOVE DIRECTIONAL FRAMING
909: 7. CONSEQUENCE
922: NO VALID MIRROR
931: | Candidate | Retrieved indicators | Ladder classification | Evidentiary distinction |
932: |---|---|---|---|
933: | Original | | | |
934: | Mirror | | | |
945: WEAK-RESEMBLANCE LIMIT
956: QUOTATION-PAIR PRESERVATION
968: | Quotation A | Quotation B | Speaker / source | Evidentiary stage | Material contrast |
969: |---|---|---|---|---|
993: SECTION A  -  COVERAGE INVENTORY
996: | Outlet | Headline | Pub date/time | Last updated | Correction note? | Headline changed? | Social/homepage headline if different | Byline | Wire attribution | Word count | Lead image subject |
997: |---|---|---|---|---|---|---|---|---|---|---|
1013: SECTION B  -  SOURCE CHAIN  (highest-value section)
1018: | Outlet | Named sources | Primary docs cited | Original reporting? | Traces to |
1019: |---|---|---|---|---|
1043: 1. That direction carries no meaning, and the whole-coverage count is not comparable
1064: | Fact or claim | Pieces asserting it | Origins located | Origin completeness | Single-origin confirmed? | Origin authority | Claim contestability | Attribution behavior | Apparent-corroboration risk | Network classification |
1065: |---|---:|---:|---|---|---|---|---|---|---|
1095: ORIGIN AUTHORITY IS PROPOSITION-SPECIFIC
1109: PERMITTED NETWORK CLASSIFICATIONS
1111: COMMON-SOURCE PROPAGATION
1126: SOURCE-DEPENDENT INTERPRETATION
1139: CLAIM AMPLIFICATION
1143: 1. The claim concerns a disputed, uncertain, inferential, causal, quantitative,
1145: 2. The originating source is not independently authoritative to establish that
1147: 3. Multiple pieces repeat the claim from the same origin in a way that may create
1159: CROSS-OUTLET CORROBORATION
1164: CONTESTED
1168: CHAIN UNRESOLVED
1173: APPARENT-CORROBORATION RISK
1185: RULES FOR THE TABLE
1198: FINDING CONSEQUENCES
1258: EVENT OBJECT CONSTRUCTION AND EXTRACTION
1262: PARTY ENUMERATION
1295: | Party / object | Why analytically significant | Relevant outlets / sources | Planned analysis location |
1296: |---|---|---|---|
1303: COMPETING EVENT CLASSIFICATIONS
1311: | Classification | Outlet / source | Placement | Attribution status | Facts available when used | Dimension captured | Dimension omitted |
1312: |---|---|---|---|---|---|---|
1330: FUNCTION / STRUCTURE COMPLETENESS TEST
1343: | Label | Function captured | Structure captured | Function omitted | Structure omitted | Complete enough to govern event identity? |
1344: |---|---|---|---|---|---|
1360: SCOPE LIMIT
1378: SAME-STAGE CLASSIFICATION TEST
1390: | Label | Evidentiary stage | Dimension captured | Dimension omitted | Attribution status | Timing explains difference? | Residual divergence |
1391: |---|---|---|---|---|---|---|
1421: FINDING OWNERSHIP FOR EVENT CLASSIFICATION
1444: SECTION C  -  SHARED FACTUAL CORE vs. UNIQUE MATERIAL
1464: | Fact | Outlets reporting | Outlets omitting | Scoop or selection | Cuts which way |
1465: |---|---|---|---|---|
1475: | Fact / source material | Available when A published? | B? | C? | D? |
1476: |---|---|---|---|---|
1482: ABSENCE-CLAIM EVIDENCE FLOOR
1505: MANDATORY AVAILABILITY CITATION FOR SELECTION CLAIMS
1566: EVIDENTIARY FLOOR
1592: PROMINENCE TABLE
1595: | Piece | Fact / dimension carried | Placement (headline / lede / body para n) | Competing fact / dimension occupying the more prominent layer | Packaging provenance | Cuts which way |
1596: |---|---|---|---|---|---|
1745: 1. State the foregrounded fact/dimension.
1746: 2. State the subordinated or qualifying fact/dimension.
1747: 3. Search the eligible comparison set for a reversed prominence relationship.
1748: 4. Classify the inverse:
1761: 5. Name the inverse piece(s), where present.
1798: SEMANTIC-GATE INTERACTION
1938: | Underlying event/action | Common bucket | Candidate specificity / outliers | Resolution |
1939: |---|---|---|---|
2094: | Outlier | Added semantic predicate | Assignment moved | Direction of movement | Why not bucketed / earned |
2095: |---|---|---|---|---|
2193: WORKED EXAMPLES
2266: LANGUAGE TRAJECTORY AND DESCRIPTIVE TREATMENT
2270: LANGUAGE TRAJECTORY AND UPDATE TEST
2293: SINGLE-EVENT RULE
2308: CORPUS-LEVEL HYPOTHESIS FORM
2319: UPDATE TRIGGER AND PERSISTENCE
2323: UPDATE TRIGGER
2328: PERSISTENCE
2338: | Party | Prior package | Update trigger | Later package | Persistence result | Residual issue |
2339: |---|---|---|---|---|---|
2348: LANGUAGE PACKAGE
2387: COMPOSITE ANALYSIS RULE
2407: ADAPTIVE DETAIL
2414: | Party | Label trajectory | Package direction (SOFT / MIXED / HARD / NEUTRAL) | Update behavior |
2415: |---|---|---|---|
2435: COUNTERPART AND AFFECTED-PARTY TREATMENT
2455: LANGUAGE-PACKAGE FINDINGS
2482: FINDING OWNERSHIP
2493: SEVERITY FACTORS
2513: LANGUAGE-TRAJECTORY EXECUTION GATE
2518: 1. Output the compressed Language Trajectory table from ADAPTIVE DETAIL for EVERY party
2521: 2. For each party, state whether full LANGUAGE PACKAGE expansion is required.
2523: 3. If no party qualifies for full expansion, state exactly:
2529: 4. If one or more parties qualify, complete the full language-package schema for
2543: SECTION D  -  FRAMING DIVERGENCE MAP
2584: | Attribute / context element | Outlet A | Outlet B | Outlet C | ... |
2585: |---|---|---|---|---|
2621: TEST THE SOURCE OF THE UNIFORMITY - CANONICAL FIVE-WAY CLASSIFICATION
2649: D-ROLE - CAUSAL AND ROLE-ASSIGNMENT MAP
2681: | Outlet | EVENT CLASSIFICATION (+ provenance) | CAUSE (+ epistemic level + provenance) | ROLE-AND-STATUS (+ provenance) | BLAME / RESPONSIBILITY (+ epistemic level + provenance) | REMEDY (+ provenance) | LEADERSHIP / POLICY (+ provenance) | Text basis |
2682: |---|---|---|---|---|---|---|---|
2684: TEXT BASIS
2693: CAUSE AND BLAME - EPISTEMIC LEVEL
2807: READ-NOT-SCORED
2820: | Figure | Outlet | Baseline / denominator | Raw or rate | Adjustment applied | Impression supported |
2821: |---|---|---|---|---|---|
2832: SECTION D2  -  CROSS-BRANCH RESOLUTION  (run if a single-piece audit preceded this)
2924: | Single-piece finding | What it flagged as undeterminable | What this sample shows | Resolution |
2925: |---|---|---|---|
2936: INDEPENDENT-EDITORIAL-CONVERGENCE / WIRE-INHERITANCE /
2937: COMMON-PRIMARY-SOURCE / LEGAL/PROFESSIONAL-CONVENTION /
2973: SECTION E  -  CLUSTERING AND CORRELATION
2994: SECTION E2  -  MAPPED PRIOR-MATCH CHECK  (MANDATORY BEFORE FLIP TEST)
3016: 1. Reproduce the completed PRIOR DECOMPOSITION AND MAPPING map.
3017: 2. Resolve every Prior ID separately.
3018: 3. Preserve the exact quantifier, denominator, eligible-source rule, and
3020: 4. Do not collapse the priors into one synthetic prediction.
3021: 5. Do not substitute:
3029: | Prior ID | Exact proposition | Eligible denominator | Threshold | Count / evidence | Result | Qualification |
3030: |---|---|---|---|---|---|---|
3084: SECTION F  -  FLIP TEST  (MANDATORY  -  DESIGNED TO BE COSTLY)
3116: | Observation | Type (A / B) | Resolution |
3117: |---|---|---|
3123: | Rank (1 = most prior-dependent) | Finding | Why more prior-dependent than the next |
3124: |---|---|---|
3151: | Finding | Mirror written? | Findings against mirror | Contradiction w/ mirror principle? | Prior-dependence rank | Verdict |
3152: |---|---|---|---|---|---|
3157: SECTION G  -  SAMPLE AUDIT  (audits your own selection)
3193: | Finding | Comparison cluster required | Cluster present in sample? | Full-text sources in cluster | Claim supportable? |
3194: |---|---|---|---:|---|
3205: SECTION H  -  STANDARDIZED FINDING TABLE
3208: | Field | Entry |
3209: |---|---|
3210: | Finding | one sentence |
3211: | Section | A-E |
3212: | Evidence | side-by-side quotes, outlet names, paragraph positions |
3213: | Finding type | common-source-propagation / source-dependent-interpretation / claim-amplification / source-chain / selection / prominence-packaging / framing-divergence / causal-role-framing / event-classification-divergence / language-package-divergence / clustering |
3214: | Severity | none / minor / moderate / major / severe |
3215: | Survives flip test | yes / no |
3216: | Sample-dependent? | yes / no  -  would it hold with a different sample? |
3217: | Possible innocent explanation | MANDATORY  -  deadline, length, wire dependence, house style, genuine scoop. "None identified" if none. Never blank. |
3218: | Availability row cited | REQUIRED for any SELECTION (cross-piece omission) claim; exact fact/source availability time and outlet publication time. Write NOT APPLICABLE for all non-selection findings, INCLUDING prominence-packaging findings — for prominence, the fact's presence in the FULL-TEXT-CONFIRMED piece establishes possession; no cross-piece Availability Matrix row exists or is required. |
3219: | What would weaken this | MANDATORY |
3220: | Verification state | from vocabulary |
3262: SECTION I  -  VERDICT
3265: RETRIEVAL DEPTH  -  REPORT BEFORE THE VERDICT
3324: FINAL REQUIRED STATEMENT  -  one of:
3346: SCOPE LIMITS  -  RESTATE IN OUTPUT
```

## prompts/media-analysis/2-framing-construction.txt

```text
16: PROMPT IDENTITY MARKERS
23: 1. RECORD THE INSTRUMENT ACTUALLY IN CONTEXT.
40: 2. MUTABLE-REFERENCE / CURRENCY RULE.
68: 3. VERSION-COLLISION ATTRIBUTION GATE.
95: 4. DISPOSITION.
108: 5. REQUIRED RUN-HEADER LINE.
131: WHAT THIS AUDITS  -  AND WHAT IT DOES NOT
196: COMPACT VOCABULARY
241: EVENT CLASSIFICATION
250: ROLE-AND-STATUS
254: BLAME / RESPONSIBILITY
262: LEADERSHIP / POLICY
268: EPISTEMIC LEVEL - CAUSE AND BLAME
291: VERB-AS-TRACE
309: BRANCH-SPECIFIC LAYERS
353: SECTION 0  -  GENRE / FORMAT GATE  (run first)
397: SECTION A  -  BASELINE: WHAT IS ESTABLISHED VS. WHAT IS ASSERTED
410: | Statement | Layer (asserted / attributed / characterization / quote) | Verification state |
411: |---|---|---|
419: SECTION B  -  HEADLINE & PACKAGING
437: SECTION C  -  SEQUENCING
442: | paragraph  | Content | Function (scene / reaction / justification / context / attribution) |
443: |---|---|---|
457: SECTION D  -  AGENCY AND VERB ASYMMETRY
462: | Party | Verbs / constructions used | Active or passive | Vivid or clinical |
463: |---|---|---|---|
487: SECTION E  -  ATTRIBUTION ASYMMETRY
499: SECTION E2  -  NARRATIVE FLAGS, CAUSAL BRIDGES & ATMOSPHERIC CUES
502: WHY THIS IS ORGANIZED AS A TRIAD
583: AXIS OWNERSHIP
606: CAUSE AND BLAME - EPISTEMIC LEVELS
647: | Attribute | Known at pub? | Treatment | First appears | Outlet voice or quote? | Material relevance |
648: |---|---|---|---|---|---|
670: VERB-AS-TRACE
730: | Wording used | Synonym only? | Bridge type (sequence/mechanism/attributed) | Added or removed? | Whose explanation? | Effect on reader's model |
731: |---|---|---|---|---|---|
782: | Figure cited | Baseline / denominator used | Alternative available | Consistent across the argument? | Would it change the impression? |
783: |---|---|---|---|---|
831: | Party | Named? | Biography | Visual detail | Emotional detail | Vividness type | Group/status label | Historical association |
832: |---|---|---|---|---|---|---|---|
904: SECTION F  -  SOURCE DISTRIBUTION
920: | Voice | Affiliation / position | Space given | Position advanced |
921: |---|---|---|---|
924: SECTION F2  -  QUOTE FUNCTION & ATTRIBUTED FRAME
941: | Quote (short) | Speaker | FACT-SOURCE (what happened) | FRAME-CARRIER (what it means) | Both | Words |
942: |---|---|---|---|---|---|
1050: | Source | Statements reported | Which foregrounded | Fact or frame | Authority multiplier? |
1051: |---|---|---|---|---|
1122: SECTION G  -  OMISSION AND DE-EMPHASIS  (two distinct finding types)
1153: | Fact | OMITTED or DE-EMPHASIZED | If de-emphasized: where it appears (paragraph  + quote) | Material because | Available at press time? | Effect |
1154: |---|---|---|---|---|---|
1163: SECTION H  -  PATTERN LINKAGE
1221: SECTION I  -  TIMING TEST  (MANDATORY INNOCENT-EXPLANATION CHECK)
1249: | Finding | Timing-explained? | Reasoning |
1250: |---|---|---|
1264: SECTION I2  -  PRIOR-MATCH CHECK  (MANDATORY, run before the flip test)
1311: SECTION J  -  FLIP TEST  (MANDATORY  -  DESIGNED TO BE COSTLY)
1397: | Rank (1 = most prior-dependent) | Finding | Why more prior-dependent than the next |
1398: |---|---|---|
1447: | Finding | Mirror written? | Findings against mirror | Contradiction w/ mirror principle? | Prior-dependence rank | Verdict |
1448: |---|---|---|---|---|---|
1457: SECTION K  -  STANDARDIZED FINDING TABLE
1462: | Field | Entry |
1463: |---|---|
1464: | Finding | one sentence |
1465: | Section | B / C / D / E / F / G / H |
1466: | Evidence | specific text, paragraph number, verb, quote |
1467: | Media finding type | factual / construction / omission / sourcing / frame-laundering / causal-bridge / causal-role-framing / narrative-flag / baseline / packaging / none |
1468: | Failure location (if applicable) | PR-media / paper / model-retrieval / mixed |
1469: | Severity | none / minor / moderate / major / severe |
1470: | Survives timing test | yes / no |
1471: | Survives flip test | yes / no |
1472: | Possible innocent explanation | MANDATORY  -  strongest non-damning reading. "None identified" if none. Never blank. |
1473: | What would weaken this | MANDATORY  -  specific evidence that would undercut it |
1474: | Verification state | from vocabulary |
1492: SECTION L  -  VERDICT
1495: RETRIEVAL DEPTH  -  REPORT BEFORE THE VERDICT
1640: FINAL REQUIRED STATEMENT  -  one of: "This piece is factually [accurate/flawed] and its
1648: SCOPE LIMITS  -  STATE THESE IN THE OUTPUT
```

## prompts/research-analysis/2-citation-network.txt

```text
16: PROMPT IDENTITY MARKERS
23: 1. RECORD THE INSTRUMENT ACTUALLY IN CONTEXT.
40: 2. MUTABLE-REFERENCE / CURRENCY RULE.
68: 3. VERSION-COLLISION ATTRIBUTION GATE.
95: 4. DISPOSITION.
108: 5. REQUIRED RUN-HEADER LINE.
147: IMPORTANT DEFINITION
172: HOW TO USE THIS PROMPT
175: 1. A one-paragraph description of the field or subfield.
176: 2. The central contested claim.
177: 3. Any founding papers or review papers you already know.
178: 4. Any adjacent fields you suspect were ignored.
179: 5. Any databases or citation sources available to you.
186: INPUT TEMPLATE
206: SHARED CLAIM MAP  -  REQUIRED FOR FULL-SEQUENCE MODE
212: DEGRADED STANDALONE MODE  -  USE ONLY WHEN NO UPSTREAM MAP EXISTS
314: 1. Never report a verification state above what was actually checked.
315: 2. Evidence type and verification state are separate axes; report both.
316: 3. FULL-TEXT-CONFIRMED and RECEPTION-CONFIRMED may both apply.
317: 4. Apply the ladder symmetrically to sources supporting and opposing the claim.
318: 5. A PROVISIONAL source or network metric may not anchor a MAJOR or FATAL finding.
333: DATA-HONESTY RULES
357: RECEPTION-MODULE CONFIRMATION RULE
391: NO-ASSUME-SUPPRESSION
400: OUTPUT EXECUTION CONTRACT  -  REQUIRED
408: REVISION-CANDIDATE CHECKER BOUNDARY
418: VALIDATION BOUNDARY
429: LOCAL REPAIR  -  DO NOT PROPAGATE BY DEFAULT
439: EXACT-HEADING RULE
481: NO SILENT MERGING
487: PRE-AUDIT CLAIM CONFIRMATION
492: SECTION A: CITATION NETWORK STRUCTURE AND CARTEL DETECTION
494: GRAPH CORPUS AND RECEIPTS
515: DENSITY INFERENCE SCOPE
524: 1. What are the top 50 most-cited papers on the central claim? List at least the top 10-15
533: 2. Of the top 50, what percentage of citations appear internal to this set? That is: how many
536: 3. Calculate the mutual citation rate: How many papers in the top 50 cite at least 3-5 other
539: 4. Identify the founding cluster: Is there a small founding cluster, typically 3-8 papers,
542: 5. What percentage of total citations in the network still flow back to this founding cluster?
544: 6. In the last 5 years, what are the most-cited new papers on the claim?
546: 7. Do recent papers primarily cite:
554: 8. Do the last 5 years show continued self-reinforcement of the original cluster, or genuine
557: 9. Is there one main review paper or synthesis paper functioning as an amplification hub?
559: 10. If yes, what does the hub do?
568: SECTION B: EVIDENCE TYPE CODING
586: 11. What percentage of the network's authority rests on direct empirical tests of the central
589: 12. What percentage rests on reviews, proxies, theory papers, qualitative studies, or
592: 13. How many papers directly measure the target construct at the relevant level of analysis?
594: 14. How many papers use proxy measures?
596: 15. How many papers are cited as if they answer the central claim despite measuring something
599: 16. Is the network evidence-rich or citation-rich?
603: SECTION C: CITATION POLARITY AND CLAIM USE
616: 17. For the top 15 papers, classify how they cite the founding cluster.
618: 18. What percentage of citations to the founding cluster are supportive or premise-building
621: 19. What percentage are merely background citations?
623: 20. Are there any serious critical citations inside the dominant network?
625: 21. If critiques exist, are they engaged substantively or cited and dismissed?
627: 22. Does the network preserve the original limitations of key studies, or drop the limitations
632: SECTION D: CLAIM MUTATION TRACKING
641: 23. What did the original source actually claim?
643: 24. What did the first major review or hub paper say the original source showed?
645: 25. How do later papers restate the review?
647: 26. Does a narrow finding become generalized?
649: 27. Does "evidence consistent with X" become "X is established"?
651: 28. Does "no effect in one proxy task" become "no meaningful difference in the real-world
654: 29. Do caveats disappear after one or two citation steps?
656: 30. Does the claim become stronger through repetition than it was in the original methods?
672: SECTION E: ADJACENT FIELD ENGAGEMENT / NEGLECT
677: 31. LOCK THE CLAIM LAYERS.
690: 32. STATE THE STRONGEST PLAUSIBLE RIVAL EXPLANATION.
697: 33. STATE THE ADJUDICATING OBSERVATIONS.
707: 34. GENERATE CANDIDATE FIELDS FROM BOTH EXPLANATIONS.
713: 35. APPLY THE SAME CORE QUALIFICATION TEST.
737: 36. MERGE, DEDUPLICATE, AND LOCK THE LIST.
771: 37. RUN THE LIST-GENERATION FLIP TEST.
781: 38. ONLY NOW INSPECT THE CITATION RECORD.
812: 39. TEST INNOCENT EXPLANATIONS.
850: RC-ONLY ADJACENCY REFINEMENTS FOR THE IAT VALIDATION RUN
859: SECTION F: HUB DEPENDENCY AND REVIEW-PAPER LAUNDERING
861: 40. Identify the main hub paper or review article.
863: 41. What percentage of recent papers cite the hub?
865: 42. What percentage cite the original primary studies directly?
867: 43. What percentage cite the hub instead of inspecting the underlying evidence?
869: 44. Does the hub accurately represent the original studies' methods and limits?
871: 45. Does the hub simplify or overstate the original evidence?
873: 46. Does the hub cite adjacent literatures?
875: 47. Does the hub become the field's substitute for direct empirical evidence?
890: SECTION G: PATTERN RECOGNITION AND RATCHET BEHAVIOR
892: 48. Does the literature treat proxy measures as equivalent to the actual construct?
894: 49. Does it export findings from low-stakes, lab, amateur, convenience, or administrative
897: 50. Has the field ignored natural experiments or long-running interventions that test its
900: 51. When predictions fail, does the field update the model?
902: 52. Or does the field expand the intervention and reinterpret failure as evidence that more
905: 53. Does the field specify falsification criteria?
907: 54. Does the field identify what evidence would change its conclusion?
909: 55. Does the intervention improve the measured metric while leaving the underlying construct
912: 56. Does the citation network reward papers that expand the premise more than papers that test
915: RATCHET SCORING ROUTE
927: MODEL-IDENTITY AND TEMPORAL GATE
943: SECTION H: IGNORED CRITIQUE AND NON-UPTAKE
950: 1. PRECONDITION ASSESSMENT.
955: 2. CRITIQUE RETRIEVAL.
959: 3. RECEPTION OPPORTUNITY.
963: 4. UPTAKE TEST.
978: 57. Identify serious critiques, failed replications, natural experiments, practitioner
981: 58. Are these critiques cited by the dominant cluster?
983: 59. If cited, are they:
991: 60. Did the citation network update after the critique appeared?
993: 61. Did recent papers incorporate the critique into methods or continue citing the old premise
996: 62. Are practitioner or domain-expert warnings visible in forums, trade publications,
999: 63. If yes, did those warnings affect the academic citation network?
1017: SECTION I: AUTHOR, INSTITUTION, JOURNAL, AND FUNDING CLUSTERING
1019: 64. Are the same authors or coauthors recurring across the founding cluster?
1021: 65. Are the same journals, conferences, departments, labs, or institutions recurring?
1023: 66. Are the same funding sources, NGOs, advocacy organizations, government agencies, or policy
1026: 67. Does the intellectual network overlap with a social, institutional, funding, or policy
1029: 68. Are dissenting papers published in the same venues, or pushed to peripheral venues?
1031: 69. Does gatekeeping appear explicit, or is the closure functional?
1033: 70. Are there signs of ideological or policy alignment that shape what gets cited?
1048: SECTION J: FALSE-POSITIVE AND BASELINE CHECK
1053: 71. Is this field small enough that dense internal citation would be expected?
1055: 72. Compare the target network with a healthier adjacent subfield of similar size. Is the
1058: 73. Does the target field show less engagement with adjacent expertise than comparable fields?
1060: 74. Are researchers citing each other because they are the only people studying the question,
1063: 75. Does the founding cluster rest on strong primary empirical evidence?
1065: 76. Are the central claims directly tested repeatedly by independent groups?
1067: 77. Are limitations preserved downstream?
1069: 78. Are failed predictions acknowledged?
1071: 79. Are critics cited and engaged?
1073: 80. Does the field have a clear mechanism for updating?
1080: SECTION J2: THE CONCEDE TEST
1089: 1. Read the Target claim declared in every proposed standardized finding row. Do not assume
1092: 2. If a row targets a different claim, mark:
1099: 3. Do not count two labels on one underlying mismatch as two independent levers. In
1103: 4. Preserve nested rows when they improve traceability, but count the mechanism once in
1122: | Finding | Declared target claim | Matches map field 6? | Same mechanism as another row? | Count separately? |
1123: |---|---|---|---|---|
1139: | Finding | Concede test: SURVIVES / NARROWS / DEFEATS | Surviving claim if NARROWS |
1140: |---|---|---|
1142: NETWORK-SPECIFIC SCOPE RULE
1152: SCOPE-LOSS ASSESSMENT  -  REQUIRED FOR EVERY NARROWS RESULT
1163: | Finding | Scope-loss level | Original claim | Surviving claim | What epistemic or practical work is lost? |
1164: |---|---|---|---|---|
1166: SCORING AND LABEL MAPPING
1185: SECTION K: CARTEL-RISK SCORING
1202: UNASSESSED
1206: UNINFORMATIVE
1218: FOUR-AXIS RULE
1222: 1. Evidence / claim state: what does the evidence establish? Use the shared verification and
1224: 2. Dimension disposition: can the dimension enter the score? Use SCORED / UNASSESSED /
1226: 3. Ordinal concern: if and only if SCORED, how concerning is it? Use 0 / 1 / 2 / 3.
1227: 4. Aggregation status: does the SCORED dimension independently enter the aggregate? Use
1235: 1. Founding-cluster dominance
1236: 2. Internal citation density
1237: 3. Recent-paper dependence on old cluster
1238: 4. Review-hub laundering
1239: 5. Proxy-to-construct mismatch
1240: 6. Claim mutation downstream
1241: 7. Adjacent-field neglect
1242: 8. Lack of decisive tests
1243: 9. Poor critique uptake
1244: 10. Intervention-evidence ratchet
1245: 11. Model non-updating
1289: PROVISIONAL COVERAGE GATE
1309: PERCENTAGE BANDS
1337: RERUN COMPLETENESS RULE
1349: SCORING DISCIPLINE
1363: RED FLAGS
1382: GREEN FLAGS
1398: REQUIRED FINAL OUTPUTS
1402: ARTIFACT 1: TOP 15 CITATION SPINE TABLE
1409: ARTIFACT 2: FOUNDING CLUSTER TABLE
1415: ARTIFACT 3: RECENT 5-YEAR CITATION BEHAVIOR TABLE
1422: ARTIFACT 4: CITATION POLARITY TABLE
1429: ARTIFACT 5: CLAIM MUTATION TABLE
1436: ARTIFACT 6: ADJACENT-LITERATURE NEGLECT TABLE
1457: ARTIFACT 7: CRITIQUE-UPTAKE TABLE
1465: ARTIFACT 8: CARTEL-RISK SCORECARD
1493: ARTIFACT 9: NETWORK MAP
1513: COMPLETION LEDGER
1520: | Required heading | Exact heading present? | Status: completed / N/A / omitted | Reason or output location |
1521: |---|---|---|---|
1523: MECHANICAL CHECK
1529: COMPLETION GATE
1533: 1. Write: "INCOMPLETE RUN  -  REQUIRED SECTION OMITTED: [heading(s)]."
1534: 2. Do not issue Artifact 10's substantive verdict, cartel-risk label, or confidence level.
1535: 3. In Artifact 10, write only: "WITHHELD  -  completion gate failed."
1536: 4. Do not allow the standardized finding table to imply a completed audit.
1542: ARTIFACT 10: FINAL VERDICT
1620: FINAL SECTION: STANDARDIZED FINDING TABLE
1631: | Field | Entry |
1632: |---|---|
1633: | Finding | One sentence |
1634: | Target claim | Claim map field 6 |
1635: | What was measured | Citation graph, citing contexts, source texts, or other network evidence actually inspected |
1636: | What was claimed | Network, consensus, independence, mutation, or uptake inference |
1637: | Failure mode | source dependence / hub laundering / claim mutation / adjacent-field neglect / critique non-uptake / closure / other taxonomy above |
1638: | Severity | none / minor / moderate / major / fatal-for-strong-claim |
1639: | Concede test | SURVIVES / NARROWS / DEFEATS |
1640: | Scope loss if NARROWS | incidental / material / near-defeat, plus surviving claim |
1641: | Evidence | Graph query, edge list, citation context, passage, table, or source text |
1642: | Evidence type | primary study / replication / meta-analysis / methodological critique / policy document / practitioner / journalism / commentary / theoretical / author inference |
1643: | Verification state | From the compact vocabulary |
1644: | Possible innocent explanation | MANDATORY  -  strongest non-damning reading; if none, write "none identified" |
1645: | What would weaken this | MANDATORY  -  specific evidence that would undercut it |
1646: | Failure location | PAPER / CITATION / PR-MEDIA / MODEL-RETRIEVAL / MIXED |
1647: | Status | confirmed / contested / provisional |
1651: 1. A finding missing either mandatory falsifiability field is not inspectable and may not be
1653: 2. Severity must agree with verification state. A PROVISIONAL finding cannot be MAJOR or
1655: 3. A SURVIVES finding cannot be MAJOR or FATAL and may not anchor the final label.
1656: 4. A NARROWS finding must state the surviving claim and scope-loss level.
1657: 5. Target claim must match field 6 of the shared Claim Map. Use MAP GAP rather than silently
1659: 6. Quantitative and reception claims must preserve their retrieval status. A model-estimated
1661: 7. If no findings of consequence were produced, say so plainly and submit an empty table with
1664: 8. If the Completion Gate failed, state that the run is incomplete. Do not present the table
```

## prompts/research-analysis/2-construct-validity.txt

```text
17: PROMPT IDENTITY MARKERS
25: 1. RECORD THE INSTRUMENT ACTUALLY IN CONTEXT.
42: 2. MUTABLE-REFERENCE / CURRENCY RULE.
70: 3. VERSION-COLLISION ATTRIBUTION GATE.
97: 4. DISPOSITION.
110: 5. REQUIRED RUN-HEADER LINE.
153: HOW TO USE THIS PROMPT
168: 1. The contested claim this source is being used to support.
169: 2. The field or debate where the source is being used.
170: 3. Any domain-specific concern you want tested.
174: INPUT TEMPLATE
206: SHARED CLAIM MAP  -  REQUIRED FOR FULL-SEQUENCE MODE
212: DEGRADED STANDALONE MODE  -  USE ONLY WHEN NO UPSTREAM MAP EXISTS
269: 1. Never report a verification state above what was actually checked.
270: 2. Evidence type and verification state are separate axes; report both.
271: 3. FULL-TEXT-CONFIRMED and RECEPTION-CONFIRMED may both apply.
272: 4. Apply the ladder symmetrically to sources supporting and opposing the claim.
273: 5. A PROVISIONAL source may not anchor a MAJOR or FATAL finding.
295: | Specific figure | Value stated | Verification state | Source |
296: |---|---|---|---|
322: CANONICAL CONSTRUCT PROPERTIES
348: MAP / PROSECUTOR DIVISION
375: HARD RULE
435: AUDIT INSTRUCTIONS
454: APPLICABLE-CHECKS NOTE
469: 1. CLAIM MAP (received; degraded fallback only when absent)
514: | Property | Claim-map status | Does the normative / causal claim depend on it? | ESTABLISHED-CITED prosecutor split | Evidence and exact inferential load | Finding disposition |
515: |---|---|---|---|---|---|
516: | PREVALENCE | | | uncontested-in-respect-required / contested-in-respect-required / N/A | | |
517: | FORM | | | uncontested-in-respect-required / contested-in-respect-required / N/A | | |
518: | DOMAIN | | | uncontested-in-respect-required / contested-in-respect-required / N/A | | |
519: | WRONGNESS | | | uncontested-in-respect-required / contested-in-respect-required / N/A | | |
520: | HARM | | | uncontested-in-respect-required / contested-in-respect-required / N/A | | |
522: 1. DEPENDENCE
528: 2. RETRIEVAL CAP
538: 3. ESTABLISHED-CITED PROSECUTOR SPLIT
559: 4. NOT-FIRING CONDITION - MANDATORY
568: 5. CONCEDE TEST
575: 6. OUTPUT OWNERSHIP
586: 2. MEASUREMENT EXTRACTION
649: 3. CLAIM VS. MEASUREMENT TABLE
681: 4. LEVEL-OF-ANALYSIS CHECK
722: 5. CONFOUND AUDIT
749: 6. ECOLOGICAL VALIDITY CHECK
772: 7. DECISIVE-TEST CHECK
792: 8. CROSS-REANALYSIS OBJECT CHECK
817: 9. CITATION-USE AUDIT
841: 10. IGNORED-LITERATURE CHECK
865: 11. EVIDENCE-TYPE, VERIFICATION, AND FAILURE-LOCATION CHECK
870: A. Evidence type:
882: B. Measurement role:
893: C. Verification state:
898: D. Failure location:
904: | Claim or evidence item | Evidence type | Measurement role | Verification state | Failure location | Directly measured / inferred / speculative | Source audit required? |
905: |---|---|---|---|---|---|---|
916: 12. INTERNAL CONSISTENCY CHECK
935: 13. THE CONCEDE TEST
952: | Finding | Concede test: SURVIVES / NARROWS / DEFEATS | Surviving claim if NARROWS |
953: |---|---|---|
964: SCOPE-LOSS ASSESSMENT  -  REQUIRED FOR EVERY NARROWS RESULT
981: | Finding | Scope-loss level | Original claim | Surviving claim | What practical or inferential work is lost? |
982: |---|---|---|---|---|
1002: 14. VERDICT
1015: A. Valid evidence for the residual claim. B. Partial evidence with clear limits. C. Useful for
1039: 15. PAPER-SAFE WORDING
1043: A. Neutral summary sentence:
1047: B. Direct methodological critique:
1051: C. Strong adversarial version:
1055: D. Decisive-test sentence:
1061: 16. FAILURE-MODE CLASSIFICATION
1124: 17. FINAL OUTPUT FORMAT
1179: FINAL SECTION: STANDARDIZED FINDING TABLE
1190: | Field | Entry |
1191: |---|---|
1192: | Finding | One sentence |
1193: | Target claim | Claim map field 6 |
1194: | What was measured | Actual operationalization |
1195: | What was claimed | Assertion the measurement is used to support |
1196: | Failure mode | Select one canonical value from Section 16 |
1197: | Failure-mode subtype | e.g. definitional scope creep, or N/A |
1198: | Severity | none / minor / moderate / major / fatal-for-strong-claim |
1199: | Concede test | SURVIVES / NARROWS / DEFEATS |
1200: | Scope loss if NARROWS | incidental / material / near-defeat, plus surviving claim |
1201: | Construct property | prevalence / form / domain / wrongness / harm / N/A |
1202: | Construct-property status | ESTABLISHED-REPORTED / ESTABLISHED-CITED / ASSERTED / UNKNOWN / N/A |
1203: | ESTABLISHED-CITED prosecutor split | uncontested-in-respect-required / contested-in-respect-required / N/A |
1204: | Operationalization retrieval basis | ITEMS-RETRIEVED / ITEMS-INFERRED / N/A |
1205: | Operationalization scope result | coextensive / narrower / broader / UNKNOWN / N/A |
1206: | P2 belief grade | ESTABLISHED-FALSE / GRADE-CONTESTED / FRINGE / ESTABLISHED-ACCURATE / N/A |
1207: | P2 strength gate | STRONG / WEAK / VOID / N/A |
1208: | Evidence | Section, table, figure, passage, or data |
1209: | Evidence type | primary study / replication / meta-analysis / methodological critique / policy document / practitioner / journalism / commentary / theoretical / author inference |
1210: | Verification state | Evidence-quality state from the compact vocabulary |
1211: | Possible innocent explanation | MANDATORY - strongest non-damning reading; if none, write "none identified" |
1212: | What would weaken this | MANDATORY - specific evidence that would undercut it |
1213: | Failure location | PAPER / CITATION / PR-MEDIA / MODEL-RETRIEVAL / MIXED |
1214: | Finding disposition | CONFIRMED / CONTESTED / PROVISIONAL |
1216: AXIS DEFINITIONS
1240: 1. A finding missing either mandatory falsifiability field is not inspectable and may not be
1242: 2. Severity must agree with verification state, construct-side retrieval
1246: 3. A SURVIVES finding cannot be MAJOR or FATAL and may not anchor the verdict.
1247: 4. A NARROWS finding must state the surviving claim and scope-loss level. A merely incidental
1249: 5. Target claim must match field 6 of the shared Claim Map. Use MAP GAP rather than silently
1251: 6. If no findings of consequence were produced, say so plainly and submit an empty table with
```

## prompts/research-analysis/2-internal-validity.txt

```text
15: PROMPT IDENTITY MARKERS
22: 1. RECORD THE INSTRUMENT ACTUALLY IN CONTEXT.
39: 2. MUTABLE-REFERENCE / CURRENCY RULE.
67: 3. VERSION-COLLISION ATTRIBUTION GATE.
94: 4. DISPOSITION.
107: 5. REQUIRED RUN-HEADER LINE.
151: 1. Foundational paper(s) or analysis: [Paste citation, abstract, methods, results, and
154: 2. Central empirical finding (fallback context if no upstream Claim Map is supplied): [State
157: 3. Claimed construct and downstream use: [What is this finding used to prove in subsequent
160: 4. Known replication attempts (if any): [Paste citations and outcomes if known. If none known,
162: 5. Pre-registration status (if known): [Was the study pre-registered? At what stage? Did the
164: 6. Optional construct-validity audit output: [Formally supply the named output, including
201: SHARED CLAIM MAP  -  REQUIRED FOR FULL-SEQUENCE MODE
207: DEGRADED STANDALONE MODE  -  USE ONLY WHEN NO UPSTREAM MAP EXISTS
276: 1. Never report a verification state above what was actually checked.
277: 2. Evidence type and verification state are separate axes; report both.
278: 3. FULL-TEXT-CONFIRMED and RECEPTION-CONFIRMED may both apply.
279: 4. Apply the ladder symmetrically to sources supporting and opposing the claim.
280: 5. A PROVISIONAL source may not anchor a MAJOR or FATAL finding.
299: 1. VERIFICATION STATE
304: 2. TECHNICAL OUTCOME STATUS
348: 3. CONDITIONAL CONCEDE RESULT
354: 4. VERDICT ELIGIBILITY
367: HARD RULES
389: DATA-HONESTY RULE
402: RECEPTION-MODULE CONFIRMATION RULE  -  REPLICATION AND POST-PUBLICATION CLAIMS
438: SECTION A: DATA GENERATION AUDIT
444: 1. How was this data collected?
450: 2. What selection effects shaped the dataset?
455: 3. What does missingness look like?
461: 4. What incentive structure governed data collection?
467: 5. For AI-assisted analysis specifically:
477: |Data source|Collection method|Selection bias risk|Missingness pattern|Incentive structure risk|AI-analysis check run|
478: |-----------|-----------------|-------------------|-------------------|------------------------|---------------------|
485: SECTION B: PRE-REGISTRATION AND ANALYSIS PLAN
487: 1. Was the study pre-registered before data collection began?
491: 2. Did the published analysis match the pre-registered plan?
496: 3. If not pre-registered: how many outcomes were tested in the study?
503: |Pre-registration status|Analysis match|Outcomes tested|Outcomes reported|Post-hoc subgroups|P-hacking risk|
504: |-----------------------|--------------|---------------|-----------------|------------------|--------------|
510: SECTION C: EFFECT SIZE AND STATISTICAL POWER
512: 1. What is the reported effect size? (r, d, OR, RR, eta2, etc.)
513: 2. How does this effect size compare to:
517: 3. What was the sample size?
518: 4. What statistical power did the study have to detect the reported effect at the reported
522: 5. Winner's curse assessment: studies that barely achieve p < .05 in underpowered designs
527: |Reported effect size|Field typical range|Corrected meta-analysis estimate|Sample size|Estimated power|Winner's curse risk|
528: |--------------------|-------------------|--------------------------------|-----------|---------------|-------------------|
534: SECTION D: HARKING (HYPOTHESIZING AFTER RESULTS ARE KNOWN)
536: 1. Is the central finding presented as confirmatory (testing a pre-specified hypothesis) or
538: 2. Does the introduction describe a specific directional hypothesis that matches the result?
541: 3. Are there signs of post-hoc hypothesis specification?
545: 4. Does the discussion present exploratory findings as if they were confirmatory?
549: |Hypothesis type|Pre-registered?|HARKing indicators|HARKing risk|
550: |---------------|---------------|------------------|------------|
556: SECTION D2: FORKING PATHS / ANALYTICAL-CHOICE MULTIVERSE
569: 1. Map the analytical decision points actually made in the study:
577: 2. For each major decision point, generate the plausible alternative choices a competent
580: 3. Assess result sensitivity under those alternatives:
587: 4. Distinguish the cases explicitly:
600: | Decision point | Choice made | Pre-specified? | Defensible alternatives | Result under alternatives (holds / weakens / disappears / reverses) | Fragility |
601: |---|---|---|---|---|---|
612: SECTION E: SELECTIVE REPORTING
614: 1. Are all pre-registered outcomes reported?
617: 2. Are there signs of selective subgroup reporting?
620: 3. Are there signs of selective time-point reporting?
623: 4. Publication bias assessment:
631: |Outcomes registered|Outcomes reported|Missing outcomes|Subgroup selectivity|Publication bias indicators|
632: |-------------------|-----------------|----------------|--------------------|---------------------------|
636: SECTION F: REPLICATION STATUS
638: 1. Has the finding been directly replicated?
643: 2. Has the finding been conceptually replicated?
647: 3. Effect size trajectory:
654: | Direct replications | Success rate | Pre-registered reps | Independent reps | Meta-analytic estimate | Effect shrinkage | Verification state |
655: |---|---|---|---|---|---|---|
659: SECTION G: DATA AND CODE AVAILABILITY
661: 1. Were the data made publicly available?
662: 2. Was the analysis code made publicly available?
663: 3. Has anyone attempted a reanalysis of the original data?
665: 4. Are there known data irregularities, anomalies, or concerns?
671: | Data available | Code available | Reanalysis attempted | Reanalysis result | PubPeer flags | Corrections issued | Verification state |
672: |---|---|---|---|---|---|---|
676: SECTION H: SUMMARY TABLE  -  INTERNAL VALIDITY
680: |Dimension               |Assessment|Severity|Notes|
681: |------------------------|----------|--------|-----|
682: |Data generation quality |          |        |     |
683: |Selection bias          |          |        |     |
684: |Missingness handling    |          |        |     |
685: |Incentive structure risk|          |        |     |
686: |Pre-registration        |          |        |     |
687: |Analysis plan compliance|          |        |     |
688: |P-hacking risk          |          |        |     |
689: |Effect size plausibility|          |        |     |
690: |Statistical power       |          |        |     |
691: |Winner's curse risk     |          |        |     |
692: |HARKing risk            |          |        |     |
693: |Forking-paths fragility |          |        |     |
694: |Selective reporting     |          |        |     |
695: |Replication success rate|          |        |     |
696: |Effect size trajectory  |          |        |     |
697: |Data/code availability  |          |        |     |
698: |Post-publication flags  |          |        |     |
704: SECTION H2: THE CONCEDE TEST
734: | Finding | Verification state | Technical outcome status | Conditional concede result: SURVIVES / NARROWS / DEFEATS | Verdict eligibility: ELIGIBLE / PENDING VERIFICATION | Eligibility basis | Surviving claim if NARROWS |
735: |---|---|---|---|---|---|---|
747: SCOPE-LOSS ASSESSMENT  -  REQUIRED FOR EVERY NARROWS RESULT
761: | Finding | Scope-loss level | Original claim | Surviving claim | What practical or inferential work is lost? |
762: |---|---|---|---|---|
764: VERDICT MAPPING
779: SECTION I: INTERNAL VALIDITY VERDICT
807: A. Strong - pre-registered, adequately powered, independently replicated, effect stable, data
821: 1. Is the foundational finding likely to be real?
822: 2. If it is real, is its magnitude sufficient to support the downstream claim?
823: 3. What is the best current estimate of the true effect size?
824: 4. What pre-registration and replication evidence would upgrade the grade?
825: 5. What decisive test has not been run?
826: 6. For AI-assisted analysis, did the adversarial check surface failures the original analysis
828: 7. Is the finding fragile to defensible analytical choices?
829: 8. Does any usable residual remain? If yes, state it exactly. If no, write "surviving
832: SECTION J: INTEGRATION WITH CONSTRUCT VALIDITY AUDIT
885: SECTION K: ONE-PARAGRAPH SUMMARY
926: FINAL SECTION: STANDARDIZED FINDING TABLE
937: | Field | Entry |
938: |---|---|
939: | Finding | One sentence |
940: | Target claim | Claim map field 6 |
941: | What was measured | Actual data, design, and analytical operation |
942: | What was claimed | Empirical finding or downstream assertion being supported |
943: | Failure mode | Internal-validity taxonomy used above |
944: | Severity | none / minor / moderate / major / fatal-for-strong-claim |
945: | Concede test | SURVIVES / NARROWS / DEFEATS |
946: | Scope loss if NARROWS | incidental / material / near-defeat, plus surviving claim |
947: | Evidence | Section, table, figure, passage, preregistration, code, or data |
948: | Evidence type | primary study / replication / meta-analysis / methodological critique / policy document / practitioner / journalism / commentary / theoretical / author inference |
949: | Verification state | From the compact vocabulary |
950: | Possible innocent explanation | MANDATORY  -  strongest non-damning reading; if none, write "none identified" |
951: | What would weaken this | MANDATORY  -  specific evidence that would undercut it |
952: | Failure location | PAPER / CITATION / PR-MEDIA / MODEL-RETRIEVAL / MIXED |
953: | Status | confirmed / contested / provisional |
957: 1. A finding missing either mandatory falsifiability field is not inspectable and may not be
959: 2. Severity must agree with verification state. A PROVISIONAL finding cannot be MAJOR or
961: 3. A SURVIVES finding cannot be MAJOR or FATAL and may not anchor the verdict.
962: 4. A NARROWS finding must state the surviving claim and scope-loss level. An incidental
964: 5. Target claim must match field 6 of the shared Claim Map. Use MAP GAP rather than silently
966: 6. A replication or post-publication finding must preserve its verification state. A
968: 7. If no findings of consequence were produced, say so plainly and submit an empty table with
```

## prompts/research-analysis/3-counter-audit.txt

```text
15: PROMPT IDENTITY MARKERS
22: 1. RECORD THE INSTRUMENT ACTUALLY IN CONTEXT.
39: 2. MUTABLE-REFERENCE / CURRENCY RULE.
67: 3. VERSION-COLLISION ATTRIBUTION GATE.
94: 4. DISPOSITION.
107: 5. REQUIRED RUN-HEADER LINE.
169: ANTI-HEDGING RULE
182: 0. Claim map (from the Claim Extraction / Inflation Map stage): [PASTE CLAIM MAP]
189: 1. Original foundational paper(s): [Paste citation, abstract, methods, or key excerpts.]
190: 2. Citation-network audit output: [Paste the prior audit, including cartel-risk scorecard if
192: 3. Construct-validity audit output: [Paste if available.]
193: 4. Internal-validity audit output: [Paste if available.] If no internal-validity audit was
204: 6. Central claim being audited: [State the claim in one sentence.]
205: 7. Current audit verdict: [Example: fatal construct-validity failure, citation-laundering
207: 8. Known citation hub / founding cluster: [List papers, authors, reviews, institutions, or
209: 9. Adjacent fields already suspected of being ignored: [List if known.]
213: DATA-HONESTY RULE
249: 1. CAP: A source whose reception has NOT been checked cannot anchor the verdict. Until
253: 2. SYMMETRY: This gate fires on sources SUPPORTING the original claim exactly as much as on
258: 3. SELF-APPLICATION: This gate applies to sources THIS counter-audit itself introduces (new
263: 4. ONE LEVEL, THEN STOP: The reception check goes one level deep. Check whether a load-bearing
268: 5. VERIFICATION STATE (replaces simple memory-vs-retrieval labeling)
314: EVIDENCE-QUALITY SCORING
352: RELATIONSHIP TO CENTRAL CLAIM
370: A. OPPOSITIONAL CITING PAPERS
391: |Paper|Year|Cites foundational/hub?|Main criticism|Evidence quality|Relationship to claim|Verification state|Field uptake|Strength|
392: |-----|---:|-----------------------|--------------|---------------:|---------------------|------------------|------------|--------|
396: B. NON-CITING OPPOSITION PAPERS
419: |Paper / source|Year|Does not cite hub?|Main argument|Why it matters|Evidence quality|Relationship to claim|Reception (if load-bearing)|
420: |--------------|---:|------------------|-------------|--------------|---------------:|---------------------|---------------------------|
424: C. NEGLECTED REFERENCES THE HUB SHOULD HAVE CITED
444: |Neglected source|Year|Relevance|Cited by foundation?|Cited by hub?|Effect of omission|Evidence quality|
445: |----------------|---:|---------|--------------------|-------------|------------------|---------------:|
449: D. IGNORED ADJACENT FIELDS
467: |Adjacent field|Key sources|Why relevant|Better method / measure|Decisive test suggested|Engagement by target field|Effect of neglect|
468: |--------------|-----------|------------|-----------------------|-----------------------|--------------------------|-----------------|
472: E. STRONGEST EVIDENCE SUPPORTING THE ORIGINAL CLAIM
474: E0. SOURCE SELF-DEFENSE CHECK  (run FIRST, before external support)
486: 1. SCOPE QUALIFIERS attached to a limitation the prosecutors quoted. A limitation is often
492: 2. SENSITIVITY OR ROBUSTNESS TESTS the source performed. Did the source remove, withhold, or
496: 3. STATED ASSUMPTIONS the source names explicitly. A source that names an assumption has not
500: 4. ACKNOWLEDGED LIMITATIONS the prosecutors presented as discoveries. If the source states the
505: | Prosecutor finding | Source passage that anticipates it (quote + location) | Type (scope / sensitivity test / stated assumption / acknowledged limitation / NONE FOUND) | Does it answer the finding? (fully / partly / not at all) | Effect on the finding |
506: |---|---|---|---|---|
540: E1. EXTERNAL SUPPORTING EVIDENCE
568: |Supporting source|Year|What it supports|Answers construct problem?|Runs decisive test?|Strong or narrow claim?|Verification state|Impact on audit|
569: |-----------------|---:|----------------|--------------------------|-------------------|-----------------------|------------------|---------------|
576: F. CITATION-NETWORK UPTAKE OF OPPOSITION
598: |Opposition / neglected source|Cited by hub?|Later uptake?|Engagement quality|Survived reception check?|Suppression vs. correctly-discounted|Network implication|
599: |-----------------------------|-------------|-------------|------------------|-------------------------|------------------------------------|-------------------|
624: G. SUMMARY TABLE  -  OPPOSITION STRENGTH
630: |Category                            |Number Found|Strongest Example|Evidence Quality|Verification state|Impact on Central Claim|
631: |------------------------------------|-----------:|-----------------|---------------:|------------------|-----------------------|
632: |Oppositional citing papers          |            |                 |                |                                    |                       |
633: |Non-citing opposition papers        |            |                 |                |                                    |                       |
634: |Neglected references                |            |                 |                |                                    |                       |
635: |Ignored adjacent fields             |            |                 |                |                                    |                       |
636: |Strongest support for original claim|            |                 |                |                                    |                       |
655: G2. DID THE PROSECUTION ATTACK THE STRONGEST VERSION?
682: | Prosecutor | Finding | Declared target claim | Claim-map version attacked | Matches field 6? | Failure location | Severity after re-aiming |
683: |---|---|---|---|---|---|---|
704: 1. WHICH VERSION DID EACH PROSECUTOR ACTUALLY ATTACK? Classify from the rows above:
710: 2. WAS THAT THE VERSION THE AUDIT WAS SUPPOSED TO EVALUATE? Compare each row against map field
714: 3. WHERE DOES EACH FAILURE ACTUALLY LIVE? Classify and name the supporting findings:
721: 4. IF A FAILURE IS NOT AT THE PAPER LAYER, SAY SO PLAINLY:
726: 5. DOES EACH FINDING'S SEVERITY SURVIVE RE-AIMING? Re-rate finding by finding. A
729: RELATIONSHIP TO THE CLAIM MAP - DO NOT DUPLICATE
741: | Question | Answer | Supporting prosecutor findings |
742: |---|---|---|
743: | Versions attacked | | |
744: | Version audit targeted (map field 6) | | |
745: | Finding-level match rate | | |
746: | Failure location(s) | | |
747: | Severity survives re-aiming? | | |
748: | Nested findings consolidated | | |
750: H. REVISED THESIS IMPACT
755: A. Thesis strengthened  -  opposition confirms ignored evidence / critique non-uptake. B.
763: 1. Which claims should be removed?
764: 2. Which claims should be narrowed?
765: 3. Which claims should be strengthened?
766: 4. Which claims require better sourcing?
767: 5. Which claims survived the adversarial review unchanged?
768: 6. Which evidence most improves the thesis?
769: 7. Which evidence most threatens the thesis?
777: I. REVISED THESIS PARAGRAPH
806: J. FINAL ADVERSARIAL VERDICT
862: J2. SELF-TILT DISCLOSURE (MANDATORY  -  THIS STAGE HAS NO DOWNSTREAM CHECK)
884: K. FINAL ONE-PARAGRAPH SUMMARY
```

## deferred/1-field-context-generator.txt

```text
1: FIELD CONTEXT GENERATOR
15: PROMPT IDENTITY MARKERS
23: 1. RECORD THE INSTRUMENT ACTUALLY IN CONTEXT.
40: 2. MUTABLE-REFERENCE / CURRENCY RULE.
68: 3. VERSION-COLLISION ATTRIBUTION GATE.
95: 4. DISPOSITION.
108: 5. REQUIRED RUN-HEADER LINE.
150: 1. Prefer GROUNDED context. Where you have been given, or can cite, real field
155: 2. LABEL every standard, red flag, and (especially) every downstream-targeting
160: 3. State an OVERALL CONFIDENCE for this Field Context Block (High / Moderate /
165: 4. Do NOT hide uncertainty behind fluent domain-sounding language. If you are
188: FIELD CONTEXT BLOCK
204: SECTION 1 — CORE STANDARDS OF REVIEW
212: SECTION 2 — SETTLED vs. CONTESTED  (guards against a dangerous failure)
231: SECTION 3 — QUESTIONS A DOMAIN EXPERT WOULD ASK
239: SECTION 4 — CHARACTERISTIC RED FLAGS (must be field-specific, not generic)
257: SECTION 5 — APPLICABLE vs. N/A DOWNSTREAM CHECKS (driven by document type)
274: SECTION 6 — DOWNSTREAM AUDIT TARGETING  ***PRIMARY DELIVERABLE***
322: SECTION 7 — ADDITIONAL NOTES FOR AUDITORS
334: INPUT
```
