from aiogram import Bot, types
from aiogram.utils import executor
from aiogram.utils.markdown import text
from aiogram.dispatcher import Dispatcher

import keyboards as kb

bot = Bot(token='1200760152:AAHkOxlETuczqdPuZkxMBDS6sTgYsoaXH6E')
dp = Dispatcher(bot)

@dp.callback_query_handler(lambda c: c.data == 'button1')
async def process_callback_button1(callback_query: types.CallbackQuery):
    await bot.answer_callback_query(callback_query.id)
    await bot.send_message(callback_query.from_user.id, 'The first button is pressed!')

@dp.callback_query_handler(lambda c: c.data and c.data.startswith('btn'))
async def process_callback_kb1btn1(callback_query: types.CallbackQuery):
    code = callback_query.data[-1]
    if code.isdigit():
        code = int(code)
    if code == 2:
        await bot.answer_callback_query(callback_query.id, text='The second button is pressed')
    elif code == 5:
        await bot.answer_callback_query(
            callback_query.id,
            text='The button with number 5 is pressed.\nAnd this text can be up to 200 characters long 😉', show_alert=True)
    else:
        await bot.answer_callback_query(callback_query.id)
    await bot.send_message(callback_query.from_user.id, f'The inline button is pressed! code={code}')

@dp.message_handler(commands=['start'])
async def process_start_command(message: types.Message):
    await message.reply('Hi!', reply_markup=kb.greet_kb)

@dp.message_handler(commands=['hi1'])
async def process_hi1_command(message: types.Message):
    await message.reply('The first is changing the size of the keyboard',
                        reply_markup=kb.greet_kb1)

@dp.message_handler(commands=['hi2'])
async def process_hi2_command(message: types.Message):
    await message.reply('The second is hiding the keyboard after one click', reply_markup=kb.greet_kb2)

@dp.message_handler(commands=['hi3'])
async def process_hi3_command(message: types.Message):
    await message.reply('Third - add more buttons', reply_markup=kb.markup3)

@dp.message_handler(commands=['hi4'])
async def process_hi4_command(message: types.Message):
    await message.reply('Fourth - put the buttons in a row', reply_markup=kb.markup4)

@dp.message_handler(commands=['hi5'])
async def process_hi5_command(message: types.Message):
    await message.reply('Fifth - add rows of buttons', reply_markup=kb.markup5)

@dp.message_handler(commands=['hi6'])
async def process_hi6_command(message: types.Message):
    await message.reply('Sixth - requesting contact and geolocation\nThese two buttons do not depend on each other', reply_markup=kb.markup_request)

@dp.message_handler(commands=['hi7'])
async def process_hi7_command(message: types.Message):
    await message.reply('Seventh - all methods together', reply_markup=kb.markup_big)

@dp.message_handler(commands=['rm'])
async def process_rm_command(message: types.Message):
    await message.reply('Remove message templates', reply_markup=kb.ReplyKeyboardRemove())

@dp.message_handler(commands=['1'])
async def process_command_1(message: types.Message):
    await message.reply('First inline button', reply_markup=kb.inline_kb1)

@dp.message_handler(commands=['2'])
async def process_command_2(message: types.Message):
    await message.reply('I send all possible buttons',
                        reply_markup=kb.inline_kb_full)

help_message = text(
    "It's a keyboard lesson.",
    "Available commands:\n",
    "/start - greeting",
    "\nKeyboard templates:",
    "/hi1 - auto size",
    "/hi2 - hide after clicking",
    "/hi3 - more buttons",
    "/hi4 - buttons in a row",
    "/hi5 - more rows",
    "/hi6 - request location and phone number",
    "/hi7 - all methods",
    "/rm - remove templates",
    "\nInline keyboards:",
    "/1 - first button",
    "/2 - a lot of buttons at once",
    sep="\n"
)

@dp.message_handler(commands=['help'])
async def process_help_command(message: types.Message):
    await message.reply(help_message)

if __name__ == '__main__':
    executor.start_polling(dp)