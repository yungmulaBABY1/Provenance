"""Adversarial contract checks. Expectations: EXPECTED.txt, written first.

No model runs, scientific ground-truth grading, or benchmark independence is
claimed by this suite. Existing fixtures are development regressions.
"""

import contextlib
import copy
from concurrent.futures import ThreadPoolExecutor
import json
from pathlib import Path
import shutil
import sqlite3
import subprocess
import sys
import tempfile
import unittest

from atlas.adapter import build
from atlas.contract import ContractError, canonical, load_json, passage_hash, sha256, validate_context
from atlas.ledger import append, export, read_export
from atlas.native import parse

ROOT = Path(__file__).resolve().parents[2]
POWER = json.loads((ROOT / "tests/atlas/power-control.json").read_text())
SHEN = json.loads((ROOT / "tests/atlas/shen-known-bad.json").read_text())
BASELINE = json.loads((ROOT / "atlas/baseline.json").read_text())
RAW = (ROOT / POWER["output"]["path"]).read_text()


def artifact(root, path):
    return {"path": path, "sha256": sha256((root / path).read_bytes())}


def codes(result):
    return {i["code"] for i in result["issues"]}


def by_type(bundle, kind):
    return [r for r in bundle["records"] if r["type"] == kind]


class ParserTests(unittest.TestCase):
    def test_native_fields_preserved(self):
        parsed = parse(RAW)
        self.assertEqual(parsed["issues"], [])
        self.assertEqual(len(parsed["findings"]), 2)
        self.assertEqual(parsed["findings"][0]["fields"]["Verification state"],
                         "FULL-TEXT-CONFIRMED; CONTESTED")
        self.assertEqual(parsed["findings"][0]["labels"]["Concede test"], "DEFEATS")
        self.assertEqual(parsed["findings"][1]["labels"]["Concede test"], "SURVIVES")
        self.assertEqual(len(parsed["scorecard"]), 11)
        self.assertEqual(parsed["source_lock"]["SOURCE-LOCK METHOD"], "POST HOC")

    def test_missing_field_not_inferred(self):
        mutated = RAW.replace("| Concede test | DEFEATS |\n", "")
        parsed = parse(mutated)
        self.assertIn("MISSING", codes(parsed))
        self.assertNotIn("Concede test", parsed["findings"][0]["labels"])

    def test_invalid_and_cross_field_swaps(self):
        for old, new in [("| Concede test | DEFEATS |", "| Concede test | MAGIC |"),
                         ("| Concede test | DEFEATS |", "| Concede test | confirmed |"),
                         ("| Status | confirmed |", "| Status | SURVIVES |"),
                         ("| Verification state | FULL-TEXT-CONFIRMED; CONTESTED |",
                          "| Verification state | GRAPH-VERIFIED |")]:
            with self.subTest(new=new):
                self.assertIn("INVALID_LABEL", codes(parse(RAW.replace(old, new))))

    def test_valid_enum_change_has_no_semantic_oracle(self):
        parsed = parse(RAW.replace("| Concede test | DEFEATS |", "| Concede test | NARROWS |").replace(
            "N/A — classified DEFEATS for Field 6 wording", "material — only a bounded claim survives"))
        self.assertEqual(parsed["issues"], [])
        self.assertEqual(parsed["semantic_review"], "SEMANTIC_REVIEW_REQUIRED")

    def test_truncation(self):
        parsed = parse(RAW[:RAW.rfind("| Verification state")])
        self.assertIn("PARTIAL_OUTPUT", codes(parsed))
        self.assertEqual(parsed["findings"][0]["labels"]["Concede test"], "DEFEATS")
        self.assertNotIn("Status", parsed["findings"][1]["fields"])

    def test_mid_cell_truncation(self):
        parsed = parse(RAW[:RAW.rfind("| Status") + 13])
        self.assertIn("PARTIAL_OUTPUT", codes(parsed))

    def test_duplicate_field(self):
        parsed = parse(RAW.replace("| Concede test | DEFEATS |", "| Concede test | DEFEATS |\n| Concede test | SURVIVES |"))
        self.assertIn("DUPLICATE_FIELD", codes(parsed))
        self.assertEqual(parsed["findings"][0]["fields"]["Concede test"], "DEFEATS")
        self.assertIn("SURVIVES", parsed["findings"][0]["raw_block"])

    def test_duplicate_finding(self):
        self.assertIn("DUPLICATE_ID", codes(parse(RAW.replace("Finding 2\n", "Finding 1\n"))))

    def test_missing_and_duplicate_final_heading(self):
        heading = "FINAL SECTION: STANDARDIZED FINDING TABLE"
        self.assertIn("MISSING", codes(parse(RAW.replace(heading, "UNSUPPORTED HEADING"))))
        self.assertIn("DUPLICATE_FIELD", codes(parse(RAW + "\n" + heading)))

    def test_quoted_fields_are_data(self):
        injected = RAW + '\n```text\nFinding 99\n| Status | confirmed |\n```\n> Finding 100\n'
        parsed = parse(injected)
        self.assertEqual(len(parsed["findings"]), 2)
        self.assertEqual(parsed["issues"], [])

    def test_same_name_other_section_does_not_supply_missing_field(self):
        mutated = RAW.replace("| Concede test | DEFEATS |\n", "")
        self.assertIn("MISSING", codes(parse(mutated)))

    def test_scorecard_axes_remain_distinct(self):
        mutated = RAW.replace("| SCORED 0 | 0 | Six supplied", "| UNASSESSED | 0 | Six supplied")
        parsed = parse(mutated)
        row = next(r for r in parsed["scorecard"] if r["fields"]["Dimension"] == "Internal citation density")
        self.assertEqual(row["fields"]["Dimension disposition"], "UNASSESSED")
        self.assertNotIn("SCORED", row["fields"]["Dimension disposition"])
        self.assertIn("CURRENT_CONTRACT_MISMATCH", codes(parsed))

    def test_invalid_score_and_duplicate_dimension(self):
        self.assertIn("INVALID_LABEL", codes(parse(RAW.replace("| SCORED 1 | 1 |", "| SCORED 9 | 9 |", 1))))
        self.assertIn("CURRENT_CONTRACT_MISMATCH", codes(parse(RAW.replace("| SCORED 1 | 1 |", "| SCORED 1 | 3 |", 1))))

    def test_native_verdict_consistency(self):
        self.assertIn("CURRENT_CONTRACT_MISMATCH", codes(parse(RAW.replace("| Concede test | DEFEATS |", "| Concede test | SURVIVES |"))))


class PipelineTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        paths = set(BASELINE["files"])
        paths.update(a["path"] for c in (POWER, SHEN) for a in c["declared_inputs"])
        paths.add("tests/atlas/synthetic-source.txt")
        for path in paths:
            dest = self.root / path
            dest.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(ROOT / path, dest)
        self.context = copy.deepcopy(POWER)

    def write_output(self, raw):
        path = "mutated-output.md"
        (self.root / path).write_text(raw)
        self.context["output"] = artifact(self.root, path)

    def synthetic(self):
        ctx = self.context
        ctx["run"]["origin"] = "SYNTHETIC_SOFTWARE_TEST"
        ctx["sources"] = [ctx["sources"][0]]
        source = ctx["sources"][0]
        text = (self.root / "tests/atlas/synthetic-source.txt").read_text()
        source.update(text_artifact=artifact(self.root, "tests/atlas/synthetic-source.txt"),
                      version="synthetic-v1", version_confidence="EXPLICIT_FIXTURE_ASSIGNMENT",
                      version_basis="Human-inspectable synthetic fixture, not a research source",
                      warnings=[], requested_components=["metadata", "methods", "results"],
                      components=[])
        for name, label in [("metadata", "Metadata:"), ("methods", "Methods:"), ("results", "Results:")]:
            start = text.index(label)
            end = text.index("\n", start)
            source["components"].append({"id": name, "kind": "metadata" if name == "metadata" else "section", "start": start, "end": end})
        comp = source["components"][1]
        quote = text[comp["start"]:comp["end"]]
        ctx["passages"] = [{"id": "P1", "source_version_id": source["id"], "component_id": "methods",
                            "start": comp["start"], "end": comp["end"], "quote": quote,
                            "normalized_sha256": passage_hash(quote)}]
        ctx["checks"] = [{"id": "methods", "kind": "content", "scope": "Synthetic methods span only",
                          "requirements": [{"source_version_id": source["id"], "component_ids": ["methods"], "passage_ids": ["P1"]}]},
                         {"id": "metadata", "kind": "metadata", "scope": "Synthetic metadata only",
                          "requirements": [{"source_version_id": source["id"], "component_ids": ["metadata"], "passage_ids": []}]}]
        ctx["finding_checks"] = {"1": ["methods"], "2": ["methods"]}
        return ctx

    def test_existing_clean_and_metadata_boundary(self):
        bundle = build(self.context, self.root)
        self.assertEqual(bundle["syntax"], "PASS")
        findings = by_type(bundle, "AuditFinding")
        self.assertEqual(len(findings), 2)
        self.assertTrue(all(f["source_eligibility"] == "NOT_ASSESSABLE" for f in findings))
        run = by_type(bundle, "AuditRun")[0]
        self.assertFalse(run["paper_clean"])
        self.assertEqual(run["human_review"], "NOT_RECORDED")
        self.assertIn(run["source_checks"]["S1-metadata"]["eligibility"], {"ELIGIBLE", "ELIGIBLE_WITH_LIMITATIONS"})
        self.assertEqual(run["source_checks"]["bounded-citation-content"]["eligibility"], "INELIGIBLE_MISSING_EVIDENCE")
        self.assertEqual(run["historical_instrument"]["identity"], "UNKNOWN")

    def test_existing_shen_is_quarantined_not_corrected(self):
        bundle = build(copy.deepcopy(SHEN), self.root)
        self.assertEqual(bundle["checker_status"], "FAIL")
        self.assertEqual(bundle["syntax"], "FAIL")
        findings = by_type(bundle, "AuditFinding")
        self.assertEqual(len(findings), 6)
        self.assertTrue(all(f["import_status"] == "QUARANTINED" for f in findings))
        self.assertEqual(findings[0]["native"]["fields"]["Verification state"], "GRAPH-VERIFIED")
        self.assertIn("INVALID_LABEL", codes(findings[0]["native"]))
        self.assertEqual(by_type(bundle, "ReviewDecision")[0]["target_binding"], "TARGET_MISMATCH")

    def test_existing_review_fixture_stays_review(self):
        self.context["output"] = artifact(self.root, "tests/cases/citation-network-checker/locked-source-review-control.md")
        bundle = build(self.context, self.root)
        self.assertEqual(bundle["syntax"], "PASS-WITH-REVIEW")
        self.assertTrue(bundle["manifest"]["checker"]["review_items"])
        self.assertEqual(by_type(bundle, "CorpusScope")[0]["lock_verification"], "NOT_VERIFIED")

    def test_synthetic_anchor_and_scoped_eligibility(self):
        bundle = build(self.synthetic(), self.root)
        self.assertEqual(by_type(bundle, "Passage")[0]["match"], "MATCH")
        self.assertEqual(by_type(bundle, "SourceReadReceipt")[0]["state"], "READ_FOR_DECLARED_SCOPE")
        self.assertEqual(by_type(bundle, "AuditRun")[0]["source_checks"]["methods"]["eligibility"], "ELIGIBLE")
        self.assertEqual(by_type(bundle, "AuditFinding")[0]["assessment"], "UNREVIEWED")
        self.assertEqual(by_type(bundle, "Relationship")[0]["kind"], "cites_as_evidence")

    def test_corrupt_anchor_quote_range_hash(self):
        for field, value in [("quote", "fabricated quotation"), ("start", 900000),
                             ("normalized_sha256", "0" * 64), ("component_id", "wrong")]:
            with self.subTest(field=field):
                self.context = copy.deepcopy(POWER)
                ctx = self.synthetic()
                ctx["passages"][0][field] = value
                bundle = build(ctx, self.root)
                self.assertEqual(bundle["syntax"], "PASS")
                self.assertEqual(by_type(bundle, "Passage")[0]["match"], "MISMATCH")
                self.assertEqual(by_type(bundle, "AuditRun")[0]["source_checks"]["methods"]["eligibility"], "PENDING_SOURCE_VERIFICATION")

    def test_missing_methods_does_not_block_metadata(self):
        ctx = self.synthetic()
        ctx["sources"][0]["components"] = ctx["sources"][0]["components"][:1]
        bundle = build(ctx, self.root)
        checks = by_type(bundle, "AuditRun")[0]["source_checks"]
        self.assertEqual(checks["metadata"]["eligibility"], "ELIGIBLE")
        self.assertEqual(checks["methods"]["eligibility"], "INELIGIBLE_MISSING_EVIDENCE")

    def test_missing_source_never_matches(self):
        ctx = self.synthetic()
        ctx["sources"][0]["text_artifact"] = None
        ctx["sources"][0]["access_outcome"] = "RETRIEVAL_FAILED"
        bundle = build(ctx, self.root)
        self.assertEqual(by_type(bundle, "Passage")[0]["match"], "UNRESOLVABLE")
        self.assertEqual(by_type(bundle, "SourceReadReceipt")[0]["state"], "RETRIEVAL_FAILED")

    def test_unverified_extraction_is_pending(self):
        ctx = self.synthetic()
        ctx["sources"][0]["extraction"]["engine"] = "unverified-ocr"
        bundle = build(ctx, self.root)
        self.assertEqual(by_type(bundle, "SourceReadReceipt")[0]["state"], "EXTRACTION_UNVERIFIED")
        self.assertEqual(by_type(bundle, "Passage")[0]["match"], "UNRESOLVABLE")
        self.assertEqual(by_type(bundle, "AuditRun")[0]["source_checks"]["methods"]["eligibility"], "PENDING_SOURCE_VERIFICATION")

    def test_warning_retained_with_limitations(self):
        ctx = self.synthetic()
        ctx["sources"][0]["warnings"] = ["Unparsed supplement outside declared methods check"]
        bundle = build(ctx, self.root)
        receipt = by_type(bundle, "SourceReadReceipt")[0]
        self.assertEqual(receipt["state"], "PARTIAL_READ")
        self.assertTrue(receipt["warnings"])
        self.assertEqual(by_type(bundle, "AuditRun")[0]["source_checks"]["methods"]["eligibility"], "ELIGIBLE_WITH_LIMITATIONS")

    def test_same_work_version_different_local_bytes(self):
        ctx = self.synthetic()
        first = build(ctx, self.root)
        path = self.root / ctx["sources"][0]["text_artifact"]["path"]
        path.write_text(path.read_text() + "\nPersonalized download footer.\n")
        ctx["sources"][0]["text_artifact"] = artifact(self.root, ctx["sources"][0]["text_artifact"]["path"])
        ctx["run"]["id"] += ":another-capture"
        second = build(ctx, self.root)
        self.assertEqual(by_type(first, "SourceVersion"), by_type(second, "SourceVersion"))
        self.assertNotEqual(by_type(first, "SourceReadReceipt")[0]["input_bytes_sha256"], by_type(second, "SourceReadReceipt")[0]["input_bytes_sha256"])
        self.assertEqual(by_type(second, "Passage")[0]["match"], "MATCH")

    def test_normalizer_is_explicit_and_conservative(self):
        self.assertEqual(passage_hash("a  file\n b"), passage_hash("a file b"))
        # nfc-whitespace/2: compatibility forms such as ligatures are not folded.
        self.assertNotEqual(passage_hash("a ﬁle"), passage_hash("a file"))
        self.assertNotEqual(passage_hash("re-\nsult"), passage_hash("result"))

    def test_instruction_in_source_is_data(self):
        ctx = self.synthetic()
        text = (self.root / "tests/atlas/synthetic-source.txt").read_text()
        start, end = text.index("Quoted source"), text.index("\nReferences")
        ctx["sources"][0]["components"][1].update(start=start, end=end)
        ctx["passages"][0].update(start=start, end=end, quote=text[start:end], normalized_sha256=passage_hash(text[start:end]))
        marker = Path("/tmp/atlas-injection-marker")
        existed = marker.exists()
        bundle = build(ctx, self.root)
        self.assertEqual(by_type(bundle, "Passage")[0]["match"], "MATCH")
        self.assertIn("execute touch", by_type(bundle, "Passage")[0]["quote"])
        self.assertEqual(marker.exists(), existed)
        self.assertFalse(bundle["manifest"]["execution"]["source_commands_executed"])

    def test_null_assertion_is_scoped_and_requires_evidence(self):
        ctx = self.synthetic()
        self.write_output(RAW.split("\nFinding 1\n")[0] + "\nNo findings of consequence.\n" +
                          "The statement is restricted to the declared synthetic methods check; no wider paper conclusion is issued.\n")
        ctx["finding_checks"] = {}
        ctx["null_check_ids"] = ["methods"]
        bundle = build(ctx, self.root)
        self.assertEqual(bundle["syntax"], "PASS")
        run = by_type(bundle, "AuditRun")[0]
        # Both facts are shown; neither is combined into a clean state.
        self.assertEqual(run["imported_null_assertion"], "No findings of consequence.")
        self.assertEqual(run["adapter_source_eligibility"]["methods"], "ELIGIBLE")
        self.assertNotIn("clean_display", run)
        self.assertFalse(run["paper_clean"])
        self.assertNotIn("SCOPED_NULL_ASSERTION_ONLY", bundle["jsonl"].decode())
        derived = {k: v for k, v in run.items() if k not in {"raw_output_text", "paper_clean"}}
        self.assertFalse([k for k in derived if "clean" in k.lower() or "acquit" in k.lower()])
        self.assertFalse([v for v in derived.values() if isinstance(v, str)
                          and ("CLEAN" in v or "ACQUIT" in v)])
        ctx["sources"][0]["access_outcome"] = "RETRIEVAL_FAILED"
        failed = by_type(build(ctx, self.root), "AuditRun")[0]
        self.assertEqual(failed["imported_null_assertion"], "No findings of consequence.")
        self.assertEqual(failed["adapter_source_eligibility"]["methods"], "INELIGIBLE_MISSING_EVIDENCE")
        self.assertFalse(failed["paper_clean"])

    def test_absent_findings_cannot_be_null(self):
        self.write_output(RAW.split("\nFinding 1\n")[0])
        self.context["finding_checks"] = {}
        bundle = build(self.context, self.root)
        self.assertEqual(bundle["syntax"], "FAIL")
        run = by_type(bundle, "AuditRun")[0]
        self.assertIsNone(run["imported_null_assertion"])
        self.assertNotIn("clean_display", run)
        self.assertFalse(run["paper_clean"])

    def test_input_hash_and_executable_pin_fail_closed(self):
        path = self.root / self.context["output"]["path"]
        path.write_bytes(path.read_bytes() + b"mutation")
        with self.assertRaisesRegex(ContractError, "INPUT_HASH_MISMATCH"):
            build(self.context, self.root)
        self.context["output"] = artifact(self.root, self.context["output"]["path"])
        # The checker runs from the vendored baseline: a mutated working-tree
        # checker is never executed, and the drift is reported, not fatal.
        checker = self.root / "prompts/research-analysis/check-citation-network-output.py"
        checker.write_text("raise RuntimeError('must never execute mutated checker')")
        bundle = build(self.context, self.root)
        self.assertEqual(bundle["checker_status"], "PASS")
        drift = bundle["manifest"]["environment"]["validation_baseline_working_tree"]
        self.assertEqual(drift["status"], "VALIDATION_BASELINE_DIFFERS_FROM_WORKING_TREE")
        self.assertIn(checker.relative_to(self.root).as_posix(), [f["path"] for f in drift["files"]])

    def test_input_boundary_and_symlink(self):
        for path in ["../outside", "/etc/passwd"]:
            self.context["output"]["path"] = path
            with self.assertRaisesRegex(ContractError, "INPUT_BOUNDARY"):
                build(self.context, self.root)
        (self.root / "link").symlink_to("/etc/passwd")
        self.context["output"]["path"] = "link"
        with self.assertRaisesRegex(ContractError, "INPUT_BOUNDARY"):
            build(self.context, self.root)

    def test_missing_check_mapping_stays_unassessable(self):
        self.synthetic()
        self.context["finding_checks"] = {}
        bundle = build(self.context, self.root)
        self.assertTrue(all(f["source_eligibility"] == "NOT_ASSESSABLE" for f in by_type(bundle, "AuditFinding")))

    def test_wrong_source_passage_reference(self):
        self.synthetic()
        self.context["checks"][0]["requirements"][0]["passage_ids"] = ["no-such-passage"]
        with self.assertRaisesRegex(ContractError, "UNRESOLVED_REFERENCE"):
            build(self.context, self.root)

    def test_duplicate_json_and_missing_contract_fields(self):
        with self.assertRaisesRegex(ContractError, "DUPLICATE_FIELD"):
            load_json(b'{"id":"a","id":"b"}')
        del self.context["run"]["exposure"]
        with self.assertRaisesRegex(ContractError, "MISSING"):
            validate_context(self.context)

    def test_counter_audit_match_does_not_establish_independence(self):
        ctx = copy.deepcopy(SHEN)
        ctx["reviews"][0]["target_output_sha256"] = ctx["output"]["sha256"]
        bundle = build(ctx, self.root)
        review = by_type(bundle, "ReviewDecision")[0]
        self.assertEqual(review["target_binding"], "MATCH")
        self.assertEqual(review["independence"], "NOT_ESTABLISHED")
        self.assertEqual(review["human_adjudication"], "NOT_RECORDED")

    def test_deterministic_export_and_restore(self):
        first = build(self.context, self.root)
        second = build(self.context, self.root)
        self.assertEqual(first["jsonl"], second["jsonl"])
        db = self.root / "ledger.db"
        self.assertEqual(append(db, first["records"]), len(first["records"]))
        self.assertEqual(append(db, first["records"]), 0)
        self.assertEqual(export(db), first["jsonl"])
        other = self.root / "restore.db"
        append(other, read_export(export(db)))
        self.assertEqual(export(other), first["jsonl"])

    def test_conflict_rolls_back_entire_import(self):
        first = build(self.context, self.root)
        db = self.root / "ledger.db"
        append(db, first["records"])
        before = export(db)
        changed = copy.deepcopy(first["records"])
        changed.append({"schema_version": first["records"][0]["schema_version"], "id": "aaa-new", "type": "Work", "metadata": {}, "refs": []})
        next(r for r in changed if r["type"] == "AuditRun")["model"]["identity"] = "changed model claim"
        with self.assertRaisesRegex(ContractError, "ID_CONTENT_CONFLICT"):
            append(db, changed)
        self.assertEqual(export(db), before)

    def test_conflicting_run_same_output_different_context(self):
        first = build(self.context, self.root)
        db = self.root / "ledger.db"
        append(db, first["records"])
        self.context["run"]["model"]["identity"] = "different claimed model"
        second = build(self.context, self.root)
        with self.assertRaisesRegex(ContractError, "ID_CONTENT_CONFLICT"):
            append(db, second["records"])

    def test_concurrent_idempotent_imports(self):
        bundle = build(self.context, self.root)
        db = self.root / "ledger.db"
        with ThreadPoolExecutor(max_workers=2) as pool:
            futures = [pool.submit(append, db, bundle["records"]) for _ in range(2)]
            inserted = [f.result() for f in futures]
        self.assertEqual(sum(inserted), len(bundle["records"]))
        self.assertEqual(export(db), bundle["jsonl"])

    def test_sql_updates_and_deletes_blocked(self):
        bundle = build(self.context, self.root)
        db = self.root / "ledger.db"
        append(db, bundle["records"])
        # closing() closes the connection; the inner `connection` keeps its commit/rollback.
        with contextlib.closing(sqlite3.connect(db)) as connection, connection:
            for sql in ["DELETE FROM records", "UPDATE records SET sha256='0'"]:
                with self.assertRaisesRegex(sqlite3.IntegrityError, "APPEND_ONLY"):
                    connection.execute(sql)

    def test_cli_replay_and_quarantined_exit(self):
        context_path = self.root / "context.json"
        context_path.write_text(canonical(self.context))
        out = self.root / "out"
        command = [sys.executable, "-m", "atlas", "import", str(context_path), "--root", str(self.root), "--out", str(out)]
        result = subprocess.run(command, cwd=ROOT, capture_output=True, text=True)
        self.assertEqual(result.returncode, 0, result.stderr)
        replay = subprocess.run([sys.executable, "-m", "atlas", "replay", str(out / "manifest.json"), str(out / "records.jsonl"), "--root", str(self.root)], cwd=ROOT, capture_output=True, text=True)
        self.assertEqual(replay.returncode, 0, replay.stderr)
        context_path.write_text(canonical(SHEN))
        command[-1] = str(self.root / "shen-out")
        result = subprocess.run(command, cwd=ROOT, capture_output=True, text=True)
        self.assertEqual(result.returncode, 1, result.stderr)
        self.assertTrue((self.root / "shen-out/records.jsonl").exists())

    def test_receipt_and_export_tampering_rejected(self):
        bundle = build(self.context, self.root)
        records = copy.deepcopy(bundle["records"])
        next(r for r in records if r["type"] == "SourceReadReceipt")["state"] = "READ_FOR_DECLARED_SCOPE"
        data = ("\n".join(canonical(r) for r in records) + "\n").encode()
        with self.assertRaisesRegex(ContractError, "RECEIPT_HASH_MISMATCH"):
            read_export(data)
        records = copy.deepcopy(bundle["records"])
        next(r for r in records if r["type"] == "AuditFinding")["assessment"] = "fake-human-review"
        data = ("\n".join(canonical(r) for r in records) + "\n").encode()
        with self.assertRaisesRegex(ContractError, "MANIFEST_RECORD_HASH_MISMATCH"):
            read_export(data)

    def test_source_version_uncertainty_does_not_disappear(self):
        self.synthetic()
        self.context["sources"][0]["version_confidence"] = "UNKNOWN"
        bundle = build(self.context, self.root)
        self.assertEqual(by_type(bundle, "Passage")[0]["match"], "MATCH")
        self.assertEqual(by_type(bundle, "AuditRun")[0]["source_checks"]["methods"]["eligibility"], "PENDING_SOURCE_VERIFICATION")

    def test_repeated_passage_is_not_relocated(self):
        ctx = self.synthetic()
        text = (self.root / "tests/atlas/synthetic-source.txt").read_text()
        start = text.rindex("Repeated text.")
        ctx["sources"][0]["components"][1].update(start=start, end=start + len("Repeated text."))
        ctx["passages"][0].update(start=start, end=start + len("Repeated text."), quote="Repeated text.", normalized_sha256=passage_hash("Repeated text."))
        good = build(ctx, self.root)
        self.assertEqual(by_type(good, "Passage")[0]["match"], "MATCH")
        ctx["passages"][0]["start"] = text.index("Repeated text.")
        ctx["passages"][0]["end"] = ctx["passages"][0]["start"] + len("Repeated text.")
        bad = build(ctx, self.root)
        self.assertEqual(by_type(bad, "Passage")[0]["match"], "MISMATCH")

    def test_missing_scope_is_not_vacuously_eligible(self):
        self.synthetic()
        self.context["checks"][0]["requirements"] = []
        bundle = build(self.context, self.root)
        self.assertEqual(by_type(bundle, "AuditRun")[0]["source_checks"]["methods"]["eligibility"], "PENDING_SOURCE_VERIFICATION")

    def test_two_models_do_not_create_independent_review(self):
        ctx = copy.deepcopy(SHEN)
        another = copy.deepcopy(ctx["reviews"][0])
        another.update(id="second-model", reviewer="different model family")
        ctx["reviews"].append(another)
        bundle = build(ctx, self.root)
        self.assertEqual(len(by_type(bundle, "ReviewDecision")), 2)
        self.assertTrue(all(r["independence"] == "NOT_ESTABLISHED" for r in by_type(bundle, "ReviewDecision")))

    def test_invalid_list_and_calendar_date_are_contract_errors(self):
        for value in [False, [True], [{}], ["same", "same"]]:
            with self.subTest(value=value):
                ctx = copy.deepcopy(self.context)
                ctx["checks"][0]["requirements"][0]["component_ids"] = value
                with self.assertRaises(ContractError):
                    validate_context(ctx)
        self.context["run"]["imported_at"] = "2026-99-99T00:00:00Z"
        with self.assertRaisesRegex(ContractError, "INVALID_TIMESTAMP"):
            validate_context(self.context)

    def test_raw_output_bytes_survive_crlf(self):
        path = self.root / "crlf.md"
        data = RAW.replace("\n", "\r\n").encode("utf-8")
        path.write_bytes(data)
        self.context["output"] = artifact(self.root, "crlf.md")
        bundle = build(self.context, self.root)
        self.assertEqual(by_type(bundle, "AuditRun")[0]["raw_output_text"].encode("utf-8"), data)
        self.assertEqual(bundle["syntax"], "PASS")

    def test_corpus_python_files_cannot_shadow_checker_imports(self):
        for directory in [self.root, self.root / "prompts/research-analysis"]:
            (directory / "dataclasses.py").write_text("raise RuntimeError('untrusted neighboring code executed')\n")
        bundle = build(self.context, self.root)
        self.assertEqual(bundle["syntax"], "PASS")

    def test_metadata_mapping_cannot_promote_citation_finding(self):
        self.context["finding_checks"] = {"1": ["S1-metadata"], "2": ["S2-metadata"]}
        bundle = build(self.context, self.root)
        self.assertEqual(bundle["syntax"], "PASS")
        self.assertTrue(all(f["source_eligibility"] == "NOT_ASSESSABLE" for f in by_type(bundle, "AuditFinding")))

    def test_metadata_mapping_cannot_enable_null_citation_result(self):
        self.write_output(RAW.split("\nFinding 1\n")[0] + "\nNo findings of consequence.\n" +
                          "This statement is limited to supplied metadata and cannot claim source verification of the paper.\n")
        self.context["finding_checks"] = {}
        self.context["null_check_ids"] = ["S1-metadata"]
        bundle = build(self.context, self.root)
        self.assertEqual(bundle["syntax"], "PASS")
        run = by_type(bundle, "AuditRun")[0]
        self.assertEqual(run["adapter_source_eligibility"]["S1-metadata"], "ELIGIBLE_WITH_LIMITATIONS")
        self.assertEqual(run["adapter_source_eligibility"]["bounded-citation-content"], "INELIGIBLE_MISSING_EVIDENCE")
        self.assertNotIn("clean_display", run)
        self.assertFalse(run["paper_clean"])


if __name__ == "__main__":
    unittest.main()
