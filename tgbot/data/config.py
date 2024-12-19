# - *- coding: utf- 8 - *-
import configparser

from apscheduler.schedulers.asyncio import AsyncIOScheduler

BOT_CONFIG = configparser.ConfigParser()
BOT_CONFIG.read("settings.ini")

# Образы и конфиги
BOT_TOKEN = BOT_CONFIG['settings']['bot_token'].strip().replace(' ', '')  # Токен бота
BOT_TIMEZONE = "Europe/Moscow"  # Временная зона бота
BOT_SCHEDULER = AsyncIOScheduler(timezone=BOT_TIMEZONE)  # Образ шедулера
BOT_VERSION = 4.1  # Версия бота

# Пути к файлам
PATH_DATABASE = "tgbot/data/database.db"  # Путь к Базе Данных
PATH_LOGS = "tgbot/data/logs.log"  # Путь к Логам


# Получение администраторов бота
def get_admins() -> list[int]:
    read_admins = configparser.ConfigParser()
    read_admins.read("settings.ini")

    admins = read_admins['settings']['admin_id'].strip().replace(" ", "")

    if "," in admins:
        admins = admins.split(",")
    else:
        if len(admins) >= 1:
            admins = [admins]
        else:
            admins = []

    while "" in admins: admins.remove("")
    while " " in admins: admins.remove(" ")
    while "\r" in admins: admins.remove("\r")
    while "\n" in admins: admins.remove("\n")

    admins = list(map(int, admins))

    return admins


# Получение описания
def get_desc() -> str:
    from tgbot.utils.const_functions import ded

    # УДАЛИШЬ ИЛИ ИЗМЕНИШЬ ССЫЛКИ НА ДОНАТ, КАНАЛ И ТЕМУ БОТА - КАСТРИРУЮ НАХУЙ <3

    return ded(f"""
        <b>♻️ Версия бота: <code>{BOT_VERSION}</code>
        👑 Разработчик бота - @djimbox
        🍩 Донат разработчику: <a href='https://t.me/send?start=IV8bjPKhYkYJ'>Click me</a>
        🤖 Канал с новостями и обновлениями: <a href='https://t.me/DJIMBO_SHOP'>Click me</a>
        🔗 Ссылка на топик с ботом [LOLZ]: <a href='https://lolz.guru/threads/1888814'>Click me</a></b>
    """).strip()
