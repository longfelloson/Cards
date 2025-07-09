from config import settings
from sqlalchemy import MetaData
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.orm import declarative_base
from sqlalchemy.pool import NullPool

Base = declarative_base()

metadata = MetaData()

engine = create_async_engine(settings.database.db_url, poolclass=NullPool)
async_session_maker = async_sessionmaker(
    engine, class_=AsyncSession, expire_on_commit=False
)


class Database:
    @staticmethod
    async def create_tables() -> None:
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)


db = Database()
