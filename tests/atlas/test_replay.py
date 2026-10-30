"""Replay levels (F4): strict is byte-exact; content ignores only environment."""

import copy
import json
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest

from atlas.adapter import build
from atlas.contract import ContractError, canonical
from atlas.replay import replay
from test_adapter import BASELINE, POWER, ROOT, SHEN


class ReplayTests(unittest.TestCase):
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
        bundle = build(copy.deepcopy(POWER), self.root)
        self.manifest = copy.deepcopy(bundle["manifest"])
        self.jsonl = bundle["jsonl"]

    def simulate_environment_change(self):
        """Rewrite the receipt as if produced on another interpreter."""
        self.manifest["environment"]["python"] = "0.0.0-simulated"
        self.manifest["environment"]["unicode"] = "0.0.0-simulated"
        lines = [json.loads(line) for line in self.jsonl.decode().splitlines()]
        lines = [self.manifest if r["type"] == "RunManifest" else r for r in lines]
        self.jsonl = ("\n".join(canonical(r) for r in lines) + "\n").encode()

    def run_replay(self, level):
        return replay((canonical(self.manifest) + "\n").encode(), self.jsonl, self.root, level)

    def test_unchanged_replay_passes_both_levels(self):
        for level in ("strict", "content"):
            with self.subTest(level=level):
                result = self.run_replay(level)
                self.assertEqual(result["replay"], "PASS")
                self.assertEqual(result["environment_delta"], {})

    def test_content_replay_passes_across_environment_change_and_reports_it(self):
        self.simulate_environment_change()
        result = self.run_replay("content")
        self.assertEqual(result["replay"], "PASS")
        self.assertEqual(result["environment_delta"]["python"]["recorded"], "0.0.0-simulated")
        self.assertEqual(set(result["environment_delta"]), {"python", "unicode"})

    def test_strict_replay_fails_on_environment_change(self):
        self.simulate_environment_change()
        with self.assertRaisesRegex(ContractError, r"REPLAY_MISMATCH \(strict\): environment: python, unicode"):
            self.run_replay("strict")

    def test_changed_input_fails_both_levels_and_names_input(self):
        output = self.root / POWER["output"]["path"]
        output.write_bytes(output.read_bytes() + b"\n")
        for level in ("strict", "content"):
            with self.subTest(level=level):
                with self.assertRaisesRegex(
                        ContractError, f"REPLAY_MISMATCH: input: INPUT_HASH_MISMATCH: {POWER['output']['path']}"):
                    self.run_replay(level)

    def test_changed_component_is_named(self):
        self.manifest["parser"]["version"] = "0-other"
        with self.assertRaisesRegex(ContractError, r"REPLAY_MISMATCH \(content\): parser"):
            self.run_replay("content")
        self.manifest = json.loads(canonical(build(copy.deepcopy(POWER), self.root)["manifest"]))
        self.manifest["normalizer"] = "nfkc-whitespace/1"
        with self.assertRaisesRegex(ContractError, r"REPLAY_MISMATCH \(content\): normalizer"):
            self.run_replay("content")

    def test_cli_level_flag(self):
        self.simulate_environment_change()
        manifest_path, jsonl_path = self.root / "manifest.json", self.root / "records.jsonl"
        manifest_path.write_text(canonical(self.manifest) + "\n")
        jsonl_path.write_bytes(self.jsonl)
        command = [sys.executable, "-m", "atlas", "replay", str(manifest_path), str(jsonl_path),
                   "--root", str(self.root)]
        strict = subprocess.run(command, cwd=ROOT, capture_output=True, text=True)
        self.assertEqual(strict.returncode, 2)
        self.assertIn("environment", strict.stderr)
        content = subprocess.run([*command, "--level", "content"], cwd=ROOT, capture_output=True, text=True)
        self.assertEqual(content.returncode, 0, content.stderr)
        self.assertIn("0.0.0-simulated", content.stdout)


if __name__ == "__main__":
    unittest.main()
