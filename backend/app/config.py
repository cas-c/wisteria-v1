from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application settings loaded from environment variables.

    pydantic-settings automatically reads env vars matching each field name
    (case-insensitive). The .env file is loaded as a fallback.
    """

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
    )

    # App
    app_name: str = "Wisteria API"
    debug: bool = False
    api_v1_prefix: str = "/api/v1"

    # Database — asyncpg connection string
    database_url: str = "postgresql+asyncpg://postgres:postgres@localhost:5432/wisteria"

    # Test database — separate DB so tests never touch dev data.
    # Created automatically by the test conftest if it doesn't exist.
    test_database_url: str = "postgresql+asyncpg://postgres:postgres@localhost:5432/wisteria_test"

    # Auth — no default: forces the env var to be set. App won't start without it.
    secret_key: str
    access_token_expire_minutes: int = 60 * 24  # 24 hours

    # Stripe
    stripe_secret_key: str = ""
    stripe_webhook_secret: str = ""

    # Resend (email)
    resend_api_key: str = ""

    # Frontend URL (for CORS + Stripe redirect)
    frontend_url: str = "http://localhost:3000"


# Singleton — import this everywhere
settings = Settings()
