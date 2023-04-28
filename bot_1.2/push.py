import telebot
from config import TOKEN
from sms import send_sms
import random
import requests
from aiogram.utils.deep_linking import decode_payload
import json
from telebot import apihelper
import time
from aiogram import Bot, Dispatcher


bot = telebot.TeleBot(token=TOKEN)
# dp = Dispatcher(bot, storage=MemoryStorage())

bot_users = requests.get(
    'https://p-api2.tehnikum.school/api/bot-users/').json()
bot_users_admin = [
    {
        'id': 657061394,
    },
    {
        "id": 1918321
    }]
print(len(bot_users))


for i in bot_users_admin:
    # bot.send_message(i, f'Пуш! Количество пользователей: {len(bot_users)}')
    time.sleep(0.1)
    try:
        chat_member = bot.get_chat_member(i['id'], bot.get_me().id)
        if chat_member.status == "left":
            print(f'User {i["id"]} has blocked the bot')
            continue
        else:
            bot.send_photo(i['id'], photo=open('push.jpg', 'rb'), caption='''
Привет, это снова TEHNIKUM. 
Мы тут заметили что твоя скидка на поумнение к лету всё еще у нас...  Лежит, ждёт тебя и пылится... 🤨 
Переходи сюда @school_tehnikum и забирай скорее! 🏃🏽‍♀️ Она ведь заслужена, а награда всегда должна находить призёра! 🥇

(иначе нам придётся отдать её кому-нибудь другому чтобы он поумнел вместо тебя 🧠)            
        ''')
    except apihelper.ApiTelegramException as e:
        if e.error_code == 403:
            # user has blocked the bot
            print(f"User {i['id']} has blocked the bot")
        else:
            # handle other API errors
            print(f"Error sending push message to user {i['id']}: {e}")


# executor.start_polling(dp, skip_updates=True)
