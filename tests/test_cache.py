from src.assessor.cache.db import get_cached_content, upsert_content

def test_cache_roundtrip(tmp_path, monkeypatch):
    db_file = tmp_path / "cache.sqlite3"
    monkeypatch.setattr("src.assessor.cache.db._DB_PATH", db_file)

    content_id = upsert_content("https://example.com", b"payload")
    cached = get_cached_content("https://example.com")
    assert cached is not None
    assert cached["id"] == content_id