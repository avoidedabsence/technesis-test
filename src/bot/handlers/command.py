from aiogram.types import Message

from bot_assets.handlers.keyboards import main_menu_keyboard
from utils.ag_utils import safe_edit_text
from database.user.db import Database


async def start_command(event):
    if isinstance(event, Message):
        await Database.check_user(event.from_user.id)

        await event.answer(
            "Привет! Я бот для парсинга зюзюблек :)",
            reply_markup=main_menu_keyboard()
        )
    else:
        await safe_edit_text(
            event.message,
            "Привет! Я бот для парсинга зюзюблек :)",
            reply_markup=main_menu_keyboard(),
        )