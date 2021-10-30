from aiogram import types
from aiogram.dispatcher.filters.builtin import CommandStart
from aiogram.types import CallbackQuery

from keyboards.inline.callback_data import open_menu_callback
from keyboards.inline.open_tree import great_tree
from keyboards.inline.show_adepts import show_adepts
from loader import dp


@dp.message_handler(CommandStart())
async def bot_start(message: types.Message):
    await message.answer(f"Привет, {message.from_user.full_name}!", reply_markup=great_tree)


@dp.callback_query_handler(open_menu_callback.filter(menu="great_tree"))
async def open_great_tree(call: CallbackQuery):
    await call.message.edit_text("Великое древо мнений", reply_markup=show_adepts)
