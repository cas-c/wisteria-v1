"""Password hashing and JWT token utilities.

**Password hashing with bcrypt:**
bcrypt is the industry standard for password storage:
- Automatically salts passwords (no manual salt needed)
- Has a configurable "work factor" that makes brute-force attacks slow
- `checkpw()` is timing-safe to prevent timing attacks

We use the `bcrypt` library directly instead of through `passlib`.
passlib hasn't been updated for bcrypt 4.1+ and throws errors with
modern versions. Using bcrypt directly is simpler and more reliable.

**JWT with PyJWT:**
JSON Web Tokens encode a payload (claims) into a signed string.
- `sub` (subject): the user's ID — who this token is for
- `exp` (expiration): when the token expires — prevents stolen tokens from working forever
- HS256: HMAC-SHA256 signing. Symmetric key — the same secret signs and verifies.
  Good enough for a single backend. Use RS256 (asymmetric) if multiple services need to verify.

We use PyJWT (not python-jose). python-jose is unmaintained since 2022 and has
known CVEs. PyJWT has the same encode/decode API, is actively maintained, and
doesn't pull in unnecessary crypto dependencies for HS256.
"""

from datetime import UTC, datetime, timedelta

import bcrypt
import jwt

from app.config import settings


def hash_password(password: str) -> str:
    """Hash a plaintext password using bcrypt.

    `bcrypt.gensalt()` generates a random salt. The salt is embedded
    in the returned hash string, so you don't need to store it separately.
    The default work factor (rounds=12) is a good balance of security vs speed.
    """
    password_bytes = password.encode("utf-8")
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(password_bytes, salt)
    return hashed.decode("utf-8")


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify a plaintext password against a bcrypt hash.

    `bcrypt.checkpw()` extracts the salt from the stored hash, hashes the
    input with that same salt, and compares. It's timing-safe — takes the
    same time whether the password matches or not (prevents timing attacks).
    """
    return bcrypt.checkpw(
        plain_password.encode("utf-8"),
        hashed_password.encode("utf-8"),
    )


def create_access_token(subject: str, expires_delta: timedelta | None = None) -> str:
    """Create a signed JWT access token.

    Args:
        subject: The token's "sub" claim — typically the user's UUID as a string.
        expires_delta: How long until the token expires. Defaults to the
                       setting in config (24 hours).

    Returns:
        A signed JWT string.
    """
    if expires_delta is None:
        expires_delta = timedelta(minutes=settings.access_token_expire_minutes)

    expire = datetime.now(UTC) + expires_delta

    # `sub` must be a string per JWT spec. We convert UUIDs to str before passing.
    payload = {"sub": subject, "exp": expire}
    return jwt.encode(payload, settings.secret_key, algorithm="HS256")


def decode_token(token: str) -> dict[str, str]:
    """Decode and verify a JWT token.

    Raises:
        jwt.PyJWTError: If the token is expired, tampered with, or malformed.

    Returns:
        The token payload (dict with "sub", "exp", etc.).
    """
    try:
        payload: dict[str, str] = jwt.decode(token, settings.secret_key, algorithms=["HS256"])
        return payload
    except jwt.PyJWTError:
        raise
