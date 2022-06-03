import overdue_hw_remover
from config import bot, logger
from db import Database

# start
from chain.start_chain import send_welcome

# hws
from chain.hw import add_hw_chain
from chain.hw import get_hw_chain
from chain.hw import get_all_hws_chain
from chain.hw import edit_hw_chain
from chain.hw import delete_hw_chain

# users
from chain.user import add_user_chain
from chain.user import get_users_chain
from chain.user import edit_user_chain
from chain.user import delete_user_chain

if __name__ == '__main__':
    # 4. хироку
    try:
        overdue_hw_remover.start()
        bot.infinity_polling()
    except Exception as e:
        logger.error(e)
    # with Database() as db:
    #    db.add_user(723134096, True, "Pashok")
    #    print(db.get_users())
