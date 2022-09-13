from aiogram.types import Message
from aiogram.dispatcher.storage import FSMContext


from loader import dp
from sql import User
from states import Anketa


@dp.message_handler(state=Anketa.name)
async def name(message: Message, state: FSMContext):
    user = User.get(User.tg_id == message.from_user.id)
    user.name = message.text
    user.save()

    await message.answer('Теперь отправте ссылку на свою соц сеть')
    await Anketa.link.set()


@dp.message_handler(state=Anketa.link)
async def link(message: Message, state: FSMContext):
    user = User.get(User.tg_id == message.from_user.id)
    user.link = message.text
    user.save()

    await message.answer('Сколько у вас подписчиков')
    await Anketa.subs.set()


@dp.message_handler(state=Anketa.subs)
async def subs(message: Message, state: FSMContext):
    try:
        user = User.get(User.tg_id == message.from_user.id)
        user.subs = int(message.text)
        user.save()

        await message.answer('Пришлите ваш город')
        await Anketa.city.set()

    except ValueError:
        await message.answer('Отправте только число')


@dp.message_handler(state=Anketa.city)
async def city(message: Message, state: FSMContext):
    user = User.get(User.tg_id == message.from_user.id)
    user.city = message.text
    user.save()

    await message.answer('Поздравляем вы прошли регистрацию, мы будем вам присылать свежие новости')
    await state.finish()
