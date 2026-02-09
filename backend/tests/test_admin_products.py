"""Tests for admin product routes (CRUD via /admin/products)."""

import uuid

from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.admin_user import AdminUser
from app.models.product import Product, ProductCategory, ProductCondition
from app.utils.security import create_access_token, hash_password


async def _create_admin(session: AsyncSession) -> AdminUser:
    admin = AdminUser(
        email="admin@test.com",
        password_hash=hash_password("testpass"),
    )
    session.add(admin)
    await session.commit()
    await session.refresh(admin)
    return admin


async def _create_product(
    session: AsyncSession,
    slug: str = "test-figure",
    is_available: bool = True,
) -> Product:
    product = Product(
        name="Test Figure",
        slug=slug,
        description="A test figurine.",
        price_cents=5000,
        condition=ProductCondition.NEW,
        category=ProductCategory.NENDOROID,
        image_url="https://example.com/test.jpg",
        is_available=is_available,
        quantity=1 if is_available else 0,
    )
    session.add(product)
    await session.commit()
    await session.refresh(product)
    return product


def _auth_header(admin: AdminUser) -> dict[str, str]:
    token = create_access_token(subject=str(admin.id))
    return {"Authorization": f"Bearer {token}"}


class TestAdminListProducts:
    """GET /admin/products — admin sees ALL products including unavailable."""

    async def test_includes_unavailable(
        self, client: AsyncClient, db_session: AsyncSession
    ) -> None:
        admin = await _create_admin(db_session)
        await _create_product(db_session, slug="available", is_available=True)
        await _create_product(db_session, slug="sold-out", is_available=False)

        response = await client.get("/admin/products", headers=_auth_header(admin))
        assert response.status_code == 200
        data = response.json()
        assert data["total"] == 2


class TestAdminCreateProduct:
    """POST /admin/products — create a new product."""

    async def test_create_product(
        self, client: AsyncClient, db_session: AsyncSession
    ) -> None:
        admin = await _create_admin(db_session)

        response = await client.post(
            "/admin/products",
            json={
                "name": "New Nendoroid",
                "slug": "new-nendoroid",
                "description": "A brand new nendoroid.",
                "price_cents": 4500,
                "condition": "new",
                "category": "nendoroid",
                "image_url": "https://example.com/img.jpg",
            },
            headers=_auth_header(admin),
        )
        assert response.status_code == 201
        data = response.json()
        assert data["name"] == "New Nendoroid"
        assert data["slug"] == "new-nendoroid"
        assert data["price_cents"] == 4500
        assert data["is_available"] is True
        assert "id" in data

    async def test_duplicate_slug_fails(
        self, client: AsyncClient, db_session: AsyncSession
    ) -> None:
        """Slug is unique at the DB level — duplicate should return 409 Conflict."""
        admin = await _create_admin(db_session)
        await _create_product(db_session, slug="taken-slug")

        response = await client.post(
            "/admin/products",
            json={
                "name": "Another Figure",
                "slug": "taken-slug",
                "description": "Should fail.",
                "price_cents": 3000,
                "condition": "new",
                "category": "nendoroid",
                "image_url": "https://example.com/img.jpg",
            },
            headers=_auth_header(admin),
        )
        assert response.status_code == 409
        assert "slug already exists" in response.json()["detail"]

    async def test_invalid_slug_format(
        self, client: AsyncClient, db_session: AsyncSession
    ) -> None:
        admin = await _create_admin(db_session)

        response = await client.post(
            "/admin/products",
            json={
                "name": "Bad Slug",
                "slug": "Has Spaces And CAPS!",
                "description": "Should fail validation.",
                "price_cents": 3000,
                "condition": "new",
                "category": "nendoroid",
                "image_url": "https://example.com/img.jpg",
            },
            headers=_auth_header(admin),
        )
        assert response.status_code == 422

    async def test_zero_price_fails(
        self, client: AsyncClient, db_session: AsyncSession
    ) -> None:
        admin = await _create_admin(db_session)

        response = await client.post(
            "/admin/products",
            json={
                "name": "Free Item",
                "slug": "free-item",
                "description": "Should fail — price must be >= 1.",
                "price_cents": 0,
                "condition": "new",
                "category": "nendoroid",
                "image_url": "https://example.com/img.jpg",
            },
            headers=_auth_header(admin),
        )
        assert response.status_code == 422

    async def test_requires_auth(self, client: AsyncClient) -> None:
        response = await client.post(
            "/admin/products",
            json={
                "name": "No Auth",
                "slug": "no-auth",
                "description": "Should be rejected.",
                "price_cents": 1000,
                "condition": "new",
                "category": "nendoroid",
                "image_url": "https://example.com/img.jpg",
            },
        )
        assert response.status_code == 403


class TestAdminUpdateProduct:
    """PUT /admin/products/{id} — partial update."""

    async def test_update_name(
        self, client: AsyncClient, db_session: AsyncSession
    ) -> None:
        admin = await _create_admin(db_session)
        product = await _create_product(db_session)

        response = await client.put(
            f"/admin/products/{product.id}",
            json={"name": "Updated Name"},
            headers=_auth_header(admin),
        )
        assert response.status_code == 200
        assert response.json()["name"] == "Updated Name"
        # Unchanged fields should be preserved
        assert response.json()["price_cents"] == 5000

    async def test_update_price(
        self, client: AsyncClient, db_session: AsyncSession
    ) -> None:
        admin = await _create_admin(db_session)
        product = await _create_product(db_session)

        response = await client.put(
            f"/admin/products/{product.id}",
            json={"price_cents": 9900},
            headers=_auth_header(admin),
        )
        assert response.status_code == 200
        assert response.json()["price_cents"] == 9900

    async def test_update_nonexistent(
        self, client: AsyncClient, db_session: AsyncSession
    ) -> None:
        admin = await _create_admin(db_session)

        response = await client.put(
            f"/admin/products/{uuid.uuid4()}",
            json={"name": "Ghost"},
            headers=_auth_header(admin),
        )
        assert response.status_code == 404


class TestAdminDeleteProduct:
    """DELETE /admin/products/{id} — soft delete (marks as unavailable)."""

    async def test_soft_delete(
        self, client: AsyncClient, db_session: AsyncSession
    ) -> None:
        admin = await _create_admin(db_session)
        product = await _create_product(db_session)

        response = await client.delete(
            f"/admin/products/{product.id}",
            headers=_auth_header(admin),
        )
        assert response.status_code == 200
        assert response.json()["is_available"] is False

    async def test_soft_deleted_hidden_from_public(
        self, client: AsyncClient, db_session: AsyncSession
    ) -> None:
        admin = await _create_admin(db_session)
        product = await _create_product(db_session, slug="to-delete")

        # Soft-delete it
        await client.delete(
            f"/admin/products/{product.id}",
            headers=_auth_header(admin),
        )

        # Public listing should not show it
        response = await client.get("/products")
        assert response.json()["total"] == 0

    async def test_delete_nonexistent(
        self, client: AsyncClient, db_session: AsyncSession
    ) -> None:
        admin = await _create_admin(db_session)

        response = await client.delete(
            f"/admin/products/{uuid.uuid4()}",
            headers=_auth_header(admin),
        )
        assert response.status_code == 404
