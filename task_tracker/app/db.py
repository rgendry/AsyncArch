from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker

from app.config import settings


engine = create_async_engine(
    settings.DB_DSN,
    echo=settings.DB_ECHO,
    future=True,
)

async_session = sessionmaker(engine, expire_on_commit=False, class_=AsyncSession, future=True, autoflush=False)


async def get_db():
    session = async_session()
    try:
        yield session
        await session.commit()
    finally:
        await session.close()

