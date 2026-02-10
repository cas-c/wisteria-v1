# Phase 3 Takeaways: Frontend Product Display

**Completed:** 2026-02-09

Phase 3 built the entire customer-facing storefront with Next.js 15+ App Router, Tailwind CSS 4, and Server Components.

---

## What Was Built

### Foundation (3 files modified)

- **globals.css** — Full theme with CSS custom properties for light/dark mode, wisteria violet accent (#8B5CF6), badge colors for product conditions
- **api.ts** — Added `next: { revalidate }` support for ISR caching
- **layout.tsx** — Added Playfair Display font, updated metadata, wrapped with Header/Footer

### Components (14 files created)

**UI Primitives** (5):

- Button, Card, Badge, Skeleton, Input

**Layout** (3):

- Header (sticky with backdrop blur, cart icon, mobile menu toggle)
- MobileNav (full-screen overlay with escape key handling)
- Footer (logo, links, copyright)

**Product** (6):

- ProductImage (colored placeholder divs by category)
- ConditionBadge (theme-aware condition labels)
- ProductCard (composable card for grid display)
- ProductGrid (responsive 1→4 column grid with empty state)
- ProductCardSkeleton (loading placeholder)
- AddToCartButton (placeholder for Phase 4, logs to console)

### Pages (6 files created)

- Homepage: Hero section + "Latest Arrivals" grid (8 products)
- Catalog: "Shop All" with pagination (12 products per page)
- Product Detail: 2-column layout with image, info, and add-to-cart
- Loading skeletons for all three pages

---

## Key Patterns

### Next.js 15+ Conventions

**params and searchParams are Promises:**

```typescript
async function Page({ params, searchParams }: PageProps) {
  const { slug } = await params;
  const filters = await searchParams;
  // ...
}
```

**Default exports required for pages:**

```typescript
function HomePage() {
  /* ... */
}
export { HomePage as default };
```

We use the "export as default" pattern to keep named exports for clarity while satisfying Next.js requirements.

### Server vs Client Components

**Default to Server Components.** Only use `"use client"` when you need:

- State (`useState`, `useReducer`)
- Effects (`useEffect`, `useRef`)
- Event handlers (`onClick`, `onChange`)
- Browser APIs (`localStorage`, `window`)

**In Phase 3:**

- **Server**: Button (when used as link), Card, Badge, Skeleton, Footer, all product components, all pages
- **Client**: Input, Header, MobileNav, AddToCartButton

### Docker Networking for SSR/ISR

**Problem:** Next.js Server Components fetch data at build/request time (server-side), but Docker containers can't reach `localhost:8000`.

**Solution:** Separate API URLs for server vs client:

```typescript
// constants.ts
export const API_BASE_URL =
  process.env.API_URL_INTERNAL ?? // http://backend:8000 (Docker network)
  process.env.NEXT_PUBLIC_API_URL ?? // http://localhost:8000 (browser)
  "http://localhost:8000/api/v1";
```

**docker-compose.yml:**

```yaml
environment:
  # Browser uses localhost (outside Docker network)
  NEXT_PUBLIC_API_URL: http://localhost:8000/api/v1
  # SSR uses Docker service name (inside Docker network)
  API_URL_INTERNAL: http://backend:8000/api/v1
```

### Tailwind CSS 4 @theme Syntax

**CSS custom properties + @theme inline:**

```css
:root {
  --accent: #8b5cf6;
}

@theme inline {
  --color-accent: var(--accent);
}
```

**Usage in components:**

```tsx
<div className="bg-accent text-accent-foreground">
```

Tailwind 4 requires `@theme inline` (not `@theme`) when values reference `var(...)`.

### ISR (Incremental Static Regeneration)

**Revalidate every 60 seconds:**

```typescript
const data = await api<Product>("/products/slug", {
  next: { revalidate: 60 },
});
```

This enables:

- Fast page loads (served from cache)
- Fresh data every minute (revalidated in the background)
- No client-side loading spinners for cached pages

---

## Gotchas & Solutions

### 1. Docker Container Restart ≠ Env Var Update

**Problem:** `docker compose restart frontend` doesn't pick up new env vars.

**Solution:** Use `--force-recreate`:

```bash
docker compose up -d --force-recreate frontend
```

### 2. TypeScript Unused Imports

**Problem:** IDE shows diagnostics for unused imports even if they're needed later.

**Solution:** Clean up imports immediately, don't defer to "later."

### 3. Mobile Menu Body Scroll Lock

**Pattern:**

```typescript
useEffect(() => {
  if (isOpen) {
    document.body.style.overflow = "hidden";
  } else {
    document.body.style.overflow = "";
  }
  return () => {
    document.body.style.overflow = "";
  };
}, [isOpen]);
```

Always restore `overflow` in the cleanup function to prevent scroll-lock bugs.

---

## Design Decisions

### Theme Colors

- **Accent:** Wisteria violet (`#8B5CF6` = Tailwind violet-500)
- **Background:** Soft stone/cream (`#fafaf9` light, `#1c1917` dark)
- **Badge colors:** Green (new), Blue (like new), Amber (used)

### Placeholder Images

Colored divs instead of external placeholders:

- Scale figures → violet
- Nendoroids → rose
- Figmas → amber
- Prize figures → sky

This avoids external dependencies and matches the brand aesthetic.

### Loading Skeletons

Every page has a matching loading state to prevent layout shift. Skeletons use `animate-pulse` and match the real component structure.

---

## What's Next

## Phase 4 will add the cart with Zustand, enabling users to add products and proceed to checkout. The `AddToCartButton` is already in place as a placeholder.

## Testing: Playwright E2E Tests

Phase 3 was completed with comprehensive E2E tests using Playwright. This section documents the testing approach.

### Test Architecture

**5 test files in `frontend/tests/e2e/`:**

1. **homepage.spec.ts** — Hero section, Latest Arrivals grid, product cards, navigation
2. **catalog.spec.ts** — Product listing, pagination, responsive grid layout
3. **product-detail.spec.ts** — Product display, price/badge/description, add-to-cart button
4. **responsive.spec.ts** — Mobile (375px), tablet (768px), desktop (1280px) viewports
5. **loading.spec.ts** — Skeleton display under slow network conditions (Slow 3G throttling)

**Total: ~25 tests covering:**

- Visual rendering and content
- User navigation flows
- Responsive breakpoints
- Accessibility selectors (getByRole, getByText)
- Network throttling and loading states

### Playwright Configuration

**playwright.config.ts settings:**

- **baseURL:** `http://localhost:3000` (frontend service in Docker stack)
- **Test directory:** `frontend/tests/e2e/`
- **Browsers:** Chromium, Firefox, WebKit (all three run by default)
- **Artifacts:** Screenshots and videos on failure, traces on retry
- **Retries:** 0 in dev, 2 in CI (for flaky tests)
- **Timeout:** 30 seconds per test, 120 seconds for server startup

### Key Testing Patterns

**1. Accessibility-First Selectors**

```typescript
// ✅ DO: Use semantic selectors
page.getByRole("heading", { name: "Wisteria" });
page.getByText("Curated Japanese figurines");

// ❌ AVOID: CSS selectors
page.locator(".hero h1");
```

**2. beforeEach Navigation**

```typescript
test.describe("Homepage", () => {
  test.beforeEach(async ({ page }) => {
    await page.goto("/");
  });

  test("displays hero section", async ({ page }) => {
    // No need to navigate again — beforeEach handles it
  });
});
```

**3. Responsive Testing with Browser Contexts**

```typescript
const context = await browser.newContext({
  viewport: { width: 375, height: 812 }, // Mobile
});
const page = await context.newPage();
```

**4. Network Throttling for Loading States**

```typescript
const client = await context.newCDPSession(page);
await client.send("Network.emulateNetworkConditions", {
  offline: false,
  downloadThroughput: (500 * 1000) / 8, // 500 kb/s
  latency: 400, // 400ms latency
});
await page.goto("/products", { waitUntil: "networkidle" });
```

**5. Console Log Assertions**

```typescript
const consoleLogs: string[] = [];
page.on("console", (msg) => {
  if (msg.type() === "log") {
    consoleLogs.push(msg.text());
  }
});

// Click button
await button.click();

// Assert console output
const log = consoleLogs.find((l) => l.includes("Add to cart:"));
expect(log).toBeDefined();
```

### Running Tests

```bash
# Against running Docker stack
docker compose -f docker/docker-compose.yml up  # Terminal 1
cd frontend && npm run test:e2e                 # Terminal 2

# Interactive debugging
npm run test:e2e:ui

# Headed mode (watch browsers)
npm run test:e2e:headed

# Specific test file
npx playwright test tests/e2e/homepage.spec.ts

# Specific test
npx playwright test -g "displays hero section"
```

### Test Data Assumptions

- Backend seed data: 9 product records (from `scripts/seed.py`)
- At least one product has slug `rem-1-7-scale-figure` (used for product detail tests)
- Pagination only shows when total products > per_page (12) — current seed has 9, so pagination tests check for conditional existence

### Future Considerations

- **CI Integration:** Add Playwright tests to GitHub Actions (after deploy pipeline is set up)
- **Visual Regression:** Could add Playwright's visual comparison feature for screenshot diffs
- **Performance Tracing:** Capture detailed traces of slow operations for optimization
- **Admin Panel E2E:** Phase 6 will need similar test coverage for admin CRUD flows
