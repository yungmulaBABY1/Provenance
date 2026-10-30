"""Exact character spans for each finding's native output anchor."""

import copy
from pathlib import Path
import shutil
import tempfile
import unittest

from atlas.adapter import build
from atlas.contract import ContractError, jsonl
from atlas.ledger import read_export
from atlas.native import output_span
from test_adapter import BASELINE, POWER, RAW, ROOT, SHEN, artifact, by_type
from test_integrity import rehash


class OutputSpanTests(unittest.TestCase):
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

    def test_span_selects_exact_finding_block(self):
        bundle = build(copy.deepcopy(POWER), self.root)
        for finding in by_type(bundle, "AuditFinding"):
            with self.subTest(finding=finding["id"]):
                anchor = finding["native_output_anchor"]
                text = RAW[anchor["char_start"]:anchor["char_end"]]
                self.assertEqual(text, finding["native"]["raw_block"])
                self.assertTrue(text.startswith(f"Finding {finding['native']['number']}"))
                self.assertEqual(anchor["char_unit"], "unicode_codepoint")
                self.assertEqual(anchor["char_interval"], "half_open")
                self.assertEqual(anchor["first_line"], finding["native"]["line_start"])

    def test_crlf_span_counts_raw_characters(self):
        data = RAW.replace("\n", "\r\n")
        (self.root / "crlf.md").write_bytes(data.encode("utf-8"))
        ctx = copy.deepcopy(POWER)
        ctx["output"] = artifact(self.root, "crlf.md")
        finding = by_type(build(ctx, self.root), "AuditFinding")[0]
        anchor = finding["native_output_anchor"]
        span = data[anchor["char_start"]:anchor["char_end"]]
        self.assertEqual(span, finding["native"]["raw_block"].replace("\n", "\r\n"))
        self.assertFalse(span.endswith("\r"))

    def test_non_ascii_offsets_are_code_points(self):
        self.assertEqual(output_span("µ²\nH₂O\nx", 2, 2), (3, 6))
        self.assertEqual(output_span("a\r\nb", 1, 2), (0, 4))

    def test_tampered_span_rejected_on_restore(self):
        records = copy.deepcopy(build(copy.deepcopy(POWER), self.root)["records"])
        finding = next(r for r in records if r["type"] == "AuditFinding")
        finding["native_output_anchor"]["char_end"] -= 1
        rehash(records, finding["audit_run_id"])
        with self.assertRaisesRegex(ContractError, "NATIVE_PROJECTION_MISMATCH: .*native_output_anchor"):
            read_export(jsonl(records))


if __name__ == "__main__":
    unittest.main()
