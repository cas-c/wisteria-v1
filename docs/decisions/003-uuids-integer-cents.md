# ADR-003: PostgreSQL with UUIDs and Integer Cents

**Status:** Accepted

**Context:** Need a database schema for products and orders.

**Decision:**
- PostgreSQL 16 (via Docker)
- UUIDs for all primary keys
- Money stored as integer cents (`price_cents INTEGER`)
- Slugs for public-facing URLs

**Reasoning:**
- **UUIDs**: prevent enumeration attacks (`/products/1`, `/products/2`), safe for client-side exposure, no sequence leaks. Slight performance cost vs auto-increment, negligible at our scale.
- **Integer cents**: floating-point math breaks with money (`0.1 + 0.2 ≠ 0.3`). Stripe uses cents. Every e-commerce system stores money as integers. This is non-negotiable.
- **Slugs**: SEO-friendly URLs (`/products/hatsune-miku-nendoroid` vs `/products/550e8400-...`). Slug is a UNIQUE column; we look up by slug for public routes, by UUID for admin routes.

**Trade-off:** UUIDs are 16 bytes vs 4 bytes for integers, slightly larger indexes. Doesn't matter until millions of rows.
