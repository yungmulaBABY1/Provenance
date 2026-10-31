"""Evidence-proposition reviews (atlas-evidence-review/2) of Finding 1's S2 clause.

A review binds to one exact proposition, finding, mapping, passage descriptors
(source version, component, offsets, unit, interval, quotation hash), source
version and input bytes. Any change unbinds it (TARGET_MISMATCH, named), so a
changed mapping never inherits an old review. A review of one clause never
approves the finding, never adjudicates, and leaves native labels as written.
"""

import contextlib
import copy
import json
from pathlib import Path
import shutil
import sqlite3
import subprocess
import sys
import tempfile
import unittest

from atlas.adapter import build
from atlas.contract import ContractError, canonical, digest, jsonl, passage_hash, sha256
from atlas.integrity import verify_records
from atlas.ledger import append, export, read_export
from atlas.reviews import load_review, passage_descriptor
from test_adapter import BASELINE, ROOT, by_type
from test_integrity import rehash

REVIEWED = json.loads((ROOT / "tests/atlas/power-sources-reviewed.json").read_text())
ORIGINAL = json.loads((ROOT / "tests/atlas/power-sources.json").read_text())
RUN = REVIEWED["run"]["id"]
REVIEW_A, REVIEW_B = f"{RUN}/review/F1-S2-review-A", f"{RUN}/review/F1-S2-review-B"
F1 = f"{RUN}/finding/1"


def reviews(bundle):
    return {r["id"]: r for r in by_type(bundle, "ReviewDecision")}


def run_record(bundle):
    return by_type(bundle, "AuditRun")[0]


class EvidenceReviewTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        paths = set(BASELINE["files"]) | {REVIEWED["output"]["path"]}
        paths.update(a["path"] for a in REVIEWED["declared_inputs"])
        paths.update(r["artifact"]["path"] for r in REVIEWED["reviews"])
        for path in paths:
            dest = self.root / path
            dest.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(ROOT / path, dest)
        self.ctx = copy.deepcopy(REVIEWED)
        self.bundle = build(copy.deepcopy(REVIEWED), self.root)

    def edit_review(self, review_id, change):
        """Rewrite a review artifact in the temp tree and redeclare its hash."""
        entry = next(r for r in self.ctx["reviews"] if r["id"] == review_id)
        path = self.root / entry["artifact"]["path"]
        # Always start from the committed artifact, so edits never accumulate.
        review = json.loads((ROOT / entry["artifact"]["path"]).read_text(encoding="utf-8"))
        change(review)
        path.write_text(json.dumps(review, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
        entry["artifact"]["sha256"] = sha256(path.read_bytes())

    def assert_unbound(self, bundle, review_id, component):
        review = reviews(bundle)[review_id]
        self.assertEqual(review["target_binding"], "TARGET_MISMATCH")
        self.assertIn(component, review["target_mismatches"])
        self.assertEqual(review["refs"], [])
        self.assertNotIn(review_id, run_record(bundle)["refs"])
        self.assertIn(review_id, run_record(bundle)["mismatched_review_ids"])

    # --- exact binding ------------------------------------------------------

    def test_both_reviews_bind_to_the_exact_target(self):
        found = reviews(self.bundle)
        for review_id in (REVIEW_A, REVIEW_B):
            with self.subTest(review=review_id):
                review = found[review_id]
                self.assertEqual(review["target_binding"], "MATCH")
                self.assertEqual(review["target_mismatches"], [])
                self.assertEqual(review["review_schema"], "atlas-evidence-review/2")
                self.assertEqual(review["refs"], [
                    RUN, F1, f"{RUN}/passage/S2-E2", f"{RUN}/passage/S2-E3",
                    f"{F1}/evidence/S2-E2", f"{F1}/evidence/S2-E3"])
                self.assertIn(review_id, run_record(self.bundle)["refs"])
                self.assertEqual(review["independence"], "NOT_ESTABLISHED")
                self.assertEqual(review["human_adjudication"], "NOT_RECORDED")
                self.assertEqual(review["finding_level_effect"], "NONE")

    def test_target_is_the_original_finding_and_mapping(self):
        """The bound identities are those of the unreviewed import (run :1)."""
        original = read_export((ROOT / "tests/atlas/receipts/power-sources/records.jsonl").read_bytes())
        finding = next(r for r in original if r["type"] == "AuditFinding" and r["native"]["number"] == 1)
        check = next(c for c in ORIGINAL["checks"] if c["id"] == "S2-reported-outcomes")
        target = reviews(self.bundle)[REVIEW_A]["declared_target"]
        self.assertEqual(target["finding_native_sha256"], digest(finding["native"]))
        self.assertEqual(finding["native"]["fields"]["Evidence"][target["proposition_start"]:target["proposition_end"]],
                         target["proposition"])
        self.assertEqual(target["check_sha256"], digest(check))
        self.assertEqual(target["output_sha256"], ORIGINAL["output"]["sha256"])
        passages = {p["native_id"]: p for p in original if p["type"] == "Passage"}
        self.assertEqual(target["passages"], {pid: passage_descriptor(passages[pid]) for pid in ("S2-E2", "S2-E3")})
        context_passages = {p["id"]: p for p in ORIGINAL["passages"]}
        for pid, descriptor in target["passages"].items():
            self.assertEqual((descriptor["start"], descriptor["end"], descriptor["component_id"]),
                             (context_passages[pid]["start"], context_passages[pid]["end"],
                              context_passages[pid]["component_id"]))
        source = next(s for s in ORIGINAL["sources"] if s["id"] == target["source_version_id"])
        self.assertEqual(target["source_input_sha256"], source["text_artifact"]["sha256"])
        # Apart from run identity and the reviews, the reviewed import is the original one.
        strip = lambda c: {k: v for k, v in c.items() if k not in {"run", "reviews", "declared_inputs"}}
        self.assertEqual(strip(REVIEWED), strip(ORIGINAL))

    def test_disagreement_preserved(self):
        found = reviews(self.bundle)
        self.assertEqual(found[REVIEW_A]["imported_disposition"], "SUPPORTS_WITH_QUALIFICATION")
        self.assertEqual(found[REVIEW_B]["imported_disposition"], "SUPPORTS")
        parts = {rid: {p["part"]: p["disposition"] for p in found[rid]["review"]["part_dispositions"]}
                 for rid in (REVIEW_A, REVIEW_B)}
        self.assertEqual(parts[REVIEW_A], {"a": "SUPPORTS", "b": "SUPPORTS_WITH_QUALIFICATION",
                                           "c": "SUPPORTS_WITH_QUALIFICATION"})
        self.assertEqual(parts[REVIEW_B], {"a": "SUPPORTS", "b": "SUPPORTS", "c": "SUPPORTS"})

    # --- partial coverage: a reviewed clause approves nothing else ----------

    def test_partial_coverage_does_not_approve_the_finding(self):
        finding = next(f for f in by_type(self.bundle, "AuditFinding") if f["id"] == F1)
        self.assertEqual(finding["assessment"], "UNREVIEWED")
        self.assertEqual(finding["native"]["fields"]["Verification state"], "FULL-TEXT-CONFIRMED; CONTESTED")
        self.assertTrue(all(r["epistemic_status"] == "UNADJUDICATED" for r in by_type(self.bundle, "Relationship")))
        self.assertFalse(run_record(self.bundle)["paper_clean"])
        referenced = {ref for r in reviews(self.bundle).values() for ref in r["refs"]}
        for unreviewed in (f"{F1}/evidence/S4-E3", f"{F1}/evidence/S4-E4", f"{RUN}/finding/2",
                           f"{RUN}/passage/S4-E3", f"{RUN}/passage/S4-E4"):
            self.assertNotIn(unreviewed, referenced)
        coverage = reviews(self.bundle)[REVIEW_A]["review"]["coverage"]
        self.assertEqual(coverage["finding_level_effect"], "NONE")
        self.assertTrue(any("S4" in item for item in coverage["not_reviewed"]))

    def test_native_projection_identical_to_unreviewed_import(self):
        original = build(copy.deepcopy(ORIGINAL), self.root)
        natives = lambda b: [f["native"] for f in by_type(b, "AuditFinding")]
        self.assertEqual(natives(self.bundle), natives(original))

    # --- changed targets never inherit the review --------------------------

    def test_changed_mapping_unbinds(self):
        def add_passage(ctx):
            check = next(c for c in ctx["checks"] if c["id"] == "S2-reported-outcomes")
            check["requirements"][0]["component_ids"].append("S2-E1")
            check["requirements"][0]["passage_ids"].append("S2-E1")

        def rescope(ctx):
            next(c for c in ctx["checks"] if c["id"] == "S2-reported-outcomes")["scope"] += " (edited)"

        def unmap(ctx):
            ctx["finding_checks"]["1"].remove("S2-reported-outcomes")

        for change in (add_passage, rescope, unmap):
            with self.subTest(change=change.__name__):
                ctx = copy.deepcopy(self.ctx)
                change(ctx)
                bundle = build(ctx, self.root)
                for review_id in (REVIEW_A, REVIEW_B):
                    self.assert_unbound(bundle, review_id, "mapping")

    def test_changed_passage_quote_unbinds(self):
        passage = next(p for p in self.ctx["passages"] if p["id"] == "S2-E3")
        passage["quote"] = passage["quote"].replace("failed to confirm", "failed to confirm any")
        passage["normalized_sha256"] = passage_hash(passage["quote"])
        self.assert_unbound(build(self.ctx, self.root), REVIEW_A, "passages")

    def shift(self, ctx, pid, by=1):
        passage = next(p for p in ctx["passages"] if p["id"] == pid)
        passage.update(start=passage["start"] + by, end=passage["end"] + by)
        return ctx

    def test_moved_locator_with_same_quotation_unbinds(self):
        """Reported gap: S2-E2's offsets moved by one, everything else unchanged."""
        for by in (1, -1):
            with self.subTest(by=by):
                bundle = build(self.shift(copy.deepcopy(self.ctx), "S2-E2", by), self.root)
                passage = next(p for p in by_type(bundle, "Passage") if p["native_id"] == "S2-E2")
                self.assertEqual(passage["match"], "MISMATCH")
                self.assertEqual(passage["quote"], next(p["quote"] for p in REVIEWED["passages"] if p["id"] == "S2-E2"))
                for review_id in (REVIEW_A, REVIEW_B):
                    self.assert_unbound(bundle, review_id, "passages")
                self.assertEqual(reviews(bundle)[REVIEW_A]["target_mismatches"], ["passages"])

    def test_every_descriptor_field_is_bound(self):
        for field, value in [("source_version_id", "doi:10.0/other/version/x"), ("component_id", "S2-E3"),
                             ("start", 905), ("end", 1161), ("unit", "utf8_byte"), ("interval", "closed"),
                             ("quote_sha256", "0" * 64)]:
            with self.subTest(field=field):
                self.ctx = copy.deepcopy(REVIEWED)
                self.edit_review("F1-S2-review-A", lambda r: r["target"]["passages"]["S2-E2"].update({field: value}))
                bundle = build(self.ctx, self.root)
                self.assert_unbound(bundle, REVIEW_A, "passages")
                self.assertEqual(reviews(bundle)[REVIEW_B]["target_binding"], "MATCH")

    def test_moved_locator_stays_detached_after_export_and_restore(self):
        bundle = build(self.shift(self.ctx, "S2-E2"), self.root)
        db, restored_db = self.root / "ledger.sqlite", self.root / "restored.sqlite"
        append(db, bundle["records"])
        restored = read_export(export(db))
        append(restored_db, restored)
        again = read_export(export(restored_db))
        self.assertEqual(verify_records(again)["native_projection_verified"], [RUN])
        found = {r["id"]: r for r in again if r["type"] == "ReviewDecision"}
        run = next(r for r in again if r["type"] == "AuditRun")
        for review_id in (REVIEW_A, REVIEW_B):
            self.assertEqual(found[review_id]["target_binding"], "TARGET_MISMATCH")
            self.assertEqual(found[review_id]["target_mismatches"], ["passages"])
            self.assertNotIn(review_id, run["refs"])
            self.assertIn(review_id, run["mismatched_review_ids"])

    def test_restore_rejects_moved_locator_with_kept_binding(self):
        """A bundle edited to move a passage but keep the review attached is rejected."""
        records = copy.deepcopy(self.bundle["records"])
        passage = next(r for r in records if r["type"] == "Passage" and r["native_id"] == "S2-E2")
        passage["locator"].update(start=passage["locator"]["start"] + 1, end=passage["locator"]["end"] + 1)
        rehash(records, RUN)
        with self.assertRaisesRegex(ContractError, "REVIEW_BINDING_MISMATCH"):
            read_export(jsonl(records))

    def test_v1_reviews_preserved_and_rejected(self):
        for name in ("F1-S2-review-A", "F1-S2-review-B"):
            v1 = (ROOT / f"tests/atlas/reviews/power-posing/v1/{name}.json").read_bytes()
            current = json.loads((ROOT / f"tests/atlas/reviews/power-posing/{name}.json").read_text())
            self.assertEqual(current["reissue"]["supersedes"]["sha256"], sha256(v1))
            with self.assertRaisesRegex(ContractError, "UNSUPPORTED_REVIEW_SCHEMA: atlas-evidence-review/1"):
                load_review(v1)
        self.ctx["reviews"][0]["review_schema"] = "atlas-evidence-review/1"
        with self.assertRaisesRegex(ContractError, "UNSUPPORTED_REVIEW_SCHEMA: atlas-evidence-review/1"):
            build(self.ctx, self.root)
        historical = ROOT / "tests/atlas/receipts/historical-4718225/power-sources-reviewed/records.jsonl"
        with self.assertRaisesRegex(ContractError, "UNSUPPORTED_REVIEW_SCHEMA: atlas-evidence-review/1"):
            read_export(historical.read_bytes())

    def test_reissue_changed_only_the_binding(self):
        for name in ("F1-S2-review-A", "F1-S2-review-B"):
            v1 = json.loads((ROOT / f"tests/atlas/reviews/power-posing/v1/{name}.json").read_text())
            v2 = json.loads((ROOT / f"tests/atlas/reviews/power-posing/{name}.json").read_text())
            self.assertEqual(sorted(k for k in set(v1) | set(v2) if v1.get(k) != v2.get(k)),
                             ["reissue", "schema", "target"])
            self.assertEqual([k for k in v1["target"] if v1["target"][k] != v2["target"][k]], ["passages"])
            self.assertEqual({pid: d["quote_sha256"] for pid, d in v2["target"]["passages"].items()},
                             v1["target"]["passages"])

    def test_changed_source_bytes_unbind(self):
        path = "tests/atlas/sources/power-posing/S2-excerpts.txt"
        target = self.root / path
        target.write_text(target.read_text(encoding="utf-8").replace("we found no", "we found an", 1), encoding="utf-8")
        digest_now = sha256(target.read_bytes())
        for artifact in [*self.ctx["declared_inputs"], *(s["text_artifact"] for s in self.ctx["sources"] if s["text_artifact"])]:
            if artifact["path"] == path:
                artifact["sha256"] = digest_now
        self.assert_unbound(build(self.ctx, self.root), REVIEW_A, "source_input")

    def test_changed_output_unbinds(self):
        self.ctx["output"] = {"path": "tests/cases/citation-network-checker/complete-clean-control.md",
                              "sha256": BASELINE["files"]["tests/cases/citation-network-checker/complete-clean-control.md"]["sha256"]}
        bundle = build(self.ctx, self.root)
        self.assert_unbound(bundle, REVIEW_A, "output")
        self.assertIn("finding", reviews(bundle)[REVIEW_A]["target_mismatches"])

    def test_changed_proposition_span_unbinds(self):
        self.edit_review("F1-S2-review-A", lambda r: r["target"].update(proposition_end=79))
        bundle = build(self.ctx, self.root)
        self.assert_unbound(bundle, REVIEW_A, "proposition")
        self.assertEqual(reviews(bundle)[REVIEW_B]["target_binding"], "MATCH")

    # --- incorrect or missing references ------------------------------------

    def test_incorrect_references_unbind_without_crashing(self):
        for field, value, component in [("finding_number", "9", "finding"),
                                         ("check_id", "no-such-check", "mapping"),
                                         ("source_version_id", "doi:10.0/none/version/x", "source_version")]:
            with self.subTest(field=field):
                self.ctx = copy.deepcopy(REVIEWED)
                self.edit_review("F1-S2-review-A", lambda r: r["target"].update({field: value}))
                self.assert_unbound(build(self.ctx, self.root), REVIEW_A, component)
        self.ctx = copy.deepcopy(REVIEWED)
        descriptor = dict(json.loads((ROOT / self.ctx["reviews"][0]["artifact"]["path"]).read_text())
                          ["target"]["passages"]["S2-E2"], component_id="S2-E9")
        self.edit_review("F1-S2-review-A", lambda r: r["target"]["passages"].update({"S2-E9": descriptor}))
        bundle = build(self.ctx, self.root)
        self.assert_unbound(bundle, REVIEW_A, "passages")
        self.assertIn("mapping", reviews(bundle)[REVIEW_A]["target_mismatches"])

    def test_missing_or_altered_artifact_fails_closed(self):
        entry = self.ctx["reviews"][0]
        (self.root / entry["artifact"]["path"]).unlink()
        with self.assertRaisesRegex(ContractError, "INPUT_UNAVAILABLE"):
            build(self.ctx, self.root)
        shutil.copyfile(ROOT / entry["artifact"]["path"], self.root / entry["artifact"]["path"])
        self.ctx = copy.deepcopy(REVIEWED)
        self.ctx["reviews"][1]["artifact"]["sha256"] = "0" * 64
        with self.assertRaisesRegex(ContractError, "INPUT_HASH_MISMATCH"):
            build(self.ctx, self.root)

    def test_malformed_reviews_rejected(self):
        cases = [
            (lambda r: r.update(disposition="APPROVED"), "INVALID_LABEL"),
            (lambda r: r["part_dispositions"][0].update(disposition="TRUE"), "INVALID_LABEL"),
            (lambda r: r.update(human_adjudication="PERFORMED"), "INVALID_REVIEW"),
            (lambda r: r.update(independence="ESTABLISHED"), "INVALID_REVIEW"),
            (lambda r: r["coverage"].update(finding_level_effect="APPROVES_FINDING"), "INVALID_REVIEW"),
            (lambda r: r["locators"][0].update(quote="altered quotation"), "INVALID_REVIEW"),
            (lambda r: r.pop("strongest_contrary_interpretation"), "MISSING"),
            (lambda r: r.update(schema="atlas-evidence-review/3"), "UNSUPPORTED_REVIEW_SCHEMA"),
            (lambda r: r["target"]["passages"]["S2-E2"].pop("start"), "MISSING"),
            (lambda r: r["target"]["passages"].update(
                {"S2-E2": r["target"]["passages"]["S2-E2"]["quote_sha256"]}), "INVALID_CONTRACT"),
            (lambda r: r["target"].update(passages={}), "INVALID_REVIEW"),
        ]
        for change, error in cases:
            with self.subTest(error=error):
                self.ctx = copy.deepcopy(REVIEWED)
                self.edit_review("F1-S2-review-B", change)
                with self.assertRaisesRegex(ContractError, error):
                    build(self.ctx, self.root)
        self.ctx = copy.deepcopy(REVIEWED)
        self.ctx["reviews"][0]["review_schema"] = "atlas-evidence-review/9"
        with self.assertRaisesRegex(ContractError, "UNSUPPORTED_REVIEW_SCHEMA"):
            build(self.ctx, self.root)

    # --- restore re-derives bindings ----------------------------------------

    def tampered(self, change):
        records = copy.deepcopy(self.bundle["records"])
        review = next(r for r in records if r["id"] == REVIEW_A)
        change(review, records)
        return rehash(records, RUN)

    def test_restore_rejects_edited_disposition(self):
        def change(review, records):
            text = review["review_artifact_text"].replace('"disposition": "SUPPORTS_WITH_QUALIFICATION"',
                                                          '"disposition": "SUPPORTS"', 1)
            review.update(review_artifact_text=text, raw_output_sha256=sha256(text.encode("utf-8")),
                          imported_disposition="SUPPORTS", review=json.loads(text))
        with self.assertRaisesRegex(ContractError, "REVIEW_ARTIFACT_MISMATCH: .*not the declared artifact"):
            read_export(jsonl(self.tampered(change)))

    def test_restore_rejects_inconsistent_record(self):
        def change(review, records):
            review["imported_disposition"] = "CONTRADICTS"
        with self.assertRaisesRegex(ContractError, "REVIEW_ARTIFACT_MISMATCH"):
            read_export(jsonl(self.tampered(change)))

    def test_restore_rejects_forged_binding(self):
        def change(review, records):
            review.update(target_mismatches=["mapping"], target_binding="TARGET_MISMATCH", refs=[])
            run = next(r for r in records if r["type"] == "AuditRun")
            run["refs"].remove(REVIEW_A)
            run["mismatched_review_ids"].append(REVIEW_A)
        with self.assertRaisesRegex(ContractError, "REVIEW_BINDING_MISMATCH"):
            read_export(jsonl(self.tampered(change)))

    # --- immutable prior records; export, restore, replay -------------------

    def test_prior_records_immutable(self):
        db = self.root / "ledger.sqlite"
        original = build(copy.deepcopy(ORIGINAL), self.root)
        append(db, original["records"])
        append(db, self.bundle["records"])
        before = export(db)
        restored = read_export(before)
        self.assertEqual([r for r in restored if r["id"].startswith(ORIGINAL["run"]["id"] + "/")
                          or r["id"] == ORIGINAL["run"]["id"]],
                         [r for r in sorted(original["records"], key=lambda r: r["id"])
                          if r["type"] not in {"Work", "SourceVersion"}])
        self.assertEqual(sorted(verify_records(restored)["native_projection_verified"]),
                         [ORIGINAL["run"]["id"], RUN])
        # A revised review under the same identity is a conflict, not an overwrite.
        self.edit_review("F1-S2-review-A", lambda r: r.update(disposition="SUPPORTS"))
        with self.assertRaisesRegex(ContractError, "ID_CONTENT_CONFLICT"):
            append(db, build(self.ctx, self.root)["records"])
        self.assertEqual(export(db), before)
        with (contextlib.closing(sqlite3.connect(db)) as connection, connection,
              self.assertRaisesRegex(sqlite3.IntegrityError, "APPEND_ONLY")):
            connection.execute("UPDATE records SET payload='{}' WHERE id=?", (REVIEW_A,))

    def test_cli_import_export_restore_replay(self):
        context = self.root / "reviewed.json"
        context.write_text(canonical(REVIEWED))
        out, ledger = self.root / "out", self.root / "ledger.sqlite"

        def cli(*args):
            return subprocess.run([sys.executable, "-m", "atlas", *args], cwd=ROOT, capture_output=True, text=True)

        self.assertEqual(cli("import", str(context), "--root", str(self.root), "--out", str(out),
                             "--ledger", str(ledger)).returncode, 1)  # archived output quarantined
        self.assertEqual(cli("export", str(ledger), str(self.root / "all.jsonl")).returncode, 0)
        restored = cli("restore", str(self.root / "all.jsonl"), str(self.root / "restored.sqlite"))
        self.assertEqual(restored.returncode, 0, restored.stderr)
        self.assertEqual(json.loads(restored.stdout)["native_projection_verified"], [RUN])
        self.assertEqual(cli("export", str(self.root / "restored.sqlite"), str(self.root / "again.jsonl")).returncode, 0)
        self.assertEqual((self.root / "all.jsonl").read_bytes(), (self.root / "again.jsonl").read_bytes())
        for level in ("strict", "content"):
            replay = cli("replay", str(out / "manifest.json"), str(out / "records.jsonl"),
                         "--root", str(self.root), "--level", level)
            self.assertEqual(replay.returncode, 0, replay.stderr)


if __name__ == "__main__":
    unittest.main()
