"""Build or re-verify the bounded power-posing source packet. Needs network and poppler.

    python tests/atlas/sources/power-posing/source_packet.py verify
    python tests/atlas/sources/power-posing/source_packet.py build

verify (default): downloads each retrievable source again, checks its SHA-256,
re-runs the pinned extraction, and checks that every recorded excerpt is the
exact text at its recorded offsets and that the committed excerpt files match.
build: records a new retrieval and rewrites SOURCES.json and the excerpt files.

This is provenance tooling for the fixture, not part of the adapter runtime and
not run in CI. The adapter reads only the committed excerpt files.
"""

import datetime
import hashlib
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import urllib.error
import urllib.request

HERE = Path(__file__).resolve().parent
SOURCES = HERE / "SOURCES.json"
REVIEWS = HERE.parent.parent / "reviews" / "power-posing"
EXTRACTION = ["pdftotext", "-enc", "UTF-8"]  # default reading-order mode, no -layout

# Packet sources (compliance/PACKET.md). Excerpts are located by exact start and
# end strings, each required to occur once in the extraction output.
SPEC = {
    "S1": {"doi": "10.1177/0956797610383437",
           "url": "https://journals.sagepub.com/stoken/rbtfl/4zEmVxPysrEHI/full", "excerpts": []},
    "S2": {"doi": "10.1177/0956797614553946",
           "url": "https://faculty.haas.berkeley.edu/dana_carney/ranehill.pdf",
           "excerpts": [
               ("S2-E1", "metadata", "Journal, volume, pages and DOI printed on the article",
                "Psychological Science\n2015, Vol. 26(5)", "DOI: 10.1177/0956797614553946"),
               ("S2-E2", "section", "Opening summary of the study's results (before Method)",
                "Consistent with the findings of Carney et al., our", "in any of the three behavioral tasks."),
               ("S2-E3", "section", "Discussion, first paragraph: results restated",
                "Using a much\nlarger sample size", "this did not yield behavioral effects."),
           ]},
    "S3": {"doi": "10.1177/0956797614566855",
           "url": "https://www.researchgate.net/publication/274458966_Review_and_Summary_of_Research_on_the_Embodied_Effects_of_Expansive_vs_Contractive_Nonverbal_Displays",
           "excerpts": []},
    "S4": {"doi": "10.1177/0956797616658563",
           "url": "https://faculty.haas.berkeley.edu/dana_carney/Simmons.Simonsoh.p-curve-evidence.pdf",
           "excerpts": [
               ("S4-E1", "metadata", "Title, authors and publication status printed on the manuscript",
                "Power Posing: P-Curving the Evidence\nJoseph P. Simmons", "Forthcoming in Psychological Science"),
               ("S4-E2", "section", "Introduction: S4's description of S3 (Carney et al., 2015); S4's words, not S3's",
                "In their response to the failed replication", "future studies could explore."),
               ("S4-E3", "section", "Introduction: question and stated conclusion",
                "In this paper we rely on p-curve analysis", "reporting? We conclude not."),
               ("S4-E4", "section", "Results: test for evidential value",
                "We first evaluated if evidential value was present.", "pfull=.63,\nrespectively)."),
           ]},
}


def sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def fetch(url: str) -> dict:
    # Plain request with urllib's default identity; no attempt to pass bot checks.
    try:
        with urllib.request.urlopen(url, timeout=60) as response:
            return {"status": response.status, "final_url": response.geturl(),
                    "content_type": response.headers.get("Content-Type"), "data": response.read()}
    except urllib.error.HTTPError as exc:
        return {"status": exc.code, "final_url": url,
                "content_type": exc.headers.get("Content-Type"), "data": None}


def poppler_version() -> str:
    try:
        out = subprocess.run(["pdftotext", "-v"], capture_output=True, text=True)
    except FileNotFoundError:
        return "pdftotext not found"
    return (out.stdout + out.stderr).splitlines()[0].strip()


def extract(pdf: bytes, first=None, last=None) -> str:
    with tempfile.TemporaryDirectory() as directory:
        path = Path(directory, "source.pdf")
        path.write_bytes(pdf)
        pages = ["-f", str(first), "-l", str(last)] if first else []
        subprocess.run([*EXTRACTION, *pages, str(path), str(Path(directory, "out.txt"))], check=True)
        return Path(directory, "out.txt").read_bytes().decode("utf-8")


def page_count(pdf: bytes) -> int:
    with tempfile.TemporaryDirectory() as directory:
        path = Path(directory, "source.pdf")
        path.write_bytes(pdf)
        info = subprocess.run(["pdfinfo", str(path)], capture_output=True, text=True, check=True).stdout
    return int(next(line.split()[-1] for line in info.splitlines() if line.startswith("Pages:")))


def locate(text: str, start: str, end: str) -> tuple[int, int]:
    if text.count(start) != 1:
        raise SystemExit(f"start marker occurs {text.count(start)} times: {start!r}")
    begin = text.index(start)
    stop = text.index(end, begin) + len(end)
    return begin, stop


def excerpt_file(source_id: str, record: dict) -> tuple[str, list[dict]]:
    lines = [f"Bounded excerpts from {source_id}: {record['citation']}",
             f"DOI {record['doi']}. Retrieved copy: {record['retrieval']['final_url']}",
             f"Retrieved {record['retrieval']['retrieved_at']}; PDF SHA-256 {record['retrieval']['sha256']}.",
             "Not the full paper. Each excerpt is an exact substring of the pinned extraction",
             "output; its offsets there are recorded in SOURCES.json. Provenance tooling:",
             "source_packet.py in this directory.", ""]
    text = "\n".join(lines) + "\n"
    components = []
    for excerpt in record["excerpts"]:
        text += f"=== {excerpt['id']} | {excerpt['kind']} | PDF page {excerpt['pdf_page']} ===\n"
        start = len(text)
        text += excerpt["text"]
        components.append({"id": excerpt["id"], "kind": excerpt["kind"], "start": start, "end": len(text)})
        text += f"\n=== end {excerpt['id']} ===\n\n"
    return text, components


def build(stamp: str) -> None:
    version = poppler_version()
    sources = {}
    for source_id, spec in SPEC.items():
        got = fetch(spec["url"])
        retrieval = {"requested_url": spec["url"], "final_url": got["final_url"], "retrieved_at": stamp,
                     "http_status": got["status"], "content_type": got["content_type"]}
        record = {"doi": spec["doi"], "retrieval": retrieval, "excerpts": []}
        if got["status"] != 200 or not got["data"] or not got["data"].startswith(b"%PDF"):
            retrieval["outcome"] = "RETRIEVAL_FAILED"
            sources[source_id] = record
            continue
        pdf = got["data"]
        text = extract(pdf)
        pages = page_count(pdf)
        retrieval.update(outcome="AVAILABLE", bytes=len(pdf), sha256=sha256(pdf), pdf_pages=pages)
        record["extraction"] = {"tool": version, "command": [*EXTRACTION, "<pdf>", "<out>"],
                                "output_sha256": sha256(text.encode("utf-8")),
                                "output_characters": len(text)}
        page_texts = {n: extract(pdf, n, n) for n in range(1, pages + 1)}
        for excerpt_id, kind, label, start, end in spec["excerpts"]:
            begin, stop = locate(text, start, end)
            quote = text[begin:stop]
            on = [n for n, page in page_texts.items() if quote in page]
            record["excerpts"].append({"id": excerpt_id, "kind": kind, "label": label,
                                       "pdf_page": on[0] if len(on) == 1 else None,
                                       "extraction_start": begin, "extraction_end": stop,
                                       "occurrences_in_extraction": text.count(quote),
                                       "sha256": sha256(quote.encode("utf-8")), "text": quote})
        sources[source_id] = record
    previous = json.loads(SOURCES.read_text()) if SOURCES.exists() else {}
    for source_id, record in sources.items():
        record.update({k: v for k, v in previous.get("sources", {}).get(source_id, {}).items()
                       if k in {"citation", "version", "sections_accessible", "notes"}})
        record.setdefault("citation", "")
    SOURCES.write_text(json.dumps({"packet": "compliance/PACKET.md", "sources": sources},
                                  indent=2, ensure_ascii=False) + "\n")
    write_excerpt_files()


def write_excerpt_files() -> None:
    data = json.loads(SOURCES.read_text())
    for source_id, record in data["sources"].items():
        if record["excerpts"]:
            text, _ = excerpt_file(source_id, record)
            (HERE / f"{source_id}-excerpts.txt").write_text(text, encoding="utf-8")


def verify(sources=None, directory=None, fetcher=None, extractor=None, reviews=None) -> int:
    """Return 0 only if every retrieved source, its whole extraction and every excerpt match.

    The keyword arguments let the offline regression test supply sources and an
    extractor without network access or poppler.
    """
    sources, directory, reviews = sources or SOURCES, directory or HERE, reviews or REVIEWS
    fetcher, extractor = fetcher or fetch, extractor or extract
    data = json.loads(sources.read_text())
    failures = 0
    texts = {}
    print(f"extraction tool here: {poppler_version()}")
    for source_id, record in data["sources"].items():
        retrieval = record["retrieval"]
        got = fetcher(retrieval["requested_url"])
        if retrieval["outcome"] != "AVAILABLE":
            print(f"{source_id}: recorded {retrieval['outcome']} (HTTP {retrieval['http_status']}); "
                  f"now HTTP {got['status']}")
            continue
        if got["status"] != 200 or sha256(got["data"] or b"") != retrieval["sha256"]:
            print(f"{source_id}: FAIL source bytes differ or unavailable (HTTP {got['status']})")
            failures += 1
            continue
        text = extractor(got["data"])
        same = sha256(text.encode("utf-8")) == record["extraction"]["output_sha256"]
        print(f"{source_id}: PDF SHA-256 OK; extraction output {'identical' if same else 'FAIL differs'}")
        # A changed extraction fails even when every excerpt still matches: the
        # recorded offsets and sections describe the whole recorded output.
        failures += not same
        texts[record["doi"]] = text
        for excerpt in record["excerpts"]:
            at = text[excerpt["extraction_start"]:excerpt["extraction_end"]]
            ok = at == excerpt["text"] and sha256(at.encode("utf-8")) == excerpt["sha256"]
            print(f"  {excerpt['id']}: {'OK' if ok else 'FAIL'} at recorded offsets")
            failures += not ok
        expected, _ = excerpt_file(source_id, record)
        committed = (directory / f"{source_id}-excerpts.txt").read_text(encoding="utf-8")
        print(f"  {source_id}-excerpts.txt: {'matches' if committed == expected else 'FAIL differs'}")
        failures += committed != expected
    # Review locators (atlas-evidence-review/1) cite the same pinned extraction.
    for path in sorted(reviews.glob("*.json")) if reviews.is_dir() else []:
        review = json.loads(path.read_text(encoding="utf-8"))
        doi = review["target"]["source_version_id"].split("doi:", 1)[1].split("/version/")[0]
        if doi not in texts:
            print(f"{path.name}: FAIL no verified extraction for {doi}")
            failures += 1
            continue
        bad = [loc["id"] for loc in review["locators"]
               if texts[doi][loc["extraction_start"]:loc["extraction_end"]] != loc["quote"]
               or sha256(loc["quote"].encode("utf-8")) != loc["quote_sha256"]]
        print(f"{path.name}: {len(review['locators']) - len(bad)}/{len(review['locators'])} locators OK"
              + (f"; FAIL {', '.join(bad)}" if bad else ""))
        failures += bool(bad)
    return 1 if failures else 0


if __name__ == "__main__":
    mode = sys.argv[1] if len(sys.argv) > 1 else "verify"
    if mode == "build":
        build(datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"))
    elif mode == "verify":
        raise SystemExit(verify())
    else:
        raise SystemExit(__doc__)
