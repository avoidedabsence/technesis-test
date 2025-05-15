from aiohttp import ClientSession
from bs4 import BeautifulSoup
from lxml import etree
from fake_useragent import UserAgent
from loguru import logger
import asyncio
import re

from config import Config

async def parse_items(data: dict) -> list[dict | None]:
    semaphore = asyncio.Semaphore(Config.CONCURRENT_REQUESTS)
    
    result = []
    
    async with semaphore:
        for key, item in data.items():
            if any(arg is None for arg in item.values()):
                result.append(None)
                continue
            
            parsed = await parse_item(item['url'], item['xpath'])
            
            if parsed is None:
                result.append(None)
                continue
            
            item['price'] = parsed
            
            result.append(item)
            

async def parse_item(url: str, xpath: str) -> int | None:
    async with ClientSession(
        headers={"UserAgent": UserAgent().chrome}
    ) as session:
        response = await session.get(url)
          
        if response.status != 200:
            logger.error("failed to parse item {}:{}, sc: {}, body: {}", url, xpath, response.status, await response.text())
            return None
        
        price = await asyncio.to_thread(parse_html, url, response.content, xpath)
        return price
        
        
def parse_html(url: str, html: str, xpath: str) -> int | None:
    try:
        soup = BeautifulSoup(html, 'lxml')
        etree = etree(str(soup))
        price_content = re.sub('[^0-9]', '', etree.xpath(xpath)[0].text)
        price = int(price_content)
        return price
    except Exception as e:
        logger.error("failed to parce price for {}:{}, exc: {}", url, xpath, e)
        return None