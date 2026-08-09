# Architecture Note: Hypotheses, Retrieval, and Open Decisions

## Status and scope

This note records the operating architecture of the Provenance toolkit as of 2026\-08\-09\. It is a design constraint for prompt changes and interface work, not a substitute for the canonical prompt files\. The prompt files execute; this note explains what must remain true across them\.

The workflow is evidence\-led and human\-adjudicated\. It may surface patterns, but it does not turn a distribution of coverage or a model output into a factual verdict\. There is no composite score\.

## Hypothesis handling

A hypothesis is a retrieval aid, not a conclusion\.

- An operator may supply a hypothesis or prior, but it must be disclosed and entered in the investigation register as **operator\-originated**\.
- The audit may also generate hypotheses from construction findings or retrieved material\. Label these **construction\-audit emergent** or **retrieval\-emergent**\.
- Origin is not evidence\. A hypothesis becomes a finding only through retrieved, attributable material that survives the applicable gates\.
- For each hypothesis, search deliberately for both confirming and disconfirming evidence\. Record the search boundary and what was found on both sides; do not treat an unperformed search as negative evidence\.
- The conclusion follows the evidence gathered\. A hypothesis may guide what is looked for; it may not determine what is reported\.
- Where a prior\-sensitive assignment is at issue \(cause, blame, role, ideology, or motive\), apply the flip/mirror guard and state the strongest alternative reading\.
- A negative result is valid\. The instrument must be able to return no construction finding, no distinctive\-outlet finding, or an unresolved result\.

## Retrieval discipline

### Corpus and source boundary

State how the corpus was selected\. An outlet set assembled from sources the operator already distrusts cannot support an unqualified distributional conclusion\.

For media, retrieve full text or substantial excerpts, exact publication **date and time**, byline, attribution, and update/correction information\. If an institution has both a written release and a spoken briefing, retrieve both when available\. Their wording may explain apparent editorial divergence\.

A closed synthetic fixture is a closed corpus: do not browse or supplement it\. A live audit must label material not retrieved as provisional rather than completing the record from memory\.

### What counts as corroboration

Independence is evaluated per load\-bearing fact, not by counting outlets\.

- Count reporting organizations and upstream information origins separately; both are descriptive\.
- For every contested or load\-bearing fact, identify the pieces asserting it and the independent origins supporting that specific fact\.
- Multiple outlets repeating one press release, wire item, ministry figure, or other origin are **amplification**, not corroboration\.
- Apply `CROSS-OUTLET-CORROBORATED` only where the particular fact has at least two independent origins, and state the per\-fact origin count\.
- Keep source\-chain status separate from substantive verification: `CHAIN-CONFIRMED`, `CHAIN-INFERRED`, or `CHAIN-PROVISIONAL` describe dependence; they do not establish the underlying fact\.

### Timing and editorial choice

Do not call an omission “selection” unless the relevant fact was available before the piece was published\. Use an availability matrix and mark the basis as documented, inferred, or unknown\. If availability is unknown, cap the result at provisional; if the fact arrived later, call it a timing artifact\.

For network\-wide uniformity, do not automatically acquit the construction\. It defeats an outlet\-specific divergence claim, but may instead reveal a shared wire/official/legal convention or a shared blind spot\. Classify the source of uniformity before drawing either conclusion\.

### Claim scope and source of truth

The research sequence remains single\-claim by default\. Claim extraction may inventory secondary claims, but those claims are **deferred**, not silently dismissed or automatically added to prosecution scope\.

Canonical prompt files are the source of truth\. Generated or embedded copies must identify their canonical path, snapshot/checksum, and say that the repository prompt wins on conflict\. No edit to a stale reference copy propagates to a live prompt\.

## Decisions that remain open

1. **Multi\-claim citation\-network scope\.** Do not grant it yet\. If the claim inventory shows material secondary claims, a future scope grant may audit only inventory\-enumerated claim IDs; the prosecutor may not expand scope by “closely related” restatements\. Any grant must also update the standardized finding table and counter\-audit target check, and must follow a run that resolves citation\-network output\-compliance gaps\.
2. **Citation\-network compliance gap\.** The prompt contained required blocks that did not appear in an MBH98 output, including the claim\-map receipt and standardized finding table\. Determine whether this was truncation or section\-skipping before expanding scope or adding more instructions\.
3. **Dangling shared\-primitives references\.** Six live prompts still point to non\-existent sections in `reference/shared-primitives.txt`\. Decide whether to delete those lines or redirect them to each prompt’s compact vocabulary, then run\-test every affected prompt\. Consider deleting the bannered stale file only under the repository deletion standard\.
4. **Acquittal validation\.** Run a full research pipeline on material that should return clean, and run the media clean\-case fixture\. Until then, the toolkit has not demonstrated that its full chains can decline to find\.
5. **Media counter\-audit\.** The media branch currently has no separate Stage 3 counter\-audit; balancing is internal to the two media prompts\. Preserve this as an explicit design decision, not an accidental gap, and revisit only with evidence that internal guards fail\.
6. **Coverage\-over\-time\.** Treat trajectory/drift as a separate, deferred branch\. Do not smuggle it into a cross\-outlet divergence audit without its own timing and update rules\.
7. **Verdict scale and automation\.** Test whether the existing verdict scale survives the concede test before replacing it\. Human adjudication remains a non\-automated stage; aggregation must not override it\.
8. **Architecture audit\.** Before simplifying the long single\-piece prompt, check for duplicated rules, ownership collisions, conflicting severity caps, dead instructions, vocabulary drift, and optional modules without triggers\. A rule may be removed only if the failure it prevents, its observed status, its replacement, and its regression protection are known\.

## Change rule

Prompt changes should be driven by observed run behavior, then validated on a targeted case or live rerun\. Record what fired, what changed, and what was killed in `tests/RESULTS.md`; use `FAILURES.md` and the changelog to distinguish observed failures from precautionary guards\. Do not delete a rule merely because a newer model might infer it\.
