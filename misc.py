import logging
from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage

bot = Bot(token="1258763969:AAH5wH_kxkt8ZnRgkjzx3JC74maCA33xQmU")
memory_storage = MemoryStorage()
dp = Dispatcher(bot, storage=memory_storage)
logging.basicConfig(level=logging.INFO)