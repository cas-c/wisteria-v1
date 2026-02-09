"""Product model — represents a figurine for sale.

Key patterns introduced here:

1. **Python Enum → SQLAlchemy Enum**: We define standard Python `enum.Enum`
   classes, then SQLAlchemy maps them to a Postgres ENUM type. The DB stores
   the *string value* (e.g., "like_new"), not the Python name. This is
   controlled by `values_callable=lambda e: [x.value for x in e]`.

2. **Mapped[...] with mapped_column(...)**: SQLAlchemy 2.0's typed column
   syntax. The `Mapped[str]` annotation tells mypy the type; the
   `mapped_column(...)` call configures the DB column (length, unique, etc.).
   If you just write `Mapped[str]` with no mapped_column, SQLAlchemy infers
   a VARCHAR with no length limit.

3. **unique=True on slug**: Enforced at the DB level. Even if our app code
   has a bug, the DB will reject duplicate slugs. Defense in depth.
"""

import enum

from sqlalchemy import Boolean, Enum, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.models.base import Base


class ProductCondition(str, enum.Enum):
    """Condition of the figurine.

    Inheriting from `str` lets us do `ProductCondition.NEW == "new"` → True,
    which makes JSON serialization simpler (Pydantic can serialize it as a plain string).
    """

    NEW = "new"
    LIKE_NEW = "like_new"
    USED = "used"


class ProductCategory(str, enum.Enum):
    """Product category. Matches the frontend ProductCategory type."""

    NENDOROID = "nendoroid"
    SCALE_FIGURE = "scale_figure"
    PLUSH = "plush"
    GOODS = "goods"


class Product(Base):
    __tablename__ = "products"

    name: Mapped[str] = mapped_column(String(255))
    slug: Mapped[str] = mapped_column(String(255), unique=True, index=True)
    description: Mapped[str] = mapped_column(Text)

    # Money as integer cents — never float. See ADR 003.
    price_cents: Mapped[int] = mapped_column(Integer)

    # SQLAlchemy Enum: `values_callable` tells it to use the enum *values*
    # ("new", "like_new") as the DB values, not the Python *names* ("NEW", "LIKE_NEW").
    # `native_enum=True` (default) creates a real Postgres ENUM type.
    condition: Mapped[ProductCondition] = mapped_column(
        Enum(ProductCondition, values_callable=lambda e: [x.value for x in e]),
    )
    category: Mapped[ProductCategory] = mapped_column(
        Enum(ProductCategory, values_callable=lambda e: [x.value for x in e]),
    )

    image_url: Mapped[str] = mapped_column(String(2048))
    is_available: Mapped[bool] = mapped_column(Boolean, default=True)

    # Usually 1 for resale items. Kept for flexibility.
    quantity: Mapped[int] = mapped_column(Integer, default=1)
