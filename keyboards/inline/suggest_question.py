from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from keyboards.inline.callback_data import open_menu_callback
from keyboards.inline.common import back_to_tree
from utils.db_api import db

finish_suggest = InlineKeyboardMarkup(inline_keyboard=[
    back_to_tree
])

question_source = InlineKeyboardMarkup(inline_keyboard=[
    [
        InlineKeyboardButton(
            text="Выбрать предложенные вопросы",
            callback_data=open_menu_callback.new(menu="select_suggested_question", id="0")
        )
    ],
    [
        InlineKeyboardButton(
            text="Предложить свой вопрос",
            callback_data=open_menu_callback.new(menu="suggest_question", id="0")
        )
    ],
])


def add_question_to_connection(connection_id):
    return InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(
                text="Добавить вопрос",
                callback_data=open_menu_callback.new(menu="add_question_to_connection", id=connection_id)
            )
        ]
    ])


def get_suggested_questions() -> InlineKeyboardMarkup:
    suggestions = db.fetchall("suggestions", ["id", "name"])[:5]
    inline = []
    for suggestion in suggestions:
        inline.append([InlineKeyboardButton(text=suggestion.get("name"),
                                            callback_data=open_menu_callback.new(menu="suggested_question",
                                                                                 id=suggestion.get("id")))])
    return InlineKeyboardMarkup(inline_keyboard=inline)
