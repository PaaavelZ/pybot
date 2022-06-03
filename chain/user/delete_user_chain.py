from auth import admin
from config import bot
from db import Database


@bot.message_handler(commands=['delete_user'])
@admin(bot)
def read_id(msg):
    bot.reply_to(msg, "Введите id пользователя")
    bot.register_next_step_handler(msg, delete_user)


def delete_user(msg) -> None:
    user_id = int(msg.text)

    with Database() as db:
        db.delete_user(user_id)

    bot.reply_to(msg, "Успешно!")
