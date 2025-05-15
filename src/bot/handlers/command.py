from aiogram.types import Message

from bot.keyboards import main_menu_keyboard
from utils.ag_utils import safe_edit_text
from database.dao import Database


async def start_command(event):
    if isinstance(event, Message):
        await Database.check_user(event.from_user.id)
        
        keyboard = await main_menu_keyboard(event.from_user.id)
        
        await event.answer(
            "Привет\! Я бот для парсинга зюзюблек :\)",
            reply_markup=keyboard
        )
    else:
        
        keyboard = await main_menu_keyboard(event.from_user.id)
        
        await safe_edit_text(
            event.message,
            "Привет\! Я бот для парсинга зюзюблек :\)",
            reply_markup=keyboard,
        )