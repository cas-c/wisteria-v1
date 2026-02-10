# Implementation Todo

Tracks remaining work across all phases. Items are checked off as completed.

---

## Phase 0: Scaffolding ✅

- [x] Monorepo directory structure
- [x] FastAPI backend skeleton (config, database, main, health router)
- [x] Alembic migration environment (async-compatible)
- [x] Next.js frontend via create-next-app (App Router, TS, Tailwind)
- [x] Frontend lib layer (api client, types, utils, constants)
- [x] Docker Compose (Postgres + backend + frontend, healthcheck)
- [x] .env.example files
- [x] Root .gitignore
- [x] Project CLAUDE.md
- [x] Ruff/mypy config in pyproject.toml
- [ ] Prettier config (deferred — ESLint in place from create-next-app)

---

## Phase 1: Backend Foundation ✅

- [x] Base SQLAlchemy model (id UUID, created_at, updated_at) — `app/models/base.py`
- [x] Product model with all columns (enums, slug, price_cents) — `app/models/product.py`
- [x] AdminUser model (email, password_hash) — `app/models/admin_user.py`
- [x] Update `alembic/env.py` to import Base and set `target_metadata`
- [x] Generate initial Alembic migration (autogenerate detected both tables + indexes)
- [x] Run migration (`alembic upgrade head`) — tables confirmed in Postgres
- [x] Add DB ping to health endpoint (`SELECT 1` via Depends(get_db))
- [x] Add DB connection check in lifespan startup (fail-fast if DB unreachable)
- [x] Verify: `docker compose up`, hit `/api/v1/health`, confirmed `{"status":"ok","database":"connected"}`
- [x] Ruff config — added per-file-ignores for B008 (FastAPI Depends pattern)
- [x] mypy strict mode — passes clean on all 14 source files
- [x] Fixed `resend==2.5.0` → `resend==2.5.1` (version didn't exist on PyPI)

## Phase 2: Product CRUD + Auth ✅

- [x] Pydantic v2 schemas: ProductCreate, ProductUpdate, ProductResponse, ProductListParams — `app/schemas/product.py`
- [x] Auth schemas: LoginRequest, TokenResponse — `app/schemas/auth.py`
- [x] Product service (list, get_by_slug, get_by_id, create, update, soft_delete) — `app/services/product.py`
- [x] Auth service (authenticate_admin) — `app/services/auth.py`
- [x] Public routes: GET /products (paginated, filterable), GET /products/{slug} — `app/routers/products.py`
- [x] Password hashing utility (bcrypt direct, replaced passlib) — `app/utils/security.py`
- [x] JWT utility (create_access_token, decode_token) — `app/utils/security.py`
- [x] `get_current_admin` dependency (HTTPBearer + JWT + DB lookup) — `app/dependencies.py`
- [x] Auth router: POST /auth/login (returns JWT) — `app/routers/auth.py`
- [x] Admin product routes: GET/POST /admin/products, GET/PUT/DELETE /admin/products/{id} — `app/routers/admin_products.py`
- [x] Duplicate slug handling: returns 409 Conflict
- [x] Seed script: admin user + 10 sample figurine products — `scripts/seed.py`
- [x] Backend tests: 34 tests covering product CRUD, auth, JWT validation, edge cases
- [x] Test infrastructure: conftest with NullPool, TRUNCATE-based isolation
- [x] Ruff clean, all linting passes

## Phase 3: Frontend Product Display ✅

- [x] Root layout (html, body, font, metadata)
- [x] UI primitives: Button, Card, Badge, Skeleton, Input components
- [x] Layout components: Header (with cart icon), Footer, MobileNav
- [x] Product components: ProductCard, ProductGrid, ConditionBadge, ProductImage
- [x] Homepage: featured products grid (Server Component, fetches from API)
- [x] /products page: full catalog with category/condition display
- [x] /products/[slug] page: large image, description, price, condition, add-to-cart button
- [x] Responsive design pass (mobile-first)
- [x] Loading skeletons for product pages
- [x] E2E testing: Playwright setup, 5 test files (homepage, catalog, product-detail, responsive, loading), ~20 tests total

## Phase 4: Cart

- [ ] Install Zustand
- [ ] Cart store: items, addItem, removeItem, clearCart, totalCents (with persist middleware)
- [ ] Duplicate item prevention (toast instead of quantity increment — resale items are unique)
- [ ] CartDrawer component (slide-out panel from header icon)
- [ ] CartItem component (image, name, price, remove button)
- [ ] CartSummary component (item count, subtotal)
- [ ] Cart icon with item count badge in Header
- [ ] /cart page (full cart view, proceed to checkout button)
- [ ] Cart store unit tests

## Phase 5: Checkout + Stripe

- [ ] Order + OrderItem SQLAlchemy models
- [ ] Alembic migration for orders tables
- [ ] Stripe service (create_checkout_session)
- [ ] POST /checkout/create-session endpoint
- [ ] Stripe webhook endpoint (POST /webhooks/stripe)
  - [ ] Raw body handling (not JSON-parsed) for signature verification
  - [ ] Create order + order_items on checkout.session.completed
  - [ ] Mark purchased products as unavailable
- [ ] GET /orders/{id} endpoint (for confirmation page)
- [ ] Email service (Resend — send order confirmation)
- [ ] /checkout page (review order, redirect to Stripe button)
- [ ] /checkout/success page (fetch order by session_id, show confirmation)
- [ ] Test with Stripe CLI (`stripe listen --forward-to`)
- [ ] Backend tests: checkout flow, webhook handling, buying unavailable product

## Phase 6: Admin Panel

- [ ] Admin login page (/admin/login)
- [ ] Admin layout with sidebar navigation + auth guard (redirect if no JWT)
- [ ] useAdmin hook (store JWT, login/logout, check expiry)
- [ ] Dashboard page: product count, recent orders summary
- [ ] Product management: table view, add form, edit form, soft-delete with confirmation
- [ ] Order management: table view, order detail, status update (dropdown)
- [ ] Admin CRUD backend tests

## Phase 7: Polish + Deploy

- [ ] Global error handling (error.tsx boundaries)
- [ ] Loading skeletons for all pages
- [ ] Empty states (no products, empty cart, no orders)
- [ ] Toast notification system
- [ ] SEO: meta tags, Open Graph images for product pages
- [ ] GitHub Actions CI: lint + type-check + test for both frontend and backend
- [ ] Deploy frontend to Vercel
- [ ] Deploy backend + Postgres to Railway
- [ ] Production env vars and Stripe webhook configuration
- [ ] Smoke test: browse → add to cart → checkout → pay → confirm → admin view
