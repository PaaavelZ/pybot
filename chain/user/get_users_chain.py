from auth import admin
from chain.user.utils import user_to_string
from config import bot
from db import Database


@bot.message_handler(commands=['get_users'])
@admin(bot)
def get_users(msg):
    reply = ""
    with Database() as db:
        users = db.get_users()
        for user in users:
            reply += user_to_string(user)

    bot.reply_to(msg, reply)
