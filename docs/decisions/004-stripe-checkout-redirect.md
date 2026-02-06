# ADR-004: Stripe Checkout Redirect over Embedded or Custom Form

**Status:** Accepted

**Context:** Need to accept payments.

**Decision:** Stripe Checkout in redirect mode (customer leaves our site → pays on Stripe's page → returns).

**Reasoning:**
- PCI compliance is Stripe's problem, not ours (no card numbers touch our server)
- Stripe handles the entire payment UI, including mobile optimization, Apple Pay, Google Pay
- Shipping address collection is built into Checkout — no need to build address forms
- 90% less code than Stripe Elements (embedded card form)
- Webhook confirms payment server-side — no trusting the client

**Trade-off:** Customer leaves our site briefly. Loss of UI control. For a resale figurine shop, this is fine — trust matters more than a seamless checkout experience.

**Rejected:**
- Stripe Elements: 10x more code, we'd need our own address form, PCI scope increases
- PayPal: worse developer experience, more complex integration
