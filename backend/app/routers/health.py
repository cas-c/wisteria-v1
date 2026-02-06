from fastapi import APIRouter

router = APIRouter(tags=["health"])


@router.get("/health")
async def health_check() -> dict[str, str]:
    """Basic liveness check. We'll add a DB ping in Phase 1."""
    return {"status": "ok"}
