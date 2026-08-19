"""
Database connection setup.

Defaults to a local SQLite file so the API runs with zero external
setup. Point DATABASE_URL at Postgres in production, e.g.:

    export DATABASE_URL="postgresql://user:password@localhost:5432/askajji"

No other code needs to change — SQLAlchemy abstracts the dialect.
"""
import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./askajji.db")

connect_args = {"check_same_thread": False} if DATABASE_URL.startswith("sqlite") else {}
engine = create_engine(DATABASE_URL, connect_args=connect_args)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


def get_db():
    """FastAPI dependency: yields a DB session and always closes it."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
