from aiogram.exceptions import TelegramBadRequest


async def safe_edit_text(message, text, **kwargs):
    try:
        await message.edit_text(text, **kwargs)
    except TelegramBadRequest as e:
        if "message can't be edited" in str(e) or "message to edit not found" in str(e):
            await message.answer(text, **kwargs)
        elif 'new message content and reply markup are exactly the same' in str(e):
            await message.answer(text, **kwargs)
            try:
                await message.delete()
            except Exception as e:
                pass  
        else:
            raise e