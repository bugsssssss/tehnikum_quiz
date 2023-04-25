import logging
from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor
from config import TOKEN
import requests
import json
import random

user_data = requests.get('http://127.0.0.1:8000/api/bot-users/').json()
print(user_data)

bot = Bot(token=TOKEN)
dp = Dispatcher(bot)



@dp.message_handler(commands=['start'])
async def send_welcome(message: types.Message):
    text = '''
    Привет)
Да, мы знаем, что как бы поздно уже готовиться к лету, но думаем, что стоит попробовать.

Если ты хочешь подтянуть именно свое тело, то ниже тебе чек-лист упражнений (не благодари)

Ну а мы считаем, что пресс должен быть не только на животе, но и в кармане. Поэтому подготовили для тебя скидки до 40% на наши курсы, для этого тебе тоже надо сделать несколько упражнений, каждое из которых поможет скинуть по 8 килограмм процентов от стоимости курса.

Если готов то жми на "Имя"
    '''
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    name = 'Имя'
    keyboard.add(name)
    # await send_photo(message.chat.id, text)
    await message.reply(text, reply_markup=keyboard, )

step = 'init'


@dp.message_handler(content_types=['text'])
async def get_text_messages(message: types.Message):
    user = {}
    global step
    if message.text == 'Имя' and step == 'init':
        await message.reply('Как тебя зовут?')
        step = 'name'

    elif step == 'name':
        user['first_name'] = message.text
        await message.reply('Отлично, а какой у тебя номер телефона?')
        keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
        name = 'Номер телефона'
        keyboard.add(name)
        step = 'phone'
    elif step == 'phone':
        user['phone_number'] = message.text
        confirmation_code = random.randint(1000, 9999)
        # Send the confirmation code to the user's phone number
        await bot.send_message(chat_id=message.chat.id, text=f"Your confirmation code is {confirmation_code}")
        step = 'confirm'


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
