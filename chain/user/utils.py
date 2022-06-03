from config import bot
from db import Database


def read_user_rights(msg) -> None:
    user_id = int(msg.text)

    if user_id <= 0:
        bot.reply_to(msg, "Неверный id!")
        return

    bot.reply_to(msg, "Укажите права для пользователя (0 - обычный, 1 - администратор)")
    bot.register_next_step_handler(msg, read_username, user_id=user_id)


def read_username(msg, user_id: int) -> None:
    user_rights = int(msg.text)

    if user_rights > 1 or user_rights < 0:
        bot.reply_to(msg, "Неверные права!")
        return

    bot.reply_to(msg, "Введите имя пользователя")
    bot.register_next_step_handler(msg, add_user, user_id=user_id, user_rights=user_rights)


def add_user(msg, user_id: int, user_rights: bool) -> None:
    username = msg.text

    with Database() as db:
        db.add_user(user_id, user_rights, username)

    bot.reply_to(msg, "Успешно!")


def user_to_string(user: tuple) -> str:
    return f"id: {user[0]}, администратор: {bool(user[1])}, имя: {user[2]}\n"
