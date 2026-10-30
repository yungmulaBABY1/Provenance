"""Local transactional append-only record store; JSONL is the interchange format.

SQLite serializes concurrent local writers. This is not a hosted multi-user
service, tamper-proof archive, authentication system or public release gate.
"""

from pathlib import Path
import sqlite3

from .contract import ContractError, canonical, jsonl, load_json, sha256, validate_records
from .integrity import verify_records


def connect(path: Path):
    db = sqlite3.connect(path, timeout=30)
    db.execute("PRAGMA foreign_keys=ON")
    db.execute("CREATE TABLE IF NOT EXISTS records (id TEXT PRIMARY KEY, payload TEXT NOT NULL, sha256 TEXT NOT NULL)")
    db.execute("CREATE TRIGGER IF NOT EXISTS no_record_update BEFORE UPDATE ON records BEGIN SELECT RAISE(ABORT, 'APPEND_ONLY'); END")
    db.execute("CREATE TRIGGER IF NOT EXISTS no_record_delete BEFORE DELETE ON records BEGIN SELECT RAISE(ABORT, 'APPEND_ONLY'); END")
    db.commit()
    return db


def append(path: Path, records: list[dict]) -> int:
    validate_records(records)
    db = connect(path)
    try:
        db.execute("BEGIN IMMEDIATE")
        inserted = 0
        for rec in sorted(records, key=lambda r: r["id"]):
            payload = canonical(rec)
            checksum = sha256(payload.encode("utf-8"))
            old = db.execute("SELECT payload, sha256 FROM records WHERE id=?", (rec["id"],)).fetchone()
            if old:
                if old != (payload, checksum):
                    raise ContractError(f"ID_CONTENT_CONFLICT: {rec['id']}")
            else:
                db.execute("INSERT INTO records VALUES (?, ?, ?)", (rec["id"], payload, checksum))
                inserted += 1
        # Inside the transaction: any integrity failure rolls back every insert.
        verify_records(records)
        db.commit()
        return inserted
    except BaseException:
        db.rollback()
        raise
    finally:
        db.close()


def export(path: Path) -> bytes:
    if not path.is_file():
        raise ContractError("LEDGER_NOT_FOUND")
    db = connect(path)
    try:
        rows = db.execute("SELECT id, payload, sha256 FROM records ORDER BY id").fetchall()
        records = []
        for id, payload, checksum in rows:
            if sha256(payload.encode("utf-8")) != checksum:
                raise ContractError(f"LEDGER_HASH_MISMATCH: {id}")
            obj = load_json(payload.encode("utf-8"))
            if obj["id"] != id or canonical(obj) != payload:
                raise ContractError(f"LEDGER_CONTENT_MISMATCH: {id}")
            records.append(obj)
        if not records:
            return b""
        verify_records(records)
        return jsonl(records)
    finally:
        db.close()


def read_export(data: bytes) -> list[dict]:
    records = [load_json(line) for line in data.splitlines() if line.strip()]
    validate_records(records)
    verify_records(records)
    return records
