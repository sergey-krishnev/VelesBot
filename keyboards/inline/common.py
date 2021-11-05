from aiogram.types import InlineKeyboardButton

from keyboards.inline.callback_data import open_menu_callback

back_to_tree = [
        InlineKeyboardButton(
            text="Вернуться в деревню адептов",
            callback_data=open_menu_callback.new(menu="great_tree", id="0")
        )
    ]