"""Evidence-proposition reviews: extension atlas-evidence-review/2.

A review artifact (JSON) records one reviewer's bounded disposition on one
proposition: an exact span of one field of one native finding, as mapped to one
source check and its passages. It is imported as a ReviewDecision record. The
review binds to exact identities: output bytes, the finding's native projection,
the proposition span, the check definition (the mapping), each passage's full
descriptor (source version, component, start and end offsets, offset unit,
interval and quotation hash), the source version and the source input bytes. If
any of those differ, the binding is TARGET_MISMATCH, naming the components, and
the run does not reference the review: a changed mapping never inherits an old
review.

Version 2 replaces /1, which bound each passage by quotation hash only: moving a
passage's offsets while keeping its quotation left a /1 review attached. /1
artifacts are rejected on import and restore (UNSUPPORTED_REVIEW_SCHEMA), never
trusted.

Dispositions are this extension's own versioned vocabulary. They do not replace
native labels, do not change AuditFinding.assessment or Relationship
epistemic_status, and say nothing about parts of the finding outside the
proposition. Version 1 records reviews, never human adjudication or independence.
"""

from .contract import (EVIDENCE_REVIEW_SCHEMA, RETIRED_REVIEW_SCHEMAS, ContractError, digest,
                       load_json, require, sha256)

SCHEMA_ID = EVIDENCE_REVIEW_SCHEMA
PASSAGE = {"source_version_id": str, "component_id": str, "start": int, "end": int,
           "unit": str, "interval": str, "quote_sha256": str}
DISPOSITIONS = {"SUPPORTS", "SUPPORTS_WITH_QUALIFICATION", "CONTRADICTS",
                "INSUFFICIENT_EVIDENCE", "PENDING"}
TARGET = {"output_sha256": str, "finding_number": str, "finding_native_sha256": str,
          "proposition": str, "proposition_field": str, "proposition_start": int,
          "proposition_end": int, "check_id": str, "check_sha256": str,
          "source_version_id": str, "source_input_sha256": str, "passages": dict}
REVIEW = {"schema": str, "review_id": str, "target": dict, "coverage": dict, "reviewer": dict,
          "performed_at": str, "method": str, "inputs": list, "exposure": dict,
          "examination_boundary": dict, "disposition": str, "part_dispositions": list,
          "reasons": list, "locators": list, "qualifications": list,
          "strongest_contrary_interpretation": str, "what_would_change": list,
          "independence": str, "human_adjudication": str}


def load_review(data: bytes) -> dict:
    review = load_json(data)
    require(review, REVIEW, "review")
    if review["schema"] != SCHEMA_ID:
        reason = RETIRED_REVIEW_SCHEMAS.get(review["schema"], "unknown")
        raise ContractError(f"UNSUPPORTED_REVIEW_SCHEMA: {review['schema']} ({reason})")
    require(review["target"], TARGET, "review.target")
    if not review["target"]["passages"]:
        raise ContractError("INVALID_REVIEW: no passages bound")
    for pid, descriptor in review["target"]["passages"].items():
        require(descriptor, PASSAGE, f"review.target.passages.{pid}")
        if set(descriptor) != set(PASSAGE):
            raise ContractError(f"INVALID_REVIEW: passage descriptor fields {pid}")
    require(review["coverage"], {"reviewed": list, "not_reviewed": list,
                                 "finding_level_effect": str}, "review.coverage")
    require(review["reviewer"], {"identity": str, "kind": str, "context": str}, "review.reviewer")
    if review["disposition"] not in DISPOSITIONS:
        raise ContractError(f"INVALID_LABEL: review disposition {review['disposition']}")
    for part in review["part_dispositions"]:
        require(part, {"part": str, "text": str, "disposition": str, "reasons": list}, "review.part")
        if part["disposition"] not in DISPOSITIONS:
            raise ContractError(f"INVALID_LABEL: part disposition {part['disposition']}")
    for locator in review["locators"]:
        require(locator, {"id": str, "pdf_page": int, "section": str, "quote": str,
                          "quote_sha256": str}, "review.locator")
        if sha256(locator["quote"].encode("utf-8")) != locator["quote_sha256"]:
            raise ContractError(f"INVALID_REVIEW: locator hash {locator['id']}")
    # Version 1 can record what a reviewer concluded; it cannot record that the
    # conclusion was adjudicated, that reviewers were independent, or that the
    # whole finding was approved.
    if (review["human_adjudication"] != "NOT_PERFORMED" or review["independence"] != "NOT_ESTABLISHED"
            or review["coverage"]["finding_level_effect"] != "NONE"):
        raise ContractError("INVALID_REVIEW: v1 records no adjudication, independence or finding approval")
    target = review["target"]
    if not 0 <= target["proposition_start"] < target["proposition_end"]:
        raise ContractError("INVALID_REVIEW: proposition span")
    return review


def passage_descriptor(passage: dict) -> dict:
    """The identity a review binds for one Passage record."""
    locator = passage["locator"]
    return {"source_version_id": passage["source_version_id"], "component_id": locator["component_id"],
            "start": locator["start"], "end": locator["end"], "unit": locator["unit"],
            "interval": locator["interval"], "quote_sha256": sha256(passage["quote"].encode("utf-8"))}


def target_mismatches(target: dict, *, run_id: str, output_sha256: str, context: dict,
                      records: list[dict]) -> list[str]:
    """Compare a declared target with one run's records; return differing components."""
    mismatches = []
    if target["output_sha256"] != output_sha256:
        mismatches.append("output")
    findings = [r for r in records if r["type"] == "AuditFinding" and r["audit_run_id"] == run_id
                and str(r["native"]["number"]) == target["finding_number"]]
    finding = findings[0] if len(findings) == 1 else None
    if finding is None or digest(finding["native"]) != target["finding_native_sha256"]:
        mismatches.append("finding")
    value = finding["native"]["fields"].get(target["proposition_field"]) if finding else None
    if value is None or value[target["proposition_start"]:target["proposition_end"]] != target["proposition"]:
        mismatches.append("proposition")
    check = next((c for c in context["checks"] if c["id"] == target["check_id"]), None)
    mapped = context["finding_checks"].get(target["finding_number"], [])
    check_passages = {pid for req in check["requirements"] for pid in req["passage_ids"]} if check else set()
    if (check is None or target["check_id"] not in mapped or digest(check) != target["check_sha256"]
            or check_passages != set(target["passages"])):
        mismatches.append("mapping")
    passages = {r["native_id"]: r for r in records
                if r["type"] == "Passage" and r["id"].startswith(f"{run_id}/passage/")}
    if any(pid not in passages or passage_descriptor(passages[pid]) != descriptor
           for pid, descriptor in target["passages"].items()):
        mismatches.append("passages")
    if any(pid in passages and passages[pid]["source_version_id"] != target["source_version_id"]
           for pid in target["passages"]):
        mismatches.append("source_version")
    receipt = next((r for r in records if r["type"] == "SourceReadReceipt" and r["audit_run_id"] == run_id
                    and r["source_version_id"] == target["source_version_id"]), None)
    if receipt is None or receipt["input_bytes_sha256"] != target["source_input_sha256"]:
        mismatches.append("source_input")
    return mismatches


def review_refs(target: dict, run_id: str, records: list[dict]) -> list[str]:
    finding = next(r for r in records if r["type"] == "AuditFinding" and r["audit_run_id"] == run_id
                   and str(r["native"]["number"]) == target["finding_number"])
    passage_ids = [f"{run_id}/passage/{pid}" for pid in sorted(target["passages"])]
    relations = [f"{finding['id']}/evidence/{pid}" for pid in sorted(target["passages"])
                 if any(r["id"] == f"{finding['id']}/evidence/{pid}" for r in records)]
    return [run_id, finding["id"], *passage_ids, *relations]


def verify_record(item: dict) -> dict:
    """Static checks on an evidence-review ReviewDecision; returns the parsed review."""
    text = item.get("review_artifact_text")
    if type(text) is not str or sha256(text.encode("utf-8")) != item["raw_output_sha256"]:
        raise ContractError(f"REVIEW_ARTIFACT_MISMATCH: {item['id']}")
    review = load_review(text.encode("utf-8"))
    if (item.get("review") != review or item.get("declared_target") != review["target"]
            or item["imported_disposition"] != review["disposition"]
            or item["independence"] != "NOT_ESTABLISHED" or item["human_adjudication"] != "NOT_RECORDED"):
        raise ContractError(f"REVIEW_ARTIFACT_MISMATCH: {item['id']}")
    mismatches = item.get("target_mismatches")
    if (type(mismatches) is not list
            or item["target_binding"] != ("MATCH" if not mismatches else "TARGET_MISMATCH")
            or (mismatches and item["refs"])):
        raise ContractError(f"INVALID_LABEL: review binding {item['id']}")
    return review
