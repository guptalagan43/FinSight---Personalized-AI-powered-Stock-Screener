"""
FinSight – Models package.
Provides shared database cursor helper with optional psycopg2 support.
When psycopg2 is not available, models fall back to the in-memory store.
"""
from flask import g

# Conditional psycopg2 import
try:
    import psycopg2.extras
    _HAS_PSYCOPG2 = True
except ImportError:
    _HAS_PSYCOPG2 = False


def get_cursor():
    """Return a RealDictCursor for the current Flask request."""
    if not _HAS_PSYCOPG2:
        raise RuntimeError("psycopg2 is not installed - database features unavailable")
    return g.db.cursor(cursor_factory=psycopg2.extras.RealDictCursor)


def use_db():
    """Return True if PostgreSQL is available and should be used."""
    return _HAS_PSYCOPG2
