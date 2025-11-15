import asyncio
import sys
from pathlib import Path


FIXTURES = Path(__file__).resolve().parent / "fixtures" / "api"


def _patch_db(monkeypatch, tmp_path):
    db_path = tmp_path / "cache.sqlite3"
    monkeypatch.setattr("src.assessor.cache.db._DB_PATH", db_path)
    # Force module reload so imports pick up the patched path
    for mod in list(sys.modules.keys()):
        if mod.startswith("src.assessor.cache") or mod.startswith("src.assessor.fetchers"):
            sys.modules.pop(mod, None)
    return db_path


def test_nvd_offline_uses_fixture(monkeypatch, tmp_path):
    _patch_db(monkeypatch, tmp_path)
    from src.assessor.fetchers import nvd
    
    results = asyncio.run(nvd.fetch_cves("PeaZip", offline=True))
    assert any(item["id"] == "CVE-2021-34527" for item in results)


def test_nvd_snapshot_hits_cache(monkeypatch, tmp_path):
    _patch_db(monkeypatch, tmp_path)
    
    from src.assessor.cache import db as cache_db
    from src.assessor.fetchers import nvd

    raw = (FIXTURES / "nvd_cve_sample.json").read_bytes()
    url = nvd._build_query_url("PeaZip")
    cache_db.upsert_content(url, raw, snapshot_id="snapshot-1")

    async def mock_http_get(*args, **kwargs):
        raise AssertionError("network call not expected")

    monkeypatch.setattr(nvd, "_http_get", mock_http_get)
    results = asyncio.run(nvd.fetch_cves("PeaZip", offline=False, snapshot_id="snapshot-1"))
    assert len(results) > 0


def test_cisa_offline_fixture(monkeypatch, tmp_path):
    _patch_db(monkeypatch, tmp_path)
    from src.assessor.fetchers import cisa_kev
    
    results = asyncio.run(cisa_kev.fetch_cisa_kev(offline=True))
    assert any(entry["id"] == "CVE-2021-34527" for entry in results)


def test_cisa_snapshot_hits_cache(monkeypatch, tmp_path):
    _patch_db(monkeypatch, tmp_path)
    
    from src.assessor.cache import db as cache_db
    from src.assessor.fetchers import cisa_kev

    raw = (FIXTURES / "cisa_kev_sample.json").read_bytes()
    cache_db.upsert_content(cisa_kev._API_URL, raw, snapshot_id="snap-2")

    async def mock_http_get(*args, **kwargs):
        raise AssertionError("network call not expected")

    monkeypatch.setattr(cisa_kev, "_http_get", mock_http_get)
    results = asyncio.run(cisa_kev.fetch_cisa_kev(offline=False, snapshot_id="snap-2"))
    assert len(results) > 0