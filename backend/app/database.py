from collections.abc import AsyncGenerator

from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from app.config import settings

# The engine manages a pool of DB connections.
# echo=True logs SQL in debug mode — useful for learning what SQLAlchemy generates.
engine = create_async_engine(
    settings.database_url,
    echo=settings.debug,
)

# Session factory — each request gets its own session (unit of work pattern).
# expire_on_commit=False lets us access attributes after commit without re-querying.
async_session = async_sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False,
)


async def get_db() -> AsyncGenerator[AsyncSession, None]:
    """FastAPI dependency that provides a DB session per request.

    Usage in a route:
        async def my_route(db: AsyncSession = Depends(get_db)):

    The `yield` pattern ensures the session is closed even if the route raises.
    """
    async with async_session() as session:
        yield session
