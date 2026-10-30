"""Small portable record contract. This is not the proposed atlas-core schema."""

from __future__ import annotations

import hashlib
from datetime import datetime
import json
from pathlib import Path
import re
import unicodedata

from . import CONTEXT_SCHEMA, SCHEMA

NORMALIZER = "nfc-whitespace/2"
TYPES = {"Work", "SourceVersion", "SourceReadReceipt", "Passage", "CorpusScope",
         "AuditRun", "AuditFinding", "Relationship", "ReviewDecision", "RunManifest"}
READ_STATES = {"NOT_RETRIEVED", "RETRIEVAL_FAILED", "METADATA_ONLY", "PARTIAL_READ",
               "READ_FOR_DECLARED_SCOPE", "EXTRACTION_UNVERIFIED"}
ELIGIBILITY = {"ELIGIBLE", "ELIGIBLE_WITH_LIMITATIONS", "PENDING_SOURCE_VERIFICATION",
               "INELIGIBLE_MISSING_EVIDENCE", "NOT_APPLICABLE"}
# Evidence-review binding contract (atlas/reviews.py). /1 bound passages by quotation
# hash only, so a moved locator kept its review; it is retired, not trusted.
EVIDENCE_REVIEW_SCHEMA = "atlas-evidence-review/2"
RETIRED_REVIEW_SCHEMAS = {"atlas-evidence-review/1": "binds passages by quotation hash only; "
                          "re-issue as atlas-evidence-review/2"}
ANCHOR_STATES = {"MATCH", "NORMALIZED_MATCH_ONLY", "MISMATCH", "UNRESOLVABLE"}
KINDS = {"metadata", "text", "page", "section", "table", "figure", "equation",
         "references", "appendix", "supplement"}
RECORD_FIELDS = {
    "Work": {"metadata": dict},
    "SourceVersion": {"work_id": str, "version": str, "version_basis": str,
                      "version_confidence": str, "source_uri": str},
    "SourceReadReceipt": {"audit_run_id": str, "work_id": str, "source_version_id": str,
                          "state": str, "extraction": dict, "extracted_components": list,
                          "failed_components": list, "warnings": list, "receipt_sha256": str,
                          "per_check_eligibility": dict},
    "Passage": {"source_version_id": str, "receipt_id": str, "locator": dict,
                "quote": str, "match": str, "normalizer": str,
                "exact_match": bool, "normalized_match": bool},
    "CorpusScope": {"declared": dict, "imported_source_lock": dict, "lock_verification": str},
    "AuditRun": {"target_work_id": str, "model": dict, "runner": dict, "exposure": dict,
                 "output_sha256": str, "context_sha256": str, "syntax": str,
                 "source_checks": dict, "paper_clean": bool, "human_review": str,
                 "raw_output_text": str, "corpus_scope_id": str, "native_scorecard": list,
                 "native_parse_issues": list, "producing_instrument_compliance": str,
                 "mismatched_review_ids": list, "adapter_source_eligibility": dict},
    "AuditFinding": {"audit_run_id": str, "native": dict, "source_checks": list,
                     "evidence_passage_ids": list, "import_status": str, "assessment": str},
    "Relationship": {"subject_id": str, "object_id": str, "kind": str,
                     "relation_basis": str, "epistemic_status": str},
    "ReviewDecision": {"artifact": dict, "target_binding": str, "imported_disposition": str,
                       "independence": str, "human_adjudication": str},
    "RunManifest": {"audit_run_id": str, "adapter": dict, "parser": dict, "input_context": dict,
                    "environment": dict, "checker": dict, "record_ids": list,
                    "records_before_manifest_sha256": str},
}
REFERENCE_FIELDS = {
    "SourceVersion": ("work_id",),
    "SourceReadReceipt": ("audit_run_id", "work_id", "source_version_id", "source_lock_ref"),
    "Passage": ("source_version_id", "receipt_id"),
    "AuditRun": ("target_work_id", "corpus_scope_id"), "AuditFinding": ("audit_run_id",),
    "Relationship": ("subject_id", "object_id"), "RunManifest": ("audit_run_id",),
}


class ContractError(ValueError):
    pass


def canonical(value: object) -> str:
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"),
                      allow_nan=False)


def sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def digest(value: object) -> str:
    return sha256(canonical(value).encode("utf-8"))


def normalize(text: str) -> str:
    # NFC + whitespace collapse only. NFKC is not used: it equates 10² with 102,
    # H₂O with H2O and µ with μ. Never dehyphenate or relocate passages.
    return " ".join(unicodedata.normalize("NFC", text).split())


def passage_hash(text: str) -> str:
    return sha256(normalize(text).encode("utf-8"))


def load_json(data: bytes) -> dict:
    def pairs(items):
        result = {}
        for key, value in items:
            if key in result:
                raise ContractError(f"DUPLICATE_FIELD: {key}")
            result[key] = value
        return result
    try:
        value = json.loads(data, object_pairs_hook=pairs,
                           parse_constant=lambda x: (_ for _ in ()).throw(
                               ContractError(f"INVALID_JSON: {x}")))
    except (ValueError, UnicodeError) as exc:
        raise ContractError(f"INVALID_JSON: {exc}") from exc
    if not isinstance(value, dict):
        raise ContractError("INVALID_JSON: expected object")
    return value


def require(obj: dict, fields: dict[str, type], where: str) -> None:
    if not isinstance(obj, dict):
        raise ContractError(f"INVALID_CONTRACT: {where} must be an object")
    for key, kind in fields.items():
        if key not in obj:
            raise ContractError(f"MISSING: {where}.{key}")
        if type(obj[key]) is not kind or (kind is str and not obj[key].strip()):
            raise ContractError(f"INVALID_CONTRACT: {where}.{key}")


def unique(items: list[dict], where: str) -> dict[str, dict]:
    result = {}
    for item in items:
        require(item, {"id": str}, where)
        if item["id"] in result:
            raise ContractError(f"DUPLICATE_ID: {where}: {item['id']}")
        result[item["id"]] = item
    return result


def string_list(value, where):
    if (type(value) is not list or any(type(v) is not str or not v.strip() for v in value)
            or len(value) != len(set(value))):
        raise ContractError(f"INVALID_CONTRACT: {where} must be distinct strings")


def read_artifact(root: Path, artifact: dict) -> bytes:
    require(artifact, {"path": str, "sha256": str}, "artifact")
    path = Path(artifact["path"])
    if path.is_absolute() or ".." in path.parts or not path.parts:
        raise ContractError(f"INPUT_BOUNDARY: {path}")
    resolved = (root / path).resolve()
    if not resolved.is_relative_to(root.resolve()):
        raise ContractError(f"INPUT_BOUNDARY: symlink {path}")
    if not re.fullmatch(r"[0-9a-f]{64}", artifact["sha256"]):
        raise ContractError(f"INVALID_HASH: {path}")
    try:
        data = resolved.read_bytes()
    except OSError as exc:
        raise ContractError(f"INPUT_UNAVAILABLE: {path}") from exc
    if sha256(data) != artifact["sha256"]:
        raise ContractError(f"INPUT_HASH_MISMATCH: {path}")
    return data


def validate_context(context: dict) -> None:
    require(context, {"schema_version": str, "run": dict, "output": dict,
                      "works": list, "sources": list, "passages": list,
                      "checks": list, "finding_checks": dict, "corpus": dict,
                      "declared_inputs": list, "reviews": list}, "context")
    if context["schema_version"] != CONTEXT_SCHEMA:
        raise ContractError("UNSUPPORTED_SCHEMA")
    require(context["run"], {"id": str, "target_work_id": str, "imported_at": str,
                             "origin": str, "model": dict, "runner": dict,
                             "historical_instrument": dict, "exposure": dict}, "run")
    if not re.fullmatch(r"\d{4}-\d\d-\d\dT\d\d:\d\d:\d\dZ", context["run"]["imported_at"]):
        raise ContractError("INVALID_TIMESTAMP")
    try:
        datetime.strptime(context["run"]["imported_at"], "%Y-%m-%dT%H:%M:%SZ")
    except ValueError as exc:
        raise ContractError("INVALID_TIMESTAMP") from exc
    for name in ("model", "runner", "historical_instrument"):
        require(context["run"][name], {"identity": str, "verification": str}, name)
    require(context["run"]["exposure"], {"prior_outputs_seen": str,
                                        "independence": str, "basis": str}, "exposure")
    works = unique(context["works"], "works")
    sources = unique(context["sources"], "sources")
    passages = unique(context["passages"], "passages")
    checks = unique(context["checks"], "checks")
    if context["run"]["target_work_id"] not in works:
        raise ContractError("UNRESOLVED_REFERENCE: target_work_id")
    for work in works.values():
        require(work, {"title": str, "kind": str, "identity_basis": str}, "work")
    for source in sources.values():
        require(source, {"work_id": str, "version": str, "version_basis": str,
                         "version_confidence": str, "source_uri": str,
                         "accessed_at": str, "access_outcome": str,
                         "rights": str, "extraction": dict, "components": list,
                         "requested_components": list, "warnings": list,
                         "failed_components": list, "origin_id": str}, "source")
        if source["work_id"] not in works:
            raise ContractError("UNRESOLVED_REFERENCE: source work_id")
        if source["access_outcome"] not in {"AVAILABLE", "NOT_RETRIEVED", "RETRIEVAL_FAILED"}:
            raise ContractError("INVALID_LABEL: access_outcome")
        require(source["extraction"], {"engine": str, "version": str,
                                       "configuration": dict}, "extraction")
        for key in ("requested_components", "warnings", "failed_components"):
            string_list(source[key], key)
        for comp in unique(source["components"], "components").values():
            require(comp, {"kind": str, "start": int, "end": int}, "component")
            if comp["kind"] not in KINDS:
                raise ContractError("INVALID_LABEL: component kind")
    for passage in passages.values():
        require(passage, {"source_version_id": str, "component_id": str,
                          "start": int, "end": int, "quote": str,
                          "normalized_sha256": str}, "passage")
        if passage["source_version_id"] not in sources:
            raise ContractError("UNRESOLVED_REFERENCE: passage source_version_id")
    for check in checks.values():
        require(check, {"kind": str, "scope": str, "requirements": list}, "check")
        if check["kind"] not in {"metadata", "content"}:
            raise ContractError("INVALID_LABEL: check kind")
        for req in check["requirements"]:
            require(req, {"source_version_id": str, "component_ids": list,
                          "passage_ids": list}, "requirement")
            string_list(req["component_ids"], "component_ids")
            string_list(req["passage_ids"], "passage_ids")
            if req["source_version_id"] not in sources:
                raise ContractError("UNRESOLVED_REFERENCE: requirement source")
            for pid in req["passage_ids"]:
                if pid not in passages or passages[pid]["source_version_id"] != req["source_version_id"]:
                    raise ContractError("UNRESOLVED_REFERENCE: requirement passage")
    for number, ids in context["finding_checks"].items():
        string_list(ids, "finding_checks")
        if not number.isdecimal() or type(ids) is not list or any(i not in checks for i in ids):
            raise ContractError("INVALID_CONTRACT: finding_checks")
    string_list(context.get("null_check_ids", []), "null_check_ids")
    require(context["corpus"], {"id": str, "boundary": str, "selection": str,
                               "retrieval_events": list, "limitations": list}, "corpus")
    for review in context["reviews"]:
        if "review_schema" in review:
            # Structured review: target and attribution live in the hashed artifact.
            require(review, {"id": str, "artifact": dict, "review_schema": str}, "review")
            if review["review_schema"] != EVIDENCE_REVIEW_SCHEMA:
                reason = RETIRED_REVIEW_SCHEMAS.get(review["review_schema"], "unknown")
                raise ContractError(f"UNSUPPORTED_REVIEW_SCHEMA: {review['review_schema']} ({reason})")
            continue
        require(review, {"id": str, "artifact": dict, "target_output_sha256": str,
                         "reviewer": str, "exposure": str, "disposition": str}, "review")


def record(record_type: str, id: str, **fields) -> dict:
    if record_type not in TYPES:
        raise ContractError(f"UNKNOWN_RECORD_TYPE: {record_type}")
    return {"schema_version": SCHEMA, "type": record_type, "id": id, **fields}


def validate_records(records: list[dict]) -> None:
    by_id = unique(records, "records")
    for item in records:
        require(item, {"schema_version": str, "type": str, "refs": list}, "record")
        string_list(item["refs"], "refs")
        if item["schema_version"] != SCHEMA or item["type"] not in TYPES:
            raise ContractError("UNSUPPORTED_RECORD")
        require(item, RECORD_FIELDS[item["type"]], item["type"])
        for key in REFERENCE_FIELDS.get(item["type"], ()):
            if item.get(key) not in item["refs"]:
                raise ContractError(f"UNDECLARED_REFERENCE: {key}")
        if item["type"] == "AuditFinding" and any(p not in item["refs"] for p in item["evidence_passage_ids"]):
            raise ContractError("UNDECLARED_REFERENCE: evidence_passage_ids")
        if item["type"] == "SourceReadReceipt":
            if item["state"] not in READ_STATES:
                raise ContractError("INVALID_LABEL: read state")
            expected = digest({k: v for k, v in item.items() if k != "receipt_sha256"})
            if item["receipt_sha256"] != expected:
                raise ContractError("RECEIPT_HASH_MISMATCH")
        if item["type"] == "Passage":
            if item["match"] not in ANCHOR_STATES:
                raise ContractError("INVALID_LABEL: anchor match")
            # Only an exact code-point match may be displayed as MATCH.
            if ((item["match"] == "MATCH" and not item["exact_match"])
                    or (item["match"] == "NORMALIZED_MATCH_ONLY"
                        and (item["exact_match"] or not item["normalized_match"]))):
                raise ContractError("INVALID_LABEL: anchor match contradicts exact/normalized fields")
        if (item["type"] == "AuditRun" and item["producing_instrument_compliance"]
                not in {"UNDETERMINED", "CONFORMS", "VIOLATION"}):
            raise ContractError("INVALID_LABEL: producing_instrument_compliance")
        if item["type"] == "AuditRun":
            if type(item.get("imported_null_assertion", 0)) not in (str, type(None)):
                raise ContractError("INVALID_CONTRACT: AuditRun.imported_null_assertion")
            string_list(item["mismatched_review_ids"], "mismatched_review_ids")
            for rid in item["mismatched_review_ids"]:
                review = by_id.get(rid, {})
                if review.get("type") != "ReviewDecision" or review.get("target_binding") != "TARGET_MISMATCH":
                    raise ContractError(f"INVALID_CONTRACT: mismatched_review_ids: {rid}")
            for ref in item["refs"]:
                if by_id.get(ref, {}).get("type") == "ReviewDecision" and by_id[ref]["target_binding"] != "MATCH":
                    raise ContractError(f"INVALID_CONTRACT: run refs a review of another output: {ref}")
        if item["type"] == "AuditRun" and sha256(item["raw_output_text"].encode("utf-8")) != item["output_sha256"]:
            raise ContractError("OUTPUT_HASH_MISMATCH")
        for ref in item["refs"]:
            if ref not in by_id:
                raise ContractError(f"UNRESOLVED_REFERENCE: {item['id']} -> {ref}")


def jsonl(records: list[dict]) -> bytes:
    validate_records(records)
    return ("\n".join(canonical(r) for r in sorted(records, key=lambda r: r["id"])) + "\n").encode("utf-8")
