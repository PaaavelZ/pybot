import logging

import telebot

SECONDS_IN_DAY = 10  # 86400
TOKEN = "5399406638:AAGQPWtgzCLNpDzF_8TpOUebXmc_W4FtiFE"

bot = telebot.TeleBot(TOKEN)
logger = telebot.logger
telebot.logger.setLevel(logging.ERROR)
