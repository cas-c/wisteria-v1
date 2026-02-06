# ADR-008: Server Components Default, Client Components for Interactivity

**Status:** Accepted

**Context:** Next.js App Router offers Server and Client Components.

**Decision:** Server Components for data-fetching pages (product listing, product detail, order confirmation). Client Components for interactive features (cart, checkout, admin panel).

**Reasoning:**
- Server Components: zero client JS, direct backend calls, better SEO, faster initial load
- Client Components: needed for state, event handlers, browser APIs (localStorage for cart)
- The split maps naturally to our features: browsing is read-only (server), cart/admin are interactive (client)

**Trade-off:** Can't use hooks in Server Components. Data flows one way (server → client via props). This is actually a good constraint — it enforces clean architecture.
