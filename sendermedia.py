import asyncio
import logging

from aiogram import Bot, types
from aiogram.utils import executor
from aiogram.utils.emoji import emojize
from aiogram.dispatcher import Dispatcher
from aiogram.types.message import ContentType
from aiogram.utils.markdown import text, bold, italic, code, pre
from aiogram.types import ParseMode, InputMediaPhoto, InputMediaVideo, ChatActions

from configforaio import TOKEN

logging.basicConfig(format=u'%(filename)s [ LINE:%(lineno)+3s ]#%(levelname)+8s [%(asctime)s] %(message)s',
                    level=logging.INFO)

CAT_BIG_EYES = 'AgACAgQAAxkDAAMnXzrnidenc68HTJnCLnu_wdIZ328AAia1MRt1UrlRPDJR6AABRb7yVJM4Jl0AAwEAAwIAA3gAA1l8AAIaBA'
KITTENS = [
    'AgACAgQAAxkDAAMqXzrniTZoFuJCCrfg7FQAAQyW20PDAAIntTEbdVK5UcMCySutaUN3Uaw-Jl0AAwEAAwIAA3cAAzp9AAIaBA',
    'AgACAgQAAxkDAAMsXzrnifS5oc-Jv7H5nj9Tt7v29-AAAii1MRt1UrlRID51vcrzErFSg3EjXQADAQADAgADeAADBdwCAAEaBA',
    'AgACAgQAAxkDAAMtXzrnipSNHSsQS0kUu8RX0RLXzm8AAim1MRt1UrlREzLXVxJCwSjhc_ciXQADAQADAgADbQADFBYFAAEaBA',
]
VOICE = 'AwACAgQAAxkDAAMoXzrnibEY-91VG-HhhWGdooglo_wAAm4IAAJOONhRc0VgLI2wv_IaBA'
VIDEO = 'BAACAgQAAxkDAAMrXzrniVts02KV-3MUsNwSNuApQH0AAnAIAAJOONhR33bLeujrCzYaBA'
TEXT_FILE = 'BQACAgQAAxkDAAMmXzrniIYS6xVZrI5_JzYSltfuJLoAAm0IAAJOONhRLjmME_J6fh4aBA'
VIDEO_NOTE = 'DQACAgQAAxkDAAMpXzrniXQsxcrnAAGDJjB_Rg6IBzztAAJvCAACTjjYUdvK79M16vvyGgQ'

bot = Bot(token=TOKEN)
dp = Dispatcher(bot)

@dp.message_handler(commands=['start'])
async def process_start_command(message: types.Message):
    await message.reply('Hi!\nUse /help '
                        'to find out the list of available commands!')

@dp.message_handler(commands=['help'])
async def process_help_command(message: types.Message):
    msg = text(bold('I can answer the following commands:'),
                '/voice', '/photo', '/group', '/note', '/file', '/testpre', '/video', sep='\n')
    await message.reply(msg, parse_mode=ParseMode.MARKDOWN)

@dp.message_handler(commands=['voice'])
async def process_voice_command(message: types.Message):
    await bot.send_voice(message.from_user.id, VOICE,
                        reply_to_message_id=message.message_id)

@dp.message_handler(commands=['photo'])
async def process_photo_command(message: types.Message):
    caption = 'What eyes! :eyes:'
    await bot.send_photo(message.from_user.id, CAT_BIG_EYES,
                        caption=emojize(caption),
                        reply_to_message_id=message.message_id)

@dp.message_handler(commands=['group'])
async def process_group_command(message: types.Message):
    media = [InputMediaVideo(VIDEO, caption='hedgehog')]
    for photo_id in KITTENS:
        media.append(InputMediaPhoto(photo_id))
    
    await bot.send_media_group(message.from_user.id, media)


@dp.message_handler(commands=['video'])
async def process_video_command(message: types.Message):
    await bot.send_video(message.from_user.id, VIDEO,
                        reply_to_message_id=message.message_id)

@dp.message_handler(commands=['note'])
async def process_note_command(message: types.Message):
    user_id = message.from_user.id
    await bot.send_chat_action(user_id, ChatActions.RECORD_VIDEO_NOTE)
    await asyncio.sleep(1)
    await bot.send_video_note(message.from_user.id, VIDEO_NOTE)

@dp.message_handler(commands=['file'])
async def process_file_command(message: types.Message):
    user_id = message.from_user.id
    await bot.send_chat_action(user_id, ChatActions.UPLOAD_DOCUMENT)
    await asyncio.sleep(1)
    await bot.send_document(user_id, TEXT_FILE,
                            caption='This file is specially for you!')

@dp.message_handler(commands=['testpre'])
async def process_testpre_command(message: types.Message):
    message_text = pre(emojize('''
@dp.message_handler(commands=['testpre'])
async def process_testpre_command(message: types.Message):
    message_text = pre(emojize('Ха! Не в этот раз :smirk:'))
    await bot.send_message(message.from_user.id, message_text)'''))
    await bot.send_message(message.from_user.id, message_text,
                           parse_mode=ParseMode.MARKDOWN)

@dp.message_handler()
async def echo_message(msg: types.Message):
    await bot.send_message(msg.from_user.id, msg.text)

@dp.message_handler(content_types=ContentType.ANY)
async def unknown_message(msg: types.Message):
    message_text = text(emojize("I don't know what to do about it :astonished:"),
                        italic("\nI'll just remind you"), "that there's a",
                        code("command"), "/help")
    await msg.reply(message_text, parse_mode=ParseMode.MARKDOWN)

if __name__ == '__main__':
    executor.start_polling(dp)