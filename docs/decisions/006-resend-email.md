# ADR-006: Resend for Transactional Email

**Status:** Accepted

**Context:** Need to send order confirmation emails.

**Decision:** Resend.

**Reasoning:**
- Best developer experience of any email provider (clean API, good docs)
- Free tier: 3,000 emails/month (more than enough for a resale shop)
- Simple Python SDK: `resend.Emails.send(from, to, subject, html)`
- No SMTP configuration, no template engines required

**Trade-off:** Vendor lock-in, but the integration is ~20 lines of code. Swappable in an hour.
