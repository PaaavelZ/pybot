from auth import user
from config import bot


@bot.message_handler(commands=['start'])
@user(bot)
def send_welcome(msg):
    bot.reply_to(msg, "Бот для домашек и их дедлайнов группы 3530904/00003.\n"
                      "Автоматически удаляет просроченные домашки с небольшой задержкой.\n"
                      "Для ознакомления с функционалом откройте левое меню.")
