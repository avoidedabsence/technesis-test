from aiogram.types import CallbackQuery, Message
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup

from bot.keyboards import cancel_fsm_keyboard, return_keyboard
from bot.handlers.command import start_command
from services.read import read_file
from services.item_parser import parse_items
from utils.ag_utils import safe_edit_text
from utils.exceptions import CustomException
from database.dao import Database

import asyncio

class AddFile(StatesGroup):
    file: State = State()
    

async def cancel_fsm_handler(callback_query: CallbackQuery, state: FSMContext):
    await callback_query.answer()
    
    await state.clear()
    
    await start_command(callback_query)
    

async def upload_file_handler(callback_query: CallbackQuery, state: FSMContext):
    await callback_query.answer()
    
    await state.set_state(AddFile.file)
    
    keyboard = cancel_fsm_keyboard()
    
    await safe_edit_text(
        callback_query.message,
        f'Загрузите файл с разрешением: `xls`, `xlsx`, `xlsm`, `xlsb`, `odf`, `ods` или `odt`:',
        reply_markup=keyboard
    )
    

async def process_file_handler(message: Message, state: FSMContext):
    file = message.document

    fail_keyboard = cancel_fsm_keyboard()
    
    if file is None:
        await message.answer(
            "К вашему сообщению не прикреплен файл\.\n\nПопробуйте еще раз\.",
            reply_markup=fail_keyboard
        )
        return
    
    if file.file_name.split(".")[-1] not in (
        'xls', 'xlsx', 'xlsm', 'xlsb', 'odf', 'ods', 'odt'
    ):
        await message.answer(
            "Ваш файл имеет неподходящее расширение\.\n\nПопробуйте еще раз\.",
            reply_markup=fail_keyboard
        )
        return

    destination = f"cache/{file.file_name}"
    await message.bot.download(file.file_id, destination=destination)

    try:
        data = await asyncio.to_thread(read_file, user_id=message.from_user.id, file_path=destination)
    except CustomException as e:
        await message.answer(
            f"Файл вызвал ошибку при чтении\: {e}\.\n\nПопробуйте еще раз\.",
            reply_markup=fail_keyboard
        )
        return
    
    await message.answer("Ожидайте\. В среднем\, обработка файла занимает 30 секунд\.")
    
    parsed_items = await parse_items(data)
    
    items = await Database.create_items(message.from_user.id, parsed_items)
    
    text = ["Следующие товары были успешно загружены\:\n\n"] + \
        [f'{item.title} \(site\_id {item.site_id}\) \: {item.price} RUB\n' for item in items if item is not None]
        
    if len(text) == 1:
        text.append(
            "никакие \:c"
        )
    
    await message.answer(''.join(text), reply_markup=return_keyboard())
    
    
    

    
    
    
    
    
    
    


    
    
    
    