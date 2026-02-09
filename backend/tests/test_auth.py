"""Tests for auth endpoints (POST /auth/login) and JWT validation."""

from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.admin_user import AdminUser
from app.utils.security import create_access_token, hash_password


async def _create_admin(
    session: AsyncSession,
    email: str = "admin@test.com",
    password: str = "testpass123",
) -> AdminUser:
    """Helper to create an admin user directly in the DB."""
    admin = AdminUser(
        email=email,
        password_hash=hash_password(password),
    )
    session.add(admin)
    await session.commit()
    await session.refresh(admin)
    return admin


class TestLogin:
    """POST /auth/login — admin authentication."""

    async def test_valid_login(
        self, client: AsyncClient, db_session: AsyncSession
    ) -> None:
        await _create_admin(db_session)

        response = await client.post(
            "/auth/login",
            json={"email": "admin@test.com", "password": "testpass123"},
        )
        assert response.status_code == 200
        data = response.json()
        assert "access_token" in data
        assert data["token_type"] == "bearer"

    async def test_wrong_password(
        self, client: AsyncClient, db_session: AsyncSession
    ) -> None:
        await _create_admin(db_session)

        response = await client.post(
            "/auth/login",
            json={"email": "admin@test.com", "password": "wrongpassword"},
        )
        assert response.status_code == 401
        assert response.json()["detail"] == "Invalid email or password"

    async def test_nonexistent_email(self, client: AsyncClient) -> None:
        response = await client.post(
            "/auth/login",
            json={"email": "nobody@test.com", "password": "whatever"},
        )
        assert response.status_code == 401
        assert response.json()["detail"] == "Invalid email or password"

    async def test_invalid_email_format(self, client: AsyncClient) -> None:
        response = await client.post(
            "/auth/login",
            json={"email": "not-an-email", "password": "whatever"},
        )
        assert response.status_code == 422

    async def test_empty_password(self, client: AsyncClient) -> None:
        response = await client.post(
            "/auth/login",
            json={"email": "admin@test.com", "password": ""},
        )
        assert response.status_code == 422


class TestJWTValidation:
    """Tests that admin-protected routes properly validate JWTs."""

    async def test_no_token(self, client: AsyncClient) -> None:
        response = await client.get("/admin/products")
        assert response.status_code == 403

    async def test_invalid_token(self, client: AsyncClient) -> None:
        response = await client.get(
            "/admin/products",
            headers={"Authorization": "Bearer invalid-token-here"},
        )
        assert response.status_code == 401

    async def test_expired_token(
        self, client: AsyncClient, db_session: AsyncSession
    ) -> None:
        from datetime import timedelta

        admin = await _create_admin(db_session)
        # Create a token that expired 1 hour ago
        token = create_access_token(
            subject=str(admin.id),
            expires_delta=timedelta(hours=-1),
        )

        response = await client.get(
            "/admin/products",
            headers={"Authorization": f"Bearer {token}"},
        )
        assert response.status_code == 401

    async def test_token_for_deleted_user(self, client: AsyncClient) -> None:
        """Token with a valid UUID that doesn't match any admin user."""
        import uuid

        token = create_access_token(subject=str(uuid.uuid4()))

        response = await client.get(
            "/admin/products",
            headers={"Authorization": f"Bearer {token}"},
        )
        assert response.status_code == 401

    async def test_valid_token(
        self, client: AsyncClient, db_session: AsyncSession
    ) -> None:
        admin = await _create_admin(db_session)
        token = create_access_token(subject=str(admin.id))

        response = await client.get(
            "/admin/products",
            headers={"Authorization": f"Bearer {token}"},
        )
        assert response.status_code == 200
