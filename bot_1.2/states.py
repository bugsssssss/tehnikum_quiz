from aiogram.dispatcher.filters.state import State, StatesGroup


# Процессы для регистрации
class Registration(StatesGroup):
    getting_started = State()
    getting_name_state = State()
    getting_phone_number = State()
    getting_verification_code = State()
