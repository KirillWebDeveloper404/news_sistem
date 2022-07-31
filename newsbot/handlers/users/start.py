from aiogram import types
from aiogram.dispatcher.filters.builtin import CommandStart

from loader import dp
from sql import User
from states import Anketa


@dp.message_handler(CommandStart())
async def bot_start(message: types.Message):
    try:
        user = User.get(User.tg_id == message.from_user.id)

        if user:
            await message.answer(f"Привет, {user.name}! \n" \
                "Это новостной бот, мы будем присылать тебе свежие новости")

    except User.DoesNotExist:
        await message.answer('Для начала заполните анкету')
        await message.answer('Как вас зовут')
        await Anketa.name.set()
