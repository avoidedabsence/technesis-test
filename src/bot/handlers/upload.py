from aiogram.types import CallbackQuery, Message
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup

from bot.keyboards import cancel_fsm_keyboard
from bot.handlers.command import start_command

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
    

async def validate_and_save_file_handler(message: Message, state: FSMContext):
    file = message.document
    
    fail_keyboard = cancel_fsm_keyboard()
    
    if file is None:
        await message.answer(
            "К вашему сообщению не прикреплен файл.\n\nПопробуйте еще раз.",
            reply_markup=fail_keyboard
        )
    
    if file.file_name.split(".")[-1] not in (
        'xls', 'xlsx', 'xlsm', 'xlsb', 'odf', 'ods', 'odt'
    ):
        await message.answer(
            "Ваш файл имеет неподходящее расширение.\n\nПопробуйте еще раз.",
            reply_markup=fail_keyboard
        )
    
    


    
    
    
    