"""Replay an import from its manifest and exact local inputs.

strict:  byte-identical records and manifest, environment included.
content: identical inputs, code, parser, normalizer, baseline and every record
         except the manifest's environment block; the environment delta is
         reported, not hidden.
Neither level reproduces the historical model run.
"""

from pathlib import Path

from .adapter import build
from .contract import ContractError, load_json
from .ledger import read_export

LEVELS = ("strict", "content")


def components(manifest: dict) -> dict:
    adapter = manifest.get("adapter", {})
    return {
        "input_context": manifest.get("input_context"),
        "declared_inputs": [manifest.get("declared_input_receipts"),
                            manifest.get("source_input_receipts")],
        "adapter_code": [adapter.get("name"), adapter.get("version"), adapter.get("code_sha256")],
        "parser": manifest.get("parser"),
        "normalizer": manifest.get("normalizer"),
        "baseline": [adapter.get("baseline_sha256"), manifest.get("validation_baseline")],
    }


def without_environment(item: dict) -> dict:
    return {k: v for k, v in item.items() if not (item.get("type") == "RunManifest" and k == "environment")}


def replay(manifest_bytes: bytes, jsonl_bytes: bytes, root: Path, level: str = "strict") -> dict:
    if level not in LEVELS:
        raise ContractError(f"UNSUPPORTED_REPLAY_LEVEL: {level}")
    manifest = load_json(manifest_bytes)
    try:
        stored = read_export(jsonl_bytes)
    except ContractError as exc:
        raise ContractError(f"REPLAY_MISMATCH: records: {exc}") from exc
    try:
        bundle = build(manifest["input_context"], root)
    except (ContractError, KeyError) as exc:
        raise ContractError(f"REPLAY_MISMATCH: input: {exc}") from exc
    fresh = bundle["manifest"]

    recorded, current = components(manifest), components(fresh)
    differing = [name for name in recorded if recorded[name] != current[name]]
    old = {r["id"]: without_environment(r) for r in stored}
    new = {r["id"]: without_environment(r) for r in bundle["records"]}
    changed = sorted(id for id in old.keys() | new.keys() if old.get(id) != new.get(id))
    if changed:
        differing.append("records: " + ", ".join(changed))
    if without_environment(manifest) != without_environment(fresh):
        differing.append("manifest")
    old_env, new_env = manifest.get("environment", {}), fresh["environment"]
    delta = {key: {"recorded": old_env.get(key), "replayed": new_env.get(key)}
             for key in sorted(old_env.keys() | new_env.keys()) if old_env.get(key) != new_env.get(key)}
    if level == "strict":
        if delta:
            differing.append("environment: " + ", ".join(delta))
        if not differing and (manifest != fresh or bundle["jsonl"] != jsonl_bytes):
            differing.append("bytes")
    if differing:
        raise ContractError(f"REPLAY_MISMATCH ({level}): " + "; ".join(differing))
    return {"replay": "PASS", "level": level, "environment_delta": delta,
            "scope": "deterministic import replay; historical model run not reproduced"}
