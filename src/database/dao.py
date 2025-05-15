from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy.future import select
from loguru import logger
from database.user.orm import *


class Database:
    _engine = None
    _sessionmaker = None

    @classmethod
    async def init(cls, db_url: str, max_conn: int):
        cls._engine = create_async_engine(db_url, echo=False, pool_size=max_conn)
        cls._sessionmaker = async_sessionmaker(cls._engine, expire_on_commit=False)
        
        async with cls._engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)
        
        logger.info(
            "db._engine init with max_conn={}", max_conn
        )
        
    @classmethod
    async def close():
        if cls._engine:
            await cls._engine.dispose()
            logger.info("db._engine closed w/ success;")
    
    