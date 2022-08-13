import logging
import traceback

import settings
from config import TOKEN
from telebot import TeleBot, StateMemoryStorage, types, ExceptionHandler
from loguru import logger

class ExceptionLogger(ExceptionHandler):
    def handle(self, exception):
        logger.exception(exception)


bot = TeleBot(
    token=TOKEN,
    state_storage=StateMemoryStorage(),
    exception_handler=ExceptionLogger()
)
settings.bot = bot

import handlers

# выбор БД которую нужно дампить
# настройка таблиц которые нужно дампить
# настройка интервала
# настройка сохранения дампов. (архивация, удаление старых дампов)
# менеджмент дампов (удаление, создание дампов вручную, рестор из выбранного дампа)
# состояние шедулера


@bot.message_handler(commands=['start'])
@bot.callback_query_handler(lambda c: c.data == 'menu')
def start_handler(obj: types.Message | types.CallbackQuery):
    text = 'Hello!'
    markup = types.InlineKeyboardMarkup().row(
        types.InlineKeyboardButton("Choose tables", callback_data='browse'),
        types.InlineKeyboardButton("Backup settings", callback_data='settings'),
    )

    bot.set_state(obj.from_user.id, '')
    if isinstance(obj, types.Message):
        bot.reply_to(
            obj,
            text,
            reply_markup=markup
        )
    else:
        bot.edit_message_text(
            text, obj.from_user.id, obj.message.message_id,
            reply_markup=markup
        )


bot.infinity_polling(logger_level=logging.DEBUG)
