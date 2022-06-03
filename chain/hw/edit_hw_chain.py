from datetime import date

from auth import user
from chain.hw.utils import parse_deadline, remove_custom_buttons, check_subject_for_existing, get_hw, reply_choose_subj
from config import bot
from db import Database


@bot.message_handler(commands=['edit_hw'])
@user(bot)
def choose_subject(msg):
    reply_choose_subj(msg)
    bot.register_next_step_handler(msg, choose_hw)


def choose_hw(msg) -> None:
    default_markup = remove_custom_buttons()

    try:
        check_subject_for_existing(msg)
    except ValueError as e:
        bot.reply_to(msg, f"Ошибка: {e}")
        return

    res = get_hw(msg)
    if "Нет домашки, отдыхай" in res:
        return

    bot.reply_to(msg, "Выберите id домашки\n", reply_markup=default_markup)
    bot.register_next_step_handler(msg, type_new_deadline)


def type_new_deadline(msg) -> None:
    try:
        hw_id = int(msg.text)
        with Database() as db:
            hw = db.get_hw(hw_id)
            if hw is None:
                bot.reply_to(msg, "Нет домашки с таким id!")
                return
    except ValueError:
        bot.reply_to(msg, "Некорректный id домашки!")
        return

    bot.reply_to(msg, "Введите новый дедлайн")
    bot.register_next_step_handler(msg, read_new_description, hw_id=hw_id)


def read_new_description(msg, hw_id: int) -> None:
    deadline = parse_deadline(msg.text)
    bot.reply_to(msg, "Введите новое описание")
    bot.register_next_step_handler(msg, edit_hw, hw_id=hw_id, deadline=deadline)


def edit_hw(msg, hw_id: int, deadline: date) -> None:
    with Database() as db:
        db.update_hw(hw_id, deadline, msg.text)

    bot.reply_to(msg, "Успешно!")
