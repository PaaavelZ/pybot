from auth import user
from chain.hw.utils import hws_to_string
from config import bot
from db import Database


@bot.message_handler(commands=['get_all_hws'])
@user(bot)
def get_all_hws(msg):
    reply = ""
    with Database() as db:
        hws = db.get_hws()
        for subj_name in hws.keys():
            reply += hws_to_string(subj_name, hws[subj_name])

    bot.reply_to(msg, reply)
