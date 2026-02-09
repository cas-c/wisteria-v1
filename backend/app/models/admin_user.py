"""AdminUser model — store owner/admin authentication.

Simple model: email + hashed password. The password is never stored in
plaintext — only the bcrypt hash (handled by passlib in Phase 2).

Note that `created_at` and `updated_at` come from Base automatically.
AdminUser doesn't need `updated_at` much, but it's there for free.
"""

from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from app.models.base import Base


class AdminUser(Base):
    __tablename__ = "admin_users"

    email: Mapped[str] = mapped_column(String(255), unique=True, index=True)
    password_hash: Mapped[str] = mapped_column(String(255))
