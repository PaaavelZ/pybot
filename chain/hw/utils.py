from datetime import date

import telebot
from telebot.types import ReplyKeyboardRemove

from config import bot
from db import Database


def reply_choose_subj(msg):
    markup = get_subjects_markup()
    bot.reply_to(msg, "Выберите предмет\n", reply_markup=markup)


def get_subjects_markup():
    markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True, selective=True)

    with Database() as db:
        subjects = db.get_subjects()
        btns = []
        for subj in subjects:
            btns.append(telebot.types.KeyboardButton(subj[1]))

    markup.add(*btns)
    return markup


def parse_deadline(deadline_str: str) -> date:
    if len(deadline_str) != 5:
        raise ValueError("Некорректный формат дедлайна")

    if deadline_str[2:3] != "-":
        raise ValueError("Некорректный формат дедлайна")

    try:
        dd = int(deadline_str[0:2])
        mm = int(deadline_str[3:5])
        yy = date.today().year
        res = date(yy, mm, dd)
    except ValueError:
        raise ValueError("Некорректная дата")

    return res


# throws an exception
def check_subject_for_existing(msg) -> None:
    with Database() as db:
        db.get_subject_id(msg.text)


def remove_custom_buttons() -> ReplyKeyboardRemove:
    return telebot.types.ReplyKeyboardRemove()


def hws_to_string(subject_name, hws: list) -> str:
    res = f"{subject_name}:\n"

    for i in range(len(hws)):
        res += hw_to_string(hws[i])

    if len(res) == len(subject_name) + 2:
        res += "Нет домашки, отдыхай"

    return res + "\n"


def hw_to_string(hw: tuple) -> str:
    return f"id: {hw[0]}, дедлайн: {hw[1]}, описание: {hw[2]}\n"


def get_hw(msg) -> str:
    default_markup = remove_custom_buttons()

    check_subject_for_existing(msg)

    with Database() as db:
        subj_name = msg.text
        hws = db.get_hws_by_subj_name(subj_name)
        reply = hws_to_string(subj_name, hws)

    bot.reply_to(msg, reply, reply_markup=default_markup)
    return reply
