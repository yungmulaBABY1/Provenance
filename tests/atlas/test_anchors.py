"""Exact versus normalized anchor matches (R2). NFKC is not used for matching."""

import copy
from pathlib import Path
import tempfile
import unittest

from atlas.contract import NORMALIZER, ContractError, passage_hash, sha256, validate_records
from atlas.sources import assess_checks, inspect_sources
from test_adapter import POWER

COMPATIBILITY_PAIRS = [("10²", "102"), ("H₂O", "H2O"), ("½", "1⁄2"), ("Ⅳ", "IV"),
                       ("ℓ", "l"), ("µ", "μ"), ("ﬁt", "fit")]


def anchor(source_text, quote):
    """Anchor `quote` against the whole of `source_text`; return (Passage, check)."""
    with tempfile.TemporaryDirectory() as directory:
        data = source_text.encode("utf-8")
        Path(directory, "source.txt").write_bytes(data)
        source = copy.deepcopy(POWER["sources"][0])
        end = len(source_text)
        source.update(text_artifact={"path": "source.txt", "sha256": sha256(data)},
                      access_outcome="AVAILABLE", warnings=[], failed_components=[],
                      version_confidence="EXPLICIT_FIXTURE_ASSIGNMENT",
                      extraction={"engine": "plain-utf8", "version": "1", "configuration": {}},
                      components=[{"id": "body", "kind": "section", "start": 0, "end": end}],
                      requested_components=["body"])
        passage = {"id": "P1", "source_version_id": source["id"], "component_id": "body",
                   "start": 0, "end": end, "quote": quote, "normalized_sha256": passage_hash(quote)}
        check = {"id": "c", "kind": "content", "scope": "test span",
                 "requirements": [{"source_version_id": source["id"], "component_ids": ["body"],
                                   "passage_ids": ["P1"]}]}
        context = {"run": POWER["run"], "sources": [source], "passages": [passage], "checks": [check]}
        _, receipts, anchors = inspect_sources(context, Path(directory))
        return anchors["P1"], assess_checks(context, receipts, anchors)["c"]


class AnchorTests(unittest.TestCase):
    def test_normalizer_id(self):
        self.assertEqual(NORMALIZER, "nfc-whitespace/2")

    def test_compatibility_pairs_never_match(self):
        for source_text, quote in COMPATIBILITY_PAIRS:
            for a, b in [(source_text, quote), (quote, source_text)]:
                with self.subTest(source=a, quote=b):
                    passage, check = anchor(a, b)
                    self.assertNotIn(passage["match"], {"MATCH", "NORMALIZED_MATCH_ONLY"})
                    self.assertFalse(passage["exact_match"])
                    self.assertFalse(passage["normalized_match"])
                    self.assertEqual(check["eligibility"], "PENDING_SOURCE_VERIFICATION")

    def test_line_break_only_difference_is_normalized_only(self):
        passage, check = anchor("effect was\nreplicated", "effect was replicated")
        self.assertEqual(passage["match"], "NORMALIZED_MATCH_ONLY")
        self.assertFalse(passage["exact_match"])
        self.assertTrue(passage["normalized_match"])
        self.assertEqual(passage["normalizer"], "nfc-whitespace/2")
        # A named limitation: never full eligibility.
        self.assertEqual(check["eligibility"], "ELIGIBLE_WITH_LIMITATIONS")
        self.assertIn("NORMALIZED_MATCH_ONLY:P1", check["limitations"])

    def test_identical_quote_is_match(self):
        passage, check = anchor("H₂O at 10² Pa", "H₂O at 10² Pa")
        self.assertEqual(passage["match"], "MATCH")
        self.assertTrue(passage["exact_match"])
        self.assertTrue(passage["normalized_match"])
        self.assertEqual(check["eligibility"], "ELIGIBLE")

    def test_unicode_minus_is_mismatch(self):
        passage, _ = anchor("−0.5", "-0.5")
        self.assertEqual(passage["match"], "MISMATCH")
        self.assertFalse(passage["exact_match"])
        self.assertFalse(passage["normalized_match"])

    def test_record_contract_rejects_match_without_exact(self):
        passage, _ = anchor("effect was\nreplicated", "effect was replicated")
        forged = dict(passage, match="MATCH")
        with self.assertRaisesRegex(ContractError, "contradicts exact/normalized"):
            validate_records([forged])


if __name__ == "__main__":
    unittest.main()
