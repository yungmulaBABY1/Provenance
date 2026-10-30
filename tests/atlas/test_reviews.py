"""Review references (F5): a run links only reviews bound to its exact output."""

import copy
from pathlib import Path
import shutil
import tempfile
import unittest

from atlas.adapter import build
from atlas.contract import ContractError, validate_records
from test_adapter import BASELINE, POWER, ROOT, SHEN, by_type

COUNTER_AUDIT = "urn:atlas:import:shen-known-bad:1/review/earlier-shen-counter-audit"


class ReviewRefTests(unittest.TestCase):
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

    def test_shen_earlier_counter_audit_not_in_run_refs(self):
        bundle = build(copy.deepcopy(SHEN), self.root)
        run = by_type(bundle, "AuditRun")[0]
        review = next(r for r in by_type(bundle, "ReviewDecision") if r["id"] == COUNTER_AUDIT)
        self.assertEqual(review["target_binding"], "TARGET_MISMATCH")
        self.assertNotIn(COUNTER_AUDIT, run["refs"])
        self.assertEqual(run["mismatched_review_ids"], [COUNTER_AUDIT])

    def test_matching_review_is_in_run_refs(self):
        ctx = copy.deepcopy(SHEN)
        ctx["reviews"][0]["target_output_sha256"] = ctx["output"]["sha256"]
        run = by_type(build(ctx, self.root), "AuditRun")[0]
        self.assertIn(COUNTER_AUDIT, run["refs"])
        self.assertEqual(run["mismatched_review_ids"], [])

    def test_record_contract_rejects_mismatched_review_in_refs(self):
        records = copy.deepcopy(build(copy.deepcopy(SHEN), self.root)["records"])
        run = next(r for r in records if r["type"] == "AuditRun")
        run["refs"].append(COUNTER_AUDIT)
        with self.assertRaisesRegex(ContractError, "review of another output"):
            validate_records(records)


if __name__ == "__main__":
    unittest.main()
