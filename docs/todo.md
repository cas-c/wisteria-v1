# Implementation Todo

Tracks remaining work across all phases.

---

## Completed

- [x] Phase 0: Scaffolding
- [x] Phase 1: Backend Foundation
- [x] Phase 2: Product CRUD + Auth
- [x] Phase 3: Frontend Product Display
- [x] Phase 4A: Cart Store & State Management
- [x] Phase 4B: Cart UI Components
- [x] Phase 4C: Cart Page & Integration
- [x] Phase 5A: Order Models, Migration, and Schemas

---

## Phase 5: Checkout + Stripe

- [x] Order + OrderItem SQLAlchemy models
- [x] Alembic migration for orders tables
- [ ] Stripe service (create_checkout_session)
- [ ] POST /checkout/create-session endpoint
- [ ] Stripe webhook endpoint (POST /webhooks/stripe)
  - [ ] Raw body handling for signature verification
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
- [ ] Admin layout with sidebar navigation + auth guard
- [ ] useAdmin hook (store JWT, login/logout, check expiry)
- [ ] Dashboard page: product count, recent orders summary
- [ ] Product management: table view, add/edit forms, soft-delete
- [ ] Order management: table view, detail, status update
- [ ] Admin CRUD backend tests

## Phase 7: Polish + Deploy

- [ ] Global error handling (error.tsx boundaries)
- [ ] Loading skeletons for all pages
- [ ] Empty states (no products, empty cart, no orders)
- [ ] Toast notification system
- [ ] SEO: meta tags, Open Graph images
- [ ] GitHub Actions CI: lint + type-check + test
- [ ] Deploy frontend to Vercel
- [ ] Deploy backend + Postgres to Railway
- [ ] Production env vars and Stripe webhook config
- [ ] Smoke test: full purchase flow
