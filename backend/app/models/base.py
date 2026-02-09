"""Base model with common columns for all tables.

SQLAlchemy 2.0 uses the "declarative" pattern — you define Python classes
that map directly to database tables. This base class provides three columns
that every table in Wisteria shares:

- id: UUID primary key (not auto-increment integers — see ADR 003)
- created_at: timestamp set automatically on INSERT
- updated_at: timestamp set automatically on INSERT and UPDATE

Every model inherits from Base, which gives it these columns for free:

    class Product(Base):
        __tablename__ = "products"
        name: Mapped[str]
        ...

The `Mapped[...]` syntax is SQLAlchemy 2.0's typed column declaration.
It replaces the older `Column(String)` style and works well with mypy.
"""

import uuid
from datetime import datetime

from sqlalchemy import func
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):
    """Abstract base class. All models inherit from this.

    DeclarativeBase is SQLAlchemy 2.0's replacement for the older
    declarative_base() function. It integrates with Python's type system
    so mypy can check your column types.
    """

    # `Mapped[uuid.UUID]` tells both SQLAlchemy and mypy that this column
    # is a UUID. `mapped_column(primary_key=True)` makes it the PK.
    # `default=uuid.uuid4` generates a new UUID in Python when creating a row.
    # (No parentheses — we pass the function itself, not its result.)
    id: Mapped[uuid.UUID] = mapped_column(
        primary_key=True,
        default=uuid.uuid4,
    )

    # `server_default=func.now()` tells the DB to set this value,
    # not Python. This ensures consistency even if rows are inserted
    # outside the app (e.g., via a migration script).
    created_at: Mapped[datetime] = mapped_column(
        server_default=func.now(),
    )

    # `onupdate=func.now()` tells SQLAlchemy to set this on every UPDATE.
    # `server_default=func.now()` sets it on INSERT too.
    updated_at: Mapped[datetime] = mapped_column(
        server_default=func.now(),
        onupdate=func.now(),
    )
