"""Validation baseline independent of the working tree (F3)."""

import copy
from pathlib import Path
import shutil
import tempfile
import unittest
from unittest import mock

from atlas import adapter
from atlas.adapter import build
from atlas.contract import ContractError
from test_adapter import BASELINE, POWER, ROOT, SHEN

PROMPT = "prompts/research-analysis/2-citation-network.txt"


class BaselineTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name) / "repo"
        paths = set(BASELINE["files"])
        paths.update(a["path"] for c in (POWER, SHEN) for a in c["declared_inputs"])
        for path in paths:
            dest = self.root / path
            dest.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(ROOT / path, dest)

    def test_vendored_copies_match_pins(self):
        for path, entry in BASELINE["files"].items():
            with self.subTest(path=path):
                self.assertEqual(len(adapter.vendored(entry)), entry["bytes"])

    def test_unchanged_tree_has_no_drift_notice(self):
        bundle = build(copy.deepcopy(POWER), self.root)
        self.assertEqual(bundle["notices"], [])
        self.assertEqual(bundle["manifest"]["environment"]["validation_baseline_working_tree"]["status"],
                         "MATCHES_VENDORED_BASELINE")

    def test_prompt_edited_in_working_tree_imports_with_drift_notice(self):
        before = build(copy.deepcopy(POWER), self.root)
        prompt = self.root / PROMPT
        prompt.write_bytes(prompt.read_bytes() + b"\n")
        after = build(copy.deepcopy(POWER), self.root)
        self.assertEqual(after["notices"], ["VALIDATION_BASELINE_DIFFERS_FROM_WORKING_TREE"])
        drift = after["manifest"]["environment"]["validation_baseline_working_tree"]
        self.assertEqual([(f["path"], f["working_tree"]) for f in drift["files"]], [(PROMPT, "DIFFERS")])
        self.assertEqual(after["syntax"], before["syntax"])
        # Only the environment block differs; every non-manifest record is identical.
        strip = lambda b: [r for r in b["records"] if r["type"] != "RunManifest"]
        self.assertEqual(strip(after), strip(before))

    def test_missing_working_tree_file_is_reported(self):
        (self.root / PROMPT).unlink()
        drift = build(copy.deepcopy(POWER), self.root)["manifest"]["environment"]["validation_baseline_working_tree"]
        self.assertIn({"path": PROMPT, "working_tree": "MISSING"}, drift["files"])

    def test_tampered_vendored_file_rejected(self):
        vendored = Path(self.temp.name) / "vendored"
        shutil.copytree(adapter.BASELINE_FILES, vendored)
        target = vendored / PROMPT
        target.write_bytes(target.read_bytes().replace(b"Finding", b"Findinq", 1))
        with mock.patch.object(adapter, "BASELINE_FILES", vendored):
            with self.assertRaisesRegex(ContractError, f"BASELINE_HASH_MISMATCH: {PROMPT}"):
                build(copy.deepcopy(POWER), self.root)


if __name__ == "__main__":
    unittest.main()
