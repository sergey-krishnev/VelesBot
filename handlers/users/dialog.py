import asyncio

from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.types import CallbackQuery

from keyboards.inline.callback_data import open_menu_callback
from keyboards.inline.no_energy import no_energy_options
from keyboards.inline.show_dialogs import get_active_dialogs
from keyboards.inline.suggest_question import add_question_to_connection, finish_suggest
from loader import dp
from states.add_question_to_connection import QuestionToConnection
from states.start_dialog import Dialog
from utils.constants import DIALOG_ENERGY_COST
from utils.db_api.adept_dao import get_adept_by_id
from utils.db_api.answer_dao import add_answer
from utils.db_api.checkpoint_dao import add_checkpoint, has_not_checkpoint, get_checkpoint_by_user_id, \
    is_not_solved_checkpoint, update_checkpoint_to_solve, update_checkpoint_to_unsolve, remove_checkpoint
from utils.db_api.connection_dao import add_connection, update_connection_with_answer, \
    update_connection_with_next_question, get_next_question_by_id, get_prev_question_by_id
from utils.db_api.dialog_dao import get_dialog_detailed
from utils.db_api.question_dao import get_random_question_by_theme, add_question_without_theme,\
    get_question_name_by_id, get_question_by_id
from utils.db_api.theme_dao import get_random_theme_by_adept
from utils.db_api.user_dao import spend_energy, get_user_by_id, register_user


@dp.callback_query_handler(open_menu_callback.filter(menu="dialog_start"), state=None)
async def start_dialog(call: CallbackQuery, callback_data: dict):
    user = get_user_by_id(call.from_user.id)
    if user is None:
        register_user(call.from_user.id)

    adept_name = get_adept_by_id(callback_data.get("id"))
    await call.message.edit_text(f"Диалог уже есть с '{adept_name}'")
    question = {"name": "Error"}  # TODO Какой это случай?
    checkpoint = get_checkpoint_by_user_id(call.from_user.id)
    if checkpoint is not None:
        question = get_question_by_id(get_prev_question_by_id(checkpoint.get("connection_id")))
    if has_not_checkpoint(call.from_user.id):
        adept_id = callback_data.get("id")
        theme_id = get_random_theme_by_adept(adept_id)
        question = get_random_question_by_theme(theme_id)
        prev_question_id = question.get("id")
        if get_user_by_id(call.from_user.id).get("energy") < DIALOG_ENERGY_COST:
            await call.message.edit_text(f"Не хватает энергии", reply_markup=no_energy_options)
            return
        connection_id = add_connection(prev_question_id)
        add_checkpoint(connection_id, call.from_user.id)
        spend_energy(call.from_user.id, DIALOG_ENERGY_COST)
        await call.message.edit_text(f"Диалог начат. Приятного общения. Чтобы попрощаться, введите 'пока'")
    await call.message.answer(question.get("name"))
    await Dialog.ANSWER.set()


@dp.message_handler(lambda message: message.text.lower() == "пока", state=Dialog.ANSWER)
async def catch_goodbye(message: types.Message, state: FSMContext):
    remove_checkpoint(message.from_user.id)
    await message.answer("Диалог окончен", reply_markup=finish_suggest)
    await state.finish()


@dp.message_handler(state=Dialog.ANSWER)
async def catch_answer(message: types.Message, state: FSMContext):
    data = await state.get_data()
    answer = message.text
    if data.get("answer") is not None:
        answer = data.get("answer")
    await state.update_data(answer=message.text)

    checkpoint = get_checkpoint_by_user_id(message.from_user.id)
    connection_id = checkpoint.get("connection_id")
    answer_id = data.get("answer_id")
    if answer_id is None:
        answer_id = add_answer(answer)
        await state.update_data(answer_id=answer_id)
    update_connection_with_answer(connection_id, answer_id)
    # TODO проинформировать админа, что ответ пришел от пользователя и нужно задать вопрос
    while is_not_solved_checkpoint(message.from_user.id):
        await asyncio.sleep(30)
    await state.reset_data()
    next_question_id = get_next_question_by_id(connection_id)
    await message.answer(get_question_name_by_id(next_question_id))
    next_connection_id = add_connection(next_question_id)
    update_checkpoint_to_unsolve(next_connection_id, checkpoint.get("id"))


@dp.callback_query_handler(open_menu_callback.filter(menu="show_dialogs"))
async def show_active_dialogs(call: CallbackQuery):
    active_dialogs = get_active_dialogs()
    if active_dialogs is not None:
        await call.message.edit_text("Список активных диалогов:", reply_markup=get_active_dialogs())
    else:
        await call.message.edit_text("Нет активных диалогов. Нажмите /manage, чтобы вернуться")


@dp.callback_query_handler(open_menu_callback.filter(menu="dialog_detailed"))
async def show_dialog_detailed(call: CallbackQuery, callback_data: dict):
    connection_id = callback_data.get("id")
    dialogs = "\n".join(get_dialog_detailed(connection_id))
    await call.message.edit_text(f"Диалог: \n {dialogs}", reply_markup=add_question_to_connection(connection_id))
    await QuestionToConnection.CONNECTION.set()


@dp.callback_query_handler(open_menu_callback.filter(menu="add_question_to_connection"),
                           state=QuestionToConnection.CONNECTION)
async def get_connection(call: CallbackQuery, callback_data: dict, state: FSMContext):
    connection_id = callback_data.get("id")
    await state.update_data(connection_id=connection_id)
    await call.message.edit_text("Введите вопрос:")
    await QuestionToConnection.next()


@dp.message_handler(state=QuestionToConnection.QUESTION)
async def add_next_question(message: types.Message, state: FSMContext):
    question = message.text
    data = await state.get_data()
    next_question_id = add_question_without_theme(question)
    update_connection_with_next_question(data.get("connection_id"), next_question_id)
    update_checkpoint_to_solve(data.get("connection_id"))
    await message.answer("Вопрос добавлен. Выберите /manage, чтобы вернуться.")
    await state.finish()
