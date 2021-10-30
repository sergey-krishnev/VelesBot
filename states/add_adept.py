from aiogram.dispatcher.filters.state import StatesGroup, State


class AdeptCreation(StatesGroup):
    ADEPT_NAME = State()
    ADEPT_DESCRIPTION = State()
