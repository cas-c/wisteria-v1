# Phase 2 Takeaways — Product CRUD + Auth

## What Was Built

### Files created
- **`app/schemas/product.py`** — Pydantic v2 schemas for products: `ProductCreate`, `ProductUpdate` (partial), `ProductResponse` (with `from_attributes`), `ProductListParams` (query filters), `PaginatedProductResponse`.
- **`app/schemas/auth.py`** — `LoginRequest` (with `EmailStr` validation) and `TokenResponse`.
- **`app/services/product.py`** — Business logic: `list_products` (paginated + filtered), `get_product_by_slug`, `get_product_by_id`, `create_product`, `update_product` (partial via `exclude_unset`), `soft_delete_product`.
- **`app/services/auth.py`** — `authenticate_admin` (email lookup + password verify, no enumeration leakage).
- **`app/utils/security.py`** — `hash_password`, `verify_password` (bcrypt direct), `create_access_token`, `decode_token` (python-jose HS256).
- **`app/routers/auth.py`** — `POST /auth/login` returns JWT.
- **`app/routers/products.py`** — Public `GET /products` (paginated, filterable by category/condition/search) and `GET /products/{slug}`.
- **`app/routers/admin_products.py`** — Admin CRUD: list (includes unavailable), create (with 409 on duplicate slug), get by UUID, partial update, soft delete.
- **`scripts/seed.py`** — Idempotent seed: 1 admin user (`admin@wisteria.com` / `admin123`) + 10 sample figurine products across all categories and conditions.
- **`tests/conftest.py`** — Test infrastructure: NullPool engine, TRUNCATE-based isolation, `override_get_db` for test session injection.
- **`tests/test_products.py`** — 12 tests: listing, filtering, search, pagination, response schema, 404.
- **`tests/test_auth.py`** — 10 tests: valid login, wrong password, nonexistent email, invalid email, empty password, missing token, invalid token, expired token, deleted user, valid token.
- **`tests/test_admin_products.py`** — 12 tests: admin list (includes unavailable), create, duplicate slug (409), invalid slug, zero price, requires auth, update name/price, update nonexistent, soft delete, visibility after delete, delete nonexistent.

### Files modified
- **`app/main.py`** — Registered auth, products, and admin_products routers.
- **`app/dependencies.py`** — Added `get_current_admin` dependency (was placeholder).
- **`app/utils/__init__.py`** — Re-exports security utilities.
- **`app/schemas/__init__.py`** — Re-exports all schemas.
- **`requirements.txt`** — Added `email-validator==2.2.0`, replaced `passlib[bcrypt]` with `bcrypt==4.2.1`.
- **`pyproject.toml`** — Added B008 ignore for `dependencies.py`, E501 ignore for `scripts/seed.py`, `asyncio_default_fixture_loop_scope = "function"`.

---

## New Patterns Introduced

### 1. Pydantic v2 `model_config = ConfigDict(from_attributes=True)`
Enables creating Pydantic schemas from SQLAlchemy model instances. Without it, `model_validate(orm_obj)` would fail because Pydantic expects dicts by default.

### 2. Partial Updates with `exclude_unset=True`
`ProductUpdate` has all optional fields. `data.model_dump(exclude_unset=True)` only returns fields the client actually sent, preventing unset fields from overwriting existing values with `None`.

### 3. FastAPI `Depends()` on Pydantic Models for Query Params
`ProductListParams = Depends()` tells FastAPI to extract each field from query parameters. Keeps validation clean without manually pulling params.

### 4. Service Layer Pattern
Routes are thin — they handle HTTP concerns. Business logic lives in `app/services/`. Routes call services, services call the DB. Services accept `AsyncSession` as their first argument (passed via DI).

### 5. HTTPBearer + JWT Authentication Chain
`HTTPBearer()` extracts the token from `Authorization: Bearer <token>`. The `get_current_admin` dependency decodes it, validates the UUID, and looks up the admin in the DB. Multiple levels of failure all map to 401.

### 6. NullPool for Async Tests
asyncpg connections are bound to the event loop they're created on. pytest-asyncio creates a new loop per test function. `NullPool` creates a fresh connection for each DB operation and closes it immediately — avoids "Future attached to a different loop" errors.

---

## Gotchas Encountered

1. **passlib + bcrypt 4.1+ incompatibility.** passlib is effectively abandoned and doesn't work with modern bcrypt. The `_calc_checksum` method throws `ValueError: password cannot be longer than 72 bytes`. Fixed by using `bcrypt` directly instead of through passlib. Simpler API, fewer dependencies.

2. **`HTTPAuthorizationCredentials.credentials` not `.token`.** FastAPI's `HTTPBearer` returns an object with `.credentials` (the actual token string) and `.scheme` (always "Bearer"). The attribute name is `.credentials`, not `.token`.

3. **asyncpg "Future attached to a different loop" in tests.** Connection pools pin connections to the event loop where they were created. When pytest-asyncio creates a new loop per test, pooled connections from the previous loop cause this error. Fix: `NullPool` for the test engine.

4. **Postgres ENUM types persist after `drop_all`.** SQLAlchemy's `Base.metadata.drop_all()` drops tables but not custom ENUM types. On the next `create_all`, it tries to recreate the ENUM type and fails. Fix: use `create_all` once (with `checkfirst=True` implicit behavior) and TRUNCATE between tests.

5. **Test isolation vs seed data.** If you run `seed.py` and then `pytest`, the seed data is still in the tables. Tests must TRUNCATE before each test, not just after.

6. **IntegrityError on duplicate slugs.** Without explicit handling, SQLAlchemy's `IntegrityError` propagates as a 500. Added a try/except in the create route to return a clean 409 Conflict.

---

## Deviations from Plan

1. **Replaced passlib with direct bcrypt usage.** The plan specified `passlib + bcrypt`, but passlib is incompatible with bcrypt 4.1+. Using bcrypt directly is simpler and more reliable.

2. **Added `get_product_by_id` to the service.** Not in the original todo but needed by admin routes (which reference products by UUID, not slug).

3. **Added 409 Conflict handling for duplicate slugs.** The original plan didn't specify error handling for this edge case. Without it, duplicate slugs return a raw 500 IntegrityError.

4. **Added `email-validator` dependency.** Required by Pydantic's `EmailStr` type used in `LoginRequest`. Not explicitly listed in the original requirements but implied by email validation.

5. **Moved tests to a dedicated `wisteria_test` database.** Tests originally ran against the dev `wisteria` DB, which caused seed data to be destroyed and test data to leak into development. Added `test_database_url` to config, auto-creation logic in conftest, and `psycopg2-binary` as a dev dependency for the bootstrap connection. See ADR 010.

6. **Adopted TDD for future phases.** Phase 2 was code-first, which worked but led to discovering edge cases late. Going forward, backend services and routes will use Red-Green-Refactor. See ADR 011.
