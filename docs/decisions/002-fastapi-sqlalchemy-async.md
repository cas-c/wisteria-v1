# ADR-002: FastAPI + SQLAlchemy Async over Django or Sync SQLAlchemy

**Status:** Accepted

**Context:** Need a Python web framework and ORM.

**Decision:** FastAPI with SQLAlchemy 2.0 async mode and asyncpg.

**Reasoning:**
- FastAPI: automatic OpenAPI docs, Pydantic validation, async-native, modern
- SQLAlchemy 2.0: industry standard ORM, strong async support since 2.0, more explicit than Django ORM
- asyncpg: fastest PostgreSQL driver for Python, native async
- Learning value: FastAPI + SQLAlchemy is the most common Python API stack outside Django shops

**Trade-off:** More boilerplate than Django (no built-in admin, no auto-migrations from models). We compensate with Alembic for migrations. No admin UI — we build our own in React (Phase 6), which is more portfolio-worthy anyway.

**Rejected:**
- Django: too much magic, less learning value for understanding how things work underneath
- Sync SQLAlchemy: would bottleneck on DB calls in an async framework
