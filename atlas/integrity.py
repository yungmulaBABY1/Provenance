"""Bundle integrity on restore/append: manifest coverage and native re-derivation.

The manifest hash is unkeyed and anyone can recompute it, so it cannot protect
native labels on its own. Each bundle carries the exact raw output and the
parser identity; native projections are re-derived from that text and must
match exactly. A parser version this code does not implement is reported as
unverified, never as verified.
"""

from . import native
from . import reviews as evidence_reviews
from .contract import ContractError, jsonl, sha256, unique

SHARED_TYPES = {"Work", "SourceVersion"}


def verify_coverage(records: list[dict]) -> dict[str, dict]:
    """Return the covering manifest for every AuditRun; reject anything uncovered."""
    by_id = unique(records, "records")
    manifests = [r for r in records if r["type"] == "RunManifest"]
    covered: dict[str, list[dict]] = {}
    run_manifest: dict[str, dict] = {}
    for manifest in manifests:
        ids = manifest["record_ids"]
        if (len(ids) != len(set(ids)) or manifest["id"] in ids
                or any(id not in by_id for id in ids)
                or any(by_id[id]["type"] == "RunManifest" for id in ids)):
            raise ContractError("INVALID_MANIFEST_RECORD_SET")
        if sha256(jsonl([by_id[id] for id in ids])) != manifest["records_before_manifest_sha256"]:
            raise ContractError("MANIFEST_RECORD_HASH_MISMATCH")
        run = by_id.get(manifest["audit_run_id"])
        if run is None or run["type"] != "AuditRun" or run["id"] not in ids:
            raise ContractError(f"INVALID_MANIFEST_COVERAGE: {manifest['id']} does not cover its AuditRun")
        if run["id"] in run_manifest:
            raise ContractError(f"INVALID_MANIFEST_COVERAGE: {run['id']} has more than one manifest")
        run_manifest[run["id"]] = manifest
        for id in ids:
            covered.setdefault(id, []).append(manifest)
    for item in records:
        if item["type"] == "RunManifest":
            continue
        owners = covered.get(item["id"], [])
        if not owners:
            raise ContractError(f"INVALID_MANIFEST_COVERAGE: {item['id']} is not covered by any RunManifest")
        if item["type"] not in SHARED_TYPES and len(owners) > 1:
            raise ContractError(f"INVALID_MANIFEST_COVERAGE: {item['id']} is covered by more than one RunManifest")
        if "audit_run_id" in item and owners[0]["audit_run_id"] != item["audit_run_id"]:
            raise ContractError(f"INVALID_MANIFEST_COVERAGE: {item['id']} is covered by another run's manifest")
    return run_manifest


def rederive(run: dict, records: list[dict], by_id: dict[str, dict]) -> None:
    """Re-parse raw_output_text and require exact equality with stored projections."""
    rid = run["id"]
    parsed = native.parse(run["raw_output_text"])
    mismatched = []
    findings = {r["id"]: r for r in records
                if r["type"] == "AuditFinding" and r["audit_run_id"] == rid}
    expected = {f"{rid}/finding/{i}": f for i, f in enumerate(parsed["findings"], 1)}
    if set(findings) != set(expected):
        mismatched.append("findings")
    else:
        for fid in sorted(findings):
            native_finding = expected[fid]
            if findings[fid]["native"] != native_finding:
                mismatched.append(f"{fid}.native")
            start, end = native.output_span(run["raw_output_text"], native_finding["line_start"],
                                            native_finding["line_end"])
            if findings[fid].get("native_output_anchor") != {
                    "output_sha256": run["output_sha256"], "first_line": native_finding["line_start"],
                    "last_line_inclusive": native_finding["line_end"], "unit": "one_based_line",
                    "char_start": start, "char_end": end, "char_unit": "unicode_codepoint",
                    "char_interval": "half_open"}:
                mismatched.append(f"{fid}.native_output_anchor")
    if run["native_scorecard"] != parsed["scorecard"]:
        mismatched.append("native_scorecard")
    if run["native_parse_issues"] != parsed["issues"]:
        mismatched.append("native_parse_issues")
    if ("imported_null_assertion" not in run
            or run["imported_null_assertion"] != parsed["null_assertion"]):
        mismatched.append("imported_null_assertion")
    corpus = by_id.get(run["corpus_scope_id"])
    if corpus is None or corpus["imported_source_lock"] != parsed["source_lock"]:
        mismatched.append("imported_source_lock")
    if mismatched:
        raise ContractError(f"NATIVE_PROJECTION_MISMATCH: {rid}: {', '.join(mismatched)}")


def verify_records(records: list[dict]) -> dict:
    """Raise on any integrity failure; report which runs were re-derived."""
    by_id = unique(records, "records")
    run_manifest = verify_coverage(records)
    verified, unverified = [], []
    for rid in sorted(run_manifest):
        parser = run_manifest[rid]["parser"]
        version = parser.get("version")
        if parser.get("name") == native.NAME and version in native.SUPPORTED_VERSIONS:
            rederive(by_id[rid], records, by_id)
            verified.append(rid)
        else:
            unverified.append({"audit_run_id": rid, "status": "NATIVE_PROJECTION_UNVERIFIED",
                               "parser": {"name": parser.get("name"), "version": version},
                               "reason": "recorded parser version is not supported by this code; "
                                         "native labels were not re-derived and are not trusted"})
    for item in records:
        if item["type"] == "ReviewDecision" and "review_schema" in item:
            verify_evidence_review(item, records, by_id, run_manifest)
    return {"native_projection_verified": verified, "native_projection_unverified": unverified}


def verify_evidence_review(item: dict, records: list[dict], by_id: dict, run_manifest: dict) -> None:
    """Re-derive an evidence review's binding from the bundle; reject any difference."""
    if item["review_schema"] != evidence_reviews.SCHEMA_ID:
        reason = evidence_reviews.RETIRED_REVIEW_SCHEMAS.get(item["review_schema"], "unknown")
        raise ContractError(f"UNSUPPORTED_REVIEW_SCHEMA: {item['review_schema']} ({reason}): {item['id']}")
    review = evidence_reviews.verify_record(item)
    rid = item["id"].split("/review/")[0]
    if rid not in run_manifest:
        raise ContractError(f"REVIEW_BINDING_MISMATCH: {item['id']}: run not in bundle")
    declared = [r for r in run_manifest[rid]["input_context"]["reviews"]
                if f"{rid}/review/{r['id']}" == item["id"]]
    if len(declared) != 1 or declared[0]["artifact"]["sha256"] != item["raw_output_sha256"]:
        raise ContractError(f"REVIEW_ARTIFACT_MISMATCH: {item['id']}: not the declared artifact")
    mismatches = evidence_reviews.target_mismatches(
        review["target"], run_id=rid, output_sha256=by_id[rid]["output_sha256"],
        context=run_manifest[rid]["input_context"], records=records)
    refs = [] if mismatches else evidence_reviews.review_refs(review["target"], rid, records)
    if item["target_mismatches"] != mismatches or item["refs"] != refs:
        raise ContractError(f"REVIEW_BINDING_MISMATCH: {item['id']}")
