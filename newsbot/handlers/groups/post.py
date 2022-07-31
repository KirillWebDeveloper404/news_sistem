from aiogram.types import Message

from loader import dp, bot
from sql import User
from data.config import admin_chat


@dp.message_handler(content_types=['photo', 'text'])
async def post(message: Message):
    if message.chat.id == int(admin_chat):
        users = User.select()
        
        for user in users:
            if user.apruve:
                text = message.text if message.text else message.caption
                chat_id = user.tg_id

                if message.text is not None:
                    await bot.send_message(chat_id=chat_id, text=text)

                elif message.photo is not None:
                    await bot.send_photo(chat_id=chat_id, photo=message.photo[-1].file_id,
                                        caption=text)
