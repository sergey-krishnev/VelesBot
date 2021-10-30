from aiogram import types
from aiogram.dispatcher.filters import Command

from keyboards.inline.admin_menu import admin_menu
from loader import dp


@dp.message_handler(Command("manage"), is_admin=True)
async def bot_admin_manage(message: types.Message):
    await message.answer("Добро пожаловать в центр управления ботом!", reply_markup=admin_menu)
