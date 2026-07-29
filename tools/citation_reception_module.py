#!/usr/bin/env python3
"""
CITATION RECEPTION MODULE
=========================
Replaces the counter-audit's memory-based reception check with REAL data
pulled from free citation APIs (OpenAlex + Semantic Scholar).

PURPOSE
-------
For any source the counter-audit makes "load-bearing" (rates strong/severe or
uses to move the verdict), this module retrieves:
  - citation count and citing-work list
  - how many citing works are formal replies/comments/rebuttals
  - citation-context snippets (the sentences where others cite this source)
  - reception-signal keywords in those snippets (refute / support / etc.)
  - open-access status + PDF link when available

It returns a structured RECEPTION PROFILE that the model then REASONS OVER,
instead of the model recalling reception from training. This is the fix for
the McShane & Wyner failure: reception becomes retrieved, not remembered.

WHAT THIS DOES AND DOES NOT DO
------------------------------
DOES: reliably establish whether a source was heavily contested, how many
formal responses it drew, and the tenor of how it's cited -- all from free APIs,
no journal subscription, no full text required.

DOES NOT: adjudicate who "won" a technical dispute. That still needs full text
and stays honestly labeled as unverified. This module answers "was it contested
and how" -- which is exactly the signal that would have caught McShane & Wyner.

REQUIREMENTS
------------
  pip install requests
  (No API keys required. A free Semantic Scholar key raises rate limits;
   set S2_API_KEY env var if you have one.)

Set a real contact email in MAILTO -- OpenAlex uses it for the polite pool
(faster, more reliable). This is required etiquette, not optional.
"""

import os
import re
import time
import requests
from urllib.parse import quote

MAILTO = os.environ.get("OPENALEX_MAILTO", "you@example.com")  # <-- set this
S2_KEY = os.environ.get("S2_API_KEY")  # optional, raises rate limits

OPENALEX = "https://api.openalex.org"
S2 = "https://api.semanticscholar.org/graph/v1"

# --- Reception-signal lexicon -------------------------------------------------
# Words in a citation-context snippet that suggest the citing paper is
# CHALLENGING the cited source vs. SUPPORTING it. Heuristic only; the model
# reasons over the actual snippets, this just pre-tallies signal.
REFUTE_TERMS = [
    "however", "but", "flawed", "misspecified", "incorrect", "erroneous",
    "we show that", "contrary to", "fails to", "does not", "cannot",
    "overstate", "overestimate", "spurious", "artifact", "criticism",
    "criticize", "rebut", "refute", "dispute", "disagree", "problematic",
    "invalid", "unwarranted", "misleading", "in contrast", "reanalysis",
    "we find no", "no evidence", "contradict", "questionable", "biased",
]
SUPPORT_TERMS = [
    "consistent with", "confirms", "in agreement", "supports", "as shown by",
    "corroborate", "replicate", "extends", "building on", "following",
    "in line with", "validate", "reproduce", "we adopt", "we use the",
    "well-established", "seminal", "foundational", "as demonstrated",
]
# Title/venue patterns that signal a formal reply/comment/rebuttal
REPLY_TITLE_PATTERNS = [
    r"\bcomment on\b", r"\breply to\b", r"\bresponse to\b", r"\brejoinder\b",
    r"\bcorrigendum\b", r"\berratum\b", r"\bretraction\b", r"\bre:\b",
    r"\bcritique of\b", r"\breanalysis of\b", r"\brevisiting\b",
    r"\ba comment\b", r"\bdiscussion of\b", r"\bconcerns? (about|regarding)\b",
]


def _get(url, params=None, headers=None, tries=3):
    for i in range(tries):
        try:
            r = requests.get(url, params=params, headers=headers, timeout=30)
            if r.status_code == 429:
                time.sleep(2 * (i + 1))
                continue
            r.raise_for_status()
            return r.json()
        except requests.RequestException:
            if i == tries - 1:
                return None
            time.sleep(1.5 * (i + 1))
    return None


def find_openalex_work(query):
    """Resolve a title/DOI string to an OpenAlex work object."""
    # If it looks like a DOI, use it directly.
    doi = re.search(r"10\.\d{4,9}/[-._;()/:A-Z0-9]+", query, re.I)
    if doi:
        w = _get(f"{OPENALEX}/works/https://doi.org/{doi.group(0)}",
                 params={"mailto": MAILTO})
        if w:
            return w
    # Otherwise title search, take best hit.
    res = _get(f"{OPENALEX}/works",
               params={"search": query, "per-page": 1, "mailto": MAILTO})
    if res and res.get("results"):
        return res["results"][0]
    return None


def fetch_citing_works(work, max_pages=5, per_page=100):
    """Pull the works that cite this work, via OpenAlex cited_by feed."""
    citing = []
    wid = work.get("id", "").split("/")[-1]
    if not wid:
        return citing
    cursor = "*"
    for _ in range(max_pages):
        res = _get(f"{OPENALEX}/works",
                   params={"filter": f"cites:{wid}",
                           "per-page": per_page, "cursor": cursor,
                           "mailto": MAILTO})
        if not res or not res.get("results"):
            break
        citing.extend(res["results"])
        cursor = res.get("meta", {}).get("next_cursor")
        if not cursor:
            break
    return citing


def fetch_s2_contexts(query):
    """
    Semantic Scholar: get citation CONTEXTS (the sentences where others cite
    this paper) plus isInfluential flags. This is the reception goldmine.
    """
    headers = {"x-api-key": S2_KEY} if S2_KEY else {}
    # Resolve paper
    search = _get(f"{S2}/paper/search",
                  params={"query": query, "limit": 1, "fields": "paperId,title"},
                  headers=headers)
    if not search or not search.get("data"):
        return None
    pid = search["data"][0]["paperId"]
    # Pull citations with contexts + influence flag
    cites = _get(f"{S2}/paper/{pid}/citations",
                 params={"limit": 1000,
                         "fields": "contexts,isInfluential,title,year"},
                 headers=headers)
    return cites.get("data") if cites else None


def classify_snippet(text):
    """Tally refute vs support signal in one citation-context snippet."""
    t = text.lower()
    refute = sum(1 for w in REFUTE_TERMS if w in t)
    support = sum(1 for w in SUPPORT_TERMS if w in t)
    return refute, support


def is_reply_title(title):
    if not title:
        return False
    t = title.lower()
    return any(re.search(p, t) for p in REPLY_TITLE_PATTERNS)


def build_reception_profile(query):
    """
    Main entry point. Given a source (title or DOI), return a structured
    reception profile built from real API data for the model to reason over.
    """
    profile = {
        "query": query,
        "resolved": False,
        "citation_count": None,
        "n_citing_pulled": 0,
        "n_formal_replies": 0,
        "reply_titles": [],
        "influential_citation_count": None,
        "n_contexts": 0,
        "refute_signal": 0,
        "support_signal": 0,
        "sample_refuting_snippets": [],
        "sample_supporting_snippets": [],
        "open_access_pdf": None,
        "abstract_available": False,
        # --- verification state (shared_primitives.txt §1) ---
        # Emitted mechanically. The module can establish LOCATED,
        # RECEPTION-CONFIRMED, CONTESTED, REBUTTED, PROVISIONAL.
        # It CANNOT establish ABSTRACT-CONFIRMED (requires judging whether the
        # abstract supports the claimed relevance) or FULL-TEXT-CONFIRMED
        # (requires a human read). Those stay None rather than being guessed.
        "verification_state": None,
        "verification_state_rationale": "",
        "full_text_confirmed": None,  # always None — human read only
        "reception_summary": "",
        "data_source": "retrieved (OpenAlex + Semantic Scholar)",
        "caveat": ("Reception SHAPE (contested vs. unchallenged) is retrieved and "
                   "reliable. Reception OUTCOME (who won a technical dispute) is NOT "
                   "established here and needs full text. Do not infer the winner."),
    }

    work = find_openalex_work(query)
    if work:
        profile["resolved"] = True
        profile["citation_count"] = work.get("cited_by_count")
        oa = work.get("open_access", {})
        profile["open_access_pdf"] = oa.get("oa_url")

        citing = fetch_citing_works(work)
        profile["n_citing_pulled"] = len(citing)
        replies = [c for c in citing
                   if is_reply_title(c.get("title") or c.get("display_name"))]
        profile["n_formal_replies"] = len(replies)
        profile["reply_titles"] = [
            (c.get("title") or c.get("display_name")) for c in replies[:15]
        ]

    # Semantic Scholar contexts (the sentence-level reception signal)
    contexts = fetch_s2_contexts(query)
    if contexts:
        infl = sum(1 for c in contexts if c.get("isInfluential"))
        profile["influential_citation_count"] = infl
        all_snips = []
        for c in contexts:
            for snip in (c.get("contexts") or []):
                all_snips.append(snip)
        profile["n_contexts"] = len(all_snips)
        for snip in all_snips:
            r, s = classify_snippet(snip)
            profile["refute_signal"] += r
            profile["support_signal"] += s
            if r > s and len(profile["sample_refuting_snippets"]) < 8:
                profile["sample_refuting_snippets"].append(snip.strip()[:400])
            elif s > r and len(profile["sample_supporting_snippets"]) < 8:
                profile["sample_supporting_snippets"].append(snip.strip()[:400])

    # --- Verification state (shared_primitives.txt §1) -----------------------
    # Mechanical derivation only. Never guesses upward.
    cc = profile["citation_count"]
    nr = profile["n_formal_replies"]
    rs, ss = profile["refute_signal"], profile["support_signal"]
    reception_checked = profile["n_citing_pulled"] > 0 or profile["n_contexts"] > 0

    if not profile["resolved"]:
        profile["verification_state"] = "PROVISIONAL"
        profile["verification_state_rationale"] = (
            "Source could not be resolved via OpenAlex/Semantic Scholar. Nothing "
            "verified. Any claim about this source rests on model memory — likely "
            "error direction is OVER-rating, since prominence is better represented "
            "in training than refutation."
        )
    elif not reception_checked:
        profile["verification_state"] = "LOCATED"
        profile["verification_state_rationale"] = (
            "Metadata resolved; no citing works or citation contexts retrieved, so "
            "reception is unchecked. Cannot anchor a severe finding."
        )
    else:
        # Reception WAS checked. Report the most specific applicable state.
        rebutted = nr >= 3 and rs > ss * 2
        contested = nr >= 2 or (rs > ss and rs >= 5)
        if rebutted:
            profile["verification_state"] = "REBUTTED"
            profile["verification_state_rationale"] = (
                f"{nr} formal replies/comments detected and refute-signal ({rs}) "
                f"substantially exceeds support-signal ({ss}). Later work appears to "
                f"directly challenge this source. Downgrade its weight regardless of "
                f"how strong its original claims read. NOTE: this establishes that a "
                f"substantial challenge EXISTS, not that the challenge was correct."
            )
        elif contested:
            profile["verification_state"] = "CONTESTED"
            profile["verification_state_rationale"] = (
                f"{nr} formal replies/comments, refute-signal {rs} vs support-signal "
                f"{ss}. Credible disagreement exists. Who is correct is NOT "
                f"established — that needs full text."
            )
        else:
            profile["verification_state"] = "RECEPTION-CONFIRMED"
            profile["verification_state_rationale"] = (
                f"Reception checked against retrieval: {cc} citations, {nr} formal "
                f"replies, refute-signal {rs} vs support-signal {ss}. No large "
                f"formal-response cluster detected. NOTE: absence of detected replies "
                f"is weaker evidence than presence — reply detection is title-pattern "
                f"based and will miss replies that don't announce themselves."
            )

    # ABSTRACT-CONFIRMED and FULL-TEXT-CONFIRMED are deliberately NOT emitted.
    # Both require judging whether the content supports a specific claim, which is
    # not a mechanical operation. The module reports availability only.

    # Human-readable one-line reception signal for the model
    if not profile["resolved"]:
        profile["reception_summary"] = "SOURCE NOT RESOLVED via API — falls back to memory-flagged, provisional."
    else:
        contested = nr >= 2 or (rs > ss and rs >= 5)
        if contested:
            profile["reception_summary"] = (
                f"CONTESTED: {cc} citations, {nr} formal replies/comments, "
                f"refute-signal {rs} vs support-signal {ss}. This source drew "
                f"substantial formal response — cap it until outcome is verified. "
                f"(This is the signal that would have caught McShane & Wyner.)"
            )
        else:
            profile["reception_summary"] = (
                f"NOT visibly contested: {cc} citations, {nr} formal replies, "
                f"refute-signal {rs} vs support-signal {ss}. No large formal-response "
                f"cluster detected — but absence of detected replies is weaker "
                f"evidence than presence; still confirm for load-bearing use."
            )
    return profile


def format_for_prompt(profile):
    """Render the profile as a block to paste into the counter-audit's
    reception-gate field for a given source."""
    lines = [
        f"RECEPTION PROFILE (retrieved) — {profile['query']}",
        f"  Resolved: {profile['resolved']}",
        f"  Citations: {profile['citation_count']}",
        f"  Influential citations (S2): {profile['influential_citation_count']}",
        f"  Citing works pulled: {profile['n_citing_pulled']}",
        f"  Formal replies/comments detected: {profile['n_formal_replies']}",
    ]
    if profile["reply_titles"]:
        lines.append("  Reply/comment titles:")
        for t in profile["reply_titles"]:
            lines.append(f"    - {t}")
    lines += [
        f"  Citation-context snippets analyzed: {profile['n_contexts']}",
        f"  Refute-signal / Support-signal: {profile['refute_signal']} / {profile['support_signal']}",
    ]
    if profile["sample_refuting_snippets"]:
        lines.append("  Sample CHALLENGING citation contexts:")
        for s in profile["sample_refuting_snippets"]:
            lines.append(f"    > {s}")
    if profile["sample_supporting_snippets"]:
        lines.append("  Sample SUPPORTING citation contexts:")
        for s in profile["sample_supporting_snippets"]:
            lines.append(f"    > {s}")
    lines += [
        f"  OA PDF: {profile['open_access_pdf']}",
        "",
        f"  >> VERIFICATION STATE: {profile['verification_state']}",
        f"     {profile['verification_state_rationale']}",
        "     FULL-TEXT-CONFIRMED: not established (human read required)",
        "     ABSTRACT-CONFIRMED: not established (requires judging relevance)",
        "",
        f"  >> RECEPTION SIGNAL: {profile['reception_summary']}",
        f"  >> CAVEAT: {profile['caveat']}",
    ]
    return "\n".join(lines)


if __name__ == "__main__":
    import sys
    if len(sys.argv) < 2:
        print("Usage: python citation_reception_module.py \"<paper title or DOI>\"")
        print("Example: python citation_reception_module.py "
              "\"A statistical analysis of multiple temperature proxies\"")
        sys.exit(1)
    q = " ".join(sys.argv[1:])
    prof = build_reception_profile(q)
    print(format_for_prompt(prof))
