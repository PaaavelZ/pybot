from auth import user
from chain.hw.utils import remove_custom_buttons, parse_deadline, check_subject_for_existing, reply_choose_subj
from config import bot
from db import Database


@bot.message_handler(commands=['add_hw'])
@user(bot)
def add_hw(msg):
    reply_choose_subj(msg)
    bot.register_next_step_handler(msg, read_deadline)


def read_deadline(msg) -> None:
    default_markup = remove_custom_buttons()

    try:
        check_subject_for_existing(msg)
    except ValueError as e:
        bot.reply_to(msg, f"Ошибка: {e}")
        return

    bot.reply_to(msg, "Укажите дедлайн в формате: дд-мм\n", reply_markup=default_markup)
    bot.register_next_step_handler(msg, read_description, subj=msg.text)


def read_description(msg, subj) -> None:
    try:
        deadline = parse_deadline(msg.text)
        with Database() as db:
            if db.get_hw_id(deadline) is not None:
                bot.reply_to(msg, "Ошибка: уже есть домашка с таким дедлайном для данного предмета."
                                  " Попробуйте совместить уже существующую домашку с текущей (функция /editHW).")
                return
    except ValueError as e:
        bot.reply_to(msg, f"Ошибка: {e}")
        return

    bot.reply_to(msg, "Укажите описание к домашке\n")
    bot.register_next_step_handler(msg, create_hw, subj=subj, deadline=deadline)


def create_hw(msg, subj, deadline) -> None:
    with Database() as db:
        subj_id = db.get_subject_id(subj)
        db.add_hw(deadline, msg.text, subj_id)
    bot.reply_to(msg, "Успешно!")
