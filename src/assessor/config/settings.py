# settings.py

# Configuration settings for the application

class Config:
    DEBUG = False
    TESTING = False
    DATABASE_URI = 'sqlite:///cache.db'
    CACHE_TYPE = 'simple'
    CACHE_DEFAULT_TIMEOUT = 300
    TIMEOUT = 10
    RETRIES = 3
    RATE_LIMIT = '100/hour'
    EVIDENCE_CACHE_TTL = 86400  # 1 day
    SNAPSHOT_MODE = False

class DevelopmentConfig(Config):
    DEBUG = True
    DATABASE_URI = 'sqlite:///dev_cache.db'

class TestingConfig(Config):
    TESTING = True
    DATABASE_URI = 'sqlite:///test_cache.db'

class ProductionConfig(Config):
    DATABASE_URI = 'sqlite:///prod_cache.db'