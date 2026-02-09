# Wisteria — Japanese Figurine E-Commerce Store

Monorepo e-commerce store for reselling Japanese figurines.
Next.js 14+ frontend, FastAPI backend, PostgreSQL database.

## Quick Start
```bash
docker compose -f docker/docker-compose.yml up
# Backend: http://localhost:8000
# Frontend: http://localhost:3000
# Postgres: localhost:5432
```

## Structure
- `backend/` — Python 3.12+, FastAPI, SQLAlchemy 2.0 async, Alembic
- `frontend/` — Next.js 14+ (App Router), TypeScript, Tailwind, Zustand
- `docker/` — Docker Compose for local development
- `docs/` — Architecture decisions, phase notes, and agent instructions

## Documentation
- `docs/agent-instructions.md` — **Read this first.** Coding standards, architecture rules, file organization, phase-specific guidance, and common pitfalls.
- `docs/decisions/` — ADRs (one file per decision). See `README.md` inside for the index.
- `docs/todo.md` — Granular task checklist for all phases.
- `docs/plan.md` — Original project plan (phases, schema, API endpoints, full spec).
- `docs/phase-0-takeaways.md` — FastAPI/SQLAlchemy/Docker patterns with explanations.
- `docs/phase-1-takeaways.md` — SQLAlchemy 2.0 model patterns, Alembic workflow, Ruff/mypy setup.

## Overrides from Parent Workspace
- **Test location:** Parent CLAUDE.md says "collocate tests with source files." For this project: backend uses `backend/tests/` (Python convention), frontend colocates tests alongside source files (JS/TS convention). Both are correct for their ecosystems.

## Key Rules (quick reference)
- **Keep docs up to date.** After completing a phase, update `docs/` — see `docs/agent-instructions.md` § "Documentation Maintenance" for details.
- Money is always integer cents (`price_cents`), never floats
- UUIDs for all primary keys
- Async everywhere on the backend
- No `any` types in TypeScript
- Named exports only (frontend)
- Conventional commits: `feat:`, `fix:`, `chore:`, `docs:`

## Learning Context
The project owner is an experienced TypeScript/Next.js developer learning
Python/FastAPI. Always explain Python idioms and patterns when introducing them.
TypeScript patterns don't need explanation unless unusual.
