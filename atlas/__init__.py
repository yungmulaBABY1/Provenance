"""Deterministic, offline Provenance import; no model or retrieval backend."""

VERSION = "0.3.0"
# Record schema. 0.2: Passage gains exact_match/normalized_match and
# normalized_sha256 is computed with nfc-whitespace/2 instead of NFKC.
SCHEMA = "atlas-adapter/0.2"
# Import-context schema; unchanged.
CONTEXT_SCHEMA = "atlas-adapter/0.1"
