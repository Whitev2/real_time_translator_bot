from aiogram import Bot
from aiogram.dispatcher import Dispatcher
from aiogram import types
from aiogram.contrib.fsm_storage.memory import MemoryStorage

storage = MemoryStorage()

bot = Bot(token='5142166743:AAGAbMVkUXGhho4y1VWqFDXv86Z-hWf-ao0', parse_mode=types.ParseMode.HTML)
dp = Dispatcher(bot, storage=storage)