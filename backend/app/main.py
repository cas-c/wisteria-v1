import logging
from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from slowapi import _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded
from sqlalchemy import text

from app.config import settings
from app.database import engine
from app.rate_limit import limiter
from app.routers import admin_products, auth, health, products

logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    """Runs on startup/shutdown.

    The lifespan context manager is FastAPI's way of running code once
    at startup (before `yield`) and once at shutdown (after `yield`).
    This replaced the older `@app.on_event("startup")` decorator.

    Here we verify the DB is reachable. If it's not, the app will fail
    to start rather than accepting requests and failing on every one.
    """
    # Verify DB connection on startup
    async with engine.connect() as conn:
        await conn.execute(text("SELECT 1"))
    logger.info("Database connection verified")
    yield


app = FastAPI(
    title=settings.app_name,
    lifespan=lifespan,
)

# Rate limiting — prevents brute-force attacks on login.
# slowapi stores hit counts in memory by default. For multi-process
# production deployments, switch to a Redis backend.
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

# CORS — allows the Next.js frontend to call this API.
# In production, lock this down to your actual domain.
app.add_middleware(
    CORSMiddleware,
    allow_origins=[settings.frontend_url],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register routers
app.include_router(health.router, prefix=settings.api_v1_prefix)
app.include_router(auth.router, prefix=settings.api_v1_prefix)
app.include_router(products.router, prefix=settings.api_v1_prefix)
app.include_router(admin_products.router, prefix=settings.api_v1_prefix)
