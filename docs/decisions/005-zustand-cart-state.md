# ADR-005: Zustand over Redux or Context API for Cart State

**Status:** Accepted

**Context:** Need client-side cart state that persists across page reloads.

**Decision:** Zustand with `persist` middleware (localStorage).

**Reasoning:**
- Zustand: ~1KB, no boilerplate (no reducers, no actions, no providers)
- Built-in `persist` middleware writes to localStorage automatically
- Works outside React components (can access store in `lib/` functions)
- Right-sized: Redux is overkill for a cart, Context causes re-render cascades

**Trade-off:** Less structured than Redux for very large state. Our cart state is ~5 fields; this is perfect.
