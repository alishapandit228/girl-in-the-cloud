"""Single transactional boundary. SQLite local development or SQLAlchemy/PostgreSQL."""
import os
import sqlite3
from contextlib import contextmanager
from functools import lru_cache

SCHEMA = [
    "CREATE TABLE IF NOT EXISTS sessions (token TEXT PRIMARY KEY, expires BIGINT NOT NULL)",
    "CREATE TABLE IF NOT EXISTS limits (bucket TEXT PRIMARY KEY, hits INTEGER NOT NULL, expires BIGINT NOT NULL)",
    "CREATE TABLE IF NOT EXISTS events (day TEXT NOT NULL, visitor TEXT NOT NULL, kind TEXT NOT NULL, path TEXT NOT NULL, device TEXT NOT NULL, referrer TEXT NOT NULL)",
    "CREATE INDEX IF NOT EXISTS events_day ON events(day)",
    "CREATE TABLE IF NOT EXISTS contacts (id TEXT PRIMARY KEY, created BIGINT NOT NULL, state TEXT NOT NULL)",
]

@lru_cache
def engine():
    from sqlalchemy import create_engine
    return create_engine(os.environ["DATABASE_URL"], pool_pre_ping=True)

@contextmanager
def transaction():
    if os.getenv("DATABASE_URL"):
        from sqlalchemy import text
        with engine().begin() as connection:
            yield lambda sql, **params: connection.execute(text(sql), params)
    else:
        connection = sqlite3.connect(os.getenv("LOCAL_DB", "portfolio.sqlite"), timeout=8)
        try:
            with connection:
                yield lambda sql, **params: connection.execute(sql,params)
        finally:
            connection.close()

def init():
    if not os.getenv("DATABASE_URL"):
        with transaction() as run:
            for sql in SCHEMA:
                run(sql)
