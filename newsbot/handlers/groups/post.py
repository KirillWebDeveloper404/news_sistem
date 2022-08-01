from aiogram.types import Message, CallbackQuery, InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.dispatcher.storage import FSMContext

from loader import dp, bot
from states import Post
from sql import User
from data.config import admin_chat


@dp.message_handler(commands=['post'], state='*')
async def post(message: Message, state: FSMContext):
    if message.chat.id == int(admin_chat):
        data = {
            'animals': '❌',
            'kids': '❌',
            'subs_min': 0,
            'subs_max': -1
        }
        await state.set_data(data)

        await message.answer(
            text='Настройте фильтры рассылки \n' \
                'Для отправки пришлите сообщение с текстом или фото(можно с подписью)',
            reply_markup=InlineKeyboardMarkup(row_width=2).add(
                InlineKeyboardButton(text=f'{data["animals"]} Животные', callback_data='animals'),
                InlineKeyboardButton(text=f'{data["kids"]} Дети', callback_data='kids'),
                InlineKeyboardButton(text='Количество подписчиков', callback_data='subs')
            )
        )

        await Post.push.set()


@dp.callback_query_handler(text='animals', state='*')
async def animals(c: CallbackQuery, state: FSMContext):
    if c.message.chat.id == int(admin_chat):
        data = await state.get_data()
        
        if data['animals'] == '❌':
            data['animals'] = '✅'
        elif data['animals'] == '✅':
            data['animals'] = '❌'

        await state.update_data(data)

        text = 'Настройте фильтры рассылки \n' \
                'Для отправки пришлите сообщение с текстом или фото(можно с подписью) \n'
        text += f'Подписчики: {data["subs_min"]} - {data["subs_max"]}' if data['subs_min'] != 0 or data['subs_max'] != -1 else ''

        await c.message.edit_text(
            text=text,
            reply_markup=InlineKeyboardMarkup(row_width=2).add(
                InlineKeyboardButton(text=f'{data["animals"]}Животные', callback_data='animals'),
                InlineKeyboardButton(text=f'{data["kids"]}Дети', callback_data='kids'),
                InlineKeyboardButton(text='Количество подписчиков', callback_data='subs')
            )
        )


@dp.callback_query_handler(text='kids', state='*')
async def kids(c: CallbackQuery, state: FSMContext):
    if c.message.chat.id == int(admin_chat):
        data = await state.get_data()
        
        if data['kids'] == '❌':
            data['kids'] = '✅'
        elif data['kids'] == '✅':
            data['kids'] = '❌'

        await state.update_data(data)

        text = 'Настройте фильтры рассылки \n' \
                'Для отправки пришлите сообщение с текстом или фото(можно с подписью) \n'
        text += f'Подписчики: {data["subs_min"]} - {data["subs_max"]}' if data['subs_min'] != 0 or data['subs_max'] != -1 else ''

        await c.message.edit_text(
            text=text,
            reply_markup=InlineKeyboardMarkup(row_width=2).add(
                InlineKeyboardButton(text=f'{data["animals"]}Животные', callback_data='animals'),
                InlineKeyboardButton(text=f'{data["kids"]}Дети', callback_data='kids'),
                InlineKeyboardButton(text='Количество подписчиков', callback_data='subs')
            )
        )


@dp.callback_query_handler(text='subs', state='*')
async def subs(c: CallbackQuery, state: FSMContext):
    if c.message.chat.id == int(admin_chat):
        await c.message.edit_text(
            'Введите диапозон количества подписчиков, в формате \n' \
            '0 / 500 \n' \
            'если максимальное количество подписчиков не ограничено введите -1 \n' \
            '500 / -1'
        )
        await Post.subs.set()


@dp.message_handler(state=Post.subs)
async def set_subs(message: Message, state: FSMContext):
    if message.chat.id == int(admin_chat):
        data = await state.get_data()

        try:
            s_min = int(message.text.split('/')[0].replace(' ', ''))
            s_max = int(message.text.split('/')[1].replace(' ', ''))

            data['subs_min'] = s_min
            data['subs_max'] = s_max

            await state.update_data(data)

            text='Настройте фильтры рассылки \n' \
                    'Для отправки пришлите сообщение с текстом или фото(можно с подписью) \n'
            text += f'Подписчики: {data["subs_min"]} - {data["subs_max"]}' if data['subs_min'] != 0 or data['subs_max'] != -1 else ''

            await message.answer(
                text=text,
                reply_markup=InlineKeyboardMarkup(row_width=2).add(
                    InlineKeyboardButton(text=f'{data["animals"]}Животные', callback_data='animals'),
                    InlineKeyboardButton(text=f'{data["kids"]}Дети', callback_data='kids'),
                    InlineKeyboardButton(text='Количество подписчиков', callback_data='subs')
                )
            )

            await Post.push.set()

        except Exception as e:
            print(e)
            await message.answer('Неверный формат!')


@dp.message_handler(content_types=['photo', 'text'], state=Post.push)
async def push(message: Message, state: FSMContext):
    if message.chat.id == int(admin_chat):
        users = User.select()
        data = await state.get_data()
        data['animals'] = data['animals'] == '✅'
        data['kids'] = data['kids'] == '✅'

        if data['subs_max'] == -1:
            data['subs_max'] = 999999999999999999999999999999999999999
        
        for user in users:
            user.kids = user.kids == 'yes'
            user.animals = user.animals == 'yes'
            print(user.kids, user.animals)
            if (user.apruve) and (user.animals == data['animals']) and (user.kids == data['kids']) and (user.subs >= data['subs_min']) and (user.subs <= data['subs_max']):
                text = message.text if message.text else message.caption
                chat_id = user.tg_id

                if message.text is not None:
                    await bot.send_message(chat_id=chat_id, text=text)

                elif message.photo is not None:
                    await bot.send_photo(chat_id=chat_id, photo=message.photo[-1].file_id,
                                        caption=text)

        await message.answer('Готово')
        await state.finish()