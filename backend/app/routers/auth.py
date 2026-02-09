"""Auth routes — admin login.

This router handles authentication. It's intentionally thin:
- Parses the request body (LoginRequest)
- Delegates credential verification to the auth service
- Returns a JWT on success or 401 on failure

The JWT is then sent by the frontend in the `Authorization: Bearer <token>`
header on subsequent requests to admin-only endpoints.
"""

from fastapi import APIRouter, Depends, HTTPException, Request, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.rate_limit import limiter
from app.schemas.auth import LoginRequest, TokenResponse
from app.services.auth import authenticate_admin
from app.utils.security import create_access_token

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/login", response_model=TokenResponse)
@limiter.limit("5/minute")
async def login(
    request: Request,
    body: LoginRequest,
    db: AsyncSession = Depends(get_db),
) -> TokenResponse:
    """Authenticate an admin user and return a JWT.

    The generic "Invalid email or password" message is intentional —
    we don't reveal whether the email exists. This is a security
    best practice to prevent user enumeration attacks.
    """
    admin = await authenticate_admin(db, body.email, body.password)

    if admin is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password",
        )

    token = create_access_token(subject=str(admin.id))
    return TokenResponse(access_token=token)
