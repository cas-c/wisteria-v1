"""Health check endpoint.

Performs a real DB query (`SELECT 1`) to verify the async connection is alive.
This catches problems like the DB container not running, connection pool
exhaustion, or network issues between backend and DB.
"""

from fastapi import APIRouter, Depends
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db

router = APIRouter(tags=["health"])


@router.get("/health")
async def health_check(db: AsyncSession = Depends(get_db)) -> dict[str, str]:
    """Liveness check with DB ping.

    Uses `Depends(get_db)` — the same dependency injection pattern every
    route will use. FastAPI calls `get_db()`, which yields an AsyncSession,
    passes it to this function, then closes the session when done.
    """
    await db.execute(text("SELECT 1"))
    return {"status": "ok", "database": "connected"}
