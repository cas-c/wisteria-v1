# Phase 4C Takeaways — Cart Page & Integration

**Completed:** 2026-02-14
**Duration:** ~15 minutes

---

## What We Built

- `/cart` page (full-width cart view with empty state)
- Wired AddToCartButton to Zustand store
- Backdrop overlay on CartDrawer (click-outside-to-close)

---

## Key Decisions

### AddToCartButton: Auto-Open Drawer + Disabled State

Initial implementation just called `addItem()`. During manual testing, we
improved it to:
- Open the drawer automatically after adding an item
- Disable the button and show "In Cart" if the product is already in the cart
- Skip the duplicate toast entirely — disabled state makes it unnecessary

**Pattern:**
```typescript
const alreadyInCart = useCartStore(
  (state) => !!state.items.find((p) => p.id === product.id),
);
```

Zustand selector keeps the component subscribed to just the relevant slice
of state. Button re-renders only when this specific product's cart status
changes.

### CartDrawer: Backdrop Added After All

Phase 4B explicitly removed the overlay to allow free navigation. During 4C
manual testing, we added it back — but as a *light* backdrop (`bg-black/30`)
that simply closes the drawer on click. No scroll lock, no blocked
interaction — just a click target behind the drawer.

**Why the reversal:** Without any click-outside behavior, the only way to
close the drawer was the X button or Escape key. The backdrop feels more
natural without restricting navigation.

### Cart Page: Minimal and Functional

Two states:
1. **Empty:** Message + "Continue Shopping" button linking to `/products`
2. **With items:** CartItem list + CartSummary + "Proceed to Checkout" button
   (placeholder for Phase 5) + "Clear cart" action + "Continue shopping" link

Reuses `CartItem` and `CartSummary` from Phase 4B — no new components needed.

---

## What We Fixed Along the Way

- **`next/image` remote patterns:** `new URL()` shorthand with glob wasn't
  working in Next.js 16. Switched to the standard object-based
  `remotePatterns` config.
- **CartDrawer z-index:** Bumped from z-40 to z-50 to sit above the header.

---

## Files Created

```
frontend/src/app/cart/page.tsx       — 62 lines
```

## Files Modified

```
frontend/src/components/product/AddToCartButton.tsx  — Store integration
frontend/src/components/cart/CartDrawer.tsx           — Backdrop overlay
frontend/next.config.ts                              — Image remote patterns fix
```

---

## What's Next: Phase 5

Checkout + Stripe integration — the big one:
- Order/OrderItem models + migration
- Stripe checkout session creation
- Webhook handler for payment confirmation
- Frontend checkout flow and success page
