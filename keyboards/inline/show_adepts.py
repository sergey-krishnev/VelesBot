from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from keyboards.inline.callback_data import open_menu_callback
from keyboards.inline.common import back_to_tree
from utils.constants import DIALOG_ENERGY_COST
from utils.db_api import db

show_adepts = InlineKeyboardMarkup(inline_keyboard=[
    [
        InlineKeyboardButton(
            text="Выбрать адепта",
            callback_data=open_menu_callback.new(menu="show_adepts", id="0")
        )
    ],
    [
        InlineKeyboardButton(
            text="Предложить свой вопрос",
            callback_data=open_menu_callback.new(menu="suggest_theme", id="0")
        )
    ],
    [
        InlineKeyboardButton(
            text="Мой профиль",
            callback_data=open_menu_callback.new(menu="my_profile", id="0")
        )
    ]
])


def get_admin_adept_keyboard() -> InlineKeyboardMarkup:
    inline = get_adept_list()
    return InlineKeyboardMarkup(inline_keyboard=inline)


def get_adept_list():
    adepts = db.fetchall("adepts", ["id", "name"])
    inline = []
    for adept in adepts:
        inline.append([InlineKeyboardButton(text=adept.get("name"),
                                            callback_data=open_menu_callback.new(menu="adept_list",
                                                                                 id=adept.get("id")))])
    return inline


def get_client_adept_keyboard() -> InlineKeyboardMarkup:
    inline = get_adept_list()
    inline.append(back_to_tree)
    return InlineKeyboardMarkup(inline_keyboard=inline)


def get_adept_detailed(adept_id) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(
                text=f"Начать диалог ( Стоимость {DIALOG_ENERGY_COST} энергии )",
                callback_data=open_menu_callback.new(menu="dialog_start", id=adept_id)
            )
        ],
        [
            InlineKeyboardButton(
                text="Назад с списку адептов",
                callback_data=open_menu_callback.new(menu="show_adepts", id="0")
            )
        ],
        back_to_tree
    ])


adept_detailed = InlineKeyboardMarkup(inline_keyboard=[
    [
        InlineKeyboardButton(
            text="Начать диалог",
            callback_data=open_menu_callback.new(menu="dialog_start", id="0")
        )
    ],
    [
        InlineKeyboardButton(
            text="Назад с списку адептов",
            callback_data=open_menu_callback.new(menu="show_adepts", id="0")
        )
    ],
    back_to_tree
])
