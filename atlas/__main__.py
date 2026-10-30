"""Run with python -m atlas. Exit 1 means retained, quarantined native output."""

import argparse
from pathlib import Path
import sys

from .adapter import build
from .contract import ContractError, canonical, load_json, sha256
from .integrity import verify_records
from .ledger import append, export, read_export


def write_once(path: Path, data: bytes):
    try:
        with path.open("xb") as file:
            file.write(data)
    except FileExistsError:
        if path.read_bytes() != data:
            raise ContractError(f"ID_CONTENT_CONFLICT: output {path}")


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="command", required=True)
    imp = sub.add_parser("import", help="import a pinned native audit; no retrieval")
    imp.add_argument("context", type=Path)
    imp.add_argument("--root", type=Path, default=Path.cwd())
    imp.add_argument("--out", type=Path, required=True)
    imp.add_argument("--ledger", type=Path)
    exp = sub.add_parser("export", help="canonical JSONL from local ledger")
    exp.add_argument("ledger", type=Path)
    exp.add_argument("out", type=Path)
    restore = sub.add_parser("restore", help="restore a complete portable JSONL bundle")
    restore.add_argument("jsonl", type=Path)
    restore.add_argument("ledger", type=Path)
    replay = sub.add_parser("replay", help="recompute import from manifest and exact local inputs")
    replay.add_argument("manifest", type=Path)
    replay.add_argument("jsonl", type=Path)
    replay.add_argument("--root", type=Path, default=Path.cwd())
    args = parser.parse_args(argv)
    try:
        if args.command == "import":
            bundle = build(load_json(args.context.read_bytes()), args.root.resolve())
            args.out.mkdir(parents=True, exist_ok=True)
            files = {"records.jsonl": bundle["jsonl"],
                     "manifest.json": (canonical(bundle["manifest"]) + "\n").encode("utf-8"),
                     "SHA256SUMS": (bundle["jsonl_sha256"] + "  records.jsonl\n").encode("ascii")}
            # Preflight every destination before a conflicting rerun writes anything.
            for name, data in files.items():
                path = args.out / name
                if path.exists() and path.read_bytes() != data:
                    raise ContractError(f"ID_CONTENT_CONFLICT: output {path}")
            if args.ledger:
                append(args.ledger, bundle["records"])
            for name, data in files.items():
                write_once(args.out / name, data)
            print(canonical({"syntax": bundle["syntax"], "checker": bundle["checker_status"],
                             "records": len(bundle["records"]), "sha256": bundle["jsonl_sha256"],
                             "scientific_validation": "NOT_PERFORMED"}))
            return 1 if bundle["syntax"] == "FAIL" else 0
        if args.command == "export":
            write_once(args.out, export(args.ledger))
        elif args.command == "restore":
            records = read_export(args.jsonl.read_bytes())
            print(canonical({"inserted": append(args.ledger, records), **verify_records(records)}))
        else:
            manifest = load_json(args.manifest.read_bytes())
            bundle = build(manifest["input_context"], args.root.resolve())
            if bundle["manifest"] != manifest or bundle["jsonl"] != args.jsonl.read_bytes():
                raise ContractError("REPLAY_MISMATCH: inputs, code, environment or records differ")
            print("PASS: deterministic import replay; historical model run not reproduced")
        return 0
    except (ContractError, OSError, UnicodeError, KeyError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
