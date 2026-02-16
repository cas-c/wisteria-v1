# Wisteria — Japanese Figurine E-Commerce Store

Monorepo: Next.js 14+ frontend, FastAPI backend, PostgreSQL.

## Quick Start
```bash
docker compose -f docker/docker-compose.yml up
# Backend: http://localhost:8000 | Frontend: http://localhost:3000
```

## Structure
- `backend/` — Python 3.12+, FastAPI, SQLAlchemy 2.0 async, Alembic
- `frontend/` — Next.js 14+ (App Router), TypeScript, Tailwind, Zustand
- `docker/` — Docker Compose for local dev
- `docs/` — Architecture decisions, phase playbook, agent instructions

## Key Docs
- **`docs/agent-instructions.md`** — Read first. Architecture, standards, testing.
- `docs/phase-playbook.md` — Per-phase implementation details and pitfalls.
- `docs/todo.md` — Task checklist across all phases.
- `docs/plan.md` — Original project spec (schema, API, full plan).
- `docs/decisions/` — ADRs (indexed in `README.md`).

## Overrides from Parent Workspace
- Backend tests in `backend/tests/` (Python convention), not colocated.

## Learning Context
Owner is an experienced TypeScript/Next.js developer learning Python/FastAPI.
Explain Python idioms and patterns when introducing them.
