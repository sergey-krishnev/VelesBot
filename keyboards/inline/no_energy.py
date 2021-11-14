from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from keyboards.inline.callback_data import open_menu_callback
from keyboards.inline.common import back_to_tree

no_energy_options = InlineKeyboardMarkup(inline_keyboard=[
    [
        InlineKeyboardButton(
            text="Восстановить полностью энергию за 10 монет",
            callback_data=open_menu_callback.new(menu="supply_energy_for_coins", id="0")
        )
    ],
    back_to_tree
])
