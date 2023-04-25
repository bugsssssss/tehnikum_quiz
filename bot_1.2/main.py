from aiogram import Dispatcher, executor, Bot, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
import os
from states import Registration
import buttons
import database
from config import TOKEN
from sms import send_sms
import random
import requests
from aiogram.utils.deep_linking import decode_payload


bot = Bot(token=TOKEN, parse_mode='HTML')
dp = Dispatcher(bot, storage=MemoryStorage())


@dp.message_handler(commands=['start'])
async def start_message(message):
    caption = '''Привет)
Да, мы знаем, что как бы поздно уже готовиться к лету, но думаем, что стоит попробовать.

Если ты хочешь подтянуть именно свое тело, то ниже тебе чек-лист упражнений (не благодари)

Ну а мы считаем, что пресс должен быть не только на животе, но и в кармане. Поэтому подготовили для тебя <b>скидки до 40% на наши курсы</b>, для этого тебе тоже надо сделать несколько упражнений, каждое из которых поможет скинуть по 8 <s>килограмм</s> процентов от стоимости курса.

Если готов то жми на "Поумней!"'''
    args = message.get_args()
    if args:
        name, phone_number = args.split('-')
        file_path = os.path.join(os.getcwd(), "tehnikum.jpg")
        with open(file_path, "rb") as photo:

            await bot.send_photo(chat_id=message.chat.id,
                                 photo=photo,
                                 caption=caption, parse_mode=types.ParseMode.HTML, reply_markup=buttons.web_app_kb())
            user_data = {
                'id': message.chat.id,
                'first_name': name,
                'phone_number': phone_number,
                'is_verified': True,
                'verification_code': 0
            }
            response = requests.post(
                'http://127.0.0.1:8000/api/bot-users/', data=user_data)
            print(f'User has been created: {response.json()}')

    else:
        caption = '''Привет)
    Да, мы знаем, что как бы поздно уже готовиться к лету, но думаем, что стоит попробовать.

    Если ты хочешь подтянуть именно свое тело, то ниже тебе чек-лист упражнений (не благодари)

    Ну а мы считаем, что пресс должен быть не только на животе, но и в кармане. Поэтому подготовили для тебя <b>скидки до 40% на наши курсы</b>, для этого тебе тоже надо сделать несколько упражнений, каждое из которых поможет скинуть по 8 <s>килограмм</s> процентов от стоимости курса.

    Если готов то жми на "Имя"'''
        # ? Получить user_id пользователя
        user_id = message.from_user.id

        user = requests.get(
            f'http://127.0.0.1:8000/api/bot-users/?id={user_id}').json()

        if user and user[0]['is_verified']:
            await message.answer('Жми на <b>Поумней!</b> ⬇️', reply_markup=buttons.web_app_kb())
        elif user and not user[0]['is_verified']:
            await message.answer('Подтверди свой номер телефона', reply_markup=buttons.phone_number_kb())
            await Registration.getting_phone_number.set()
            get_number(message)
        else:
            file_path = os.path.join(os.getcwd(), "tehnikum.jpg")
            with open(file_path, "rb") as photo:

                await bot.send_photo(chat_id=message.chat.id,
                                     photo=photo,
                                     caption=caption, parse_mode=types.ParseMode.HTML, reply_markup=buttons.name_kb())

            # ? Переход на этап получения имени
            await Registration.getting_started.set()


@ dp.message_handler(state=Registration.getting_started)
async def getting_started(message):
    await message.answer('''Красава!
Мы всегда за то, что надо качать не только 🍑 , но  и 🧠

Как зовут то тебя? Один (одна) тут отдыхаешь?''')

    await Registration.getting_name_state.set()


# Этап получения имени
@ dp.message_handler(state=Registration.getting_name_state)
async def get_name(message, state=Registration.getting_name_state):
    # Получаем отправленное имя
    user_name = message.text
    await state.update_data(name=user_name)

    await message.answer('Теперь нужен твой номер телефона, чтобы зачислить по нему скидку)', reply_markup=buttons.phone_number_kb())

    # Переход на этап получения номера

    await Registration.getting_phone_number.set()


# Этап получения номера телефона
@ dp.message_handler(state=Registration.getting_phone_number, content_types=['contact'])
async def get_number(message, state=Registration.getting_phone_number):
    # Получаем отправленный контакт
    await state.update_data(user_id=message.from_user.id)
    print(message.text)
    if message.contact:
        phone_number = message.contact.phone_number
        get_verification(message, state=Registration.getting_verification_code)
    elif len(message.text) == 12:
        phone_number = message.text
        get_verification(message, state=Registration.getting_verification_code)
    else:
        await message.answer('Неверный формат номера')

    await state.update_data(number=phone_number)

    await message.answer('Теперь надо подтвердить. Отправили тебе смс с кодом, введи его сюда)', reply_markup=types.ReplyKeyboardRemove())

    # ? отправляем смс с кодом подтверждения
    verification_code = random.randint(1000, 999999)
    # send_sms(message.contact.phone_number,
    #          f'Ваш код подтверждения: {verification_code}')

    all_info = await state.get_data()

    name = all_info.get("name")
    user_id = message.from_user.id
    code = all_info.get("verification_code")

    already_user = requests.get(
        f'http://127.0.0.1:8000/api/bot-users/?id={message.from_user.id}').json()
    print(already_user)

    # ? Проверяем, есть ли пользователь в базе
    if already_user:
        new_user_info = {
            "id": user_id,
            "first_name": already_user[0]['first_name'],
            "phone_number": phone_number,
            "verification_code": verification_code,
            "is_verified": "False"
        }
        url = f'http://127.0.0.1:8000/api/bot-users/{user_id}/'

        # ? Обновляем его верификационный код
        response = requests.put(url, data=new_user_info)
        print(f'Verification code has been updated: {response.json()}')
    else:
        user_info = {
            "id": user_id,
            "first_name": name,
            "phone_number": phone_number,
            "verification_code": verification_code,
            "is_verified": "False"

        }
        url = 'http://127.0.0.1:8000/api/bot-users/'

        # ? Отпправляем юзера в базу данных
        response = requests.post(url, data=user_info)
        print(f'User has been created: {response.json()}')

    # database.add_user(user_id, name, phone_number, code)
    # print(database.get_users())


@ dp.message_handler(state=Registration.getting_phone_number, content_types=['text'])
async def get_verification(message, state=Registration.getting_verification_code,):
    verification_code = message.text
    await state.update_data(verification_code=verification_code)

    url = f'http://127.0.0.1:8000/api/bot-users/?id={message.from_user.id}'

    try:

        user = requests.get(url).json()[0]
        print(user)

    except:
        user = None

    # ? Проверяем, есть ли пользователь в базе
    if user:
        # ? Проверяем код подтверждения
        if int(verification_code) == int(user['verification_code']):
            await message.answer('Верификация прошла успешно! Теперь ты зарегистрирован в нашей системе и уже можешь пройти квиз и получить скидку на курc. Жми на <b>Пройти квиз!</b> ⬇️', reply_markup=buttons.web_app_kb())
            user_data = {
                'id': user['id'],
                'first_name': user['first_name'],
                'phone_number': user['phone_number'],
                "is_verified": "True",
                'verification_code': user['verification_code']
            }
            url = f'http://127.0.0.1:8000/api/bot-users/{user["id"]}/'
            response = requests.put(url, data=user_data)
            # ? Обновляем статус верификации
            print(f'Is verified status has been updated: {response.json()}')
        else:
            await message.answer('Неверный код подтверждения! Проверьте свой номер!', reply_markup=buttons.phone_number_kb())
            await Registration.getting_phone_number.set()

    all_info = await state.get_data()
    print(all_info)

    await Registration.getting_verification_code.set()

executor.start_polling(dp, skip_updates=True)
