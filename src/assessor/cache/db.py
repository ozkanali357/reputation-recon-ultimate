import hashlib
import json
import sqlite3
from contextlib import contextmanager
from pathlib import Path
from typing import Any, Dict, Optional

_DB_PATH = Path(__file__).resolve().parent / "cache.sqlite3"
_SCHEMA_PATH = Path(__file__).resolve().parent / "schema.sql"


def _ensure_schema(conn: sqlite3.Connection) -> None:
    with _SCHEMA_PATH.open("r", encoding="utf-8") as handle:
        conn.executescript(handle.read())


@contextmanager
def get_connection(readonly: bool = False):
    if readonly:
        uri = f"file:{_DB_PATH}?mode=ro"
        conn = sqlite3.connect(uri, uri=True)
    else:
        conn = sqlite3.connect(_DB_PATH)

    conn.row_factory = sqlite3.Row

    if not readonly:
        _ensure_schema(conn)

    try:
        yield conn
    finally:
        conn.commit()
        conn.close()


def _sha256(content: bytes) -> str:
    return hashlib.sha256(content).hexdigest()


def upsert_content(url: str, raw: bytes, snapshot_id: Optional[str] = None) -> int:
    sha256 = _sha256(raw)
    with get_connection() as conn:
        conn.execute(
            """
            INSERT INTO content (url, sha256, retrieved_at, snapshot_id, raw)
            VALUES (?, ?, datetime('now'), ?, ?)
            ON CONFLICT(url) DO UPDATE SET
                sha256=excluded.sha256,
                retrieved_at=datetime('now'),
                snapshot_id=excluded.snapshot_id,
                raw=excluded.raw
            """,
            (url, sha256, snapshot_id, raw),
        )
        row = conn.execute("SELECT id FROM content WHERE url = ?", (url,)).fetchone()
        return row["id"]


def get_cached_content(
    url: str,
    max_age_seconds: Optional[int] = None,
    snapshot_id: Optional[str] = None,
) -> Optional[Dict[str, Any]]:
    if not _DB_PATH.exists():
        return None
    query = "SELECT * FROM content WHERE url = ?"
    params = [url]

    if snapshot_id:
        query += " AND snapshot_id = ?"
        params.append(snapshot_id)

    with get_connection(readonly=True) as conn:
        row = conn.execute(query, params).fetchone()
        if not row:
            return None

        if max_age_seconds is not None:
            age = conn.execute(
                "SELECT strftime('%s','now') - strftime('%s', ?)",
                (row["retrieved_at"],),
            ).fetchone()[0]
            if age > max_age_seconds:
                return None

        return dict(row)


def record_fact(
    content_id: int,
    claim: str,
    parser_id: str,
    source_type: str,
    payload: Dict[str, Any],
    snapshot_id: Optional[str] = None,
) -> int:
    with get_connection() as conn:
        cur = conn.execute(
            """
            INSERT INTO facts (content_id, claim, parser_id, source_type, payload, snapshot_id)
            VALUES (?, ?, ?, ?, ?, ?)
            """,
            (content_id, claim, parser_id, source_type, json.dumps(payload), snapshot_id),
        )
        return cur.lastrowid