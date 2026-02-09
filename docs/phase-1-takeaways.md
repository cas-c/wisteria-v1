# Phase 1 Takeaways — Backend Foundation

## What Was Built

### Files created
- **`app/models/base.py`** — Abstract `Base` class with UUID `id`, `created_at`, `updated_at`. All models inherit from this.
- **`app/models/product.py`** — Product model with `ProductCondition` and `ProductCategory` enums, slug (unique/indexed), `price_cents` (integer), `image_url`, `is_available`, `quantity`.
- **`app/models/admin_user.py`** — AdminUser model with `email` (unique/indexed) and `password_hash`.
- **`app/models/__init__.py`** — Re-exports all models. Alembic needs this to discover tables via `Base.metadata`.
- **`alembic/versions/f0ed3a8373d5_create_products_and_admin_users_tables.py`** — Initial migration creating both tables, their indexes, and Postgres ENUM types.

### Files modified
- **`alembic/env.py`** — Uncommented `target_metadata = Base.metadata` and imported from `app.models`.
- **`app/routers/health.py`** — Now performs `SELECT 1` via `Depends(get_db)` to verify DB connectivity.
- **`app/main.py`** — Added DB connection check in `lifespan` startup. App fails fast if DB is unreachable.
- **`pyproject.toml`** — Added `per-file-ignores` for B008 in routers (FastAPI `Depends()` pattern).
- **`requirements.txt`** — Fixed `resend==2.5.0` → `resend==2.5.1` (2.5.0 doesn't exist on PyPI).

---

## New Patterns Introduced

### 1. SQLAlchemy 2.0 Typed Columns (`Mapped[T]` + `mapped_column()`)
SQLAlchemy 2.0 uses `Mapped[str]` type annotations instead of the older `Column(String)` style. This gives mypy full type checking on model attributes. The `mapped_column()` call configures the DB column (length, unique, default, etc.).

### 2. Python str Enum → Postgres ENUM
Python enums that inherit from both `str` and `enum.Enum` map to Postgres ENUM types. The `values_callable=lambda e: [x.value for x in e]` parameter tells SQLAlchemy to store the enum's `.value` (e.g., `"like_new"`) rather than the Python name (e.g., `"LIKE_NEW"`).

### 3. DeclarativeBase (replaces `declarative_base()`)
SQLAlchemy 2.0's `DeclarativeBase` is a class you inherit from, replacing the older `declarative_base()` factory function. It integrates with Python's type system for mypy.

### 4. FastAPI Lifespan Context Manager
The `@asynccontextmanager` decorated `lifespan()` function runs code on startup (before `yield`) and shutdown (after `yield`). We use it to verify the DB connection before accepting any requests.

### 5. Ruff B008 Exception for FastAPI
Ruff's B008 rule ("Do not perform function call in argument defaults") is a false positive for FastAPI's `Depends()` pattern. We suppress it only in router files via `per-file-ignores`.

---

## Gotchas Encountered

1. **`resend==2.5.0` doesn't exist on PyPI.** The version jumps from 2.4.0 to 2.5.1. Fixed by pinning to 2.5.1.

2. **Alembic `ModuleNotFoundError: No module named 'app'`** when running `alembic` directly in the container. Fixed by using `python -m alembic` instead, which ensures the working directory is on the Python path.

3. **Ruff B008 vs FastAPI Depends.** The `Depends(get_db)` pattern is intentional (FastAPI evaluates it per-request, not at import time). Suppressed via per-file-ignores scoped to `app/routers/*.py`.

---

## Deviations from Plan

None. Phase 1 was implemented exactly as specified in `docs/todo.md` and `docs/agent-instructions.md`.
