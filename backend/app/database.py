"""
Database engine, session factory, and declarative Base.
Every module imports Base and get_db from here.
"""

from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

from app.config import settings

# ── Engine ──────────────────────────────────────────────────────────
engine = create_engine(
    settings.DATABASE_URL,
    pool_pre_ping=True,       # reconnect stale connections
    pool_size=10,
    max_overflow=20,
)

# ── Session factory ─────────────────────────────────────────────────
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
)

# ── Declarative Base ────────────────────────────────────────────────
Base = declarative_base()


# ── Dependency for FastAPI routes ───────────────────────────────────
def get_db():
    """Yield a DB session per request, auto-close on exit."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
