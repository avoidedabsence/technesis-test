from aiohttp import ClientSession
from bs4 import BeautifulSoup
from fake_useragent import UserAgent
from loguru import logger
import asyncio

from .config import Config

async def parse_items(data: list[list[str | None]]) -> list[list[str | int] | None]: # str - all arguments from given data; 
    semaphore = asyncio.Semaphore(Config.CONCURRENT_REQUESTS)
    
    result = []
    
    async with semaphore:
        for item in data:
            if any(arg is None for arg in item):
                result.append(None)
                continue
            
            parsed = await parse_item[]
            
            
            
            
            
        

async def parse_item(url: str, xpath: str) -> int | Exception:
    async with ClientSession(
        headers={"UserAgent": UserAgent().chrome}
    ) as session:
        response = await session.get(
            url
        )
        
        if response.status != 200:
            logger.error("failed to parse item {}:{}, sc: {}, body: {}", url, xpath, response.status, await response.text())
            return None