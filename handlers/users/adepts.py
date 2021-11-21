from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.types import CallbackQuery

from keyboards.inline.callback_data import open_menu_callback
from keyboards.inline.show_adepts import get_client_adept_keyboard, get_adept_detailed, get_adepts_for_open, \
    back_to_adept_list
from loader import dp
from states.add_adept import AdeptCreation
from utils.constants import ADEPT_COST_SELECT, ADEPT_COST_RANDOM
from utils.db_api import adept_dao
from utils.db_api.adept_dao import get_adept_by_id, get_random_unowned_adept_id
from utils.db_api.trust_dao import is_new_account, add_trust
from utils.db_api.user_dao import spend_coins, get_user_by_id, register_user


@dp.callback_query_handler(open_menu_callback.filter(menu="show_adepts"))
async def show_adepts(call: CallbackQuery):
    user = get_user_by_id(call.from_user.id)
    if user is None:
        register_user(call.from_user.id)

    if is_new_account(call.from_user.id):
        await call.message.edit_text("У Вас нет открытых адептов. Выберите одного бесплатного адепта:",
                                     reply_markup=get_adepts_for_open(call.from_user.id, True))
    else:
        await call.message.edit_text("Выбрать адепта:",
                                     reply_markup=get_client_adept_keyboard(call.from_user.id))


@dp.callback_query_handler(open_menu_callback.filter(menu="purchase_free_adept"))
async def purchase_free_adept(call: CallbackQuery, callback_data: dict):
    adept_id = callback_data.get("id")
    add_trust(call.from_user.id, adept_id)
    adept_name = get_adept_by_id(adept_id)
    await call.message.edit_text(f"'{adept_name}' получен.",
                                 reply_markup=get_adept_detailed(adept_id))


@dp.callback_query_handler(open_menu_callback.filter(menu="purchase_adept"))
async def purchase_adept(call: CallbackQuery, callback_data: dict):
    adept_id = callback_data.get("id")
    spend_coins(call.from_user.id, ADEPT_COST_SELECT)
    add_trust(call.from_user.id, adept_id)
    adept_name = get_adept_by_id(adept_id)
    await call.message.edit_text(f"'{adept_name}' получен.",
                                 reply_markup=get_adept_detailed(adept_id))


@dp.callback_query_handler(open_menu_callback.filter(menu="buy_selected_adept"))
async def buy_selected_adept(call: CallbackQuery):
    if get_user_by_id(call.from_user.id).get("coin") >= ADEPT_COST_SELECT:
        await call.message.edit_text("Выберите адепта, которого хотите открыть:",
                                     reply_markup=get_adepts_for_open(call.from_user.id, False))
    else:
        await call.message.edit_text("Не хватает монет", reply_markup=back_to_adept_list)


@dp.callback_query_handler(open_menu_callback.filter(menu="buy_random_adept"))
async def buy_random_adept(call: CallbackQuery):
    if get_user_by_id(call.from_user.id).get("coin") >= ADEPT_COST_RANDOM:
        adept_id = get_random_unowned_adept_id(call.from_user.id)
        spend_coins(call.from_user.id, ADEPT_COST_RANDOM)
        add_trust(call.from_user.id, adept_id)
        adept_name = get_adept_by_id(adept_id)
        await call.message.edit_text(f"Случайный '{adept_name}' получен.",
                                     reply_markup=get_adept_detailed(adept_id))
    else:
        await call.message.edit_text("Не хватает монет", reply_markup=back_to_adept_list)


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
