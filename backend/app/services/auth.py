"""Auth service — admin authentication logic.

Handles authenticating admin users by email + password.
The route calls this service; the service queries the DB and verifies credentials.
"""

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.admin_user import AdminUser
from app.utils.security import verify_password


async def authenticate_admin(
    session: AsyncSession,
    email: str,
    password: str,
) -> AdminUser | None:
    """Verify admin credentials and return the user if valid.

    Returns None if the email doesn't exist or the password is wrong.
    We intentionally don't distinguish between "user not found" and
    "wrong password" — this prevents attackers from enumerating valid emails.
    """
    result = await session.execute(select(AdminUser).where(AdminUser.email == email))
    admin = result.scalar_one_or_none()

    if admin is None:
        return None

    if not verify_password(password, admin.password_hash):
        return None

    return admin
