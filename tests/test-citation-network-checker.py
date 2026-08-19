#!/usr/bin/env python3
"""Regression checks for the patched citation-network compliance checker."""

from pathlib import Path
import subprocess
import sys


TESTS = Path(__file__).resolve().parent
REPO = TESTS.parent
CHECKER = REPO / "prompts" / "research-analysis" / "check-citation-network-output.py"
FIXTURES = TESTS / "cases" / "citation-network-checker"
DIRTY = FIXTURES / "shen-revised-known-bad.txt"
CLEAN_VOCAB = FIXTURES / "shen-v1-whitelist-clean.txt"
POSITIVE = FIXTURES / "complete-clean-control.md"
REVIEW = FIXTURES / "locked-source-review-control.md"


def run(*args: str) -> tuple[int, str]:
    result = subprocess.run(
        [sys.executable, str(CHECKER), *args],
        check=False,
        capture_output=True,
        text=True,
    )
    return result.returncode, result.stdout + result.stderr


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def main() -> int:
    dirty_code, dirty_output = run(str(DIRTY))
    require(dirty_code == 1, "Known-bad Shen revised output must fail.")
    expected_tokens = {
        "CONTEXT-VERIFIED": 24,
        "GRAPH-VERIFIED": 37,
        "RECEPTION-VERIFIED": 1,
        "SOURCE-VERIFIED": 9,
    }
    for token, count in expected_tokens.items():
        require(
            f"VERIFICATION_VOCAB_FAIL\t{token}\tcount={count}\tlines=" in dirty_output,
            f"Missing line-numbered whitelist failure for {token} x{count}.",
        )
    require(
        "CONTENT_FORM_FAIL\tmissing or empty\tRISK BAND:" in dirty_output,
        "Known-bad Shen output must fail the explicit risk-band check.",
    )
    for label in (
        "GRAPH CORPUS NODE LIST:",
        "INTERNAL EDGE LIST:",
        "DENSITY NUMERATOR:",
        "DENSITY DENOMINATOR:",
        "DENSITY INPUT COVERAGE:",
    ):
        require(
            f"GRAPH_RECEIPT_FAIL\tmissing or empty\t{label}" in dirty_output,
            f"Known-bad Shen output must fail graph receipt {label}.",
        )

    clean_code, clean_output = run("--vocab-only", str(CLEAN_VOCAB))
    require(clean_code == 0, "Shen V1 must pass the whitelist-only clean control.")
    require("CONTENT_RESULT\tPASS" in clean_output, "Clean whitelist control did not pass.")

    positive_code, positive_output = run(str(POSITIVE))
    require(positive_code == 0, "Patched positive fixture must pass.")
    require("STRUCTURAL_RESULT\tPASS" in positive_output, "Positive structural layer failed.")
    require("CONTENT_RESULT\tPASS" in positive_output, "Positive content layer failed.")
    require(
        "PASS\tAll deterministic structural and content-form checks passed" in positive_output,
        "Positive fixture did not reach bare PASS.",
    )

    review_code, review_output = run(str(REVIEW))
    require(review_code == 0, "Review fixture must pass deterministic checks.")
    require(
        "CONTENT_RESULT\tPASS-WITH-REVIEW\titems=1" in review_output,
        "Review fixture did not expose its pending review count.",
    )
    require(
        "REVIEW_ITEM_1\tSOURCE_LOCK_TRUTH" in review_output,
        "Review fixture did not emit the targeted source-lock review item.",
    )
    require(
        "PASS-WITH-REVIEW: 1 items" in review_output,
        "Review fixture incorrectly returned bare PASS.",
    )

    print(
        "PASS\tdirty full fixture failed; Shen V1 whitelist control passed; "
        "clean fixture returned PASS; review fixture returned PASS-WITH-REVIEW."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
