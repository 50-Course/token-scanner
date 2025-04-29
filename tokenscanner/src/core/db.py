from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from src.core.config import settings

if settings.ENVIRONMENT == "production" and not settings.DATABASE_URI:
    # just like django - ENFORCE_DB is required in production
    raise ValueError(
        "DATABASE_URI is required in production. Please set it in your environment variables."
    )


if (
    settings.DEBUG_ENABLED
    and settings.ENVIRONMENT == "local"
    and settings.DATABASE_URI is None
):
    # we should use sqlite for local development
    engine = create_async_engine(
        "sqlite+aiosqlite:///./test.db",
        echo=True,
    )


if settings.DATABASE_URI is not None:
    engine = create_async_engine(
        settings.DATABASE_URI,
        echo=True,
    )
    AsyncSessionLocal = async_sessionmaker(bind=engine, expire_on_commit=False)

    async def get_db() -> AsyncSession:
        """
        Dependency that provides a database session to the route handler.
        """
        async with AsyncSessionLocal() as session:
            return session
