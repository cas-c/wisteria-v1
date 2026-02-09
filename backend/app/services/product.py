"""Product service — business logic for product operations.

The service layer pattern keeps routes thin: routes handle HTTP concerns
(parsing the request, returning the response), while services contain
the actual logic (queries, validation, transformations).

Each function takes `AsyncSession` as its first argument — injected by
the route via FastAPI's dependency injection. This makes the service
testable (you can pass a test session) and keeps it decoupled from
the web framework.

**SQLAlchemy async query patterns used here:**
- `select(Product).where(...)` — builds a SELECT query
- `session.execute(stmt)` — runs it, returns a `Result` object
- `result.scalars().all()` — extracts the ORM objects from the result rows
- `result.scalar_one_or_none()` — returns one object or None
- `session.add(obj)` → `session.commit()` — INSERT or UPDATE
"""

import math
import uuid

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.product import Product
from app.schemas.product import ProductCreate, ProductListParams, ProductUpdate


async def list_products(
    session: AsyncSession,
    params: ProductListParams,
) -> tuple[list[Product], int]:
    """List products with pagination and optional filters.

    Returns:
        A tuple of (products, total_count) for building paginated responses.
    """
    # Build the base query — SELECT * FROM products
    query = select(Product)

    # Apply filters conditionally. Each `.where()` ANDs another condition.
    if params.available_only:
        query = query.where(Product.is_available.is_(True))
    if params.category is not None:
        query = query.where(Product.category == params.category)
    if params.condition is not None:
        query = query.where(Product.condition == params.condition)
    if params.search is not None:
        # `ilike` is case-insensitive LIKE — Postgres-specific.
        # The `%` wildcards match any characters before/after the search term.
        query = query.where(Product.name.ilike(f"%{params.search}%"))

    # Count total matching rows (before pagination) for the "pages" field.
    count_query = select(func.count()).select_from(query.subquery())
    total_result = await session.execute(count_query)
    total = total_result.scalar_one()

    # Apply pagination: OFFSET = skip rows, LIMIT = max rows returned.
    offset = (params.page - 1) * params.per_page
    query = query.order_by(Product.created_at.desc()).offset(offset).limit(params.per_page)

    result = await session.execute(query)
    products = list(result.scalars().all())

    return products, total


async def get_product_by_slug(session: AsyncSession, slug: str) -> Product | None:
    """Fetch a single product by its URL-friendly slug."""
    result = await session.execute(select(Product).where(Product.slug == slug))
    return result.scalar_one_or_none()


async def get_product_by_id(session: AsyncSession, product_id: uuid.UUID) -> Product | None:
    """Fetch a single product by UUID (for admin routes)."""
    result = await session.execute(select(Product).where(Product.id == product_id))
    return result.scalar_one_or_none()


async def create_product(session: AsyncSession, data: ProductCreate) -> Product:
    """Create a new product.

    `model_dump()` converts the Pydantic schema to a dict, which we
    unpack into the SQLAlchemy model constructor with `**`.
    """
    product = Product(**data.model_dump())
    session.add(product)
    await session.commit()
    # Refresh loads the DB-generated fields (id, created_at, updated_at)
    # back into the Python object.
    await session.refresh(product)
    return product


async def update_product(
    session: AsyncSession,
    product: Product,
    data: ProductUpdate,
) -> Product:
    """Update an existing product with partial data.

    `exclude_unset=True` is the key pattern here — it only returns fields
    the client actually sent in the request body. If the client sends
    `{"name": "New Name"}`, only `name` is in the dict. Fields not sent
    (like `price_cents`) are excluded, so they keep their current values.

    Without `exclude_unset`, all optional fields would default to None
    and overwrite existing data.
    """
    update_data = data.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(product, field, value)
    await session.commit()
    await session.refresh(product)
    return product


async def soft_delete_product(session: AsyncSession, product: Product) -> Product:
    """Soft-delete a product by marking it unavailable.

    We never hard-delete products because they might be referenced
    by existing orders. Setting `is_available = False` hides them
    from the storefront while preserving order history.
    """
    product.is_available = False
    await session.commit()
    await session.refresh(product)
    return product


def calculate_pages(total: int, per_page: int) -> int:
    """Calculate total number of pages for pagination."""
    return max(1, math.ceil(total / per_page))
