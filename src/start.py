from aiogram import Bot, Dispatcher, BaseMiddleware
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.client.default import DefaultBotProperties
from aiogram.enums.parse_mode import ParseMode
from loguru import logger

from .config import Config
from database.dao import Database

class LoguruMiddleware(BaseMiddleware):
    async def __call__(self, handler, event, data):
        try:
            return await handler(event, data)
        except Exception as e:
            logger.exception(f"Exception in handler: {e}")
            raise

async def entrypoint():
    await Database.init(Config.DB_URL)
    
    storage = MemoryStorage()
    
    bot = Bot(
        token=Config.BOT_TOKEN,
        default=DefaultBotProperties(
            parse_mode=ParseMode.MARKDOWN_V2
            )
        )
    
    dp = Dispatcher(
        bots=bot,
        storage=storage
    )
    
    dp.message.middleware(LoguruMiddleware())
    dp.callback_query.middleware(LoguruMiddleware())
    
    