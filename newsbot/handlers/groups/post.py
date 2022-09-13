from aiogram.types import Message, CallbackQuery, InlineKeyboardButton, InlineKeyboardMarkup, KeyboardButton, ReplyKeyboardMarkup
from aiogram.dispatcher.storage import FSMContext

from loader import dp, bot
from states import Post
from sql import User, Tema
from data.config import admin_chat


async def show(message: Message, state: FSMContext):
    data = await state.get_data()
    tems = Tema.select()

    tema = []
    for el in tems:
        tema.append(
            [KeyboardButton(el.name)]
        )

    kb = ReplyKeyboardMarkup(keyboard=tema, resize_keyboard=True)
    await message.answer('Рассылка', reply_markup=kb)

    text = 'Настройте фильтры рассылки \n' \
                'Для отправки пришлите сообщение с текстом или фото(можно с подписью) \n'
    text += f'Подписчики: {data["subs_min"]} - {data["subs_max"]}' if data['subs_min'] != 0 or data['subs_max'] != 999999999 else ''
    text += f'Тематики: {data["tema"]}'

    await message.answer(
            text=text,
            reply_markup=InlineKeyboardMarkup(row_width=2).add(
                InlineKeyboardButton(text=f'{data["animals"]} Животные', callback_data='animals'),
                InlineKeyboardButton(text=f'{data["kids"]} Дети', callback_data='kids'),
                InlineKeyboardButton(text=f'{data["men"]} Муж', callback_data='men'),
                InlineKeyboardButton(text=f'{data["women"]} Жен', callback_data='women'),
                InlineKeyboardButton(text='Количество подписчиков', callback_data='subs')
            ).add(
                InlineKeyboardButton(text='Готово', callback_data='send')
            )
        )

    await Post.push.set()


@dp.message_handler(commands=['post'], state='*')
async def post(message: Message, state: FSMContext):
    if message.chat.id == int(admin_chat):
        data = {
            'animals': '❌',
            'kids': '❌',
            'men': '✅',
            'women': '✅',
            'tema': [],
            'subs_min': 0,
            'subs_max': 999999999
        }
        await state.set_data(data)

        await show(message, state)


@dp.callback_query_handler(text='animals', state='*')
async def animals(c: CallbackQuery, state: FSMContext):
    if c.message.chat.id == int(admin_chat):
        data = await state.get_data()
        
        if data['animals'] == '❌':
            data['animals'] = '✅'
        elif data['animals'] == '✅':
            data['animals'] = '❌'

        await state.update_data(data)

        await show(c.message, state)


@dp.callback_query_handler(text='kids', state='*')
async def kids(c: CallbackQuery, state: FSMContext):
    if c.message.chat.id == int(admin_chat):
        data = await state.get_data()
        
        if data['kids'] == '❌':
            data['kids'] = '✅'
        elif data['kids'] == '✅':
            data['kids'] = '❌'

        await state.update_data(data)

        await show(c.message, state)


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

            await show(message, state)

            await Post.push.set()

        except Exception as e:
            print(e)
            await message.answer('Неверный формат!')


@dp.callback_query_handler(text='men', state='*')
async def men(c: CallbackQuery, state: FSMContext):
    if c.message.chat.id == int(admin_chat):
        data = await state.get_data()
        
        if data['men'] == '❌':
            data['men'] = '✅'
        elif data['men'] == '✅':
            data['men'] = '❌'

        await state.update_data(data)

        await show(c.message, state)


@dp.callback_query_handler(text='women', state='*')
async def women(c: CallbackQuery, state: FSMContext):
    if c.message.chat.id == int(admin_chat):
        data = await state.get_data()
        
        if data['women'] == '❌':
            data['women'] = '✅'
        elif data['women'] == '✅':
            data['women'] = '❌'

        await state.update_data(data)

        await show(c.message, state)


@dp.message_handler(state=Post.push)
async def tema(message: Message, state: FSMContext):
    data = await state.get_data()

    if message.text in data['tema']:
        data['tema'].pop(data['tema'].index(message.text))
    else:
        data['tema'].append(message.text)

    await state.update_data(data)

    await show(message, state)


@dp.callback_query_handler(text='send', state=Post.push)
async def send(c: CallbackQuery, state: FSMContext):
    await Post.send.set()
    await c.message.answer('Пришлите сообщение для рассылки')


@dp.message_handler(content_types=['photo', 'text'], state=Post.send)
async def push(message: Message, state: FSMContext):
    if message.chat.id == int(admin_chat):
        num = 0
        users = User.select()
        data = await state.get_data()
        data['animals'] = data['animals'] == '✅'
        data['kids'] = data['kids'] == '✅'

        if data['subs_max'] == -1:
            data['subs_max'] = 999999999999999999999999999999999999999
        
        for user in users:
            send = False

            user.kids = user.kids == 'yes'
            user.animals = user.animals == 'yes'

            if data['animals'] == False:
                user.animals = False
            if data['kids'] == False:
                user.kids = False

            if user.sex == 'm' and data['men'] == '✅':
                send = True
            elif user.sex == 'w' and data['women'] == '✅':
                send = True
            else:
                send = True

            if len(data['tema']) > 0:
                tem_list = [el.name for el in user.tema]
                for el in data['tema']:
                    if el in tem_list:
                        send = True
                    else:
                        send = False
                        break
 
            if (user.apruve) and (send) and (user.animals == data['animals']) and (user.kids == data['kids']) and (user.subs >= data['subs_min']) and (user.subs <= data['subs_max']):
                try:
                    num += 1
                    text = message.text if message.text else message.caption
                    chat_id = user.tg_id

                    if message.text is not None:
                        await bot.send_message(chat_id=chat_id, text=text)

                    elif message.photo is not None:
                        await bot.send_photo(chat_id=chat_id, photo=message.photo[-1].file_id,
                                        caption=text, parse_mode='html')
                except:
                    num-=1

        await message.answer(f'Готово \nРассылка доставлена {num} из {len(users)} пользователей')
        await state.finish()
