# from telegram import ReplyKeyboardMarkup

web_app = WebAppInfo(url='https://mralex-neo.github.io/TelegrammBot/')


keyboard = ReplyKeyboardMarkup(
    keyboard=[
        KeyboardButton(text='Подписаться на канал', web_app=web_app)
    ],
    resize_keyboard=True
)
