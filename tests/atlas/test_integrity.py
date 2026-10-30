"""Restore/append integrity: manifest coverage and native re-derivation (R1, F1, F6).

The manifest hash is recomputable, so every mutation here recomputes it; the
rejection must come from coverage or from re-parsing the stored raw output.
"""

import copy
from pathlib import Path
import shutil
import tempfile
import unittest

from atlas.adapter import build
from atlas.contract import ContractError, canonical, jsonl, sha256
from atlas.integrity import verify_records
from atlas.ledger import append, export, read_export
from test_adapter import BASELINE, POWER, ROOT, SHEN, artifact, by_type


def raw_jsonl(records):
    # Bypass jsonl() so a test can serialize a set that validation must reject.
    return ("\n".join(canonical(r) for r in records) + "\n").encode()


def rehash(records, run_id):
    manifest = next(r for r in records if r["type"] == "RunManifest" and r["audit_run_id"] == run_id)
    body = [r for r in records if r["id"] in set(manifest["record_ids"])]
    manifest["records_before_manifest_sha256"] = sha256(jsonl(body))
    return records


def flip_concede(records):
    finding = next(r for r in records if r["type"] == "AuditFinding")
    original = finding["native"]["fields"]["Concede test"]
    altered = {"SURVIVES": "DEFEATS", "NARROWS": "SURVIVES", "DEFEATS": "SURVIVES"}[original]
    finding["native"]["fields"]["Concede test"] = altered
    finding["native"]["labels"]["Concede test"] = altered
    return rehash(records, finding["audit_run_id"])


class IntegrityTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        paths = set(BASELINE["files"])
        paths.update(a["path"] for c in (POWER, SHEN) for a in c["declared_inputs"])
        for path in paths:
            dest = self.root / path
            dest.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(ROOT / path, dest)
        self.power = build(copy.deepcopy(POWER), self.root)

    def test_missing_manifest_rejected(self):
        records = [r for r in self.power["records"] if r["type"] != "RunManifest"]
        with self.assertRaisesRegex(ContractError, "INVALID_MANIFEST_COVERAGE"):
            read_export(raw_jsonl(records))

    def test_uncovered_record_rejected(self):
        records = copy.deepcopy(self.power["records"])
        records.append({"schema_version": records[0]["schema_version"], "type": "Work",
                        "id": "injected/work", "metadata": {"title": "not covered"}, "refs": []})
        with self.assertRaisesRegex(ContractError, "INVALID_MANIFEST_COVERAGE: injected/work"):
            read_export(raw_jsonl(records))

    def test_run_record_covered_twice_rejected(self):
        ctx = copy.deepcopy(POWER)
        ctx["run"]["id"] += ":second"
        second = copy.deepcopy(build(ctx, self.root)["records"])
        manifest = next(r for r in second if r["type"] == "RunManifest")
        # The first run's CorpusScope refs only shared SourceVersions, so the
        # second manifest's record set still resolves when it claims it too.
        corpus = next(r["id"] for r in self.power["records"] if r["type"] == "CorpusScope")
        manifest["record_ids"] = sorted([*manifest["record_ids"], corpus])
        records = list({r["id"]: r for r in [*self.power["records"], *second]}.values())
        rehash(records, manifest["audit_run_id"])
        with self.assertRaisesRegex(ContractError, "INVALID_MANIFEST_COVERAGE: .*more than one RunManifest"):
            read_export(raw_jsonl(records))

    def test_concede_mutation_with_recomputed_manifest_hash_rejected(self):
        records = flip_concede(copy.deepcopy(self.power["records"]))
        with self.assertRaisesRegex(ContractError, "NATIVE_PROJECTION_MISMATCH: .*finding/1.native"):
            read_export(jsonl(records))
        with self.assertRaisesRegex(ContractError, "NATIVE_PROJECTION_MISMATCH"):
            append(self.root / "ledger.db", records)

    def test_run_level_projection_mutations_rejected(self):
        for mutate, component in [
                (lambda run, corpus: run["native_scorecard"].pop(), "native_scorecard"),
                (lambda run, corpus: run["native_parse_issues"].append(
                    {"code": "MISSING", "field": "x", "line": None}), "native_parse_issues"),
                (lambda run, corpus: run.update(imported_null_assertion="No findings of consequence."),
                 "imported_null_assertion"),
                (lambda run, corpus: corpus["imported_source_lock"].update(
                    {"SOURCE-LOCK METHOD": "LOCKED QUERY"}), "imported_source_lock")]:
            with self.subTest(component=component):
                records = copy.deepcopy(self.power["records"])
                run = next(r for r in records if r["type"] == "AuditRun")
                corpus = next(r for r in records if r["type"] == "CorpusScope")
                mutate(run, corpus)
                rehash(records, run["id"])
                with self.assertRaisesRegex(ContractError, f"NATIVE_PROJECTION_MISMATCH: .*{component}"):
                    read_export(jsonl(records))

    def test_removed_finding_rejected(self):
        records = copy.deepcopy(self.power["records"])
        drop = next(r["id"] for r in records if r["type"] == "AuditFinding")
        records = [r for r in records if r["id"] != drop and drop not in r["refs"]]
        manifest = next(r for r in records if r["type"] == "RunManifest")
        manifest["record_ids"] = [i for i in manifest["record_ids"] if i in {r["id"] for r in records}]
        rehash(records, manifest["audit_run_id"])
        with self.assertRaisesRegex(ContractError, "NATIVE_PROJECTION_MISMATCH: .*findings"):
            read_export(jsonl(records))

    def test_unsupported_parser_version_reported_unverified(self):
        records = flip_concede(copy.deepcopy(self.power["records"]))
        manifest = next(r for r in records if r["type"] == "RunManifest")
        manifest["parser"]["version"] = "0-not-implemented"
        restored = read_export(jsonl(records))
        report = verify_records(restored)
        rid = manifest["audit_run_id"]
        self.assertEqual(report["native_projection_verified"], [])
        self.assertEqual(report["native_projection_unverified"][0]["audit_run_id"], rid)
        self.assertEqual(report["native_projection_unverified"][0]["status"], "NATIVE_PROJECTION_UNVERIFIED")
        self.assertEqual(report["native_projection_unverified"][0]["parser"]["version"], "0-not-implemented")
        self.assertNotIn(rid, report["native_projection_verified"])

    def test_valid_multi_run_export_restores(self):
        shen = build(copy.deepcopy(SHEN), self.root)
        ctx = copy.deepcopy(POWER)
        ctx["run"]["id"] += ":second-capture"
        second = build(ctx, self.root)
        db = self.root / "ledger.db"
        for bundle in (self.power, shen, second):
            append(db, bundle["records"])
        data = export(db)
        restored = read_export(data)
        report = verify_records(restored)
        self.assertEqual(sorted(report["native_projection_verified"]),
                         sorted(r["id"] for r in restored if r["type"] == "AuditRun"))
        self.assertEqual(len(report["native_projection_verified"]), 3)
        self.assertEqual(report["native_projection_unverified"], [])
        other = self.root / "restored.db"
        append(other, restored)
        self.assertEqual(export(other), data)

    def test_failed_integrity_check_rolls_back_entire_append(self):
        db = self.root / "ledger.db"
        append(db, self.power["records"])
        before = export(db)
        shen = build(copy.deepcopy(SHEN), self.root)["records"]
        ctx = copy.deepcopy(POWER)
        ctx["run"]["id"] += ":tampered"
        tampered = flip_concede(copy.deepcopy(build(ctx, self.root)["records"]))
        with self.assertRaisesRegex(ContractError, "NATIVE_PROJECTION_MISMATCH"):
            append(db, [*shen, *tampered])
        self.assertEqual(export(db), before)


if __name__ == "__main__":
    unittest.main()
