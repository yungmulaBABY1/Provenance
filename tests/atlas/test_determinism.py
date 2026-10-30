"""Parse output and import bytes must not depend on the per-process hash seed.

Every other test builds and re-derives inside one process, which hides
set-ordering differences; these run separate interpreters with fixed seeds.
"""

import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

from atlas import native
from atlas.contract import canonical
from test_adapter import ROOT

OUTPUTS = ["tests/cases/runs/2026-07-30-case-12-13-sol/12-output.md",
           "tests/cases/runs/2026-07-30-case-12-13-sol/13-output.md",
           "compliance/run-output-large.txt"]
SEEDS = ["0", "1", "2", "3", "4"]


def run(code, seed, *args):
    env = {**os.environ, "PYTHONHASHSEED": seed}
    result = subprocess.run([sys.executable, "-c", code, *args], cwd=ROOT, env=env,
                            capture_output=True, text=True, check=True)
    return result.stdout


class DeterminismTests(unittest.TestCase):
    def test_parser_version(self):
        self.assertEqual(native.VERSION, "3")

    def test_parse_identical_across_hash_seeds(self):
        code = ("import sys; from atlas.native import parse; from atlas.contract import canonical; "
                "print(canonical(parse(open(sys.argv[1], encoding='utf-8').read())))")
        for path in OUTPUTS:
            with self.subTest(path=path):
                results = {seed: run(code, seed, path) for seed in SEEDS}
                self.assertEqual(len(set(results.values())), 1, path)

    def test_import_in_one_process_restores_in_another(self):
        with tempfile.TemporaryDirectory() as directory:
            for name in ("case12-healthy", "case13-closed"):
                with self.subTest(name=name):
                    out = Path(directory) / name
                    subprocess.run([sys.executable, "-m", "atlas", "import", f"tests/atlas/{name}.json",
                                    "--root", ".", "--out", str(out)], cwd=ROOT,
                                   env={**os.environ, "PYTHONHASHSEED": "1"}, capture_output=True, check=False)
                    for seed in ("2", "3"):
                        restored = subprocess.run(
                            [sys.executable, "-m", "atlas", "restore", str(out / "records.jsonl"),
                             str(Path(directory) / f"{name}-{seed}.sqlite")],
                            cwd=ROOT, env={**os.environ, "PYTHONHASHSEED": seed}, capture_output=True, text=True)
                        self.assertEqual(restored.returncode, 0, restored.stderr)
                        report = json.loads(restored.stdout)
                        self.assertEqual(len(report["native_projection_verified"]), 1)
                        replay = subprocess.run(
                            [sys.executable, "-m", "atlas", "replay", str(out / "manifest.json"),
                             str(out / "records.jsonl"), "--root", "."],
                            cwd=ROOT, env={**os.environ, "PYTHONHASHSEED": seed}, capture_output=True, text=True)
                        self.assertEqual(replay.returncode, 0, replay.stderr)


if __name__ == "__main__":
    unittest.main()
