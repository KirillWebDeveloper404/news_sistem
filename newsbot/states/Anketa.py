from aiogram.dispatcher.filters.state import State, StatesGroup


class Anketa(StatesGroup):
    tg_id = State()
    name = State()
    link = State()
    city = State()
    subs = State()
    phone = State()
