"""Bounded real-source packet for the power-posing pilot (compliance/PACKET.md).

Three facts stay separate throughout:
  1. what the historical audit asserted (native labels, kept as written);
  2. what the adapter can read and match now (receipts, anchors, eligibility);
  3. whether a passage substantively supports a finding (never decided here:
     UNREVIEWED / UNADJUDICATED).
A matching quotation is not scientific support and not evidence of what the
historical run read. These are offline software tests; source_packet.py
re-verifies the excerpts against the retrieved PDFs when network is available.
"""

import contextlib
import copy
import io
import json
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest

from atlas.adapter import build
from atlas.contract import ContractError, passage_hash, sha256
from atlas.integrity import verify_records
from atlas.ledger import append, export, read_export
from atlas.native import parse
from test_adapter import BASELINE, ROOT, by_type

PACKET_DIR = "tests/atlas/sources/power-posing"
CONTEXT = json.loads((ROOT / "tests/atlas/power-sources.json").read_text())
SOURCES = json.loads((ROOT / PACKET_DIR / "SOURCES.json").read_text())
sys.path.insert(0, str(ROOT / PACKET_DIR))
import source_packet  # noqa: E402

F1, F2 = "urn:atlas:import:power-posing-sources:1/finding/1", "urn:atlas:import:power-posing-sources:1/finding/2"


def checks(bundle):
    return {cid: c["eligibility"] for cid, c in by_type(bundle, "AuditRun")[0]["source_checks"].items()}


def findings(bundle):
    return {f["id"]: f for f in by_type(bundle, "AuditFinding")}


def passages(bundle):
    return {p["native_id"]: p for p in by_type(bundle, "Passage")}


def source(ctx, packet_id):
    return next(s for s in ctx["sources"] if s["work_id"] == f"doi:{SOURCES['sources'][packet_id]['doi']}")


class PowerSourcePacketTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        paths = set(BASELINE["files"]) | {CONTEXT["output"]["path"]}
        paths.update(a["path"] for a in CONTEXT["declared_inputs"])
        for path in paths:
            dest = self.root / path
            dest.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(ROOT / path, dest)
        self.ctx = copy.deepcopy(CONTEXT)
        self.bundle = build(copy.deepcopy(CONTEXT), self.root)

    def rewrite(self, path, old, new):
        """Change bytes of a declared file and redeclare its hash everywhere."""
        target = self.root / path
        data = target.read_text(encoding="utf-8")
        self.assertEqual(data.count(old), 1)
        target.write_text(data.replace(old, new), encoding="utf-8")
        digest = sha256(target.read_bytes())
        for artifact in [*self.ctx["declared_inputs"], *(s["text_artifact"] for s in self.ctx["sources"]
                                                       if s["text_artifact"])]:
            if artifact["path"] == path:
                artifact["sha256"] = digest

    def assert_no_clean_verdict(self, bundle):
        run = by_type(bundle, "AuditRun")[0]
        self.assertFalse(run["paper_clean"])
        self.assertIsNone(run["imported_null_assertion"])
        self.assertFalse([k for k in run if "clean" in k.lower() and k != "paper_clean"])
        for finding in by_type(bundle, "AuditFinding"):
            self.assertEqual(finding["assessment"], "UNREVIEWED")
        for relation in by_type(bundle, "Relationship"):
            self.assertEqual(relation["epistemic_status"], "UNADJUDICATED")

    # --- packet provenance -------------------------------------------------

    def test_excerpt_files_match_recorded_excerpts(self):
        for packet_id, record in SOURCES["sources"].items():
            with self.subTest(source=packet_id):
                if record["retrieval"]["outcome"] != "AVAILABLE":
                    self.assertEqual(record["excerpts"], [])
                    self.assertFalse((ROOT / PACKET_DIR / f"{packet_id}-excerpts.txt").exists())
                    continue
                expected, components = source_packet.excerpt_file(packet_id, record)
                committed = (ROOT / PACKET_DIR / f"{packet_id}-excerpts.txt").read_text(encoding="utf-8")
                self.assertEqual(committed, expected)
                self.assertEqual(source(CONTEXT, packet_id)["components"], components)
                for excerpt in record["excerpts"]:
                    self.assertEqual(sha256(excerpt["text"].encode("utf-8")), excerpt["sha256"])
                    self.assertEqual(excerpt["occurrences_in_extraction"], 1)
                    self.assertEqual(excerpt["extraction_end"] - excerpt["extraction_start"], len(excerpt["text"]))

    def test_context_passages_are_recorded_excerpts(self):
        recorded = {e["id"]: e["text"] for r in SOURCES["sources"].values() for e in r["excerpts"]}
        self.assertEqual({p["id"]: p["quote"] for p in CONTEXT["passages"]}, recorded)
        for passage in CONTEXT["passages"]:
            self.assertEqual(passage["normalized_sha256"], passage_hash(passage["quote"]))

    def test_originals_preserved(self):
        # Pinned hashes, not git history: CI's shallow checkout lacks the base commit.
        originals = json.loads((ROOT / PACKET_DIR / "ORIGINALS.json").read_text())
        self.assertEqual(originals["files"]["compliance/PACKET.md"]["sha256"],
                         BASELINE["files"]["compliance/PACKET.md"]["sha256"])
        self.assertIn(CONTEXT["output"]["path"], originals["files"])
        changed = []
        for path, pin in sorted(originals["files"].items()):
            target = ROOT / path
            if not target.is_file() or sha256(target.read_bytes()) != pin["sha256"]:
                changed.append(path)
        self.assertEqual(changed, [], "original packet or archived outputs changed")

    def test_unretrieved_sources_recorded_as_limitations(self):
        for packet_id in ("S1", "S3"):
            with self.subTest(source=packet_id):
                record = SOURCES["sources"][packet_id]
                self.assertEqual(record["retrieval"]["outcome"], "RETRIEVAL_FAILED")
                self.assertEqual(record["retrieval"]["http_status"], 403)
                ctx_source = source(CONTEXT, packet_id)
                self.assertIsNone(ctx_source["text_artifact"])
                self.assertEqual(ctx_source["access_outcome"], "RETRIEVAL_FAILED")

    # --- the three facts on the real packet --------------------------------

    def test_historical_assertions_kept_as_written(self):
        raw = (ROOT / CONTEXT["output"]["path"]).read_text(encoding="utf-8")
        native = parse(raw)["findings"]
        stored = findings(self.bundle)
        self.assertEqual(stored[F1]["native"], native[0])
        self.assertEqual(stored[F2]["native"], native[1])
        self.assertEqual(stored[F1]["native"]["fields"]["Verification state"], "FULL-TEXT-CONFIRMED; CONTESTED")
        self.assertEqual(stored[F2]["native"]["fields"]["Verification state"],
                         "FULL-TEXT-CONFIRMED; CROSS-SOURCE-CONFIRMED")
        # The archived pilot predates the current grammar: quarantined, not corrected.
        self.assertTrue(all(f["import_status"] == "QUARANTINED" for f in stored.values()))

    def test_adapter_reads_and_matches_now(self):
        self.assertTrue(all(p["match"] == "MATCH" and p["exact_match"] for p in passages(self.bundle).values()))
        self.assertEqual(len(passages(self.bundle)), 7)
        states = {r["source_version_id"].split("/version/")[0]: r["state"]
                  for r in by_type(self.bundle, "SourceReadReceipt")}
        self.assertEqual(states, {"doi:10.1177/0956797610383437": "RETRIEVAL_FAILED",
                                  "doi:10.1177/0956797614553946": "PARTIAL_READ",
                                  "doi:10.1177/0956797614566855": "RETRIEVAL_FAILED",
                                  "doi:10.1177/0956797616658563": "PARTIAL_READ"})
        self.assertEqual(checks(self.bundle), {
            "S2-reported-outcomes": "ELIGIBLE_WITH_LIMITATIONS",
            "S4-evidential-value": "ELIGIBLE_WITH_LIMITATIONS",
            "S2-S4-venue": "ELIGIBLE_WITH_LIMITATIONS",
            "S3-engages-S2": "INELIGIBLE_MISSING_EVIDENCE",
            "S4-describes-S3": "ELIGIBLE_WITH_LIMITATIONS",
            "S1-founding-results": "INELIGIBLE_MISSING_EVIDENCE",
            "S2-methods": "INELIGIBLE_MISSING_EVIDENCE"})
        stored = findings(self.bundle)
        self.assertEqual(stored[F1]["source_eligibility"], "ELIGIBLE_FOR_DECLARED_CHECKS")
        self.assertEqual(stored[F1]["evidence_passage_ids"],
                         [f"urn:atlas:import:power-posing-sources:1/passage/{p}"
                          for p in ("S2-E2", "S2-E3", "S4-E3", "S4-E4")])
        # Finding 2 needs S3's own text, which was not retrieved; S4's description
        # of S3 does not stand in for it.
        self.assertEqual(stored[F2]["source_eligibility"], "NOT_ASSESSABLE")

    def test_substantive_support_is_not_decided(self):
        self.assert_no_clean_verdict(self.bundle)
        self.assertEqual(by_type(self.bundle, "ReviewDecision"), [])
        self.assertEqual(len(by_type(self.bundle, "Relationship")), 7)
        for relation in by_type(self.bundle, "Relationship"):
            self.assertEqual(relation["relation_basis"], "DOCUMENTED_IMPORT_MAPPING")
        receipt = next(r for r in by_type(self.bundle, "SourceReadReceipt") if r["state"] == "PARTIAL_READ")
        self.assertIn("historical runner reading is not established", receipt["consumption_scope"])

    # --- deterministic controls --------------------------------------------

    def test_control_missing_methods_blocks_only_dependent_check(self):
        result = checks(self.bundle)
        self.assertEqual(result["S2-methods"], "INELIGIBLE_MISSING_EVIDENCE")
        self.assertEqual(result["S2-reported-outcomes"], "ELIGIBLE_WITH_LIMITATIONS")
        self.ctx["finding_checks"]["1"].append("S2-methods")
        bundle = build(self.ctx, self.root)
        self.assertEqual(findings(bundle)[F1]["source_eligibility"], "NOT_ASSESSABLE")
        self.assertEqual(checks(bundle)["S4-evidential-value"], "ELIGIBLE_WITH_LIMITATIONS")
        self.assert_no_clean_verdict(bundle)

    def test_control_failed_extraction(self):
        source(self.ctx, "S4")["extraction"] = {"engine": "pdftotext", "version": "24.02.0",
                                                "configuration": {"enc": "UTF-8"}}
        bundle = build(self.ctx, self.root)
        receipt = next(r for r in by_type(bundle, "SourceReadReceipt") if "0956797616658563" in r["source_version_id"])
        self.assertEqual(receipt["state"], "EXTRACTION_UNVERIFIED")
        self.assertTrue(all(p["match"] == "UNRESOLVABLE" for k, p in passages(bundle).items() if k.startswith("S4")))
        result = checks(bundle)
        self.assertEqual(result["S4-evidential-value"], "PENDING_SOURCE_VERIFICATION")
        self.assertEqual(result["S4-describes-S3"], "PENDING_SOURCE_VERIFICATION")
        self.assertEqual(result["S2-reported-outcomes"], "ELIGIBLE_WITH_LIMITATIONS")
        self.assertEqual(findings(bundle)[F1]["source_eligibility"], "NOT_ASSESSABLE")
        self.assert_no_clean_verdict(bundle)

    def test_control_changed_source_bytes_undeclared_fail_closed(self):
        path = self.root / PACKET_DIR / "S2-excerpts.txt"
        path.write_bytes(path.read_bytes().replace(b"we found no", b"we found a", 1))
        with self.assertRaisesRegex(ContractError, f"INPUT_HASH_MISMATCH: {PACKET_DIR}/S2-excerpts.txt"):
            build(self.ctx, self.root)

    def test_control_changed_source_bytes_redeclared(self):
        # Same-length edit: only the edited passage stops matching.
        self.rewrite(f"{PACKET_DIR}/S2-excerpts.txt", "However, we found no", "However, we found an")
        bundle = build(self.ctx, self.root)
        found = passages(bundle)
        self.assertEqual(found["S2-E2"]["match"], "MISMATCH")
        self.assertEqual(found["S2-E3"]["match"], "MATCH")
        result = checks(bundle)
        self.assertEqual(result["S2-reported-outcomes"], "PENDING_SOURCE_VERIFICATION")
        self.assertEqual(result["S4-evidential-value"], "ELIGIBLE_WITH_LIMITATIONS")
        self.assertEqual(result["S2-S4-venue"], "ELIGIBLE_WITH_LIMITATIONS")
        self.assertEqual(findings(bundle)[F1]["source_eligibility"], "NOT_ASSESSABLE")
        self.assert_no_clean_verdict(bundle)

    def test_control_length_change_shifts_later_offsets_in_that_file_only(self):
        self.rewrite(f"{PACKET_DIR}/S2-excerpts.txt", "However, we found no", "However, we found a")
        found = passages(build(self.ctx, self.root))
        # Offsets are bound to exact bytes: every later S2 span moves; nothing is relocated.
        self.assertEqual({k: p["match"] for k, p in found.items() if k.startswith("S2")},
                         {"S2-E1": "MATCH", "S2-E2": "MISMATCH", "S2-E3": "MISMATCH"})
        self.assertTrue(all(p["match"] == "MATCH" for k, p in found.items() if k.startswith("S4")))

    def test_control_incorrect_quotation(self):
        passage = next(p for p in self.ctx["passages"] if p["id"] == "S4-E4")
        passage["quote"] = passage["quote"].replace("pfull=.63", "pfull=.03")
        passage["normalized_sha256"] = passage_hash(passage["quote"])
        bundle = build(self.ctx, self.root)
        self.assertEqual(passages(bundle)["S4-E4"]["match"], "MISMATCH")
        result = checks(bundle)
        self.assertEqual(result["S4-evidential-value"], "PENDING_SOURCE_VERIFICATION")
        self.assertEqual(result["S2-reported-outcomes"], "ELIGIBLE_WITH_LIMITATIONS")
        self.assertEqual(result["S4-describes-S3"], "ELIGIBLE_WITH_LIMITATIONS")
        self.assert_no_clean_verdict(bundle)

    def test_control_reflowed_quotation_is_never_match(self):
        passage = next(p for p in self.ctx["passages"] if p["id"] == "S2-E2")
        passage["quote"] = " ".join(passage["quote"].split())
        passage["normalized_sha256"] = passage_hash(passage["quote"])
        bundle = build(self.ctx, self.root)
        self.assertEqual(passages(bundle)["S2-E2"]["match"], "NORMALIZED_MATCH_ONLY")
        check = by_type(bundle, "AuditRun")[0]["source_checks"]["S2-reported-outcomes"]
        self.assertEqual(check["eligibility"], "ELIGIBLE_WITH_LIMITATIONS")
        self.assertIn("NORMALIZED_MATCH_ONLY:S2-E2", check["limitations"])

    def test_control_unavailable_source(self):
        s2 = source(self.ctx, "S2")
        s2.update(access_outcome="RETRIEVAL_FAILED", text_artifact=None)
        bundle = build(self.ctx, self.root)
        self.assertTrue(all(p["match"] == "UNRESOLVABLE" for k, p in passages(bundle).items() if k.startswith("S2")))
        result = checks(bundle)
        self.assertEqual(result["S2-reported-outcomes"], "INELIGIBLE_MISSING_EVIDENCE")
        self.assertEqual(result["S2-S4-venue"], "INELIGIBLE_MISSING_EVIDENCE")
        self.assertEqual(result["S4-evidential-value"], "ELIGIBLE_WITH_LIMITATIONS")
        self.assertEqual(result["S4-describes-S3"], "ELIGIBLE_WITH_LIMITATIONS")
        self.assertEqual(findings(bundle)[F1]["source_eligibility"], "NOT_ASSESSABLE")
        self.assert_no_clean_verdict(bundle)

    def test_all_sources_missing_never_clean(self):
        for packet_id in ("S2", "S4"):
            source(self.ctx, packet_id).update(access_outcome="RETRIEVAL_FAILED", text_artifact=None)
        bundle = build(self.ctx, self.root)
        self.assertTrue(all(f["source_eligibility"] == "NOT_ASSESSABLE" for f in findings(bundle).values()))
        self.assertNotIn("ELIGIBLE", {e for e in checks(bundle).values()})
        self.assert_no_clean_verdict(bundle)

    # --- import, export, restore, content replay ---------------------------

    def test_shares_work_identities_with_existing_power_import(self):
        power = json.loads((ROOT / "tests/atlas/power-control.json").read_text())
        self.assertEqual(CONTEXT["works"], power["works"])
        for artifact in power["declared_inputs"]:
            shutil.copyfile(ROOT / artifact["path"], self.root / artifact["path"])
        ledger = self.root / "ledger.sqlite"
        append(ledger, build(power, self.root)["records"])
        append(ledger, self.bundle["records"])
        report = verify_records(read_export(export(ledger)))
        self.assertEqual(report["native_projection_verified"],
                         ["urn:atlas:import:power-control:1", "urn:atlas:import:power-posing-sources:1"])

    def test_import_export_restore_and_content_replay(self):
        context = self.root / "power-sources.json"
        context.write_text(json.dumps(CONTEXT))
        out, ledger = self.root / "out", self.root / "ledger.sqlite"

        def cli(*args):
            return subprocess.run([sys.executable, "-m", "atlas", *args], cwd=ROOT, capture_output=True, text=True)

        imported = cli("import", str(context), "--root", str(self.root), "--out", str(out), "--ledger", str(ledger))
        self.assertEqual(imported.returncode, 1, imported.stderr)  # quarantined archived output
        self.assertEqual(json.loads(imported.stdout)["notices"], [])
        self.assertEqual(cli("export", str(ledger), str(self.root / "all.jsonl")).returncode, 0)
        restored = cli("restore", str(self.root / "all.jsonl"), str(self.root / "restored.sqlite"))
        self.assertEqual(restored.returncode, 0, restored.stderr)
        self.assertEqual(json.loads(restored.stdout)["native_projection_verified"],
                         ["urn:atlas:import:power-posing-sources:1"])
        self.assertEqual(cli("export", str(self.root / "restored.sqlite"), str(self.root / "again.jsonl")).returncode, 0)
        self.assertEqual((self.root / "all.jsonl").read_bytes(), (self.root / "again.jsonl").read_bytes())
        for level in ("content", "strict"):
            replay = cli("replay", str(out / "manifest.json"), str(out / "records.jsonl"),
                         "--root", str(self.root), "--level", level)
            self.assertEqual(replay.returncode, 0, replay.stderr)
        self.assertEqual(len(read_export((out / "records.jsonl").read_bytes())), len(self.bundle["records"]))


class SourceVerifierTests(unittest.TestCase):
    """source_packet.verify, offline: fake fetcher and extractor, synthetic record."""

    PDF = b"%PDF-1.4 synthetic test bytes"
    TEXT = "Running head\n\nalpha excerpt that is quoted\n\nunquoted tail paragraph\n"

    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.dir = Path(self.temp.name)
        quote = "alpha excerpt that is quoted"
        start = self.TEXT.index(quote)
        record = {
            "doi": "10.0000/synthetic", "citation": "Synthetic verifier fixture", "excerpts": [{
                "id": "X-E1", "kind": "section", "label": "synthetic", "pdf_page": 1,
                "extraction_start": start, "extraction_end": start + len(quote),
                "occurrences_in_extraction": 1, "sha256": sha256(quote.encode("utf-8")), "text": quote}],
            "retrieval": {"requested_url": "https://example.invalid/x.pdf", "final_url": "https://example.invalid/x.pdf",
                          "retrieved_at": "2026-10-30T00:00:00Z", "http_status": 200, "outcome": "AVAILABLE",
                          "sha256": sha256(self.PDF)},
            "extraction": {"output_sha256": sha256(self.TEXT.encode("utf-8"))}}
        missing = {"doi": "10.0000/missing", "excerpts": [], "retrieval": {
            "requested_url": "https://example.invalid/y", "outcome": "RETRIEVAL_FAILED", "http_status": 403}}
        (self.dir / "SOURCES.json").write_text(json.dumps({"sources": {"X": record, "Y": missing}}))
        (self.dir / "X-excerpts.txt").write_text(source_packet.excerpt_file("X", record)[0], encoding="utf-8")

    def run_verify(self, text):
        def fetcher(url):
            if url.endswith("x.pdf"):
                return {"status": 200, "final_url": url, "content_type": "application/pdf", "data": self.PDF}
            return {"status": 403, "final_url": url, "content_type": "text/html", "data": None}
        out = io.StringIO()
        with contextlib.redirect_stdout(out):
            code = source_packet.verify(sources=self.dir / "SOURCES.json", directory=self.dir,
                                        fetcher=fetcher, extractor=lambda pdf: text,
                                        reviews=self.dir / "reviews")
        return code, out.getvalue()

    def test_identical_extraction_passes(self):
        code, out = self.run_verify(self.TEXT)
        self.assertEqual(code, 0, out)
        self.assertIn("extraction output identical", out)

    def test_extraction_differs_outside_excerpts_fails(self):
        changed = self.TEXT.replace("unquoted tail", "unquoted TAIL")
        code, out = self.run_verify(changed)
        self.assertEqual(code, 1, out)
        self.assertIn("extraction output FAIL differs", out)
        self.assertIn("X-E1: OK at recorded offsets", out)  # the excerpt alone would still pass

    def test_extraction_differs_inside_excerpt_fails(self):
        code, out = self.run_verify(self.TEXT.replace("alpha", "ALPHA"))
        self.assertEqual(code, 1, out)
        self.assertIn("X-E1: FAIL at recorded offsets", out)

    def write_review(self, quote, start):
        (self.dir / "reviews").mkdir(exist_ok=True)
        (self.dir / "reviews" / "r.json").write_text(json.dumps({
            "target": {"source_version_id": "doi:10.0000/synthetic/version/x"},
            "locators": [{"id": "L1", "extraction_start": start, "extraction_end": start + len(quote),
                          "quote": quote, "quote_sha256": sha256(quote.encode("utf-8"))}]}))

    def test_review_locators_checked(self):
        self.write_review("unquoted tail", self.TEXT.index("unquoted tail"))
        code, out = self.run_verify(self.TEXT)
        self.assertEqual(code, 0, out)
        self.assertIn("r.json: 1/1 locators OK", out)

    def test_review_locator_at_wrong_offset_fails(self):
        self.write_review("unquoted tail", self.TEXT.index("unquoted tail") + 1)
        code, out = self.run_verify(self.TEXT)
        self.assertEqual(code, 1, out)
        self.assertIn("FAIL L1", out)

    def test_changed_source_bytes_fail(self):
        self.PDF = b"%PDF-1.4 different bytes"
        code, out = self.run_verify(self.TEXT)
        self.assertEqual(code, 1, out)
        self.assertIn("FAIL source bytes differ", out)


if __name__ == "__main__":
    unittest.main()
