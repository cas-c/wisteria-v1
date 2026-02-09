"""Shared FastAPI dependencies.

**FastAPI dependency injection** is how cross-cutting concerns (DB sessions,
auth, rate limiting) are wired into routes without importing them directly.

Usage in a route:
    @router.get("/admin/products")
    async def list_products(
        admin: AdminUser = Depends(get_current_admin),
        db: AsyncSession = Depends(get_db),
    ):
        ...

FastAPI resolves the dependency chain automatically:
- `get_current_admin` depends on `get_db` and the `Authorization` header
- FastAPI creates the DB session, passes it to `get_current_admin`,
  then passes the resulting AdminUser to the route
- After the route returns, the DB session is closed

`get_db` lives in database.py to avoid circular imports (models import Base,
which would create a cycle if database.py imported models).
"""

import uuid

import jwt
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.models.admin_user import AdminUser
from app.utils.security import decode_token

# HTTPBearer extracts the token from the `Authorization: Bearer <token>` header.
# `auto_error=True` (default) means FastAPI returns 403 if the header is missing.
bearer_scheme = HTTPBearer()


async def get_current_admin(
    credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme),
    db: AsyncSession = Depends(get_db),
) -> AdminUser:
    """Dependency that extracts and validates the JWT, then returns the admin user.

    Raises HTTPException 401 if:
    - The token is expired or tampered with
    - The token's `sub` claim doesn't match any admin user
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid or expired token",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        payload = decode_token(credentials.credentials)
        subject = payload.get("sub")
        if subject is None:
            raise credentials_exception
    except jwt.PyJWTError:
        raise credentials_exception from None

    try:
        admin_id = uuid.UUID(subject)
    except ValueError:
        raise credentials_exception from None

    result = await db.execute(select(AdminUser).where(AdminUser.id == admin_id))
    admin = result.scalar_one_or_none()

    if admin is None:
        raise credentials_exception

    return admin
