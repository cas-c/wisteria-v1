# Phase Playbook — Wisteria

Implementation details for each phase. Read the relevant section before
starting work on that phase. For architecture rules and project-wide
conventions, see [`agent-instructions.md`](agent-instructions.md).

---

## Phase 1: Backend Foundation ✅
- Create `app/models/base.py` with a `Base` class that has `id` (UUID),
  `created_at`, `updated_at` columns. All models inherit from this.
- Product model goes in `app/models/product.py`. Use SQLAlchemy `Enum` type
  for condition and category.
- AdminUser model goes in `app/models/admin_user.py`.
- After creating models, update `alembic/env.py` to import Base and set
  `target_metadata = Base.metadata`.
- The health endpoint should attempt a simple query (`SELECT 1`) to verify
  the DB connection is alive.
- Test the full Docker stack: `docker compose up` → hit health → see DB
  connected.

## Phase 2: Product CRUD + Auth ✅
- Pydantic schemas should use `model_config = ConfigDict(from_attributes=True)`
  to enable creating schemas from SQLAlchemy model instances.
- Product service methods should accept `AsyncSession` as their first argument
  (passed from the route via dependency injection).
- JWT: use `PyJWT` with HS256. Token payload: `{"sub": admin_user.id, "exp": ...}`.
  (Originally python-jose, swapped to PyJWT — see ADR 012.)
- Password hashing: use `bcrypt` directly (NOT passlib — see ADR 009).
- The seed script should be a standalone Python script (`backend/scripts/seed.py`)
  that can be run with `python -m scripts.seed`.
- Include edge case tests: duplicate slugs, buying unavailable products,
  invalid JWT, expired JWT.
- Test setup: use `NullPool` for async test engine, `TRUNCATE CASCADE`
  for test isolation, dedicated `wisteria_test` database (see ADR 010).

## Phase 3: Frontend Product Display
- Use Server Components for product listing and detail pages.
  Call the backend API directly (server-side fetch, no CORS needed).
- Build small, composable UI primitives first. Don't skip this step.
- ProductCard: image, name, price (formatted from cents), condition badge.
- Mobile-first responsive design. Use Tailwind breakpoints (`sm:`, `md:`, `lg:`).
- **TDD for any new backend work** (e.g., if API changes are needed for
  the frontend). Write tests first, then implement. See ADR 011.

## Phase 4: Cart
- Zustand store with `persist` middleware targets localStorage.
- Cart items are Product objects. Since these are resale items (usually qty=1),
  adding a duplicate should show a toast, not increment quantity.
- The cart icon in the header should show item count as a badge.
- CartDrawer slides out from the right side of the screen.

## Phase 5: Checkout + Stripe
- **Security:** Add request body size limit (see ADR 012).
- **Critical:** The Stripe webhook endpoint must read the raw request body
  for signature verification. FastAPI parses JSON by default — use
  `Request.body()` to get raw bytes before any parsing.
- Create Order + OrderItems in the webhook handler, NOT in the checkout
  endpoint. The checkout endpoint only creates a Stripe session.
- After order creation, mark all purchased products as `is_available = False`.
- Send confirmation email via Resend in the webhook handler.
- Test locally with `stripe listen --forward-to localhost:8000/api/v1/webhooks/stripe`.
- **TDD for all checkout/webhook backend code.** Write tests for order
  creation, webhook handling, and availability marking before implementing.

## Phase 6: Admin Panel
- **Security:** Add token revocation / denylist (see ADR 012).
- JWT stored in memory (Zustand store, NOT localStorage — avoids XSS).
- Admin layout: sidebar with nav links, main content area.
- Auth guard: if no valid JWT, redirect to /admin/login.
- Product soft-delete: set `is_available = False`, don't actually DELETE.
- Order status updates: dropdown with pending → paid → shipped → cancelled.

## Phase 7: Polish + Deploy
- **Security:** Add security headers middleware, verify `DEBUG=false` (see ADR 012).
- error.tsx at the app root and in key route segments.
- Loading skeletons that match the actual content layout (not generic spinners).
- Vercel: set `NEXT_PUBLIC_API_URL` to the Railway backend URL.
- Railway: set all env vars from `.env.example`, use Railway's managed Postgres.
- Production Stripe webhook URL: `https://your-railway-url/api/v1/webhooks/stripe`.

---

## Known Pitfalls

Things we've hit (or expect to hit) during development. Check here if you
encounter a confusing error.

1. **Don't return SQLAlchemy models directly from routes.** Always convert to
   Pydantic schemas. SQLAlchemy models have lazy-loaded relationships that
   break serialization.

2. **Don't forget `await` on async DB operations.** SQLAlchemy async will
   silently return a coroutine object instead of results if you forget `await`.

3. **Don't parse the Stripe webhook body as JSON before verifying the signature.**
   The signature is computed over the raw bytes. If you parse + re-serialize,
   the bytes change and verification fails.

4. **Don't use `float` for money anywhere.** Not in Python, not in TypeScript,
   not in the database. Always integer cents.

5. **Don't commit Alembic migrations without reviewing them.** Autogenerate
   is a suggestion, not gospel. It sometimes drops columns it shouldn't or
   creates redundant indexes.

6. **Don't use `git add .` or `git add -A`.** Always add specific files.
   The `.env` files contain secrets.

7. **Don't install frontend dependencies (Zustand, etc.) until the phase
   that needs them.** Keeps the working tree clean and focused.

8. **Don't use passlib for password hashing.** passlib is abandoned and
   incompatible with bcrypt 4.1+. Use `bcrypt` directly. See ADR 009.

9. **Don't share asyncpg connections across event loops in tests.** Use
   `NullPool` for the test engine. asyncpg connections are bound to the
   event loop they were created on. Without NullPool, you'll get "Future
   attached to a different loop" errors.

10. **Don't forget to TRUNCATE before tests, not just after.** Seed data
    or data from previous test runs can pollute the first test.

11. **`HTTPAuthorizationCredentials` uses `.credentials`, not `.token`.**
    FastAPI's `HTTPBearer` returns an object with `.credentials` (the token)
    and `.scheme` (always "Bearer").

12. **Tests must use `test_database_url`, not `database_url`.** If conftest
    points at the dev database, tests will destroy seed data and pollute
    dev with test rows. Always use the dedicated `wisteria_test` DB.
