"""Pydantic schemas for Product request/response validation.

Pydantic v2 schemas serve as the "contract" between API and clients.
They control exactly which fields are exposed in responses and validated
in requests. We NEVER return raw SQLAlchemy models from routes —
always convert to a schema first.

Key Pydantic v2 patterns:
- `model_config = ConfigDict(from_attributes=True)` lets you do
  `ProductResponse.model_validate(sqlalchemy_obj)` to convert from
  a SQLAlchemy model instance to a Pydantic schema.
- `Field(ge=0)` is a validator: greater-than-or-equal-to 0.
- Optional fields in `ProductUpdate` use `None` defaults so you can
  send a partial update (only the fields you want to change).
"""

import uuid
from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field

from app.models.product import ProductCategory, ProductCondition


class ProductCreate(BaseModel):
    """Schema for creating a new product (admin-only)."""

    name: str = Field(min_length=1, max_length=255)
    slug: str = Field(min_length=1, max_length=255, pattern=r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
    description: str = Field(min_length=1)
    price_cents: int = Field(ge=1)
    condition: ProductCondition
    category: ProductCategory
    image_url: str = Field(min_length=1, max_length=2048)
    quantity: int = Field(ge=0, default=1)


class ProductUpdate(BaseModel):
    """Schema for updating a product (admin-only).

    All fields are optional — send only what you want to change.
    This is the "partial update" pattern. FastAPI's `model.model_dump(exclude_unset=True)`
    returns only the fields the client actually sent, so unchanged fields
    aren't overwritten with None.
    """

    name: str | None = Field(default=None, min_length=1, max_length=255)
    slug: str | None = Field(
        default=None, min_length=1, max_length=255, pattern=r"^[a-z0-9]+(?:-[a-z0-9]+)*$"
    )
    description: str | None = Field(default=None, min_length=1)
    price_cents: int | None = Field(default=None, ge=1)
    condition: ProductCondition | None = None
    category: ProductCategory | None = None
    image_url: str | None = Field(default=None, min_length=1, max_length=2048)
    is_available: bool | None = None
    quantity: int | None = Field(default=None, ge=0)


class ProductResponse(BaseModel):
    """Schema for product in API responses.

    `from_attributes=True` enables:
        product_schema = ProductResponse.model_validate(sqlalchemy_product)
    This reads attributes from the SQLAlchemy object and builds the Pydantic model.
    Without it, Pydantic would expect a dict, not an ORM object.
    """

    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    name: str
    slug: str
    description: str
    price_cents: int
    condition: ProductCondition
    category: ProductCategory
    image_url: str
    is_available: bool
    quantity: int
    created_at: datetime
    updated_at: datetime


class ProductListParams(BaseModel):
    """Query parameters for the product list endpoint.

    Using a Pydantic model for query params keeps validation clean.
    FastAPI can inject this via `Depends(ProductListParams)`.
    """

    page: int = Field(ge=1, default=1)
    per_page: int = Field(ge=1, le=100, default=20)
    category: ProductCategory | None = None
    condition: ProductCondition | None = None
    search: str | None = None
    available_only: bool = True


class PaginatedProductResponse(BaseModel):
    """Paginated response wrapper for product lists."""

    items: list[ProductResponse]
    total: int
    page: int
    per_page: int
    pages: int
