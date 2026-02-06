# Phase 0 Takeaways — Scaffolding

Completed: Phase 0 monorepo scaffold for Wisteria (Next.js + FastAPI + PostgreSQL).

---

## What Was Built

### Backend (Python / FastAPI)
- `app/config.py` — Settings singleton via `pydantic-settings`
- `app/database.py` — Async SQLAlchemy engine, session factory, `get_db` dependency
- `app/main.py` — FastAPI app with CORS and lifespan context manager
- `app/routers/health.py` — `/api/v1/health` endpoint
- `alembic/` — Async migration environment (ready, no migrations yet)
- Empty `models/`, `schemas/`, `services/`, `utils/` packages (populated in Phase 1+)

### Frontend (TypeScript / Next.js)
- Next.js 14+ via `create-next-app` (App Router, TypeScript, Tailwind, src dir)
- `src/types/index.ts` — Product, Order, OrderItem, PaginatedResponse interfaces
- `src/lib/api.ts` — Typed fetch wrapper for calling the backend
- `src/lib/constants.ts` — API URL, site name, label maps
- `src/lib/utils.ts` — `formatPrice()` (cents → dollars), `cn()` (class joiner)
- Empty `components/`, `hooks/`, `stores/` directories (populated in Phase 3+)

### Infrastructure
- `docker/docker-compose.yml` — Postgres 16, backend, frontend with hot reload
- `.env.example` files for both backend and frontend
- Root `.gitignore` covering Python, Node, env files, IDE, Docker

---

## FastAPI Patterns to Remember

### 1. pydantic-settings for Configuration
```python
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    database_url: str = "postgresql+asyncpg://..."
    debug: bool = False

settings = Settings()  # reads from env vars automatically
```
- Each field becomes an env var (case-insensitive match)
- `.env` file is loaded as fallback
- Type validation happens at startup — if `DEBUG=notabool`, it fails immediately
- **Comparison to Node**: Like `zod` + `dotenv` combined, but built into the framework

### 2. Dependency Injection with `Depends()`
```python
async def get_db() -> AsyncGenerator[AsyncSession, None]:
    async with async_session() as session:
        yield session

# In a route:
async def list_products(db: AsyncSession = Depends(get_db)):
    ...
```
- `yield` dependencies clean up after the request (like `try/finally`)
- Dependencies can depend on other dependencies (composable)
- FastAPI resolves the dependency tree per request
- **Comparison to Node**: Like Express middleware, but explicit and type-safe. Instead of `req.db`, you declare `db` as a parameter.

### 3. Lifespan Context Manager
```python
@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    # startup logic
    yield
    # shutdown logic
```
- Replaces the older `@app.on_event("startup")` / `@app.on_event("shutdown")`
- Code before `yield` runs on startup, code after runs on shutdown
- **Comparison to Node**: Like Next.js `instrumentation.ts` or Express app-level setup

### 4. Router Registration
```python
app.include_router(health.router, prefix=settings.api_v1_prefix)
```
- Routers are like Express `Router()` — group related endpoints
- `prefix` prepends to all routes in the router
- `tags` group endpoints in auto-generated API docs (FastAPI gives you Swagger at `/docs`)

---

## SQLAlchemy Async Patterns to Remember

### Engine vs Session
- **Engine** = connection pool manager (one per app)
- **Session** = unit of work (one per request)
- `expire_on_commit=False` — after committing, you can still access object attributes without another DB query. Without this, SQLAlchemy would mark all attributes as "expired" and try to lazily load them, which fails in async.

### Alembic with asyncpg
Alembic doesn't natively support async. The `env.py` workaround:
```python
async def run_async_migrations() -> None:
    connectable = async_engine_from_config(...)
    async with connectable.connect() as connection:
        await connection.run_sync(do_run_migrations)

def run_migrations_online() -> None:
    asyncio.run(run_async_migrations())
```
- `run_sync()` bridges sync Alembic with our async engine
- `target_metadata` is `None` for now — will point to `Base.metadata` once we define models

---

## Docker Compose Patterns to Remember

### Healthcheck + depends_on
```yaml
db:
  healthcheck:
    test: ["CMD-SHELL", "pg_isready -U postgres"]
    interval: 5s

backend:
  depends_on:
    db:
      condition: service_healthy
```
- `depends_on` alone only controls **start order**, not **readiness**
- `condition: service_healthy` makes the backend wait until Postgres actually accepts connections
- Without this, the backend would crash on startup trying to connect to a DB that's still initializing

### Volume Mounts for Hot Reload
```yaml
volumes:
  - ../backend:/app          # whole dir for uvicorn --reload
  - ../frontend/src:/app/src  # src + public for Next.js
```
- Host file changes are reflected inside the container immediately
- Backend: uvicorn `--reload` watches for Python file changes
- Frontend: Next.js dev server watches `src/` for changes
- `node_modules/` is NOT mounted — it was installed inside the container during build

### Named Volume for Data Persistence
```yaml
volumes:
  postgres_data:
```
- Docker manages this volume — it persists across `docker compose down` and `up`
- To truly reset the DB: `docker compose down -v` (the `-v` flag removes volumes)

---

## Frontend Decisions Already Embedded

### Money as Integer Cents
```typescript
export function formatPrice(cents: number): string {
  return new Intl.NumberFormat("en-US", {
    style: "currency",
    currency: "USD",
  }).format(cents / 100);
}
```
- `price_cents: number` everywhere, never `price: number`
- Division by 100 only happens at the display boundary
- Stripe also uses cents — so no conversion needed when creating checkout sessions

### Typed API Client
```typescript
const products = await api<PaginatedResponse<Product>>("/products");
```
- Generic return type `api<T>()` gives type safety without runtime validation
- Error responses extract FastAPI's `detail` field automatically
- Content-Type header is set automatically for JSON bodies

---

## What's NOT Done Yet (Deferred from Phase 0)
- Ruff and mypy config files for backend (will add in Phase 1 alongside actual Python code to lint)
- Prettier config for frontend (ESLint is in place from create-next-app)
- Zustand not yet installed (Phase 4)
- No pyproject.toml yet (will add when we need tool configs)
