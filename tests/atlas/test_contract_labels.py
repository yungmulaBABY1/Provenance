"""Contract-relative labels (F2): historical outputs are not charged with
violating an instrument nobody has verified they were given."""

import copy
from pathlib import Path
import shutil
import tempfile
import unittest

from atlas.adapter import build
from test_adapter import BASELINE, POWER, RAW, ROOT, SHEN, artifact, by_type

ARCHIVED_OUTPUTS = [
    "compliance/run-output.md",
    "compliance/run-output-medium.md",
    "compliance/run-output-large.txt",
    "tests/cases/runs/2026-07-30-case-12-13-sol/12-output.md",
    "tests/cases/runs/2026-07-30-case-12-13-sol/13-output.md",
    "examples/research/shen/04_citation_network.txt",
]
PROMPT_BLOB = BASELINE["files"]["prompts/research-analysis/2-citation-network.txt"]["git_blob_sha1"]


def all_issue_codes(bundle):
    run = by_type(bundle, "AuditRun")[0]
    codes = {i["code"] for i in run["native_parse_issues"]}
    for finding in by_type(bundle, "AuditFinding"):
        codes.update(i["code"] for i in finding["native"]["issues"])
    return codes


class ContractLabelTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        paths = set(BASELINE["files"]) | set(ARCHIVED_OUTPUTS)
        paths.update(a["path"] for c in (POWER, SHEN) for a in c["declared_inputs"])
        for path in paths:
            dest = self.root / path
            dest.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(ROOT / path, dest)

    def archived(self, path):
        ctx = copy.deepcopy(SHEN)
        ctx["run"]["id"] = f"urn:atlas:test:{path}"
        ctx["output"] = artifact(self.root, path)
        ctx["finding_checks"] = {}
        ctx["reviews"] = []
        return build(ctx, self.root)

    def test_archived_outputs_are_current_contract_mismatches(self):
        for path in ARCHIVED_OUTPUTS:
            with self.subTest(path=path):
                bundle = self.archived(path)
                codes = all_issue_codes(bundle)
                self.assertIn("CURRENT_CONTRACT_MISMATCH", codes)
                self.assertNotIn("INSTRUMENT_VIOLATION", codes)
                run = by_type(bundle, "AuditRun")[0]
                self.assertEqual(run["producing_instrument_compliance"], "UNDETERMINED")
                # Quarantine is unchanged.
                self.assertEqual(bundle["syntax"], "FAIL")
                self.assertTrue(all(f["import_status"] == "QUARANTINED"
                                    for f in by_type(bundle, "AuditFinding")))

    def test_case_13_native_values_kept_as_written(self):
        bundle = self.archived("tests/cases/runs/2026-07-30-case-12-13-sol/13-output.md")
        pairs = [(f["native"]["fields"].get("Concede test"), f["native"]["fields"].get("Severity"))
                 for f in by_type(bundle, "AuditFinding")]
        self.assertIn(("SURVIVES", "major"), pairs)

    def test_verified_instrument_can_conform_or_violate(self):
        ctx = copy.deepcopy(POWER)
        ctx["run"]["historical_instrument"] = {"identity": PROMPT_BLOB, "verification": "VERIFIED"}
        self.assertEqual(by_type(build(ctx, self.root), "AuditRun")[0]
                         ["producing_instrument_compliance"], "CONFORMS")
        (self.root / "mutated.md").write_text(RAW.replace("| Concede test | DEFEATS |", "| Concede test | MAGIC |"))
        ctx["output"] = artifact(self.root, "mutated.md")
        self.assertEqual(by_type(build(ctx, self.root), "AuditRun")[0]
                         ["producing_instrument_compliance"], "VIOLATION")

    def test_unverified_or_other_instrument_is_undetermined(self):
        (self.root / "mutated.md").write_text(RAW.replace("| Concede test | DEFEATS |", "| Concede test | MAGIC |"))
        for instrument in [{"identity": PROMPT_BLOB, "verification": "INSTRUMENT VERSION UNVERIFIED"},
                           {"identity": "0" * 40, "verification": "VERIFIED"}]:
            with self.subTest(instrument=instrument):
                ctx = copy.deepcopy(POWER)
                ctx["run"]["historical_instrument"] = instrument
                ctx["output"] = artifact(self.root, "mutated.md")
                bundle = build(ctx, self.root)
                self.assertEqual(bundle["syntax"], "FAIL")
                self.assertEqual(by_type(bundle, "AuditRun")[0]["producing_instrument_compliance"],
                                 "UNDETERMINED")


if __name__ == "__main__":
    unittest.main()
