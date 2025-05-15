from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy.future import select
from loguru import logger
from typing import Any

from database.models import Base, Site, Item, User


class Database:
    _engine = None
    _sessionmaker = None

    @classmethod
    async def init(cls, db_url: str, max_conn: int = 5):
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
            
    @classmethod
    async def check_user(cls, user_id: int) -> bool:
        async with cls._sessionmaker() as session:
            result = await session.execute(
                select(User).where(User.user_id == user_id)
            )
            result = result.scalar_one_or_none()
            if result is None:
                usr_obj = User(
                    user_id=user_id,
                )
                session.add(usr_obj)
                await session.commit()
                logger.info(f"Created user:{user_id}")
                return
            
            logger.info(f"user:{user_id} already exists;")

    @classmethod
    async def get_user_by_telegram_id(cls, user_id: int) -> User | None:
        async with cls._sessionmaker() as session:
            result = await session.execute(
                select(User).where(User.user_id == user_id)
            )
            result = result.scalar_one_or_none()
            
            if result is None:
                logger.error("failed to retrieve existing user:{};", user_id)
                return None
            
            return result
        
    @classmethod
    async def create_items():
        ...
    