from auth import admin
from config import bot
from db import Database


@bot.message_handler(commands=['delete_hw'])
@admin(bot)
def read_id(msg):
    bot.reply_to(msg, "Введите id домашки")
    bot.register_next_step_handler(msg, delete_hw)


def delete_hw(msg) -> None:
    hw_id = int(msg.text)

    with Database() as db:
        db.delete_hw(hw_id)

    bot.reply_to(msg, "Успешно!")
