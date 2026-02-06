# Architecture Decision Records

Each ADR is a short document capturing a significant technical decision.

**Format:** `NNN-short-title.md` (e.g., `001-monorepo-structure.md`)

**When to add one:** Any time you choose between two or more reasonable
approaches, or make a decision that a future reader might question.

**Template:**
```markdown
# ADR-NNN: Title

**Status:** Accepted | Revised | Superseded by ADR-NNN

**Context:** What problem are we solving? What are the options?

**Decision:** What did we choose?

**Reasoning:** Why this option over the others?

**Trade-off:** What are we giving up?

**Rejected:** (optional) What alternatives were considered?
```

## Index

| ADR | Decision | Phase |
| --- | -------- | ----- |
| [001](001-monorepo-structure.md) | Monorepo with separate backend and frontend | 0 |
| [002](002-fastapi-sqlalchemy-async.md) | FastAPI + SQLAlchemy async over Django | 0 |
| [003](003-uuids-integer-cents.md) | PostgreSQL with UUIDs and integer cents | 0 |
| [004](004-stripe-checkout-redirect.md) | Stripe Checkout redirect over embedded form | 0 |
| [005](005-zustand-cart-state.md) | Zustand over Redux or Context API | 0 |
| [006](006-resend-email.md) | Resend for transactional email | 0 |
| [007](007-docker-compose-local-dev.md) | Docker Compose for local development | 0 |
| [008](008-server-vs-client-components.md) | Server Components default, Client for interactivity | 0 |
