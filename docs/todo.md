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
- [ ] Ruff/mypy config (deferred — add when there's code to lint)
- [ ] Prettier config (deferred — ESLint in place from create-next-app)
- [ ] pyproject.toml (deferred — add when tool configs needed)

---

## Phase 1: Backend Foundation
- [ ] Base SQLAlchemy model (id, created_at, updated_at mixin)
- [ ] Product model with all columns (UUID PK, slug, price_cents, condition enum, category enum, etc.)
- [ ] AdminUser model (UUID PK, email, password_hash)
- [ ] Uncomment `target_metadata` in `alembic/env.py` to point at Base.metadata
- [ ] Generate initial Alembic migration (`alembic revision --autogenerate`)
- [ ] Run migration (`alembic upgrade head`)
- [ ] Add DB ping to health endpoint (verify async connection works)
- [ ] Add DB connection check in lifespan startup
- [ ] Verify: `docker compose up`, hit `/api/v1/health`, confirm DB connects
- [ ] Ruff config (pyproject.toml or ruff.toml)
- [ ] mypy config

## Phase 2: Product CRUD + Auth
- [ ] Pydantic v2 schemas: ProductCreate, ProductUpdate, ProductResponse, ProductListParams
- [ ] Product service (list, get_by_slug, create, update, soft_delete)
- [ ] Public routes: GET /products (paginated, filterable), GET /products/{slug}
- [ ] Password hashing utility (passlib + bcrypt)
- [ ] JWT utility (create_access_token, decode_token)
- [ ] `get_current_admin` dependency (extract + validate JWT from Authorization header)
- [ ] Auth router: POST /auth/login (returns JWT)
- [ ] Admin product routes: GET/POST /admin/products, PUT/DELETE /admin/products/{id}
- [ ] Seed script: create admin user + 8-10 sample figurine products
- [ ] Backend tests: product CRUD, auth, edge cases

## Phase 3: Frontend Product Display
- [ ] Root layout (html, body, font, metadata)
- [ ] UI primitives: Button, Card, Badge, Skeleton, Input components
- [ ] Layout components: Header (with cart icon), Footer, MobileNav
- [ ] Product components: ProductCard, ProductGrid, ConditionBadge, ProductImage
- [ ] Homepage: featured products grid (Server Component, fetches from API)
- [ ] /products page: full catalog with category/condition display
- [ ] /products/[slug] page: large image, description, price, condition, add-to-cart button
- [ ] Responsive design pass (mobile-first)
- [ ] Loading skeletons for product pages

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
