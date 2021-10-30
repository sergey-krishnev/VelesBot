from aiogram.dispatcher.filters.state import StatesGroup, State


class SuggestionTheme(StatesGroup):
    ROOT_QUESTION = State()
    