import json
from datetime import datetime
from pathlib import Path
from typing import Optional

from .db import get_connection

_SNAPSHOT_META = Path(__file__).resolve().parent / "snapshot.json"


def current_snapshot() -> Optional[str]:
    if not _SNAPSHOT_META.exists():
        return None
    data = json.loads(_SNAPSHOT_META.read_text(encoding="utf-8"))
    return data.get("snapshot_id")


def create_snapshot(snapshot_id: str, dependency_lock: dict) -> None:
    payload = {
        "snapshot_id": snapshot_id,
        "created_at": datetime.utcnow().isoformat(),
        "dependency_lock": dependency_lock,
    }
    _SNAPSHOT_META.write_text(json.dumps(payload, indent=2), encoding="utf-8")

    with get_connection() as conn:
        conn.execute(
            """
            INSERT INTO snapshots (snapshot_id, created_at, dependency_lock)
            VALUES (?, ?, ?)
            ON CONFLICT(snapshot_id) DO NOTHING
            """,
            (snapshot_id, payload["created_at"], json.dumps(dependency_lock)),
        )