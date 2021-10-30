from aiogram.dispatcher.filters.state import StatesGroup, State


class RootQuestionCreation(StatesGroup):
    QUESTION = State()
    ADEPT = State()
    THEME = State()
