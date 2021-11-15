from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.types import CallbackQuery

from keyboards.inline.callback_data import open_menu_callback
from keyboards.inline.suggest_question import finish_suggest
from loader import dp
from states.suggest_theme import SuggestionTheme
from utils.db_api.suggestion_dao import add_suggestion


@dp.callback_query_handler(open_menu_callback.filter(menu="suggest_theme"), state=None)
async def suggest_question(call: CallbackQuery):
    await call.message.edit_text("Введите вопрос, который можно будет задать в начале диалога")
    await SuggestionTheme.ROOT_QUESTION.set()


@dp.message_handler(state=SuggestionTheme.ROOT_QUESTION)
async def catch_question(message: types.Message, state: FSMContext):
    suggestion = message.text
    add_suggestion(suggestion, message.from_user.id)
    await message.answer(f"Ваше предложение: '{suggestion}' добавлено", reply_markup=finish_suggest)
    await state.finish()
