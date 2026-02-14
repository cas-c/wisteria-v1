# Phase 4B Takeaways — Cart UI Components

**Completed:** 2026-02-13
**Duration:** ~30 minutes

---

## What We Built

- CartItem component (product thumbnail, name, price, remove button)
- CartSummary component (item count and subtotal)
- CartDrawer component (slide-out panel from right)
- Updated Header with cart icon and item count badge
- Extended cart store with drawer state (persisted)

---

## Key Decisions

### CartItem: Simple and Reusable

Built as a small, focused component used in both the drawer and cart page (Phase 4C).

**Features:**
- Product image as clickable link to product detail
- Product name as clickable link
- Formatted price display
- Remove button with aria-label for accessibility
- Tailwind line-clamp for long product names

**Pattern:**
```typescript
export function CartItem({ product }: CartItemProps) {
  const removeItem = useCartStore((state) => state.removeItem);
  // ... render
}
```

Directly accesses the store's `removeItem` action — no prop drilling needed.

### CartSummary: Computed Values from Store

Uses Zustand selectors to compute total and item count on the fly.

**Why selectors:**
- Avoids storing derived data in state
- Components subscribe only to what they need
- Re-renders only when relevant data changes

**Pattern:**
```typescript
const itemCount = useCartStore(selectCartItemCount);
const total = useCartStore(selectCartTotal);
```

### CartDrawer: No Overlay, Free Navigation

**User requirement:** Allow browsing while cart is open.

**Decisions made:**
- ❌ No overlay (user rejected — would block navigation)
- ❌ No body scroll prevention (user rejected — want to scroll while cart open)
- ✅ Drawer slides out from right, stays above content
- ✅ Escape key closes drawer
- ✅ Drawer state persists across page refreshes

This creates a "persistent sidebar" UX pattern rather than a traditional modal.

**Implementation:**
- Fixed positioning with transform animation
- `translate-x-full` when closed, `translate-x-0` when open
- Tailwind transitions for smooth slide effect
- No pointer-events manipulation needed

### Drawer State Persistence

Added `isDrawerOpen`, `openDrawer`, and `closeDrawer` to the cart store.

**Why in the cart store:**
- User wanted drawer state to persist across refreshes
- Zustand's persist middleware handles it automatically
- Keeps cart-related state together
- No need for separate UI state store

**Trade-off:** Drawer state is now in localStorage. If we ever needed non-persistent drawer state, we'd need to exclude it from the persist config or use a separate store.

### Header Integration

Updated existing Header component to:
- Import cart store and selectors
- Read item count reactively
- Call `openDrawer()` on cart icon click
- Show badge when `itemCount > 0`
- Render `<CartDrawer />` component

**Badge styling:**
- Absolute positioned pill (`-top-1 -right-1`)
- Red background (`bg-accent`)
- White text, small size
- Only shown when cart has items

---

## Component Structure

```
frontend/src/components/
  cart/
    CartItem.tsx          — Product row (image, name, price, remove)
    CartSummary.tsx       — Item count + subtotal
    CartDrawer.tsx        — Slide-out panel container
  layout/
    Header.tsx            — Updated with cart icon + badge
```

All cart components are client components (`"use client"`) because they use:
- Zustand store hooks
- Event handlers (onClick)
- React hooks (useEffect)

---

## Visual Design

### CartItem
- Horizontal layout: image | info | remove button
- 80px square product image
- Border between items for visual separation
- Remove button in red for clear affordance

### CartSummary
- Border-top for section separation
- Two-line layout: item count + "Subtotal" label, then total price
- Small disclaimer text about shipping/taxes
- Semantic spacing with Tailwind space-y

### CartDrawer
- Full height, max-width 384px (max-w-md)
- Three sections: header, scrollable items, footer
- Header: "Your Cart" + close button
- Items area: scrollable with overflow-y-auto
- Footer: summary + "View Cart" button (full width)
- Empty state: centered message + link to /products

### Header Badge
- Small circular badge (20px / h-5 w-5)
- Positioned absolutely on top-right of cart icon
- Red background for high visibility
- Shows count (not just a dot)

---

## Accessibility

- Cart button has dynamic aria-label: `"Shopping cart (N items)"`
- Close button has aria-label: `"Close cart"`
- Remove button has aria-label: `"Remove {product name} from cart"`
- Escape key closes drawer (keyboard navigation)
- All interactive elements are keyboard accessible (native button elements)

---

## What We Didn't Do

- **No animations on items:** Items appear/disappear instantly when added/removed. Could add fade/slide transitions later.
- **No loading states:** Drawer assumes cart data is always available (it's in memory).
- **No empty cart illustration:** Just text for now.
- **No "Continue Shopping" button in drawer:** Only "View Cart" link. "Continue Shopping" is in empty state.

These are all polish items that can be added in Phase 7 if needed.

---

## Challenges & Solutions

### Challenge: Where to Store Drawer State?

**Options considered:**
1. React state in Header (would reset on refresh)
2. Separate Zustand store for UI state
3. Add to cart store

**Solution:** Added to cart store because user wanted persistence. Simple and works.

### Challenge: Overlay vs. Free Navigation

**Initial approach:** Traditional drawer with overlay and scroll lock.

**User feedback:** "I don't get that. I think ideally, they can navigate the site normally while the cart is open."

**Solution:** Removed overlay and scroll lock. Drawer is now a persistent sidebar that doesn't block interaction with the rest of the site. Users can:
- Scroll the page
- Click links
- Navigate
- All while cart stays open

This is an unconventional but valid UX pattern for e-commerce.

---

## Files Created

```
frontend/src/components/cart/
  CartItem.tsx              — 58 lines
  CartSummary.tsx           — 28 lines
  CartDrawer.tsx            — 99 lines
```

## Files Modified

```
frontend/src/stores/cart.ts           — Added drawer state
frontend/src/components/layout/Header.tsx  — Cart icon integration
```

---

## What's Next: Phase 4C

Wire everything together:
- Create `/cart` page (full cart view)
- Add "Add to Cart" button to product detail page
- End-to-end manual testing

Phase 4C is the integration phase — all the pieces exist, now we connect them.
