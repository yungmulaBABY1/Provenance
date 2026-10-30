"""Byte-bound source receipts and per-check eligibility, independent of labels."""

from pathlib import Path

from .contract import normalize, passage_hash, read_artifact, record, sha256, NORMALIZER


def inspect_sources(context: dict, root: Path) -> tuple[list[dict], dict, dict]:
    records, receipts, anchors = [], {}, {}
    run_id = context["run"]["id"]
    for source in context["sources"]:
        sid = source["id"]
        records.append(record("SourceVersion", sid, work_id=source["work_id"],
                              version=source["version"], version_basis=source["version_basis"],
                              version_confidence=source["version_confidence"],
                              source_uri=source["source_uri"], refs=[source["work_id"]]))
        artifact = source.get("text_artifact")
        data = read_artifact(root, artifact) if artifact else None
        text = None
        warnings = list(source["warnings"])
        if data is not None:
            try:
                text = data.decode("utf-8")
            except UnicodeError:
                warnings.append("INVALID_UTF8")
        direct_text = (source["extraction"]["engine"] == "plain-utf8"
                       and source["extraction"]["version"] == "1"
                       and source["extraction"]["configuration"] == {})
        available, failed = [], list(source["failed_components"])
        for comp in source["components"]:
            if (text is not None and 0 <= comp["start"] < comp["end"] <= len(text)
                    and comp["id"] not in failed):
                available.append(comp)
            else:
                failed.append(comp["id"])
        if source["access_outcome"] != "AVAILABLE":
            state = source["access_outcome"]
            available = []
        elif not direct_text or text is None:
            state = "EXTRACTION_UNVERIFIED"
        elif available and all(c["kind"] == "metadata" for c in available):
            state = "METADATA_ONLY"
        elif (set(source["requested_components"]) <= {c["id"] for c in available}
              and available and not failed and not warnings):
            state = "READ_FOR_DECLARED_SCOPE"
        else:
            state = "PARTIAL_READ"
        receipt_id = f"{run_id}/read/{sid}"
        receipt = record("SourceReadReceipt", receipt_id, audit_run_id=run_id,
                         work_id=source["work_id"], source_version_id=sid,
                         state=state, access_outcome=source["access_outcome"],
                         accessed_at=source["accessed_at"], source_uri=source["source_uri"],
                         rights=source["rights"], extraction=source["extraction"],
                         declared_input=artifact, input_bytes_sha256=sha256(data) if data is not None else None,
                         byte_hash_scope="RUN_LOCAL_NOT_CANONICAL_IDENTITY",
                         requested_components=source["requested_components"],
                         declared_components=source["components"], extracted_components=available,
                         character_count=len(text) if text is not None else None,
                         version_confidence=source["version_confidence"],
                         failed_components=sorted(set(failed)), warnings=warnings,
                         origin_id=source["origin_id"],
                         consumption_scope="ADAPTER_INPUT; historical runner reading is not established",
                         refs=[run_id, sid, source["work_id"]])
        receipts[sid] = receipt
        records.append(receipt)
        by_component = {c["id"]: c for c in available}
        for passage in context["passages"]:
            if passage["source_version_id"] != sid:
                continue
            comp = by_component.get(passage["component_id"])
            start, end = passage["start"], passage["end"]
            status = "UNRESOLVABLE"
            actual_hash = None
            exact = normalized = declared = False
            if text is not None and source["access_outcome"] == "AVAILABLE" and direct_text:
                status = "MISMATCH"
                if (comp and comp["start"] <= start < end <= comp["end"]
                        and 0 <= start < end <= len(text)):
                    span, quote = text[start:end], passage["quote"]
                    actual_hash = passage_hash(span)
                    exact = span == quote
                    normalized = normalize(span) == normalize(quote)
                    # A declared hash that disagrees with the quote is an
                    # inconsistent context, whatever the span says.
                    declared = passage["normalized_sha256"] == passage_hash(quote)
                    if declared and exact:
                        status = "MATCH"
                    elif declared and normalized:
                        status = "NORMALIZED_MATCH_ONLY"
            anchor = record("Passage", f"{run_id}/passage/{passage['id']}",
                            native_id=passage["id"], source_version_id=sid,
                            receipt_id=receipt_id, locator={"component_id": passage["component_id"],
                            "start": start, "end": end, "unit": "unicode_codepoint",
                            "interval": "half_open"}, quote=passage["quote"],
                            normalizer=NORMALIZER, hash_algorithm="sha256",
                            expected_normalized_sha256=passage["normalized_sha256"],
                            actual_normalized_sha256=actual_hash, declared_hash_match=declared,
                            exact_match=exact, normalized_match=normalized, match=status,
                            diagnostic="ANCHOR_MISMATCH" if status == "MISMATCH" else status,
                            version_confidence=source["version_confidence"],
                            public_release="NOT_REVIEWED", refs=[sid, receipt_id])
            anchors[passage["id"]] = anchor
            records.append(anchor)
    return records, receipts, anchors


def assess_checks(context: dict, receipts: dict, anchors: dict) -> dict:
    results = {}
    for check in context["checks"]:
        missing, pending, limitations = [], [], []
        if not check["requirements"]:
            pending.append("NO_REQUIREMENTS_DECLARED")
        for requirement in check["requirements"]:
            receipt = receipts[requirement["source_version_id"]]
            components = {c["id"]: c for c in receipt["extracted_components"]}
            if not requirement["component_ids"]:
                pending.append("NO_COMPONENT_SCOPE_DECLARED")
            for cid in requirement["component_ids"]:
                if cid not in components:
                    missing.append(f"{receipt['source_version_id']}:{cid}")
                elif check["kind"] == "content" and components[cid]["kind"] == "metadata":
                    missing.append(f"METADATA_IS_NOT_CONTENT:{cid}")
            if receipt["state"] in {"NOT_RETRIEVED", "RETRIEVAL_FAILED"}:
                missing.append(receipt["state"])
            if receipt["state"] == "EXTRACTION_UNVERIFIED":
                pending.append("EXTRACTION_UNVERIFIED")
            if check["kind"] == "content":
                if receipt["version_confidence"] == "UNKNOWN":
                    pending.append("SOURCE_VERSION_UNVERIFIED")
                if receipt["state"] == "METADATA_ONLY":
                    missing.append("METADATA_ONLY")
                if not requirement["passage_ids"]:
                    pending.append("NO_SOURCE_ANCHORS")
                for pid in requirement["passage_ids"]:
                    anchor = anchors[pid]
                    if anchor["locator"]["component_id"] not in requirement["component_ids"]:
                        pending.append(f"ANCHOR_OUTSIDE_CHECK_SCOPE:{pid}")
                    if anchor["match"] == "NORMALIZED_MATCH_ONLY":
                        # Not an exact quotation: a named limitation, never full eligibility.
                        limitations.append(f"NORMALIZED_MATCH_ONLY:{pid}")
                    elif anchor["match"] != "MATCH":
                        pending.append(f"{anchor['diagnostic']}:{pid}")
            if receipt["warnings"] or receipt["failed_components"]:
                limitations.append(receipt["id"])
        state = ("INELIGIBLE_MISSING_EVIDENCE" if missing else
                 "PENDING_SOURCE_VERIFICATION" if pending else
                 "ELIGIBLE_WITH_LIMITATIONS" if limitations else "ELIGIBLE")
        results[check["id"]] = {"id": check["id"], "kind": check["kind"],
                               "scope": check["scope"], "eligibility": state,
                               "requirements": check["requirements"],
                               "missing": sorted(set(missing)), "pending": sorted(set(pending)),
                               "limitations": sorted(set(limitations)),
                               "semantic_review": "REQUIRED"}
    return results
