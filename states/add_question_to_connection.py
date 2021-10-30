from aiogram.dispatcher.filters.state import StatesGroup, State


class QuestionToConnection(StatesGroup):
    CONNECTION = State()
    QUESTION = State()
