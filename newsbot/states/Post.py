from aiogram.dispatcher.filters.state import State, StatesGroup


class Post(StatesGroup):
    subs = State()
    push = State()