from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, WebAppInfo, InlineKeyboardButton, InlineKeyboardMarkup


def name_kb():
    kb = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)

    button = KeyboardButton('Имя')

    kb.add(button)

    return kb


def phone_number_kb():
    kb = ReplyKeyboardMarkup(resize_keyboard=True)

    button = KeyboardButton('Поделиться контактом', request_contact=True)

    kb.add(button)

    return kb


def web_app_kb():

    web_app = WebAppInfo(url='https://mralex-neo.github.io/TelegrammBot/')

    kb = ReplyKeyboardMarkup(resize_keyboard=True)

    button = KeyboardButton('Поумней!', web_app=web_app)

    kb.add(button)

    return kb


def web_app_inline_kb():

    web_app = WebAppInfo(url='https://mralex-neo.github.io/TelegrammBot/')

    kb = InlineKeyboardMarkup()

    button = InlineKeyboardButton('Поумней!', web_app=web_app)

    kb.add(button)

    return kb
