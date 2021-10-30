from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.types import CallbackQuery

from keyboards.inline.callback_data import open_menu_callback
from keyboards.inline.show_adepts import get_admin_adept_keyboard
from loader import dp
from states.add_theme import ThemeCreation
from utils.db_api import theme_dao


@dp.callback_query_handler(open_menu_callback.filter(menu="add_theme"), state=None)
async def add_theme(call: CallbackQuery):
    await call.message.edit_text("Введите название темы")
    await ThemeCreation.THEME_NAME.set()


@dp.message_handler(state=ThemeCreation.THEME_NAME)
async def catch_theme_name(message: types.Message, state: FSMContext):
    theme_name = message.text
    await state.update_data(theme_name=theme_name)
    await message.answer("Выберите адепта", reply_markup=get_admin_adept_keyboard())
    await ThemeCreation.next()


@dp.callback_query_handler(open_menu_callback.filter(menu="adept_list"), state=ThemeCreation.CHOSEN_ADEPT)
async def catch_chosen_adept(call: CallbackQuery, callback_data: dict, state: FSMContext):
    data = await state.get_data()
    theme_name = data.get("theme_name")
    adept_id = callback_data.get("id")
    theme_dao.add_theme(theme_name, adept_id)
    await call.message.edit_text(f"Данные Сохранены. Название темы: {theme_name} Id адепта: {adept_id}."
                                 f" Нажмите /manage, чтобы вернуться в главное меню")
    await state.finish()
