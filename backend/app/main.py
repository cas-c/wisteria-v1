from contextlib import asynccontextmanager
from collections.abc import AsyncGenerator

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.config import settings
from app.routers import health


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    """Runs on startup/shutdown. We'll add DB connection checks here later."""
    yield


app = FastAPI(
    title=settings.app_name,
    lifespan=lifespan,
)

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
