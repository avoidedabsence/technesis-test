from aiogram.types import CallbackQuery

from bot.keyboards import return_keyboard
from database.dao import Database
from utils.ag_utils import safe_edit_text

async def statistics_handler(callback_query: CallbackQuery):
    await callback_query.answer()
    
    keyboard = return_keyboard()
    
    data = await Database.get_items_grouped_by_domain(callback_query.from_user.id)
    
    stats = {dom: round(sum(it.price for it in items) / len(items), 2) for dom, items in data.items()}
    
    text = ["Ваша статистика по сайтам\:\n\n"] + \
        [f"{domain.replace(".", "\.")}\: {str(mean).replace(".", "\.")}\n" for domain, mean in stats.items()]
    
    await safe_edit_text(callback_query.message, ''.join(text), reply_markup=keyboard)