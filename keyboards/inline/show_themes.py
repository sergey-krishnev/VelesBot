from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from keyboards.inline.callback_data import open_menu_callback
from utils.db_api import db


def get_themes(adept_id) -> InlineKeyboardMarkup:
    themes = db.fetchall_with_filter("themes", ["id", "name"], [f"adept_id={adept_id}"])
    inline = []
    for theme in themes:
        inline.append([InlineKeyboardButton(text=theme.get("name"),
                                            callback_data=open_menu_callback.new(menu="themes",
                                                                                 id=theme.get("id")))])
    return InlineKeyboardMarkup(inline_keyboard=inline)
