"""Admin product routes — CRUD for store management.

All routes in this router require a valid admin JWT via `get_current_admin`.
Products are referenced by UUID in admin routes (not slug), because admins
might change the slug during an edit.

**Why a separate router from public products?**
- Different auth requirements (all admin routes need JWT)
- Different URL structure (/admin/products/{id} vs /products/{slug})
- Cleaner separation of concerns in the codebase
"""

import uuid

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.dependencies import get_current_admin
from app.models.admin_user import AdminUser
from app.schemas.product import (
    PaginatedProductResponse,
    ProductCreate,
    ProductListParams,
    ProductResponse,
    ProductUpdate,
)
from app.services.product import (
    calculate_pages,
    create_product,
    get_product_by_id,
    list_products,
    soft_delete_product,
    update_product,
)

router = APIRouter(prefix="/admin/products", tags=["admin-products"])


@router.get("", response_model=PaginatedProductResponse)
async def admin_list_products(
    params: ProductListParams = Depends(),
    _admin: AdminUser = Depends(get_current_admin),
    db: AsyncSession = Depends(get_db),
) -> PaginatedProductResponse:
    """List all products (including unavailable) for admin management.

    The `_admin` parameter uses an underscore prefix because we don't
    use the admin object in this route — we only need the dependency
    to run for its auth side effect (rejecting unauthenticated requests).
    """
    # Admins see all products, including unavailable ones
    params.available_only = False
    products, total = await list_products(db, params)

    return PaginatedProductResponse(
        items=[ProductResponse.model_validate(p) for p in products],
        total=total,
        page=params.page,
        per_page=params.per_page,
        pages=calculate_pages(total, params.per_page),
    )


@router.post("", response_model=ProductResponse, status_code=status.HTTP_201_CREATED)
async def admin_create_product(
    body: ProductCreate,
    _admin: AdminUser = Depends(get_current_admin),
    db: AsyncSession = Depends(get_db),
) -> ProductResponse:
    """Create a new product."""
    try:
        product = await create_product(db, body)
    except IntegrityError as exc:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="A product with this slug already exists",
        ) from exc
    return ProductResponse.model_validate(product)


@router.get("/{product_id}", response_model=ProductResponse)
async def admin_get_product(
    product_id: uuid.UUID,
    _admin: AdminUser = Depends(get_current_admin),
    db: AsyncSession = Depends(get_db),
) -> ProductResponse:
    """Get a single product by UUID."""
    product = await get_product_by_id(db, product_id)

    if product is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Product not found",
        )

    return ProductResponse.model_validate(product)


@router.put("/{product_id}", response_model=ProductResponse)
async def admin_update_product(
    product_id: uuid.UUID,
    body: ProductUpdate,
    _admin: AdminUser = Depends(get_current_admin),
    db: AsyncSession = Depends(get_db),
) -> ProductResponse:
    """Update a product (partial update — send only changed fields)."""
    product = await get_product_by_id(db, product_id)

    if product is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Product not found",
        )

    updated = await update_product(db, product, body)
    return ProductResponse.model_validate(updated)


@router.delete("/{product_id}", response_model=ProductResponse)
async def admin_delete_product(
    product_id: uuid.UUID,
    _admin: AdminUser = Depends(get_current_admin),
    db: AsyncSession = Depends(get_db),
) -> ProductResponse:
    """Soft-delete a product (marks as unavailable, doesn't remove from DB).

    Products are never hard-deleted because existing orders might reference them.
    """
    product = await get_product_by_id(db, product_id)

    if product is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Product not found",
        )

    deleted = await soft_delete_product(db, product)
    return ProductResponse.model_validate(deleted)
