from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from keyboards.inline.callback_data import open_menu_callback

great_tree = InlineKeyboardMarkup(inline_keyboard=[
                                    [
                                        InlineKeyboardButton(
                                            text="Начать свой путь",
                                            callback_data=open_menu_callback.new(menu="great_tree", id="0")
                                        )
                                    ]
                                 ])
