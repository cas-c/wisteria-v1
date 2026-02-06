# ADR-007: Docker Compose for Local Development

**Status:** Accepted

**Context:** Need to run Postgres, backend, and frontend together locally.

**Decision:** Docker Compose with three services + healthcheck.

**Reasoning:**
- One command (`docker compose up`) starts everything
- No "install Postgres on your Mac" instructions
- Healthcheck ensures backend doesn't start before Postgres is ready
- Volume mounts preserve hot reload for both frontend and backend
- Matches production topology (separate services)

**Trade-off:** Docker adds startup time (~10s). Requires Docker Desktop. Worth it for reproducibility.
