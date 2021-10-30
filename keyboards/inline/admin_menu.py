from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from keyboards.inline.callback_data import open_menu_callback

admin_menu = InlineKeyboardMarkup(inline_keyboard=[
    [
        InlineKeyboardButton(
            text="Показать активные диалоги",
            callback_data=open_menu_callback.new(menu="show_dialogs", id="0")
        )
    ],
    [
        InlineKeyboardButton(
            text="Добавить адепта",
            callback_data=open_menu_callback.new(menu="add_adept", id="0")
        )
    ],
    [
        InlineKeyboardButton(
            text="Добавить тему",
            callback_data=open_menu_callback.new(menu="add_theme", id="0")
        )
    ],
    [
        InlineKeyboardButton(
            text="Добавить вопрос",
            callback_data=open_menu_callback.new(menu="add_root_question", id="0")
        )
    ]
])
