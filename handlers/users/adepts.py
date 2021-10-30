from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.types import CallbackQuery

from keyboards.inline.callback_data import open_menu_callback
from keyboards.inline.show_adepts import get_client_adept_keyboard, get_adept_detailed
from loader import dp
from states.add_adept import AdeptCreation
from utils.db_api import adept_dao
from utils.db_api.adept_dao import get_adept_by_id


@dp.callback_query_handler(open_menu_callback.filter(menu="show_adepts"))
async def show_adepts(call: CallbackQuery):
    await call.message.edit_text("Выберите, чтобы посмотреть, о чем можно поговорить с каждым адептом:",
                                 reply_markup=get_client_adept_keyboard())


@dp.callback_query_handler(open_menu_callback.filter(menu="adept_list"))
async def show_adept_detailed(call: CallbackQuery, callback_data: dict):
    adept_id = callback_data.get("id")
    adept_name = get_adept_by_id(adept_id)
    await call.message.edit_text(f"Выбран адепт: '{adept_name}'", reply_markup=get_adept_detailed(adept_id))


@dp.callback_query_handler(open_menu_callback.filter(menu="add_adept"), state=None)
async def add_adept(call: CallbackQuery):
    await call.message.edit_text("Введите имя адепта")
    await AdeptCreation.ADEPT_NAME.set()


@dp.message_handler(state=AdeptCreation.ADEPT_NAME)
async def catch_adept_name(message: types.Message, state: FSMContext):
    adept_name = message.text
    await state.update_data(adept_name=adept_name)
    await message.answer("Введите описание адепта")
    await AdeptCreation.next()


@dp.message_handler(state=AdeptCreation.ADEPT_DESCRIPTION)
async def catch_adept_description(message: types.Message, state: FSMContext):
    data = await state.get_data()
    adept_name = data.get("adept_name")
    adept_description = message.text
    adept_dao.add_adept(adept_name, adept_description)
    await message.answer(f"Данные Сохранены. Имя: {adept_name} Описание {adept_description}. Нажмите /manage,"
                         f" чтобы вернуться в главное меню")
    await state.finish()
