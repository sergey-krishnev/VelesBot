import os

from aiogram import types
from aiogram.dispatcher.filters import Command
from aiogram.types import CallbackQuery

from keyboards.inline.admin_menu import admin_menu
from keyboards.inline.callback_data import open_menu_callback
from loader import dp


@dp.message_handler(Command("manage"), is_admin=True)
async def bot_admin_manage(message: types.Message):
    await message.answer("Добро пожаловать в центр управления ботом!", reply_markup=admin_menu)


@dp.callback_query_handler(open_menu_callback.filter(menu='get_db'))
async def send_backup(call: CallbackQuery):
    with open(os.path.join("data", "veles.db"), 'rb') as f:
        await call.bot.send_document(call.message.chat.id, f)
