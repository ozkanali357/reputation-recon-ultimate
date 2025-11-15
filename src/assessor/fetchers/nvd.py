import asyncio
import json
from pathlib import Path
from typing import Any, Dict, List, Optional
from urllib.parse import urlencode

import httpx

from assessor.cache.db import get_cached_content, upsert_content

_API_URL = "https://services.nvd.nist.gov/rest/json/cves/2.0"
_FIXTURE = Path(__file__).resolve().parents[3] / "tests/fixtures/api/nvd_cve_sample.json"
_MAX_RETRIES = 3
_BACKOFF = 0.5
_TIMEOUT = 15.0


def _build_query_url(product: str) -> str:
    params = urlencode({"keywordSearch": product})
    return f"{_API_URL}?{params}"


def _load_fixture() -> Dict[str, Any]:
    return json.loads(_FIXTURE.read_text(encoding="utf-8"))


def _decode_raw(raw: Any) -> Dict[str, Any]:
    if isinstance(raw, (bytes, bytearray, memoryview)):
        raw = bytes(raw)
    return json.loads(raw)


def _normalize_items(payload: Dict[str, Any]) -> List[Dict[str, Any]]:
    items: List[Dict[str, Any]] = []
    for entry in payload.get("CVE_Items", []):
        cve_block = entry.get("cve", {})
        description = ""
        desc_list = cve_block.get("description", {}).get("description_data", [])
        if desc_list:
            description = desc_list[0].get("value", "")

        meta = cve_block.get("CVE_data_meta", {})
        cve_id = meta.get("ID") or cve_block.get("id")

        impact = entry.get("impact", {}).get("baseMetricV3", {})
        references = [
            ref.get("url")
            for ref in cve_block.get("references", {}).get("reference_data", [])
            if ref.get("url")
        ]

        items.append(
            {
                "id": cve_id,
                "description": description,
                "severity": impact.get("severity"),
                "score": impact.get("baseScore"),
                "references": references,
                "published": entry.get("publishedDate") or entry.get("published"),
                "last_modified": entry.get("lastModifiedDate") or entry.get("lastModified"),
            }
        )
    return items


async def _http_get(url: str, params: Dict[str, str]) -> httpx.Response:
    attempt = 0
    while True:
        try:
            async with httpx.AsyncClient(timeout=_TIMEOUT) as client:
                response = await client.get(url, params=params)
            response.raise_for_status()
            return response
        except httpx.HTTPError:
            attempt += 1
            if attempt >= _MAX_RETRIES:
                raise
            await asyncio.sleep(_BACKOFF * attempt)


async def fetch_cves(
    product: str,
    offline: bool = False,
    snapshot_id: Optional[str] = None,
) -> List[Dict[str, Any]]:
    query_url = _build_query_url(product)
    
    if offline or snapshot_id:
        cached = get_cached_content(query_url, snapshot_id=snapshot_id)
        if cached:
            payload = _decode_raw(cached["raw"])
            return _normalize_items(payload)
    
    if offline:
        return _normalize_items(_load_fixture())
    
    response = await _http_get(_API_URL, {"keywordSearch": product})
    payload = response.json()
    upsert_content(query_url, response.content, snapshot_id=snapshot_id)
    return _normalize_items(payload)

def fetch_cves_sync(
    product: str,
    offline: bool = False,
    snapshot_id: Optional[str] = None,
) -> List[Dict[str, Any]]:
    return asyncio.run(fetch_cves(product, offline=offline, snapshot_id=snapshot_id))