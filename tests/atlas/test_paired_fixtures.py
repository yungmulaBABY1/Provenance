"""Paired healthy/closed packet fixtures (cases 12 and 13), ported from package B.

Hashes are package B's pins, verified against d700031. Both outputs predate the
current grammar: they are quarantined as current-contract mismatches, with
native labels preserved as written.
"""

import json
from pathlib import Path
import shutil
import tempfile
import unittest

from atlas.adapter import build
from atlas.ledger import read_export
from test_adapter import BASELINE, ROOT, by_type

FIXTURES = {name: json.loads((ROOT / f"tests/atlas/{name}.json").read_text())
            for name in ("case12-healthy", "case13-closed")}
B_PINS = {  # package B, implementation/atlas_adapter/fixtures.json
    "case12-healthy": ("ee8f024d4e4b63d9e8aab79e291b3c04583ff08cb8ab83974a5d05daaaf153e9",
                       "2ec183817c16c9a8c76125a275cdf0b573591492d9919d4b35df55f77d5e321d"),
    "case13-closed": ("8b9b1c5b4253d51aef653d1e4670a318dc378006a8807fff04f14ae589c3cccb",
                      "17c3ca6b6b52ebfd614b3dee534156eebc642880371c82f79a8bcf58aa66d568"),
}


class PairedFixtureTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        paths = set(BASELINE["files"])
        for ctx in FIXTURES.values():
            paths.add(ctx["output"]["path"])
            paths.update(a["path"] for a in ctx["declared_inputs"])
        for path in paths:
            dest = self.root / path
            dest.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(ROOT / path, dest)
        self.bundles = {name: build(ctx, self.root) for name, ctx in FIXTURES.items()}

    def test_contexts_use_package_b_pins(self):
        for name, (output, packet) in B_PINS.items():
            with self.subTest(name=name):
                self.assertEqual(FIXTURES[name]["output"]["sha256"], output)
                self.assertEqual(FIXTURES[name]["sources"][0]["text_artifact"]["sha256"], packet)

    def test_quarantined_as_current_contract_mismatch(self):
        for name, bundle in self.bundles.items():
            with self.subTest(name=name):
                run = by_type(bundle, "AuditRun")[0]
                codes = {i["code"] for i in run["native_parse_issues"]}
                self.assertIn("CURRENT_CONTRACT_MISMATCH", codes)
                self.assertNotIn("INSTRUMENT_VIOLATION", codes)
                self.assertEqual(run["producing_instrument_compliance"], "UNDETERMINED")
                self.assertEqual(bundle["syntax"], "FAIL")
                findings = by_type(bundle, "AuditFinding")
                self.assertTrue(findings)
                self.assertTrue(all(f["import_status"] == "QUARANTINED" for f in findings))

    def test_native_labels_preserved(self):
        for name, bundle in self.bundles.items():
            for finding in by_type(bundle, "AuditFinding"):
                for field in ("Concede test", "Severity", "Status"):
                    value = finding["native"]["fields"].get(field)
                    if value is not None:
                        with self.subTest(name=name, finding=finding["id"], field=field):
                            self.assertIn(f"| {field} | {value} |", finding["native"]["raw_block"])
        pairs = {(f["native"]["fields"]["Concede test"], f["native"]["fields"]["Severity"])
                 for f in by_type(self.bundles["case13-closed"], "AuditFinding")}
        self.assertIn(("SURVIVES", "major"), pairs)

    def test_source_read_states_recorded(self):
        for name, bundle in self.bundles.items():
            with self.subTest(name=name):
                receipt = by_type(bundle, "SourceReadReceipt")[0]
                self.assertEqual(receipt["state"], "PARTIAL_READ")
                self.assertEqual([c["id"] for c in receipt["extracted_components"]],
                                 ["metadata", "citation_contexts"])
                self.assertEqual(receipt["input_bytes_sha256"], B_PINS[name][1])
                eligibility = by_type(bundle, "AuditRun")[0]["adapter_source_eligibility"]
                self.assertEqual(eligibility, {"packet_metadata": "ELIGIBLE",
                                               "paper_methods_audit": "INELIGIBLE_MISSING_EVIDENCE",
                                               "synthetic_citation_packet": "PENDING_SOURCE_VERIFICATION"})

    def test_bundles_restore_verified(self):
        for name, bundle in self.bundles.items():
            with self.subTest(name=name):
                self.assertEqual(len(read_export(bundle["jsonl"])), len(bundle["records"]))


if __name__ == "__main__":
    unittest.main()
