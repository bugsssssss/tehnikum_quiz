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
import json

registered_numbers = []


bot = Bot(token=TOKEN, parse_mode='HTML')
dp = Dispatcher(bot, storage=MemoryStorage())

status = 'start'


@dp.message_handler(commands=['start'])
async def start_message(message):
    print(f'Step 1 - start_message. From user: {message.from_user.id}')
    caption1 = '''Привет)
Да, мы знаем, что как бы поздно уже готовиться к лету, но думаем, что стоит попробовать.

Если ты хочешь подтянуть именно свое тело, то ниже тебе чек-лист упражнений (не благодари)

Ну а мы считаем, что пресс должен быть не только на животе, но и в кармане. Поэтому подготовили для тебя <b>скидки до 40% на наши курсы</b>, для этого тебе тоже надо сделать несколько упражнений, каждое из которых поможет скинуть по 8 <s>килограмм</s> процентов от стоимости курса.

Если готов то жми на "Поумней!"'''
    caption2 = '''Привет)
Да, мы знаем, что как бы поздно уже готовиться к лету, но думаем, что стоит попробовать.

Если ты хочешь подтянуть именно свое тело, то ниже тебе чек-лист упражнений (не благодари)

Ну а мы считаем, что пресс должен быть не только на животе, но и в кармане. Поэтому подготовили для тебя <b>скидки до 40% на наши курсы</b>, для этого тебе тоже надо сделать несколько упражнений, каждое из которых поможет скинуть по 8 <s>килограмм</s> процентов от стоимости курса.

Если готов то жми на "Имя"'''
    caption_final = '''
Таааак, вот и первые добровольцы у нас!

Если не успели подготовиться к лету, то
в бассейн можно походить и в водолазном костюме, а вот без новой профессии и $
не разгуляешься

Поэтому давай-ка мы тебя подтянем по скиллам, чтобы лето не прошло зря!

Жми «ПОУМНЕТЬ»"'''
    args = message.get_args()
    if args:

        response = requests.get(
            f'https://p-api2.tehnikum.school/api/temp-users/{args}/')
        if response.status_code == 200:
            print('такой юзер есть')
            user_data_json = response.json()
            name = user_data_json['name']
            phone_number = user_data_json['phone_number']
            url = f'https://tg-api.tehnikum.school/amo_crm/v1/create_lead?phone={phone_number}&name={name}&action=m-bot'
            response = requests.get(url)
            print(response.text)
            file_path = os.path.join(os.getcwd(), "tehnikum.jpg")
            with open(file_path, "rb") as photo:

                await bot.send_photo(chat_id=message.chat.id,
                                     photo=photo,
                                     caption=caption1, parse_mode=types.ParseMode.HTML, reply_markup=buttons.web_app_inline_kb())

            user_data = {
                'id': message.chat.id,
                'first_name': name,
                'phone_number': phone_number,
                'is_verified': True,
                'verification_code': 0
            }
            response = requests.post(
                'https://p-api2.tehnikum.school/api/bot-users/', data=user_data)
            print(f'User has been created: {response.json()}')
    else:
        user_id = message.from_user.id

        user = requests.get(
            f'https://p-api2.tehnikum.school/api/bot-users/?id={user_id}').json()

        if user and user[0]['is_verified']:
            await message.answer(caption_final, parse_mode=types.ParseMode.HTML, reply_markup=buttons.web_app_inline_kb())
        else:
            await Registration.getting_started.set()
            file_path = os.path.join(os.getcwd(), "tehnikum.jpg")
            with open(file_path, "rb") as photo:
                await bot.send_photo(chat_id=message.chat.id,
                                     photo=photo,
                                     caption=caption2, parse_mode=types.ParseMode.HTML, reply_markup=buttons.name_kb())


@dp.message_handler(state=Registration.getting_started)
async def getting_started(message):
    global status
    print(f'Step 2 - getting_started.  From user: {message.from_user.id}')
    status = 'name'
    await message.answer('''Красава!
Мы всегда за то, что надо качать не только 🍑 , но  и 🧠

Как зовут то тебя? Один (одна) тут отдыхаешь?''')

    await Registration.getting_name_state.set()


# ? Этап получения имени


@ dp.message_handler(state=Registration.getting_name_state)
async def get_name(message, state=Registration.getting_name_state):
    print(f'Step 3 - get_name.  From user: {message.from_user.id}')

    global status
    # ? Получаем отправленное имя
    user_name = message.text
    await state.update_data(name=user_name)

    await message.answer('Теперь нужен твой номер телефона, чтобы зачислить по нему скидку)', reply_markup=buttons.phone_number_kb(), parse_mode=types.ParseMode.HTML)
    status = 'number'
    # ? Переход на этап получения номера

    await Registration.getting_phone_number.set()

# ? Этап получения номера телефона


@ dp.message_handler(state=Registration.getting_phone_number, content_types=['contact', 'text'])
async def get_number(message, state=Registration.getting_phone_number):
    print(f'Step 4 - get_number.  From user: {message.from_user.id}')
    caption1 = '''Привет)
    Да, мы знаем, что как бы поздно уже готовиться к лету, но думаем, что стоит попробовать.

    Если ты хочешь подтянуть именно свое тело, то ниже тебе чек-лист упражнений (не благодари)

    Ну а мы считаем, что пресс должен быть не только на животе, но и в кармане. Поэтому подготовили для тебя <b>скидки до 40% на наши курсы</b>, для этого тебе тоже надо сделать несколько упражнений, каждое из которых поможет скинуть по 8 <s>килограмм</s> процентов от стоимости курса.

    Если готов то жми на "Поумней!"'''
    global status

    all_users = requests.get(
        'https://p-api2.tehnikum.school/api/bot-users/').json()

    registered_numbers = [user['phone_number']
                          for user in all_users if user['is_verified']]
    print(registered_numbers)
    is_valid = False
    already_registered = False
    if status == 'number':
        if message.contact:
            print(type(message.contact.phone_number))
            print(registered_numbers)
            if message.contact.phone_number in registered_numbers:
                await message.answer('Этот номер уже зарегистрирован. Попробуй другой.')
                already_registered = True
            else:
                phone_number = message.contact.phone_number
                is_valid = True
        elif len(message.text) == 12:
            phone_number = message.text
            if phone_number in registered_numbers:
                await message.answer('Этот номер уже зарегистрирован. Попробуй другой.')
                already_registered = True
            else:
                is_valid = True
        elif len(message.text) == 13 and message.text[0] == '+':
            phone_number = message.text
            if phone_number in registered_numbers:
                await message.answer('Этот номер уже зарегистрирован. Попробуй другой.')
                already_registered = True
            else:
                is_valid = True
        else:
            is_valid = False
            # await state.update_data(number=phone_number)
        if is_valid:
            await message.answer('Теперь надо подтвердить. Отправили тебе смс с кодом, введи его сюда)', reply_markup=types.ReplyKeyboardRemove())
        # ! генерируем код подтверждения
            verification_code = random.randint(1000, 9999)

        # ! отправляем смс с кодом подтверждения
            send_sms(phone_number,
                     f'TEHNIKUM: Ваш код {verification_code}')

            all_info = await state.get_data()

            name = all_info.get("name")
            user_id = message.from_user.id
            code = all_info.get("verification_code")

            already_user = requests.get(
                f'https://p-api2.tehnikum.school/api/bot-users/?id={message.from_user.id}').json()
            print(already_user)

        # ! Проверяем, есть ли пользователь в базе
            if already_user:
                # ! Если есть, то обновляем его верификационный код
                new_user_info = {
                    "id": user_id,
                    "first_name": name,
                    "phone_number": phone_number,
                    "verification_code": verification_code,
                    "is_verified": "False"
                }
                url = f'https://p-api2.tehnikum.school/api/bot-users/{user_id}/'

                # ! Обновляем его верификационный код
                response = requests.put(url, data=new_user_info)
                print(f'Verification code has been updated: {response.json()}')
                status = 'code'
                # await get_verification(verification_code, user_id=message.from_user.id)

            else:
                # ! Если нет, то создаем нового пользователя
                user_info = {
                    "id": user_id,
                    "first_name": name,
                    "phone_number": phone_number,
                    "verification_code": verification_code,
                    "is_verified": "False"

                }
                url = 'https://p-api2.tehnikum.school/api/bot-users/'

                # ! Отпправляем юзера в базу данных
                response = requests.post(url, data=user_info)
                print(f'User has been created: {response.json()}')
                status = 'code'
                # await get_verification(verification_code, user_id=message.from_user.id)

        if is_valid == False and already_registered == False:
            await message.answer('Неверный формат номера. Попробуй еще раз', reply_markup=buttons.phone_number_kb())

    if status == 'code':
        await get_verification(message)


@ dp.message_handler(state=Registration.getting_phone_number, content_types=['text'])
# async def get_verification(verification_code, user_id, state=Registration.getting_verification_code,):
async def get_verification(message, state=Registration.getting_verification_code,):
    print(f'Step 5 - get_verification.  From user: {message.from_user.id}')
    global status, registered_numbers
    if status == 'code':
        caption_final = '''
Таааак, вот и первые добровольцы у нас!

Если не успели подготовиться к лету, то
в бассейн можно походить и в водолазном костюме, а вот без новой профессии и $
не разгуляешься

Поэтому давай-ка мы тебя подтянем по скиллам, чтобы лето не прошло зря!

Жми «ПОУМНЕТЬ»"'''
        print('Verification')
        verification_code = message.text
        url = f'https://p-api2.tehnikum.school/api/bot-users/?id={message.from_user.id}'

        try:

            user = requests.get(url).json()[0]
            print(user)

        except:
            user = None

        # ! Проверяем, есть ли пользователь в базе
        if user:
            # ! Проверяем код подтверждения
            if int(verification_code) == int(user['verification_code']):
                status = 'start'
                # ! Если код верный, то обновляем статус верификации
                # file_path = os.path.join(os.getcwd(), "tehnikum.jpg")
                # with open(file_path, "rb") as photo:
                #     await bot.send_photo(chat_id=message.from_user.id,
                #                          photo=photo,
                #                          caption=caption_final, parse_mode=types.ParseMode.HTML, reply_markup=buttons.web_app_inline_kb(),
                #                          #  show_alert=True
                #                          )
                await message.answer(caption_final, parse_mode=types.ParseMode.HTML, reply_markup=buttons.web_app_inline_kb())
                user_data = {
                    'id': user['id'],
                    'first_name': user['first_name'],
                    'phone_number': user['phone_number'],
                    "is_verified": "True",
                    'verification_code': user['verification_code']
                }
                url = f'https://p-api2.tehnikum.school/api/bot-users/{user["id"]}/'
                # ? Обновляем статус верификации

                response = requests.put(
                    url, data={'category_id': None, 'is_verified': True, 'verification_code': user['verification_code']})

                url_amo = f'https://tg-api.tehnikum.school/amo_crm/v1/create_lead?phone={user_data["phone_number"]}&name={user_data["first_name"]}&action=m-bot'
                response_amo = requests.get(url_amo)
                print(
                    f'Is verified status has been updated: {response.json()}')
            else:
                # ! Если код неверный, то выводим сообщение об ошибке
                await message.answer('Неверный код. Отправили тебе новый код, введи его сюда: ')
                verification_code = random.randint(1000, 9999)
                user_data = {
                    'id': user['id'],
                    'first_name': user['first_name'],
                    'phone_number': user['phone_number'],
                    "is_verified": "False",
                    'verification_code': verification_code
                }
                 # ! генерируем код подтверждения

                 # ! отправляем смс с кодом подтверждения
                send_sms(user_data['phone_number'],
                        f'TEHNIKUM: Ваш новый код {verification_code}')
                url = f'https://p-api2.tehnikum.school/api/bot-users/{user_data["id"]}/'

                # ! Обновляем его верификационный код
                response = requests.put(url, data=user_data)
                print(response.json())
                status = 'code'
    # all_info = await state.get_data()
    # print(all_info)


executor.start_polling(dp, skip_updates=True)
