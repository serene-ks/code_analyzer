"""
Database Configuration
========================
Uses SQLite locally. Switch DATABASE_URL in .env for PostgreSQL/MySQL in production.
"""

import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from dotenv import load_dotenv

load_dotenv()

# Default: SQLite (local dev). Change to PostgreSQL for production:
# DATABASE_URL = "postgresql://user:password@localhost:5432/code_analyzer"
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./code_analyzer.db")

# connect_args only needed for SQLite (allows multiple threads)
connect_args = {"check_same_thread": False} if DATABASE_URL.startswith("sqlite") else {}

engine = create_engine(DATABASE_URL, connect_args=connect_args)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


# ─────────────────────────────────────────────
# Dependency: get DB session (used in routes)
# ─────────────────────────────────────────────
def get_db():
    """
    FastAPI dependency that yields a DB session per request.
    Always closes session after request ends.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
