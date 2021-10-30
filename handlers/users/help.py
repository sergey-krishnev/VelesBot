from aiogram import types
from aiogram.dispatcher.filters.builtin import CommandHelp

from data.config import ADMINS
from loader import dp


@dp.message_handler(CommandHelp())
async def bot_help(message: types.Message):
    text = ["Список команд: ",
            "/start - Начать диалог",
            "/help - Получить список команд"]
    if message.from_user.id in ADMINS:
        text.append("/manage - Управление ботом")
    
    await message.answer("\n".join(text))
