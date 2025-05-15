from aiogram import Dispatcher
from aiogram.filters import CommandStart

from bot.handlers import command, upload


def register_handlers(dp: Dispatcher):
    dp.message.register(command.start_command, CommandStart())
    
    dp.callback_query.register(
        command.start_command, lambda c: c.data == "start_command"
    )

    dp.callback_query.register(
        upload.upload_file_handler,
        lambda c: c.data == "add_file"
    )
    
    dp.message.register(
        upload.process_file_handler,
        upload.AddFile.file
    )
    

    
    