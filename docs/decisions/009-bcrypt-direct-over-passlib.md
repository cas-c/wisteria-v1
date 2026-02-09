# ADR-009: Direct bcrypt over passlib

**Status:** Accepted

**Context:** The original plan specified `passlib[bcrypt]` for password hashing. passlib is a popular library that wraps multiple hashing algorithms and supports transparent upgrades between schemes.

However, passlib hasn't been actively maintained since 2020. bcrypt 4.1+ changed its internal API, causing passlib to throw `ValueError: password cannot be longer than 72 bytes` during its internal wrap-bug detection. This is a known issue with no fix from the passlib maintainers.

**Decision:** Use the `bcrypt` library directly instead of through passlib.

**Reasoning:**
- passlib is effectively abandoned — no releases since 2020, known incompatibility with bcrypt 4.1+
- Using bcrypt directly is simpler: `bcrypt.hashpw()` and `bcrypt.checkpw()` vs CryptContext
- bcrypt is actively maintained by the PyCA (Python Cryptographic Authority)
- We only use one hashing scheme (bcrypt), so passlib's multi-scheme support adds no value

**Trade-off:** We lose passlib's transparent scheme migration (e.g., upgrading from bcrypt to argon2 without re-hashing). If we need to switch algorithms later, we'd need to build migration logic ourselves. For our scale, this is unlikely to matter.

**Rejected:** Pinning to an older bcrypt version — this would mean using unsupported software with potential security issues.
