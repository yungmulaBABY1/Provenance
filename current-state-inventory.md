# Provenance Current\-State Inventory

> **Snapshot:** 2026-08-09. Reconciled at repository commit
> `17fd1eca510a686b44970113552da55527515789` against the registry, result log,
> prompt identities, and Ceuta regression materials dated the same day.

This inventory reconciles what exists, what executes, what has been tested, and
what remains outside the canonical prompt set\. It is a status map, not another
implementation\. The files under `prompts/` remain the source of truth for prompt
execution\.

## Executive state

- The research and media branches both have canonical prompt files and recorded
  run history\. Stage 4 synthesis is the one planned main\-stage prompt that does
  not exist\.
- The repository records 42 runs: 23 research and 19 media\. Those runs are not
  evenly distributed; the research evidence is still concentrated on MBH98 and
  Donovan et al\.
- The current Coverage Network prompt contains proposition\-level source
  independence, prominence\-packaging, the semantic equivalence/earnedness gate,
  the complete hypothesis machinery, and the shared `MEDIA-P1` axes\.
- `FAIL-MB-017` and `FAIL-MB-018` have complete, fixture\-bearing cases and a
  passing integrated RC2 rerun on the 3,232\-line artifact at Git blob
  `d5f3502fc3ab1af083c12be0a0b1440cbf2adf6f`\. Those analytical blocks are now
  canonical\.
- Current `main` renamed the prompt to
  `prompts/media-analysis/2-network-coverage.txt` and added TOOL\-004’s instrument
  preflight\. The current 3,340\-line / 131,417\-byte prompt has Git blob
  `9380b619fd16b4212dabec28971f1c6a6b3d18b6`\. Its two\-version collision case is
  specified but not built or run\.
- The citation\-network completion contract is validated on three supplied
  packets, through 26 sources and 70 selected edges\. It is not validated under
  open\-ended retrieval, and the checker’s own regression fixtures still omit the
  original silent\-omission behavior\.
- Local acquittal behavior has been observed at claim\-map and citation\-network
  stages\. No full research chain has yet returned a clean result\. The media clean
  case is built but has not been run\.
- The webapp is an experimental sandbox prototype, not a complete or supported
  application\. Its prompt payload is nevertheless derivative and mechanically
  checkable: it exposes
  canonical paths, checksums, sizes, and snapshot metadata, and
  `tools/embed_prompts.py --check` currently passes\. Its explanatory prose and
  run\-library content are still separately authored copies\.

## Source\-of\-truth order

|Question                         |Governing source                                                                               |
|---------------------------------|-----------------------------------------------------------------------------------------------|
|What instructions execute?       |`prompts/`, plus the named tool or deferred file when explicitly invoked                       |
|What happened in a run?          |`tests/RESULTS.md` and preserved raw run artifacts                                             |
|Why does a rule exist?           |`FAILURES.md` and `CHANGELOG.md`                                                               |
|What is protected by a case?     |`tests/cases/` and its precommitted oracle                                                     |
|What is pending?                 |This inventory and `TODO.md`                                                                   |
|What does the prototype display? |`webapp/provenance.html`, as a derivative sandbox snapshot                                     |
|What does the workbook establish?|`Revision_Log_v0.2.xlsx`, as a supplemental revision ledger—not an override of any source above|

## Prompt and stage inventory

Implementation and validation are deliberately separate here\. A prompt may be
canonical but untested; a repair may be tested but not yet canonical\.

|Stage or capability      |Canonical implementation                            |Validation state                                                                                          |Reconciliation note                                                                                                                                                                       |
|-------------------------|----------------------------------------------------|----------------------------------------------------------------------------------------------------------|------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
|Stage 0 field diagnostic |`prompts/0-field-diagnostic.txt`                    |No logged run of the current file                                                                         |The prompt calls itself a go/no-go gate; some documentation has called it an on-ramp. Direct target entry remains possible in current practice.                                           |
|Stage 1 claim extraction |`prompts/1-claim-extraction.txt`                    |Extensively run across MBH98; newest claim-inventory and label-verification changes remain untested       |Single-claim prosecution remains the default; deferred claims are inventoried rather than silently added.                                                                                 |
|Construct validity       |`prompts/research-analysis/2-construct-validity.txt`|Run on MBH98 and Donovan; retrieve-before-verdict repairs from `FAIL-CV-003/004` lack a fresh prompt rerun|The split claim-space verdict object is implemented.                                                                                                                                      |
|Internal validity        |`prompts/research-analysis/2-internal-validity.txt` |Never run                                                                                                 |Prompt is built, but its execution and handoffs are unvalidated.                                                                                                                          |
|Citation network         |`prompts/research-analysis/2-citation-network.txt`  |Substantive runs exist; completion contract passed three supplied-packet pilots                           |Open-ended retrieval compliance and `TOOL-002` checker coverage remain open.                                                                                                              |
|Stage 3 counter-audit    |`prompts/research-analysis/3-counter-audit.txt`     |E0 source-self-defense search and reception gate changed outcomes in recorded runs                        |Terminal model-based balancing stage for research.                                                                                                                                        |
|Single-piece framing     |`prompts/media-analysis/2-framing-construction.txt` |Multiple live runs across models                                                                          |Current file contains `MEDIA-P1`, but the later companion, party, trajectory, and quotation additions have not been reconciled as one canonical authored source across both media prompts.|
|Coverage network         |`prompts/media-analysis/2-network-coverage.txt`     |Multiple live runs; integrated `FAIL-MB-017/018` artifact exercised                                       |Canonical sample rule is minimum 3 pieces, with 5–8 preferred. TOOL-004 preflight is present but regression-untested.                                                                     |
|Human adjudication       |No prompt by design                                 |Used as the required decision point in the architecture                                                   |It must remain human and cannot be replaced by a composite score.                                                                                                                         |
|Stage 4 synthesis        |No file                                             |Not built                                                                                                 |Intended to compress an adjudicated set while preserving residuals, uncertainty, and provenance.                                                                                          |
|Stage 5 voice restoration|`prompts/5-voice-restoration.txt`                   |Current carve-out has no logged verification run                                                          |May tighten prose but may not remove epistemic flags.                                                                                                                                     |
|Field-context generator  |`deferred/1-field-context-generator.txt`            |Built, unrun                                                                                              |Deferred configuration aid, not a live required stage.                                                                                                                                    |

## 1\. Done and canonical

|Item                                    |What is established                                                                                                                                                                                                         |
|----------------------------------------|----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
|Research execution files                |Stages 0, 1, three Stage 2 prosecutors, Stage 3, and Stage 5 exist in canonical paths.                                                                                                                                      |
|Media execution files                   |Both single-piece and coverage-network prompts exist in canonical paths.                                                                                                                                                    |
|Proposition-level source independence   |Whole-coverage origin counts are descriptive only; per-fact origins carry amplification/corroboration judgments in the current coverage prompt.                                                                             |
|Shared media causal-role axes           |`MEDIA-P1` is present in both media prompts and owns event classification, cause, role/status, blame, remedy, and leadership/policy assignments.                                                                            |
|Citation completion contract and checker|The prompt contract and `check-citation-network-output.py` are canonical; three supplied-packet compliance pilots passed.                                                                                                   |
|Failure and behavior records            |`FAILURES.md`, `CHANGELOG.md`, and `tests/RESULTS.md` distinguish observed failure, repair rationale, and run behavior.                                                                                                     |
|Ceuta case material                     |The exact eight-piece synthetic fixture is embedded in both `FAIL-MB-017/018` case files.                                                                                                                                   |
|Integrated Ceuta analytical repairs     |Prominence-packaging and the semantic materiality/earnedness gate are present in the canonical Coverage Network prompt.                                                                                                     |
|Prototype prompt synchronization        |Eleven repository files are embedded in the sandbox by `tools/embed_prompts.py`; path, checksum prefix, byte count, line count, and snapshot are exposed in the UI. This does not make the prototype a complete application.|
|No-composite-score rule                 |The prompts, reference documents, and webapp all preserve disaggregated findings and human adjudication.                                                                                                                    |

## 2\. Done but needs updating or propagation

|Item                                  |Completed evidence                                                                                                                                                                             |Remaining update                                                                                                                                                                  |
|--------------------------------------|-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
|TOOL-004 instrument preflight         |Observed failure is logged and the guard is in the canonical Coverage Network prompt                                                                                                           |Build and run the stale/current two-version fixture; then promote one shared implementation to a launcher/router.                                                                 |
|`FAIL-MB-018` cross-branch propagation|Semantic equivalence/earnedness is canonical and passed on Coverage Network                                                                                                                    |Review the single-piece branch for equivalent entry conditions without duplicating authored rules.                                                                                |
|August media revisions                |Companion retrieval, competing classifications, label trajectory, language package, party enumeration, quotation-pair preservation, and contextual identity inference changed recorded outcomes|Consolidate their authored source and verify parity across the two canonical media prompts. The workbook’s referenced `Prompt_Additions/` files are not present in the repository.|
|Hypothesis resolution                 |`REFRAMED` and balanced hypothesis handling changed Madison/Seattle outcomes and are canonical in Coverage Network                                                                             |Reconcile equivalent authored sources and terminology across prompts without weakening branch-specific ownership.                                                                 |
|Verdict output                        |Construct and internal-validity prompts implement audited-claim status plus a surviving residual                                                                                               |Document and harmonize the object across prosecutors; the `residual: none` path has not been produced in a run.                                                                   |
|Architecture audit                    |Cross-prompt drift/duplication reviews were completed for both branch pairs, and targeted parity fixes were applied                                                                            |The cold deletion pass against the repository deletion standard remains undone.                                                                                                   |
|Revision workbook                     |`Revision_Log_v0.2.xlsx` records 22 revisions, six earlier media run records, prompt-addition metadata, and a parking lot                                                                      |Reconcile row status against canonical files and logs. Treat missing source paths and off-repository artifacts explicitly.                                                        |

## 3\. Duplicated across implementations

|Duplicate                                                                         |Current control                                    |Residual risk                                                                                                                                                      |
|----------------------------------------------------------------------------------|---------------------------------------------------|-------------------------------------------------------------------------------------------------------------------------------------------------------------------|
|Prompt text in the webapp prototype                                               |Generated payload plus checksum parity check       |Safe as a sandbox derivative if the generator is run after prompt changes.                                                                                         |
|Philosophy, methodology, vocabulary, and limitations prose in the webapp prototype|No equivalent generated-source check               |Prototype prose can drift from `reference/*.md`; repository reference files win.                                                                                   |
|Compact verification/failure vocabularies across prompts                          |Local copies execute without an external dependency|Manual authored duplication can drift. The desired architecture is one canonical authored primitive plus generated self-contained prompt copies and a parity check.|
|`MEDIA-P1` in both media prompts                                                  |Current compact copies were harmonized             |No build-time parity check yet; a future edit can reintroduce branch drift.                                                                                        |
|Revision history across workbook, changelog, failure registry, results, and TODO  |Each file has a different intended role            |The workbook currently overlaps all four roles and uses row statuses that do not always describe canonical implementation.                                         |
|Run-library copies in the webapp prototype                                        |Curated for presentation                           |They are not a substitute for raw outputs or `tests/RESULTS.md`.                                                                                                   |

## 4\. Actually unfinished

|Item                                 |Completion condition                                                                                                                                                                                    |
|-------------------------------------|--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
|TOOL-004 collision regression        |Build `mutable-prompt-version-collision` with coherent stale/current versions, require unresolved disposition before independent discrimination, and block formal execution until identity is confirmed.|
|Shared instrument preflight          |Move TOOL-004 from its first prompt-local implementation to a canonical run launcher/router when that layer exists.                                                                                     |
|Full-chain research acquittal        |Run a sound target through claim extraction, applicable prosecutors, counter-audit, and human adjudication without manufactured findings.                                                               |
|Media clean control                  |Run `tests/cases/11-proportionate.md` and log the result.                                                                                                                                               |
|Internal-validity validation         |Complete and log the first real run of the canonical prompt.                                                                                                                                            |
|Built-but-unrun controls             |Run CE-006/007 and MIX-01; preserve failures and passes.                                                                                                                                                |
|`ceuta-prominence-d2-ownership`      |Build a case with a supplied prior single-piece packaging finding and test cross-branch ownership without duplication.                                                                                  |
|Checker regression coverage          |Add a fixture for the original `FAIL-CN-001` behavior: required sections absent, gate not fired, verdict still issued.                                                                                  |
|Citation-network retrieval validation|Exercise the completion contract during open-ended retrieval rather than a supplied packet.                                                                                                             |
|Shared-primitives authoring model    |Choose one canonical authored source, generate self-contained prompt copies, and add parity checking—or explicitly retain manual local ownership.                                                       |
|Stage 4 synthesis                    |Create the prompt only after its input/output object is stable enough to specify.                                                                                                                       |
|Coverage over time                   |Build a separate branch with its own sampling, timing, and update rules; do not fold it into cross-outlet divergence.                                                                                   |

## 5\. Obsolete or superseded

|Item                                                        |Disposition                                                                                                                                                                                     |
|------------------------------------------------------------|------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
|`reference/shared-primitives.txt`                           |Bannered superseded. It is an older reflowed claim-extraction prompt, not a live primitives source. Six prompt headers still point to nonexistent sections and must be resolved before deletion.|
|`reference/narrative-flags-module.txt`                      |Bannered superseded. Its operational content was merged into the media prompts; retain only as design rationale until the deletion standard is satisfied.                                       |
|Whole-coverage ratio as an amplification verdict            |Superseded by proposition-level origin analysis. Whole-coverage counts remain descriptive and convention-sensitive.                                                                             |
|“Every vivid denotational variant is framing”               |Superseded for wording-derived candidates by the canonical semantic materiality and earnedness gate.                                                                                            |
|Prompt size as a primary runtime rationale                  |Not supported by the fixed-fixture measurements. Prompt size did not behave as a dominant runtime predictor across the measured range.                                                          |
|Earlier claim that the webapp had no version metadata       |Resolved for the prototype’s embedded prompt copies by the generator and displayed checksum/path metadata. This says nothing about application completeness.                                    |
|Earlier claim that citation compliance was wholly unresolved|Superseded by the three supplied-packet pilots. The remaining problem is narrower: retrieval validation and checker-regression coverage.                                                        |

## 6\. App\-only, repo\-only, and shared capabilities

|Surface                  |Capability                                                                                                                                                                                                               |Boundary                                                                                                                                                                                                               |
|-------------------------|-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
|Prototype only           |Experimental branch/stage navigation, prompt copy buttons, curated run-library browsing, documentation panels, theme controls, and a local browser run notebook with output/notes                                        |These are sandbox behaviors, not a supported capability contract. Browser state is local. The prototype does not run a model, retrieve sources, execute the checker, update registers, or write canonical prompt files.|
|Repo only                |Canonical prompt editing and version history, raw run artifacts, regression fixtures and oracles, compliance packets/reports, mechanical checker, failure/changelog/TODO records, generator source, and revision workbook|These are the auditable control plane and evidence record.                                                                                                                                                             |
|Shared with the prototype|Prompt text, sequence descriptions, selected run summaries, philosophy/methodology concepts, and vocabulary                                                                                                              |Prompt copies have parity metadata; explanatory prose and curated run copies do not. The repository remains authoritative.                                                                                             |

## Resolved review questions

|Question                                                     |Reconciled answer                                                                                                                                                                                   |
|-------------------------------------------------------------|----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
|Is the coverage-network default 2–4 pieces or at least 3?    |The canonical prompt says minimum 3, with 5–8 preferred. The proposed 2–4 casual-use inversion was not applied.                                                                                     |
|Does the webapp prototype lack prompt-copy version pinning?  |No. Its prompt copies carry canonical path, checksum prefix, size, lines, and snapshot metadata, and the parity check passes. The prototype is still incomplete and noncanonical.                   |
|Is the citation-network compliance failure still undiagnosed?|The execution repair is validated for supplied packets; open retrieval and checker-fixture coverage remain open.                                                                                    |
|Does the verdict scale need replacement?                     |No new scale is justified. The concede test supplies the derivation rule; notation and the unobserved `residual: none` path still need validation.                                                  |
|Can Provenance acquit?                                       |Individual stages have acquitted or returned no gap. A full research clean chain has not; the media clean case remains unrun.                                                                       |
|Are the Ceuta repairs canonical?                             |Yes. Their cases, failure records, integrated rerun evidence, and execution blocks are in the repository. The later TOOL-004 preflight is canonical but has not passed its own dedicated regression.|

## Maintenance rule

Update this file when an item crosses one of three boundaries:

1. a design becomes a canonical implementation;
2. an implementation receives its first meaningful run; or
3. a tested repair is synchronized, superseded, or removed\.

Do not use “implemented,” “tested,” and “canonical” as synonyms\.
