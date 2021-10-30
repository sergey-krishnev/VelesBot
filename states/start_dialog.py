from aiogram.dispatcher.filters.state import StatesGroup, State


class Dialog(StatesGroup):
    ANSWER = State()
    QUESTION = State()
