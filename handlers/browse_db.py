from telebot import types

from backup.main import backup_manager
from settings import bot, backup_databases


@bot.callback_query_handler(lambda c: c.data == 'browse')
def choose_db(call: types.CallbackQuery):
    markup = types.InlineKeyboardMarkup(row_width=2)
    btns = []

    dbs = backup_manager.get_databases()
    for database in dbs:
        btns.append(types.InlineKeyboardButton(
            database, callback_data=f'db_{database}'
        ))
    markup.add(*btns)
    markup.row(types.InlineKeyboardButton(text='Back', callback_data='menu'))

    bot.edit_message_text(
        "Choose DB",
        call.message.chat.id,
        call.message.message_id,
        reply_markup=markup
    )


@bot.callback_query_handler(lambda c: c.data.startswith('db'))
def choose_table(call: types.CallbackQuery, after_click=False):
    if after_click:
        with bot.retrieve_data(call.from_user.id) as data:
            db = data.get('db')
    else:
        _, db = call.data.split('_')
        bot.add_data(call.from_user.id, db=db)

    markup = types.InlineKeyboardMarkup(row_width=3)
    if tables_btns := get_tables_markup(db):
        markup.row(types.InlineKeyboardButton('✔️ Check All ✔️', callback_data='table_*'))
        markup.add(*tables_btns)
    markup.row(types.InlineKeyboardButton(
        text='Back', callback_data='browse'
    ))

    bot.edit_message_text(
        "Choose table",
        call.message.chat.id,
        call.message.message_id,
        reply_markup=markup
    )


@bot.callback_query_handler(lambda c: c.data.startswith('table'))
def onclick_table(call: types.CallbackQuery):
    _, table = call.data.split('_')
    with bot.retrieve_data(call.from_user.id) as data:
        db = data['db']

    if table == '*':
        tables = backup_manager.get_tables(db)
        if backup_databases.get(db) != set(tables):
            backup_databases[db] = set(
                table for table in tables
            )
        else:
            backup_databases[db] = set()
    else:
        backup_databases.setdefault(
            db, set()
        ).symmetric_difference_update({table})
    choose_table(call, after_click=True)


def table_name(db_name, table):
    return f'✅ {table}' if table in backup_databases.get(db_name, {}) else table


def get_tables_markup(db_name: str) -> list[types.InlineKeyboardButton]:
    return [
        types.InlineKeyboardButton(
            text=table_name(db_name, table),
            callback_data=f'table_{table}'
        )
        for table in backup_manager.get_tables(db_name)
    ]
