"""Tests for public product endpoints (GET /products, GET /products/{slug})."""

from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.product import Product, ProductCategory, ProductCondition


async def _create_product(
    session: AsyncSession,
    *,
    name: str = "Test Figure",
    slug: str = "test-figure",
    price_cents: int = 5000,
    condition: ProductCondition = ProductCondition.NEW,
    category: ProductCategory = ProductCategory.NENDOROID,
    is_available: bool = True,
) -> Product:
    """Helper to create a product directly in the DB for testing."""
    product = Product(
        name=name,
        slug=slug,
        description="A test figurine for testing purposes.",
        price_cents=price_cents,
        condition=condition,
        category=category,
        image_url="https://example.com/test.jpg",
        is_available=is_available,
        quantity=1 if is_available else 0,
    )
    session.add(product)
    await session.commit()
    await session.refresh(product)
    return product


class TestListProducts:
    """GET /products — public product listing."""

    async def test_empty_list(self, client: AsyncClient) -> None:
        response = await client.get("/products")
        assert response.status_code == 200
        data = response.json()
        assert data["items"] == []
        assert data["total"] == 0
        assert data["pages"] == 1

    async def test_returns_available_products(
        self, client: AsyncClient, db_session: AsyncSession
    ) -> None:
        await _create_product(db_session, slug="figure-1", name="Figure 1")
        await _create_product(db_session, slug="figure-2", name="Figure 2")

        response = await client.get("/products")
        assert response.status_code == 200
        data = response.json()
        assert data["total"] == 2
        assert len(data["items"]) == 2

    async def test_hides_unavailable_products(
        self, client: AsyncClient, db_session: AsyncSession
    ) -> None:
        await _create_product(db_session, slug="available", is_available=True)
        await _create_product(db_session, slug="sold-out", is_available=False)

        response = await client.get("/products")
        data = response.json()
        assert data["total"] == 1
        assert data["items"][0]["slug"] == "available"

    async def test_filter_by_category(
        self, client: AsyncClient, db_session: AsyncSession
    ) -> None:
        await _create_product(db_session, slug="nendo", category=ProductCategory.NENDOROID)
        await _create_product(db_session, slug="plush", category=ProductCategory.PLUSH)

        response = await client.get("/products?category=nendoroid")
        data = response.json()
        assert data["total"] == 1
        assert data["items"][0]["slug"] == "nendo"

    async def test_filter_by_condition(
        self, client: AsyncClient, db_session: AsyncSession
    ) -> None:
        await _create_product(db_session, slug="new-item", condition=ProductCondition.NEW)
        await _create_product(db_session, slug="used-item", condition=ProductCondition.USED)

        response = await client.get("/products?condition=new")
        data = response.json()
        assert data["total"] == 1
        assert data["items"][0]["slug"] == "new-item"

    async def test_search_by_name(
        self, client: AsyncClient, db_session: AsyncSession
    ) -> None:
        await _create_product(db_session, slug="miku-fig", name="Hatsune Miku Nendoroid")
        await _create_product(db_session, slug="rem-fig", name="Rem Scale Figure")

        response = await client.get("/products?search=miku")
        data = response.json()
        assert data["total"] == 1
        assert data["items"][0]["slug"] == "miku-fig"

    async def test_search_case_insensitive(
        self, client: AsyncClient, db_session: AsyncSession
    ) -> None:
        await _create_product(db_session, slug="miku-fig", name="Hatsune Miku")

        response = await client.get("/products?search=MIKU")
        data = response.json()
        assert data["total"] == 1

    async def test_pagination(
        self, client: AsyncClient, db_session: AsyncSession
    ) -> None:
        for i in range(5):
            await _create_product(db_session, slug=f"item-{i}", name=f"Item {i}")

        response = await client.get("/products?page=1&per_page=2")
        data = response.json()
        assert data["total"] == 5
        assert len(data["items"]) == 2
        assert data["pages"] == 3
        assert data["page"] == 1

    async def test_pagination_last_page(
        self, client: AsyncClient, db_session: AsyncSession
    ) -> None:
        for i in range(5):
            await _create_product(db_session, slug=f"item-{i}", name=f"Item {i}")

        response = await client.get("/products?page=3&per_page=2")
        data = response.json()
        assert len(data["items"]) == 1

    async def test_response_schema(
        self, client: AsyncClient, db_session: AsyncSession
    ) -> None:
        await _create_product(db_session, price_cents=4500)

        response = await client.get("/products")
        item = response.json()["items"][0]

        assert "id" in item
        assert item["name"] == "Test Figure"
        assert item["slug"] == "test-figure"
        assert item["price_cents"] == 4500
        assert item["condition"] == "new"
        assert item["category"] == "nendoroid"
        assert "created_at" in item
        assert "updated_at" in item


class TestGetProduct:
    """GET /products/{slug} — single product detail."""

    async def test_get_existing_product(
        self, client: AsyncClient, db_session: AsyncSession
    ) -> None:
        await _create_product(db_session, slug="my-figure", name="My Figure")

        response = await client.get("/products/my-figure")
        assert response.status_code == 200
        assert response.json()["name"] == "My Figure"

    async def test_product_not_found(self, client: AsyncClient) -> None:
        response = await client.get("/products/does-not-exist")
        assert response.status_code == 404
        assert response.json()["detail"] == "Product not found"
