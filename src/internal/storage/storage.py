from typing import Generator

from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker

engine = create_async_engine("postgresql+asyncpg://localhost:5432/pgforms", echo=True)
async_session = async_sessionmaker(autocommit=False, autoflush=False, bind=engine)


async def get_db() -> Generator:
    async with async_session() as db:
        try:
            yield db
        finally:
            await db.close()
