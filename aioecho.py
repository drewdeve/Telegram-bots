import logging 
from aiogram import Bot, Dispatcher, executor, types
logging.basicConfig(level=logging.INFO)

bot = Bot(token="1388836709:AAH7VTzwi6Lc7lPOUL2vdjcNfGq0VXO70xg")
dp = Dispatcher(bot)

@dp.message_handler()
async def echo (message: types.Message):
    await message.reply(message.text)

if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)