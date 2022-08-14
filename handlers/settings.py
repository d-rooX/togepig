import loguru
from apscheduler.triggers.interval import IntervalTrigger
from telebot import types

import settings
from backup.main import backup_scheduler
from settings import bot


def get_current_interval_button():
    match settings.interval:
        case 1:
            return types.InlineKeyboardButton(
                'Interval: 1h',
                callback_data='interval_6h'
            )
        case 6:
            return types.InlineKeyboardButton(
                'Interval: 6h',
                callback_data='interval_1d'
            )
        case 24:
            return types.InlineKeyboardButton(
                'Interval: 1d',
                callback_data='interval_1h'
            )


@bot.callback_query_handler(lambda c: c.data == 'settings')
def settings_cb(call: types.CallbackQuery):
    text = "Settings of backuper"
    markup = types.InlineKeyboardMarkup().row(
        get_current_interval_button(),
        types.InlineKeyboardButton('DB Credentials', callback_data='creds')
    ).row(
        types.InlineKeyboardButton('Back', callback_data='menu')
    )

    bot.edit_message_text(
        text, call.from_user.id,
        call.message.message_id,
        reply_markup=markup
    )

@bot.callback_query_handler(lambda c: c.data.startswith('interval'))
def interval_onclick(call: types.CallbackQuery):
    _, new_interval = call.data.split('_')

    match new_interval:
        case '1h':
            settings.interval = 1
        case '6h':
            settings.interval = 6
        case '1d':
            settings.interval = 24

    backup_scheduler.reschedule_job('do_backup', trigger=IntervalTrigger(hours=settings.interval))
    loguru.logger.debug(backup_scheduler.get_job('do_backup'))
    settings_cb(call)


@bot.callback_query_handler(lambda c: c.data == 'creds')
def creds_cb(call: types.CallbackQuery):
    pass



