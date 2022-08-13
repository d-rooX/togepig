import telebot

tables_to_backup = {}

# hours
interval = 1
bot: telebot.TeleBot = None