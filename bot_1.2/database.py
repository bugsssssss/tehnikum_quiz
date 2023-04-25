import sqlite3


# Создать/подключиться к базе данных
connection = sqlite3.connect('users.db')
# Создаем переводчика
sql = connection.cursor()

sql.execute("""
    CREATE TABLE IF NOT EXISTS users (
        user_id,
        name TEXT,
        phone_number TEXT
        )
""")


def add_user(user_id, name, phone_number):
    # Создать/подключиться к базе данных
    connection = sqlite3.connect('users.db')
    # Создаем переводчика
    sql = connection.cursor()

    # Добавление пользователя в базу
    sql.execute('INSERT INTO users VALUES (?, ?, ?);', (user_id, name, phone_number))

    # Фиксируем обновления
    connection.commit()


# Получение пользователя
def get_users():
    # Создать/подключиться к базе данных
    connection = sqlite3.connect('users.db')
    # Создаем переводчика
    sql = connection.cursor()

    # Зпрос для получения данных из базе
    users = sql.execute('SELECT name, phone_number FROM users;')

    # Вывод всего в виде списка с кортежами
    return users.fetchall()





# Функция для получения данных о пользователей
def get_user(name):
    # Создать/подключиться к базе данных
    connection = sqlite3.connect('users.db')
    # Создаем переводчика
    sql = connection.cursor()

    all_users = sql.execute('SELECT * FROM users WHERE name=?;', (name, ))

    return all_users.fetchone()


# Функция для проверки пользователя на наличие в базе
def check_user(user_id):
    # Создать/подключиться к базе данных
    connection = sqlite3.connect('users.db')
    # Создаем переводчика
    sql = connection.cursor()

    checker = sql.execute('SELECT user_id FROM users WHERE user_id=?;', (user_id,))

    # Проверка есть ли данные из запроса
    if checker.fetchone():
        return True

    else:
        return False


