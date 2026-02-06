# ADR-001: Monorepo with Separate Backend and Frontend

**Status:** Accepted

**Context:** We need a Next.js frontend and a FastAPI backend. Options:
1. Monorepo (both in one git repo, separate directories)
2. Polyrepo (separate git repos)
3. Next.js API routes instead of separate backend

**Decision:** Monorepo with `backend/` and `frontend/` directories.

**Reasoning:**
- Single repo is simpler to manage for a solo project (one PR, one clone, shared CI)
- Separate backend lets us learn FastAPI properly — Next.js API routes would hide that
- Separate backend is more realistic for senior-level interviews (service boundaries)
- Shared Docker Compose file makes local dev seamless
- If the backend grows, it can be extracted to its own repo later with no code changes

**Trade-off:** Slightly more complex CI (need to detect which directory changed), but GitHub Actions path filters handle this well.
