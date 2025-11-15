DROP TABLE IF EXISTS facts;
DROP TABLE IF EXISTS content;
DROP TABLE IF EXISTS snapshots;

CREATE TABLE snapshots (
    snapshot_id TEXT PRIMARY KEY,
    created_at TEXT NOT NULL,
    dependency_lock TEXT NOT NULL
);

CREATE TABLE content (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    url TEXT NOT NULL UNIQUE,
    sha256 TEXT NOT NULL,
    retrieved_at TEXT NOT NULL,
    snapshot_id TEXT,
    raw BLOB NOT NULL,
    FOREIGN KEY (snapshot_id) REFERENCES snapshots(snapshot_id)
);

CREATE TABLE facts (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    content_id INTEGER NOT NULL,
    claim TEXT NOT NULL,
    parser_id TEXT NOT NULL,
    source_type TEXT NOT NULL,
    payload TEXT NOT NULL,
    snapshot_id TEXT,
    FOREIGN KEY (content_id) REFERENCES content(id),
    FOREIGN KEY (snapshot_id) REFERENCES snapshots(snapshot_id)
);