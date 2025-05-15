from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload
from loguru import logger
from typing import Any
from urllib.parse import urlparse
import asyncio

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
    async def close(cls):
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
    async def get_items_grouped_by_domain(cls, user_id: int) -> dict | None:
        async with cls._sessionmaker() as session:
            result = await session.execute(
                select(User).where(User.user_id == user_id)
            )
            result = result.scalar_one_or_none()
            
            if result is None:
                logger.error("failed to retrieve existing user:{};", user_id)
                return None
            
            return {site.domain: site.items for site in result.sites}
    
    @classmethod
    async def create_item_and_site_if_not_exists(cls, user_id: int, item: dict):
        if item['price'] is None:
            return None
        
        async with cls._sessionmaker() as session:
            try:
                domain_name = urlparse(item["url"]).netloc
        
                exists = (await session.execute(
                    select(Site).where(Site.domain == domain_name and Site.user_id == user_id)
                )).fetchone()
                
                if not exists:
                    site = Site(
                        domain=domain_name,
                        user_id=user_id
                    )
                    session.add(site)
                    
                    await session.commit()
                    await session.refresh(site)
                    
                    site_id = site.id
                else:
                    site_id = exists[0].id
                
                item_obj = Item(
                    site_id=site_id,
                    title=item['title'],
                    url=item['url'],
                    xpath=item['xpath'],
                    price=item['price']
                )
                
                session.add(item_obj)
                    
                await session.commit()
                await session.refresh(item_obj)
                
                return item_obj
            except Exception as e:
                logger.error('failed to create item {}, exc {}', item, exc)
                return None
            

    @classmethod
    async def create_items(cls, user_id: int, items_list: dict) -> list[Item]:
        tasks = []
        for _, item in items_list.items():
            tasks.append(cls.create_item_and_site_if_not_exists(user_id, item))
        return await asyncio.gather(*tasks) # wont do much bcs sqlite :D
    