from aiogram.filters.state import State, StatesGroup


class FSMRegistration(StatesGroup):
    age = State()
    name = State()
    info = State()
