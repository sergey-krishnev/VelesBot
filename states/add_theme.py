from aiogram.dispatcher.filters.state import State, StatesGroup


class ThemeCreation(StatesGroup):
    THEME_NAME = State()
    CHOSEN_ADEPT = State()
