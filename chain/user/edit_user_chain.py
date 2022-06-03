from auth import admin
from chain.user import add_user_chain
from config import bot


@bot.message_handler(commands=['edit_user'])
@admin(bot)
def read_user_id(msg):
    add_user_chain.read_user_id(msg)
