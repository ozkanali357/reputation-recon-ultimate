from sqlalchemy import create_engine, Column, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os

Base = declarative_base()

class CacheEntry(Base):
    __tablename__ = 'cache'

    id = Column(Integer, primary_key=True)
    url = Column(String, unique=True, nullable=False)
    sha256 = Column(String, nullable=False)
    retrieved_at = Column(DateTime, nullable=False)

DATABASE_URL = os.getenv('DATABASE_URL', 'sqlite:///cache.db')

engine = create_engine(DATABASE_URL)
Base.metadata.create_all(engine)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()