import asyncio
import json
from pathlib import Path
from typing import Any, Dict, List, Optional

import httpx

from assessor.cache.db import get_cached_content, upsert_content

_API_URL = "https://www.cisa.gov/sites/default/files/feeds/known_exploited_vulnerabilities.json"
_FIXTURE = Path(__file__).resolve().parents[3] / "tests/fixtures/api/cisa_kev_sample.json"
_MAX_RETRIES = 3
_BACKOFF = 0.5
_TIMEOUT = 15.0


def _load_fixture() -> Dict[str, Any]:
    return json.loads(_FIXTURE.read_text(encoding="utf-8"))


def _decode_raw(raw: Any) -> Dict[str, Any]:
    if isinstance(raw, (bytes, bytearray, memoryview)):
        raw = bytes(raw)
    return json.loads(raw)


def _normalize(payload: Dict[str, Any]) -> List[Dict[str, Any]]:
    kev_entries = payload.get("cisa_kev") or payload.get("vulnerabilities") or []
    normalized: List[Dict[str, Any]] = []
    for item in kev_entries:
        normalized.append(
            {
                "id": item.get("id") or item.get("cveID"),
                "name": item.get("name"),
                "description": item.get("description"),
                "cvss": item.get("cvss", {}),
                "published": item.get("publishedDate") or item.get("dateAdded"),
                "last_modified": item.get("lastModifiedDate") or item.get("dueDate"),
                "references": item.get("references", []),
            }
        )
    return normalized


async def _http_get(url: str) -> httpx.Response:
    attempt = 0
    while True:
        try:
            async with httpx.AsyncClient(timeout=_TIMEOUT) as client:
                response = await client.get(url)
            response.raise_for_status()
            return response
        except httpx.HTTPError:
            attempt += 1
            if attempt >= _MAX_RETRIES:
                raise
            await asyncio.sleep(_BACKOFF * attempt)


async def fetch_cisa_kev(
    offline: bool = False,
    snapshot_id: Optional[str] = None,
) -> List[Dict[str, Any]]:
    cached = None
    if offline or snapshot_id:
        cached = get_cached_content(_API_URL, snapshot_id=snapshot_id)

    if cached:
        payload = _decode_raw(cached["raw"])
        return _normalize(payload)

    if offline:
        return _normalize(_load_fixture())

    response = await _http_get(_API_URL)
    payload = response.json()
    upsert_content(_API_URL, response.content, snapshot_id=snapshot_id)
    return _normalize(payload)


def fetch_cisa_kev_sync(
    offline: bool = False,
    snapshot_id: Optional[str] = None,
) -> List[Dict[str, Any]]:
    return asyncio.run(fetch_cisa_kev(offline=offline, snapshot_id=snapshot_id))