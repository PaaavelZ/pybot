from db import Database


def admin(bot):
    def inner(func):
        def wrapper(msg):
            with Database() as db:
                if not db.is_admin(msg.from_user.id):
                    return bot.reply_to(msg, "Доступ запрещён\n"
                                             f"Ваш ID: {msg.from_user.id}\n"
                                             f"Отправьте его администратору")
            return func(msg)

        return wrapper

    return inner


def user(bot):
    def inner(func):
        def wrapper(msg):
            with Database() as db:
                if not db.is_user(msg.from_user.id):
                    return bot.reply_to(msg, "Доступ запрещён\n"
                                             f"Ваш ID: {msg.from_user.id}\n"
                                             f"Отправьте его администратору")
            return func(msg)

        return wrapper

    return inner
