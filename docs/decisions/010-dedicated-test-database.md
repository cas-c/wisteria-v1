# ADR-010: Dedicated Test Database

**Status:** Accepted

**Context:** During Phase 2, tests ran against the same `wisteria` database used for local development. This caused several problems:

1. Running the seed script before tests polluted test data — the first test saw unexpected rows.
2. Running tests after seeding destroyed seed data via TRUNCATE.
3. A crashed test run could leave stale data in the dev DB.
4. No way to safely run tests while the dev server is using the same DB.

The options:
- **A) Same database, careful TRUNCATE** — what we had. Fragile.
- **B) Dedicated `wisteria_test` database** — tests never touch dev data.
- **C) SQLite in-memory for tests** — fast but different SQL dialect. Postgres-specific features (ENUM, UUID generation, JSON operators) won't work.
- **D) Testcontainers (ephemeral Postgres per test run)** — ideal isolation but adds significant complexity and startup time.

**Decision:** Use a dedicated `wisteria_test` Postgres database (option B).

**Reasoning:**
- Zero risk of tests corrupting dev data or vice versa.
- Same Postgres engine as production — no dialect mismatches.
- Minimal complexity: one new env var (`TEST_DATABASE_URL`) and a small bootstrap function.
- The test DB is auto-created by `conftest.py` on first run — no manual setup needed.

**Implementation:**
- `config.py` has `test_database_url` pointing at `wisteria_test`.
- `conftest.py` runs `_ensure_test_db_exists()` at import time — connects to the `postgres` DB via sync psycopg2 and runs `CREATE DATABASE wisteria_test` if missing.
- `docker-compose.yml` passes `TEST_DATABASE_URL` to the backend container.
- `psycopg2-binary` added as a dev dependency for the sync bootstrap connection.

**Trade-off:** Adds one more database to the Postgres instance and one more dependency (`psycopg2-binary`). Both are negligible — the DB is tiny and psycopg2 is only used at test startup.
