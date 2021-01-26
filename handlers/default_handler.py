from aiogram import types
from misc import dp

@dp.message_handler(content_types=types.ContentTypes.ANY, state="*")
async def all_other_messages(message: types.Message):
    if message.content_type == "text":
        await message.reply("I don't get it!") 
    else:
        await message.reply("This bot only receives text messages!")