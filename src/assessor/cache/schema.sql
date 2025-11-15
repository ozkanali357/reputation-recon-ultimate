CREATE TABLE content (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    url TEXT NOT NULL,
    sha256 TEXT NOT NULL,
    retrieved_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE facts (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    content_id INTEGER NOT NULL,
    claim_id INTEGER NOT NULL,
    FOREIGN KEY (content_id) REFERENCES content(id),
    FOREIGN KEY (claim_id) REFERENCES claims(id)
);

CREATE TABLE claims (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    product_id INTEGER NOT NULL,
    category TEXT NOT NULL,
    text TEXT NOT NULL,
    score_contrib REAL NOT NULL,
    confidence REAL NOT NULL
);

CREATE TABLE evidence (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    claim_id INTEGER NOT NULL,
    url TEXT NOT NULL,
    source_type TEXT NOT NULL,
    excerpt TEXT NOT NULL,
    retrieved_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    parser_id INTEGER NOT NULL,
    FOREIGN KEY (claim_id) REFERENCES claims(id)
);

CREATE TABLE cve_stats (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    year_bins TEXT NOT NULL,
    open_count INTEGER NOT NULL,
    critical_count INTEGER NOT NULL,
    last_seen TIMESTAMP NOT NULL,
    kev_hits INTEGER NOT NULL
);

CREATE TABLE snapshots (
    snapshot_id INTEGER PRIMARY KEY AUTOINCREMENT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    dependency_lock TEXT NOT NULL
);