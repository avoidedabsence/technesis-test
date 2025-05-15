from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

from database.dao import Database
from database.models import User

async def main_menu_keyboard(user_id: int) -> InlineKeyboardMarkup:
    keyboard = InlineKeyboardBuilder()
    
    user_obj = await Database.get_user_by_telegram_id(user_id)
    
    if user_obj.sites:
        keyboard.row(
            InlineKeyboardButton(
                text=f'Статистика по вашим зюзюз... как их там',
                callback_data=f'show_stats'
            )
        )
    
    keyboard.row(
        InlineKeyboardButton(
            text=f'Добавить новые зюзюзюзики',
            callback_data=f'add_file'
        )
    )
    
    return keyboard.as_markup()


def cancel_fsm_keyboard() -> InlineKeyboardMarkup:
    keyboard = InlineKeyboardBuilder()
    
    keyboard.row(
        InlineKeyboardButton(
            text=f'Отмена',
            callback_data=f'cancel_fsm'
        )
    )

def return_keyboard() -> InlineKeyboardMarkup:
    keyboard = InlineKeyboardBuilder()
    
    keyboard.row(
        InlineKeyboardButton(
            text=f'Вернуться в меню',
            callback_data=f'start_command'
        )
    )
    
    return keyboard.as_markup()
    
    
    