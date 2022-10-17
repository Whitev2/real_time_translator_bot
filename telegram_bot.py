import sys
sys.path.append ('../')
from aiogram.utils import executor
from start_config import dp
from data_base import sqlite_db



async def on_startup(_):
    print('The bot went online')
    sqlite_db.sql_start()
from handlers import client

client.regiser_handlers_client(dp)

from translator import translator

translator.regiser_translate_client(dp)





executor.start_polling(dp, skip_updates=True, on_startup=on_startup)