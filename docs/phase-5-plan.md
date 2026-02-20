# Phase 5: Checkout + Stripe — Implementation Plan

## Context

Phase 4 (cart) is complete. Users can browse products, add to cart, and view their cart. The "Proceed to Checkout" button exists but isn't wired. Phase 5 adds the payment flow: Stripe Checkout redirect, webhook-based order creation, confirmation email, and frontend checkout/success pages.

This phase touches ~15 files (new + modified), so it's broken into 5 subphases.

---

## Subphase 5A: Order Models, Migration, and Schemas

**New files:**
- `backend/app/models/order.py` — Order + OrderItem models, OrderStatus enum
- `backend/app/schemas/order.py` — OrderResponse, OrderItemResponse, CheckoutRequest, CheckoutResponse

**Modified files:**
- `backend/app/models/__init__.py` — export Order, OrderItem, OrderStatus

**Then:** Run Alembic autogenerate + review + apply migration inside Docker.

### Model design

```
Order (extends Base):
  customer_email: str
  customer_name: str
  stripe_checkout_session_id: str (unique)
  stripe_payment_intent_id: str | None
  status: OrderStatus (pending/paid/shipped/cancelled)
  total_cents: int
  shipping_address_json: dict (JSONB)
  items: relationship → OrderItem[]

OrderItem (extends Base):
  order_id: UUID (FK → orders.id)
  product_id: UUID (FK → products.id)
  product_name: str (snapshot — survives product deletion)
  price_cents: int (snapshot — price at time of purchase)
  quantity: int (default 1)
  order: relationship → Order
  product: relationship → Product
```

Using `price_cents` (not `unit_price_cents`) to match the existing frontend `OrderItem` type. The `product_name` snapshot field needs adding to the frontend type.

### Schemas

- `CheckoutRequest`: `items: list[CheckoutLineItem]` where each has `product_id: UUID`
- `CheckoutResponse`: `checkout_url: str, session_id: str`
- `OrderResponse` / `OrderItemResponse`: mirror models with `ConfigDict(from_attributes=True)`

---

## Subphase 5B: Checkout Endpoint (TDD)

**New files:**
- `backend/app/services/stripe.py` — `create_checkout_session()`
- `backend/app/routers/checkout.py` — `POST /checkout/create-session`
- `backend/tests/test_checkout.py` — tests (written first)

**Modified files:**
- `backend/app/main.py` — register checkout router

### Checkout flow

1. Frontend POSTs `{ items: [{ product_id }] }` (no prices — never trust the client)
2. Backend looks up products by ID, verifies all `is_available`
3. Creates Stripe Checkout Session with `price_data` (inline pricing) and `metadata.product_ids`
4. Returns `{ checkout_url, session_id }`

### Key decisions

- **Inline `price_data`** instead of pre-created Stripe Prices — simpler for unique resale items
- **Product IDs in session `metadata`** — webhook reads these to know which products were purchased
- **Mock `stripe.checkout.Session.create`** in tests — never hit real Stripe API
- Unavailable product → 409, nonexistent product → 404

### Tests (write first)

- Happy path: valid items → 200 with checkout_url
- Empty items → 422
- Unavailable product → 409
- Nonexistent product → 404
- Verifies DB prices used (not client prices)

---

## Subphase 5C: Webhook Handler + Order Service (TDD)

**New files:**
- `backend/app/services/order.py` — `create_order_from_checkout()`, `get_order_by_id()`, `get_order_by_session_id()`
- `backend/app/routers/webhooks.py` — `POST /webhooks/stripe`
- `backend/tests/test_webhooks.py` — tests (written first)

**Modified files:**
- `backend/app/main.py` — register webhooks router

### Critical: raw body for signature verification

```python
payload = await request.body()  # raw bytes, NOT a Pydantic model
sig = request.headers.get("stripe-signature")
event = stripe.Webhook.construct_event(payload, sig, webhook_secret)
```

### Order creation (in webhook, NOT checkout endpoint)

1. Parse `product_ids` from session metadata
2. `SELECT ... FOR UPDATE` on those products (race condition protection)
3. Create Order with customer info from Stripe session data
4. Create OrderItems with snapshot pricing from DB
5. Mark all products `is_available = False`
6. Single commit (atomic transaction)

### Eager loading

Must use `selectinload(Order.items)` when fetching orders — async SQLAlchemy doesn't support lazy loading.

### Tests (write first)

- Mock `stripe.Webhook.construct_event` (bypass signature check)
- Happy path: creates order, order items, marks products unavailable
- Invalid/missing signature → 400
- Unhandled event type → 200 (ignore gracefully)
- Duplicate session_id → idempotent (no crash)

---

## Subphase 5D: Email Service, Order Retrieval, Body Size Limit

**New files:**
- `backend/app/services/email.py` — `send_order_confirmation()` via Resend
- `backend/app/routers/orders.py` — `GET /orders/{id}`, `GET /orders/by-session/{session_id}`
- `backend/tests/test_orders.py`

**Modified files:**
- `backend/app/routers/webhooks.py` — call email service after order creation
- `backend/app/main.py` — register orders router, add body size limit middleware

### Email

- Resend SDK is sync — call directly for MVP (it's a fast HTTP call)
- Mock `resend.Emails.send` in tests
- Use `onboarding@resend.dev` as `from` for dev (no domain verification needed)

### Order retrieval

Two access patterns:
- `GET /orders/{id}` — by UUID (for admin, confirmation links)
- `GET /orders/by-session/{session_id}` — by Stripe session ID (for success page redirect)

Both public (UUIDs and session IDs are unguessable). Route `by-session/` registered first to avoid path conflicts.

### Body size limit

Middleware rejecting requests > 1MB. Stripe webhooks are typically <10KB.

---

## Subphase 5E: Frontend Checkout + Success Pages

**New files:**
- `frontend/src/app/checkout/page.tsx` — review cart, redirect to Stripe
- `frontend/src/app/checkout/success/page.tsx` — order confirmation

**Modified files:**
- `frontend/src/app/cart/page.tsx` — wire "Proceed to Checkout" as link to `/checkout`
- `frontend/src/types/index.ts` — add `product_name` to `OrderItem`

### Checkout page (client component)

1. Read cart from Zustand
2. Display order review (items, prices, total)
3. "Pay with Stripe" button → POST to `/checkout/create-session` → redirect to `checkout_url`
4. Uses `API_BASE_URL_CLIENT` (browser-side fetch, not Docker internal URL)
5. Handle loading state + errors (409 = item unavailable)
6. Empty cart → redirect to `/cart`

### Success page

1. Read `session_id` from URL search params
2. Fetch order via `GET /orders/by-session/{session_id}`
3. Display confirmation: order details, items, total
4. Clear cart via small client component (`<ClearCartEffect />`)
5. Link back to `/products`

### Cart page update

Wire "Proceed to Checkout" button with `href="/checkout"`.

---

## Docker Compose

Add Stripe env vars to backend service:
```yaml
STRIPE_SECRET_KEY: ${STRIPE_SECRET_KEY}
STRIPE_WEBHOOK_SECRET: ${STRIPE_WEBHOOK_SECRET}
RESEND_API_KEY: ${RESEND_API_KEY}
```

These read from the host's `.env` or shell environment, keeping secrets out of the compose file.

---

## Verification

After each subphase, run tests inside Docker:
```
docker compose -f docker/docker-compose.yml exec backend pytest tests/ -v
```

After 5E, full manual test:
1. Browse → add items to cart → go to `/checkout`
2. Click "Pay with Stripe" → redirected to Stripe test checkout
3. Use test card `4242 4242 4242 4242` → complete payment
4. Redirected to `/checkout/success` → order confirmation displayed
5. Cart is cleared
6. Product detail page shows item as unavailable

This requires `stripe listen --forward-to localhost:8000/api/v1/webhooks/stripe` running locally.
