from auth import admin
from chain.user.utils import read_user_rights
from config import bot


@bot.message_handler(commands=['add_user'])
@admin(bot)
def read_user_id(msg):
    bot.reply_to(msg, "Введите id пользователя")
    bot.register_next_step_handler(msg, read_user_rights)
