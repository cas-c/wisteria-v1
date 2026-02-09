"""Public product routes — browsing the storefront.

These endpoints are unauthenticated — anyone can browse products.
Products are fetched by slug (URL-friendly identifier) for public
routes, keeping UUIDs internal.
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.schemas.product import (
    PaginatedProductResponse,
    ProductListParams,
    ProductResponse,
)
from app.services.product import calculate_pages, get_product_by_slug, list_products

router = APIRouter(prefix="/products", tags=["products"])


@router.get("", response_model=PaginatedProductResponse)
async def get_products(
    params: ProductListParams = Depends(),
    db: AsyncSession = Depends(get_db),
) -> PaginatedProductResponse:
    """List products with pagination and optional filters.

    Query params (all optional):
    - page, per_page: pagination
    - category: filter by ProductCategory
    - condition: filter by ProductCondition
    - search: case-insensitive name search
    - available_only: defaults to true (hides sold items)

    `Depends()` on a Pydantic model tells FastAPI to pull each field
    from query parameters. So `?page=2&category=nendoroid` populates
    the ProductListParams model automatically.
    """
    products, total = await list_products(db, params)

    return PaginatedProductResponse(
        items=[ProductResponse.model_validate(p) for p in products],
        total=total,
        page=params.page,
        per_page=params.per_page,
        pages=calculate_pages(total, params.per_page),
    )


@router.get("/{slug}", response_model=ProductResponse)
async def get_product(
    slug: str,
    db: AsyncSession = Depends(get_db),
) -> ProductResponse:
    """Get a single product by slug.

    The slug is the URL-friendly identifier used in the storefront URL:
    /products/hatsune-miku-nendoroid-2024
    """
    product = await get_product_by_slug(db, slug)

    if product is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Product not found",
        )

    return ProductResponse.model_validate(product)
