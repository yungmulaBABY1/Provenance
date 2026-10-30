"""Native-output import with exact UTF-8 text retention. No models or retrieval."""

from __future__ import annotations

import platform
from pathlib import Path
import subprocess
import sys
import tempfile

from . import SCHEMA, VERSION
from .contract import (ContractError, canonical, digest, jsonl, load_json, read_artifact,
                       record, sha256, validate_context)
from . import native
from .native import parse
from .sources import assess_checks, inspect_sources

CHECKER = "prompts/research-analysis/check-citation-network-output.py"
PROMPT = "prompts/research-analysis/2-citation-network.txt"
BASELINE_PATH = Path(__file__).with_name("baseline.json")


def pinned_checker(root, raw_bytes, baseline):
    # Executable path is fixed by code, never taken from the audit output/sidecar.
    pinned = {path: read_artifact(root, baseline["files"][path])
              for path in (CHECKER, PROMPT, "reference/shared-primitives.txt")}
    # Execute exactly the verified bytes. Do not re-open mutable user paths after
    # validation or import neighboring Python files from a corpus directory.
    with tempfile.TemporaryDirectory(prefix="atlas-check-") as directory:
        snapshot = Path(directory)
        (snapshot / "checker.py").write_bytes(pinned[CHECKER])
        (snapshot / "audit-output.txt").write_bytes(raw_bytes)
        result = subprocess.run([sys.executable, "-I", "checker.py", "audit-output.txt"],
                                cwd=snapshot, capture_output=True, text=True,
                                timeout=30, check=False)
    if result.returncode not in (0, 1):
        raise ContractError(f"CHECKER_EXECUTION_ERROR: {result.returncode}: {result.stderr}")
    report = result.stdout
    status = "FAIL" if result.returncode else (
        "PASS-WITH-REVIEW" if "CONTENT_RESULT\tPASS-WITH-REVIEW" in report else "PASS")
    return {"status": status, "exit_code": result.returncode,
            "report": report, "stderr": result.stderr,
            "review_items": [s for s in report.splitlines() if s.startswith("REVIEW_ITEM_")],
            "scope": "native checker structure/content-form only; no scientific verification"}


def build(context: dict, root: Path) -> dict:
    validate_context(context)
    baseline = load_json(BASELINE_PATH.read_bytes())
    inputs = []
    for artifact in [context["output"], *context["declared_inputs"]]:
        data = read_artifact(root, artifact)
        inputs.append({**artifact, "bytes": len(data)})
    raw_bytes = read_artifact(root, context["output"])
    try:
        raw = raw_bytes.decode("utf-8")
    except UnicodeError as exc:
        raise ContractError("OUTPUT_NOT_UTF8") from exc
    parsed = parse(raw)
    checker = pinned_checker(root, raw_bytes, baseline)
    # Source preflight is computed before granting any finding/display eligibility.
    source_records, receipts, anchors = inspect_sources(context, root)
    check_results = assess_checks(context, receipts, anchors)
    run = context["run"]
    rid = run["id"]
    observed_numbers = {str(f["number"]) for f in parsed["findings"]}
    if any(n not in observed_numbers for n in context["finding_checks"]):
        raise ContractError("UNRESOLVED_REFERENCE: finding_checks target")
    # Duplicate native IDs are diagnostics. Ordinals keep both raw blocks inspectable.
    records = [record("Work", w["id"], metadata={k: v for k, v in w.items() if k != "id"}, refs=[])
               for w in context["works"]]
    records.extend(source_records)
    corpus_id = f"{rid}/corpus/{context['corpus']['id']}"
    for receipt in receipts.values():
        receipt["per_check_eligibility"] = {
            cid: check for cid, check in check_results.items()
            if any(req["source_version_id"] == receipt["source_version_id"]
                   for req in check["requirements"])}
        receipt["input_context_sha256"] = digest(context)
        receipt["source_lock_ref"] = corpus_id
        receipt["refs"].append(corpus_id)
        receipt["receipt_sha256"] = digest(receipt)
    records.append(record("CorpusScope", corpus_id, declared=context["corpus"],
                          imported_source_lock=parsed["source_lock"], lock_verification="NOT_VERIFIED",
                          refs=[s["id"] for s in context["sources"]]))
    syntax = "FAIL" if parsed["issues"] or checker["status"] == "FAIL" else checker["status"]
    for index, finding in enumerate(parsed["findings"], 1):
        fid = f"{rid}/finding/{index}"
        check_ids = context["finding_checks"].get(str(finding["number"]), [])
        selected = [check_results[c] for c in check_ids]
        eligible = (bool(selected) and any(c["kind"] == "content" for c in selected)
                    and all(c["eligibility"] in {
                        "ELIGIBLE", "ELIGIBLE_WITH_LIMITATIONS"} for c in selected))
        pids = sorted({pid for c in selected for req in c["requirements"] for pid in req["passage_ids"]})
        receipt_ids = sorted({receipts[req["source_version_id"]]["id"] for c in selected
                              for req in c["requirements"]})
        records.append(record("AuditFinding", fid, audit_run_id=rid,
                              native=finding, source_check_ids=check_ids,
                              native_output_anchor={"output_sha256": sha256(raw_bytes),
                                                    "first_line": finding["line_start"],
                                                    "last_line_inclusive": finding["line_end"],
                                                    "unit": "one_based_line"},
                              source_eligibility="ELIGIBLE_FOR_DECLARED_CHECKS" if eligible else "NOT_ASSESSABLE",
                              source_checks=selected,
                              source_basis="EXPLICIT_IMPORT_MAPPING; not inferred from model prose",
                              evidence_passage_ids=[anchors[p]["id"] for p in pids],
                              import_status="QUARANTINED" if syntax == "FAIL" else "IMPORTED_UNADJUDICATED",
                              assessment="UNREVIEWED", public_release="NOT_REVIEWED",
                              refs=[rid, *receipt_ids, *[anchors[p]["id"] for p in pids]]))
        for pid in pids:
            records.append(record("Relationship", f"{fid}/evidence/{pid}",
                                  subject_id=fid, object_id=anchors[pid]["id"],
                                  kind="cites_as_evidence", relation_basis="DOCUMENTED_IMPORT_MAPPING",
                                  epistemic_status="UNADJUDICATED", inference=None,
                                  refs=[fid, anchors[pid]["id"]]))
    review_ids = []
    for review in context["reviews"]:
        data = read_artifact(root, review["artifact"])
        target_match = review["target_output_sha256"] == sha256(raw_bytes)
        review_id = f"{rid}/review/{review['id']}"
        review_ids.append(review_id)
        records.append(record("ReviewDecision", review_id, artifact=review["artifact"],
                              raw_output_sha256=sha256(data),
                              declared_target_output_sha256=review["target_output_sha256"],
                              target_binding="MATCH" if target_match else "TARGET_MISMATCH",
                              imported_disposition=review["disposition"], reviewer=review["reviewer"],
                              exposure=review["exposure"], independence="NOT_ESTABLISHED",
                              decision_status="IMPORTED_UNVERIFIED", human_adjudication="NOT_RECORDED",
                              refs=[rid] if target_match else []))
    null_checks = context.get("null_check_ids", [])
    if type(null_checks) is not list or any(c not in check_results for c in null_checks):
        raise ContractError("UNRESOLVED_REFERENCE: null_check_ids")
    scoped_null = (parsed["null_assertion"] is not None and not parsed["findings"]
                   and syntax != "FAIL" and bool(null_checks)
                   and any(check_results[c]["kind"] == "content" for c in null_checks)
                   and all(check_results[c]["eligibility"] in {"ELIGIBLE", "ELIGIBLE_WITH_LIMITATIONS"}
                           for c in null_checks))
    records.append(record("AuditRun", rid, target_work_id=run["target_work_id"],
                          origin=run["origin"], imported_at=run["imported_at"],
                          model=run["model"], runner=run["runner"],
                          historical_instrument=run["historical_instrument"],
                          validation_instrument=baseline["files"][PROMPT],
                          exposure=run["exposure"], independence="NOT_ESTABLISHED_BY_IMPORT",
                          context_sha256=digest(context), output_sha256=sha256(raw_bytes),
                          output_path=context["output"]["path"], raw_output_text=raw,
                          native_scorecard=parsed["scorecard"],
                          source_checks=check_results, native_parse_issues=parsed["issues"],
                          syntax=syntax, checker_status=checker["status"],
                          semantic_review="SEMANTIC_REVIEW_REQUIRED", human_review="NOT_RECORDED",
                          clean_display="SCOPED_NULL_ASSERTION_ONLY" if scoped_null else "NOT_ASSESSABLE_AS_CLEAN",
                          null_assertion=parsed["null_assertion"], null_check_ids=null_checks,
                          corpus_scope_id=corpus_id,
                          paper_clean=False, public_release="NOT_REVIEWED",
                          refs=[run["target_work_id"], corpus_id, *review_ids]))
    code_files = {p.name: sha256(p.read_bytes()) for p in sorted(Path(__file__).parent.glob("*.py"))}
    manifest = record("RunManifest", f"{rid}/manifest", audit_run_id=rid,
                      adapter={"name": "citation-network", "version": VERSION,
                               "code_sha256": code_files, "baseline_sha256": sha256(BASELINE_PATH.read_bytes())},
                      parser={"name": native.NAME, "version": native.VERSION,
                              "code_sha256": sha256(Path(native.__file__).read_bytes())},
                      validation_baseline=baseline, input_context=context,
                      declared_input_receipts=inputs,
                      source_input_receipts=[r["declared_input"] for r in receipts.values() if r["declared_input"]],
                      environment={"implementation": platform.python_implementation(),
                                   "python": platform.python_version(), "unicode": __import__("unicodedata").unidata_version},
                      checker=checker, records_before_manifest_sha256=sha256(jsonl(records)),
                      record_ids=sorted(r["id"] for r in records),
                      execution={"network": "NOT_USED; no OS-level network sandbox is claimed",
                                 "models_invoked": [], "source_commands_executed": False,
                                 "historical_run_reproduced": False,
                                 "scope": "deterministic import of frozen inputs"},
                      refs=[rid])
    records.append(manifest)
    # Fully resolved portable references, including run/source/relationship records.
    payload = jsonl(records)
    return {"records": records, "jsonl": payload, "manifest": manifest,
            "syntax": syntax, "checker_status": checker["status"],
            "jsonl_sha256": sha256(payload)}
