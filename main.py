from aiogram import Dispatcher, Bot
from aiogram import types
from aiogram.dispatcher import FSMContext

from config import TOKEN
from backup.main import backup_manager

bot = Bot(token=TOKEN)
dp = Dispatcher(bot)

# выбор БД которую нужно дампить
# настройка таблиц которые нужно дампить
# настройка интервала
# настройка сохранения дампов. (архивация, удаление старых дампов)
# менеджмент дампов (удаление, создание дампов вручную, рестор из выбранного дампа)
# состояние шедулера


@dp.message_handler(commands=['start'])
async def start_handler(message: types.Message, state: FSMContext):
    pass


dp.start_polling()
