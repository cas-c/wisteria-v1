# ADR-012: Security Hardening Plan

**Status:** Accepted

**Context:** End-of-Phase-2 security audit of the FastAPI backend. The app
has solid foundations (CORS locked down, bcrypt hashing, no user enumeration,
Pydantic schema validation, UUID primary keys) but several gaps that are
commonly exploited in production FastAPI apps.

**Findings and plan:**

## Must fix before deploy

### 1. Rate limiting on `/auth/login` — Phase 2 (now)
**Risk:** Unlimited brute-force attempts on admin password.
**Fix:** Add `slowapi` — 5 attempts/minute/IP on login.
**Status:** DONE — `slowapi==0.1.9`, limiter in `app/rate_limit.py`, applied to `/auth/login`.

### 2. Replace `python-jose` with `PyJWT` — Phase 2 (now)
**Risk:** python-jose is unmaintained (last release 2022), has known CVEs
in RSA/EC operations, and uses deprecated `datetime.utcnow()`.
**Fix:** Swap to `PyJWT`. API is nearly identical — `jwt.encode()`/`jwt.decode()`
with minor argument name differences.
**Status:** DONE — `PyJWT==2.10.1` replaced `python-jose[cryptography]==3.3.0`.
Updated `security.py`, `dependencies.py`. Exception class: `jwt.PyJWTError`.

### 3. Request body size limit — Phase 5 (checkout)
**Risk:** DoS via oversized POST bodies (e.g., 500MB JSON to `/auth/login`).
**Fix:** Set `--limit-request-body` in uvicorn or add size-limiting middleware.
**Status:** TODO

### 4. Security headers middleware — Phase 7 (deploy)
**Risk:** Missing `X-Content-Type-Options`, `Strict-Transport-Security`, etc.
Browsers can't enforce security policies without these headers.
**Fix:** ~10-line middleware that sets standard security headers on all responses.
**Status:** TODO

### 5. Token revocation — Phase 6 (admin panel)
**Risk:** Compromised JWTs valid for full 24-hour lifetime with no way to
invalidate them.
**Fix:** Shorten token lifetime to 1 hour. Add a token denylist table
(checked in `get_current_admin`). Clear denylist entries older than the
max token lifetime via a periodic task or on-read cleanup.
**Status:** TODO

## Already handled

| Concern | How |
|---|---|
| Predictable SECRET_KEY default | Removed default — app won't start without env var |
| User enumeration on login | Generic "Invalid email or password" for both cases |
| Algorithm confusion (JWT) | `algorithms=["HS256"]` pinned in `decode_token` |
| Mass assignment | Pydantic schemas whitelist allowed fields |
| ID enumeration | UUID primary keys, not sequential integers |
| CORS | Locked to `frontend_url`, not `*` |
| SQL injection | SQLAlchemy ORM parameterizes all queries |
| Password hashing | bcrypt with work factor 12, timing-safe verify |
| Brute-force login | slowapi rate limit: 5/minute/IP on `/auth/login` |
| Unmaintained JWT lib | Replaced python-jose with PyJWT |

## Not applicable yet (revisit when relevant)

| Concern | When |
|---|---|
| CSRF | Only if we switch from Bearer tokens to cookie auth |
| SSRF | Only if we add user-controlled URL fetching |
| File upload abuse | Phase 6 if product image uploads are added |
| Debug mode in production | Verify `DEBUG=false` at deploy time (Phase 7) |
