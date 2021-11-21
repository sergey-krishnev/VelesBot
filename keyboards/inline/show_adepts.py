from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from keyboards.inline.callback_data import open_menu_callback
from keyboards.inline.common import back_to_tree
from utils.constants import DIALOG_ENERGY_COST, ADEPT_COST_SELECT, ADEPT_COST_RANDOM
from utils.db_api import db
from utils.db_api.trust_dao import is_not_all_adepts_opened

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
    inline = []
    adepts = db.fetchall("adepts", ["id", "name"])
    for adept in adepts:
        inline.append([InlineKeyboardButton(text=adept.get("name"),
                                            callback_data=open_menu_callback.new(menu="adept_list",
                                                                                 id=adept.get("id")))])
    return InlineKeyboardMarkup(inline_keyboard=inline)


def get_adept_list(user_id):
    opened_adepts_ids = db.fetchall_with_filter("trust", ["adept_id"], [f"user_id={user_id}"])
    if opened_adepts_ids:
        opened_adepts_ids = tuple([c["adept_id"] for c in opened_adepts_ids])
        adepts = db.fetchall_with_filter("adepts", ["id", "name"], [f"id in {tuple(opened_adepts_ids)}"
                                                                    if len(opened_adepts_ids) > 1
                                                                    else f"id={opened_adepts_ids[0]}"])
    else:
        adepts = db.fetchall("adepts", ["id", "name"])
    inline = []
    for adept in adepts:
        inline.append([InlineKeyboardButton(text=adept.get("name"),
                                            callback_data=open_menu_callback.new(menu="adept_list",
                                                                                 id=adept.get("id")))])
    return inline


def get_client_adept_keyboard(user_id) -> InlineKeyboardMarkup:
    inline = get_adept_list(user_id)
    inline.append(back_to_tree)
    if is_not_all_adepts_opened(user_id):
        inline.append([
            InlineKeyboardButton(
                text=f"Открыть желаемого адепта за {ADEPT_COST_SELECT} монет",
                callback_data=open_menu_callback.new(menu="buy_selected_adept", id="0")
            )
        ])
        inline.append([
            InlineKeyboardButton(
                text=f"Открыть случайного адепта за {ADEPT_COST_RANDOM} монет",
                callback_data=open_menu_callback.new(menu="buy_random_adept", id="0")
            )
        ])
    return InlineKeyboardMarkup(inline_keyboard=inline)


def get_adept_list_except_opened(user_id, is_free):
    opened_adepts_ids = db.fetchall_with_filter("trust", ["adept_id"], [f"user_id={user_id}"])
    if opened_adepts_ids:
        opened_adepts_ids = tuple([c["adept_id"] for c in opened_adepts_ids])
        adepts = db.fetchall_with_filter("adepts", ["id", "name"], [f"id not in {tuple(opened_adepts_ids)}"
                                                                    if len(opened_adepts_ids) > 1
                                                                    else f"id<>{opened_adepts_ids[0]}"])
    else:
        adepts = db.fetchall("adepts", ["id", "name"])
    inline = []
    for adept in adepts:
        inline.append([InlineKeyboardButton(text=adept.get("name"),
                                            callback_data=open_menu_callback.new(menu="purchase_free_adept"
                                            if is_free else "purchase_adept",
                                                                                 id=adept.get("id")))])
    return inline


def get_adepts_for_open(user_id, is_free) -> InlineKeyboardMarkup:
    inline = get_adept_list_except_opened(user_id, is_free)
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

back_to_adept_list = InlineKeyboardMarkup(inline_keyboard=[
    [
        InlineKeyboardButton(
            text="Назад с списку адептов",
            callback_data=open_menu_callback.new(menu="show_adepts", id="0")
        )
    ],
])
