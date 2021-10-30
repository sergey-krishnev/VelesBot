from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.types import CallbackQuery

from keyboards.inline.callback_data import open_menu_callback
from keyboards.inline.show_adepts import get_admin_adept_keyboard
from keyboards.inline.show_themes import get_themes
from keyboards.inline.suggest_question import question_source, get_suggested_questions
from loader import dp
from states.add_root_question import RootQuestionCreation
from utils.db_api.question_dao import add_question
from utils.db_api.suggestion_dao import get_suggestion_by_id


@dp.callback_query_handler(open_menu_callback.filter(menu="add_root_question"), state=None)
async def add_root_question(call: CallbackQuery):
    await call.message.edit_text("Выберите источник вопроса:", reply_markup=question_source)


@dp.callback_query_handler(open_menu_callback.filter(menu="suggest_question"), state=None)
async def suggest_question(call: CallbackQuery):
    await call.message.edit_text("Введите вопрос:")
    await RootQuestionCreation.QUESTION.set()


@dp.callback_query_handler(open_menu_callback.filter(menu="suggested_question"), state=None)
async def suggested_question(call: CallbackQuery, callback_data: dict):
    suggestion_id = callback_data.get("id")
    suggestion = get_suggestion_by_id(suggestion_id)
    await call.message.edit_text(f"Перепишите вопрос в соответствии с правилами: '{suggestion}'")
    await RootQuestionCreation.QUESTION.set()


@dp.message_handler(state=RootQuestionCreation.QUESTION)
async def catch_question(message: types.Message, state: FSMContext):
    question_name = message.text
    await state.update_data(question_name=question_name)
    await message.answer("Выберите адепта", reply_markup=get_admin_adept_keyboard())
    await RootQuestionCreation.next()


@dp.callback_query_handler(open_menu_callback.filter(menu="adept_list"), state=RootQuestionCreation.ADEPT)
async def catch_chosen_adept(call: CallbackQuery, callback_data: dict):
    adept_id = callback_data.get("id")
    await call.message.edit_text("Выберите тему:", reply_markup=get_themes(adept_id))
    await RootQuestionCreation.next()


@dp.callback_query_handler(open_menu_callback.filter(menu="themes"), state=RootQuestionCreation.THEME)
async def catch_chosen_theme(call: CallbackQuery, callback_data: dict, state: FSMContext):
    data = await state.get_data()
    question_name = data.get("question_name")
    theme_id = callback_data.get("id")
    add_question(question_name, theme_id)
    await call.message.edit_text(f"Вопрос '{question_name}' добавлен. Выберите /manage, чтобы вернуться")
    await state.finish()


@dp.callback_query_handler(open_menu_callback.filter(menu="select_suggested_question"), state=None)
async def select_suggested_question(call: CallbackQuery):
    await call.message.edit_text("Выберите предложенные вопросы:", reply_markup=get_suggested_questions())
