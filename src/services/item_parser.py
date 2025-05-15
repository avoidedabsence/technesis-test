from fake_useragent import UserAgent
from loguru import logger
from requests_html import AsyncHTMLSession
import asyncio
import re

from config import Config


async def parse_items(data: dict):
    semaphore = asyncio.Semaphore(Config.CONCURRENT_REQUESTS)
    
    result, tasks = {}, []
    
    for key, item in data.items():
        if any(arg is None for arg in item.values()):
            result[key] = item | {'price': None}
            continue
        
        tasks.append(parse_item(key, item['url'], item['xpath'], semaphore))
            
    results = await asyncio.gather(*tasks)
    
    result = result | {key: data[key] | {'price': val} for key, val in results}
    
    return result
    

async def parse_item(key, url: str, xpath: str, semaphore: asyncio.Semaphore):
    async with semaphore:
        session = AsyncHTMLSession()
        
        r = await session.get(url, headers={
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
        })

        await r.html.arender(timeout=30, sleep=2)

        elem = r.html.xpath(xpath + "/text()")
        
        if elem:
            price_text = ''.join(t.strip() for t in elem if t.strip())
            
            return key, int(re.sub(r'[^\d]', '', price_text))
        else:
            return key, None