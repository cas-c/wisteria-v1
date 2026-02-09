"""Test fixtures — shared setup for all backend tests.

**How async testing works with FastAPI + SQLAlchemy:**

1. Tests insert data via `db_session` — a dedicated session for test setup.
2. The HTTP client's requests go through FastAPI, which calls `get_db` to
   get a session. We override `get_db` to use our test session factory
   (same DB, fresh session per request).
3. `httpx.AsyncClient` speaks ASGI directly to the FastAPI app — no real
   HTTP server needed.

**Key gotcha: event loop + connection pool.**
asyncpg connections are bound to the event loop they were created on.
pytest-asyncio creates a new loop per test (in function scope mode).
Using `NullPool` avoids keeping connections across loops — each query
creates and destroys its own connection. Slower but correct for tests.

**Dedicated test database:**
Tests run against `wisteria_test`, not the dev `wisteria` DB. This means:
- Seed data in dev is never touched by tests
- Tests can TRUNCATE freely without destroying your working data
- The test DB is auto-created on first run (see `_ensure_test_db_exists`)
"""

from collections.abc import AsyncGenerator

import pytest
from httpx import ASGITransport, AsyncClient
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.pool import NullPool

from app.config import settings
from app.database import get_db
from app.main import app
from app.models.base import Base


def _ensure_test_db_exists() -> None:
    """Create the wisteria_test database if it doesn't exist.

    This uses a SYNC connection to the default `postgres` database.
    Why sync? We only run this once at import time, before any async
    event loop exists. Trying to use async here would require creating
    and managing a loop manually — not worth the complexity for a
    one-shot DDL statement.

    The `AUTOCOMMIT` isolation level is required because CREATE DATABASE
    cannot run inside a transaction block in Postgres.
    """
    from sqlalchemy import create_engine

    # Swap asyncpg → psycopg2 (sync driver) and target the default `postgres` DB.
    # The `postgres` database always exists — it's the bootstrap DB.
    sync_url = settings.test_database_url.replace(
        "+asyncpg", ""
    ).rsplit("/", 1)[0] + "/postgres"

    engine = create_engine(sync_url, isolation_level="AUTOCOMMIT")
    with engine.connect() as conn:
        result = conn.execute(
            text("SELECT 1 FROM pg_database WHERE datname = 'wisteria_test'")
        )
        if not result.scalar():
            conn.execute(text("CREATE DATABASE wisteria_test"))
    engine.dispose()


_ensure_test_db_exists()

# NullPool is critical for tests: it creates a fresh connection per operation
# and closes it immediately. This avoids "Future attached to a different loop"
# errors that happen when pooled connections cross event loop boundaries.
test_engine = create_async_engine(
    settings.test_database_url,
    echo=False,
    poolclass=NullPool,
)
test_session_factory = async_sessionmaker(
    test_engine,
    class_=AsyncSession,
    expire_on_commit=False,
)

_tables_created = False


@pytest.fixture(autouse=True)
async def setup_db() -> AsyncGenerator[None, None]:
    """Ensure tables exist and are empty before each test."""
    global _tables_created
    if not _tables_created:
        async with test_engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)
        _tables_created = True

    # Truncate before AND after each test. The "before" handles stale data
    # from the seed script or a previous test run that didn't clean up.
    async with test_engine.begin() as conn:
        table_names = ", ".join(Base.metadata.tables.keys())
        if table_names:
            await conn.execute(text(f"TRUNCATE {table_names} CASCADE"))
    yield
    async with test_engine.begin() as conn:
        table_names = ", ".join(Base.metadata.tables.keys())
        if table_names:
            await conn.execute(text(f"TRUNCATE {table_names} CASCADE"))


@pytest.fixture
async def db_session() -> AsyncGenerator[AsyncSession, None]:
    """Session for test setup (inserting test data).

    This is a SEPARATE session from what the route handlers use.
    After committing data here, it's visible to other sessions
    (route handlers) via normal Postgres transaction isolation.
    """
    async with test_session_factory() as session:
        yield session


@pytest.fixture
async def client() -> AsyncGenerator[AsyncClient, None]:
    """Async HTTP client with test DB injected.

    Each route handler call gets its OWN session from `test_session_factory`.
    This avoids asyncpg InterfaceError from concurrent operations on a single
    connection.
    """

    async def override_get_db() -> AsyncGenerator[AsyncSession, None]:
        async with test_session_factory() as session:
            yield session

    app.dependency_overrides[get_db] = override_get_db

    async with AsyncClient(
        transport=ASGITransport(app=app),
        base_url=f"http://test{settings.api_v1_prefix}",
    ) as ac:
        yield ac

    app.dependency_overrides.clear()
