from auth import user
from chain.hw.utils import reply_choose_subj, get_hw
from config import bot


@bot.message_handler(commands=['get_hw'])
@user(bot)
def get(msg):
    reply_choose_subj(msg)
    bot.register_next_step_handler(msg, get_hw)
