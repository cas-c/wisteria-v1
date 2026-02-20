"""Order and OrderItem models — represent completed purchases.

Key patterns:

1. **OrderStatus enum**: Same str+Enum pattern as ProductCondition/ProductCategory.
   Values match the frontend OrderStatus type exactly.

2. **Snapshot fields on OrderItem**: `product_name` and `price_cents` capture the
   product state at purchase time. If the product is later deleted or repriced,
   the order history stays accurate.

3. **JSONB for shipping_address**: Flexible schema for address fields that may
   vary by country. Stored as a Postgres JSONB column.

4. **ForeignKey + relationship**: OrderItem links to both Order and Product.
   `back_populates` creates bidirectional navigation (order.items ↔ item.order).
   With async SQLAlchemy, always use `selectinload()` when querying —
   lazy loading doesn't work in async mode.
"""

import enum
import uuid

from sqlalchemy import Enum, ForeignKey, Integer, String
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base


class OrderStatus(str, enum.Enum):
    """Order lifecycle status. Matches frontend OrderStatus type."""

    PENDING = "pending"
    PAID = "paid"
    SHIPPED = "shipped"
    CANCELLED = "cancelled"


class Order(Base):
    __tablename__ = "orders"

    customer_email: Mapped[str] = mapped_column(String(255))
    customer_name: Mapped[str] = mapped_column(String(255))

    stripe_checkout_session_id: Mapped[str] = mapped_column(
        String(255), unique=True, index=True
    )
    stripe_payment_intent_id: Mapped[str | None] = mapped_column(
        String(255), nullable=True
    )

    status: Mapped[OrderStatus] = mapped_column(
        Enum(OrderStatus, values_callable=lambda e: [x.value for x in e]),
        default=OrderStatus.PENDING,
    )

    total_cents: Mapped[int] = mapped_column(Integer)

    shipping_address_json: Mapped[dict] = mapped_column(JSONB, default=dict)

    items: Mapped[list["OrderItem"]] = relationship(
        back_populates="order", cascade="all, delete-orphan"
    )


class OrderItem(Base):
    __tablename__ = "order_items"

    order_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("orders.id", ondelete="CASCADE"), index=True
    )
    product_id: Mapped[uuid.UUID | None] = mapped_column(
        ForeignKey("products.id", ondelete="SET NULL"), nullable=True
    )

    # Snapshot fields — survive product deletion or price changes
    product_name: Mapped[str] = mapped_column(String(255))
    price_cents: Mapped[int] = mapped_column(Integer)
    quantity: Mapped[int] = mapped_column(Integer, default=1)

    order: Mapped["Order"] = relationship(back_populates="items")
    product: Mapped["Product | None"] = relationship()
