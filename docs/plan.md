# Wisteria — Japanese Figurine E-Commerce Store

A real e-commerce store for reselling Japanese figurines and goods. Monorepo with Next.js frontend + FastAPI backend.

---

## Stack

| Layer    | Technology                                                             |
| -------- | ---------------------------------------------------------------------- |
| Frontend | Next.js 14+ (App Router), TypeScript, React 18+, Tailwind CSS, Zustand |
| Backend  | Python 3.12+, FastAPI, SQLAlchemy 2.0 (async), Alembic, asyncpg        |
| Database | PostgreSQL 16                                                          |
| Payments | Stripe Checkout (redirect flow + webhook)                              |
| Email    | Resend                                                                 |
| Infra    | Docker Compose (local), Vercel (frontend), Railway (backend + DB)      |

---

## Monorepo Structure

```
~/claude/wisteria-v1/
├── .github/workflows/       # CI for backend + frontend
├── backend/
│   ├── alembic/             # DB migrations
│   ├── app/
│   │   ├── main.py          # FastAPI app, CORS, lifespan
│   │   ├── config.py        # pydantic-settings env loading
│   │   ├── database.py      # async engine + session factory
│   │   ├── dependencies.py  # get_db, get_current_admin
│   │   ├── models/          # SQLAlchemy models (product, order, order_item, admin_user)
│   │   ├── schemas/         # Pydantic v2 request/response schemas
│   │   ├── routers/         # Route handlers (products, checkout, webhooks, admin, auth)
│   │   ├── services/        # Business logic (product, order, stripe, email)
│   │   └── utils/           # JWT, password hashing, email templates
│   ├── tests/
│   ├── pyproject.toml
│   ├── requirements.txt
│   └── Dockerfile
├── frontend/
│   ├── src/
│   │   ├── app/             # Next.js App Router pages
│   │   │   ├── (shop)/      # Public: products, product detail
│   │   │   ├── cart/        # Shopping cart
│   │   │   ├── checkout/    # Checkout + success page
│   │   │   └── (admin)/     # Admin: dashboard, product CRUD, orders
│   │   ├── components/      # ui/, layout/, product/, cart/, order/
│   │   ├── lib/             # api.ts, stripe.ts, utils.ts, constants.ts
│   │   ├── hooks/           # useCart, useAdmin
│   │   ├── stores/          # cart-store.ts (Zustand)
│   │   └── types/           # TypeScript interfaces
│   ├── package.json
│   └── Dockerfile
├── docker/
│   └── docker-compose.yml   # postgres + backend + frontend
├── docs/                    # Architecture decisions, API docs
├── CLAUDE.md                # Project-level Claude context
└── README.md
```

---

## Database Schema

**4 tables:** `admin_users`, `products`, `orders`, `order_items`

### products

- `id` UUID PK, `name`, `slug` (UNIQUE), `description`, `price_cents` INTEGER (never floats for money), `condition` (new/like_new/used), `category` (nendoroid/scale_figure/plush/goods), `image_url` VARCHAR, `is_available` BOOLEAN, `quantity` INTEGER (usually 1 for resale), `created_at`, `updated_at`

### orders

- `id` UUID PK, `stripe_checkout_session_id` UNIQUE, `stripe_payment_intent_id`, `status` (pending/paid/shipped/cancelled), `customer_email`, `customer_name`, `shipping_address_json` JSONB, `total_cents` INTEGER, `created_at`, `updated_at`

### order_items

- `id` UUID PK, `order_id` FK, `product_id` FK, `price_cents` INTEGER (snapshot at purchase), `quantity`

### admin_users

- `id` UUID PK, `email` UNIQUE, `password_hash`, `created_at`

**Key decisions:** UUIDs prevent enumeration. Money as integer cents. Slug for SEO-friendly URLs. Snapshot pricing in order_items. JSONB for shipping address (Stripe collects it).

---

## API Endpoints

### Public (no auth)

| Method | Path                              | Description                                                           |
| ------ | --------------------------------- | --------------------------------------------------------------------- |
| GET    | `/api/v1/products`                | List available products (paginated, filterable by category/condition) |
| GET    | `/api/v1/products/{slug}`         | Single product by slug                                                |
| POST   | `/api/v1/checkout/create-session` | Create Stripe checkout session                                        |
| POST   | `/api/v1/webhooks/stripe`         | Stripe webhook (raw body, signature verification)                     |
| GET    | `/api/v1/orders/{id}`             | Order detail (for confirmation page)                                  |
| GET    | `/api/v1/health`                  | Health check                                                          |

### Admin (JWT required)

| Method     | Path                               | Description                  |
| ---------- | ---------------------------------- | ---------------------------- |
| POST       | `/api/v1/auth/login`               | Admin login, returns JWT     |
| GET/POST   | `/api/v1/admin/products`           | List all / Create product    |
| PUT/DELETE | `/api/v1/admin/products/{id}`      | Update / Soft-delete product |
| GET        | `/api/v1/admin/orders`             | List all orders              |
| GET        | `/api/v1/admin/orders/{id}`        | Order detail                 |
| PATCH      | `/api/v1/admin/orders/{id}/status` | Update order status          |

**Pagination envelope:** `{ items, total, page, per_page, pages }`

---

## Frontend Pages

| Route                       | Description                                            | Type             |
| --------------------------- | ------------------------------------------------------ | ---------------- |
| `/`                         | Homepage — featured products grid                      | Server Component |
| `/products`                 | Full catalog                                           | Server Component |
| `/products/[slug]`          | Product detail — large image, description, add to cart | Server Component |
| `/cart`                     | Shopping cart                                          | Client Component |
| `/checkout`                 | Review order, redirect to Stripe                       | Client Component |
| `/checkout/success`         | Order confirmation                                     | Server Component |
| `/admin`                    | Dashboard — product count, recent orders               | Client Component |
| `/admin/products`           | Product table with edit/delete                         | Client Component |
| `/admin/products/new`       | Add product form                                       | Client Component |
| `/admin/products/[id]/edit` | Edit product form                                      | Client Component |
| `/admin/orders`             | Order table                                            | Client Component |
| `/admin/orders/[id]`        | Order detail + status update                           | Client Component |

**Cart:** Zustand store with `persist` middleware (localStorage). Resale items are unique — duplicate adds show a toast instead of incrementing.

---

## Stripe Checkout Flow

1. Frontend sends cart items → `POST /api/v1/checkout/create-session`
2. Backend creates Stripe Checkout Session with line items, shipping collection
3. Frontend redirects to Stripe's hosted checkout page
4. Customer pays on Stripe → redirected to `/checkout/success?session_id=xxx`
5. Stripe sends webhook → `POST /api/v1/webhooks/stripe`
6. Backend: verify signature, create order + order_items, mark products unavailable, send confirmation email

**Critical:** Webhook reads raw body for signature verification. Never parse as JSON first.

---

## Implementation Phases

### Phase 0: Scaffolding

- Create monorepo structure, init Next.js + FastAPI projects
- Docker Compose (Postgres + backend + frontend with hot reload)
- `.env.example` files, `.gitignore`, linters (Ruff + mypy, ESLint + Prettier)
- Project CLAUDE.md, git init, first commit

### Phase 1: Backend Foundation

- Config, database, base model, Product + AdminUser models
- Alembic setup + initial migration
- FastAPI app with CORS, health endpoint
- Verify: docker compose up, hit health, DB connects

### Phase 2: Product CRUD + Auth

- Pydantic schemas, product service, public product routes
- JWT auth (bcrypt + python-jose), admin login endpoint
- Admin product CRUD routes
- Seed script (admin user + sample products)

### Phase 3: Frontend Product Display

- Root layout, API client (`lib/api.ts`), TypeScript types
- UI primitives (Button, Card, Badge, Skeleton, Input)
- Header, Footer, MobileNav
- ProductCard, ProductGrid, ConditionBadge, ProductImage
- Homepage, `/products`, `/products/[slug]` pages
- Responsive polish (mobile-first)

### Phase 4: Cart

- Zustand cart store with localStorage persistence
- CartDrawer (slide-out), CartItem, CartSummary components
- Add to Cart buttons, cart icon with count badge
- `/cart` page, duplicate prevention

### Phase 5: Checkout + Stripe

- Stripe service, checkout endpoint, Order + OrderItem models
- Alembic migration for orders
- Webhook handler (signature verification, order creation, mark products unavailable)
- Email service (Resend)
- `/checkout` and `/checkout/success` pages
- Test with Stripe CLI: `stripe listen --forward-to localhost:8000/api/v1/webhooks/stripe`

### Phase 6: Admin Panel

- Admin login page, layout with sidebar + auth guard
- Product management (table, add, edit, soft-delete)
- Order management (table, detail, status update)

### Phase 7: Polish + Deploy

- Error handling, loading skeletons, empty states, toasts
- Basic SEO (meta tags, Open Graph)
- GitHub Actions CI (lint, type-check, test for both frontend + backend)
- Deploy: Vercel (frontend), Railway (backend + Postgres)
- Production Stripe webhook, env vars, smoke test

---

## Future Features (not built now, designed for)

- User accounts + order history
- Search & filters (series, character, condition, price range)
- S3/R2 image uploads (replace URL strings)
- Inventory auto-decrement
- Wishlist / notify-when-available
- Multi-language (EN + JP)
- Shipping API integration
- Analytics dashboard

---

## Key Technical Decisions

| Decision   | Choice                                 | Why                                                          |
| ---------- | -------------------------------------- | ------------------------------------------------------------ |
| Cart state | Zustand + localStorage                 | Minimal boilerplate, built-in persist, right-sized for scope |
| Payments   | Stripe Checkout redirect               | 10x simpler, Stripe handles PCI + shipping + mobile UX       |
| ORM        | SQLAlchemy 2.0 async                   | Industry standard, best async support, valuable to learn     |
| Admin auth | JWT (single admin)                     | Simplest possible for one-person business MVP                |
| Images     | URL strings                            | Ship fast; clear migration path to S3/R2 later               |
| Email      | Resend                                 | Best DX, free tier (3k/mo), simple Python SDK                |
| Testing    | pytest + httpx (BE), vitest + msw (FE) | Modern, fast, async-native                                   |
| Deploy     | Vercel + Railway                       | Zero ops burden, focus on building the store                 |

---

## Testing Strategy

**Backend (priority):** pytest + httpx AsyncClient. Mock Stripe. Test product CRUD, checkout session creation, webhook handling, auth, edge cases (buying unavailable product, duplicate slugs).

**Frontend:** vitest for unit tests (cart store, utils), @testing-library/react for components, Playwright for E2E happy path.

**Test priority:** Backend API tests first (protect payment flow) → cart store unit tests → E2E happy path.

---

## Verification

1. `docker compose up` — all three services start, DB connects
2. Hit `localhost:8000/api/v1/health` — backend responds
3. Hit `localhost:3000` — frontend renders
4. Seed products, browse catalog, add to cart
5. Full Stripe test flow: cart → checkout → pay with test card → webhook fires → order created → confirmation page
6. Admin login → manage products → view orders
7. `pytest` passes, `npm test` passes, `npm run build` succeeds
8. Deploy to Vercel + Railway, smoke test production
