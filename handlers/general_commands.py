from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from misc import dp, bot


@dp.message_handler(commands="cancel", state="*")
@dp.message_handler(Text(equals="cancel", ignore_case=True), state="*")
async def cmd_cancel(message: types.Message, state: FSMContext):
    await state.finish()
    await message.answer("Action cancelled", reply_markup=types.ReplyKeyboardRemove())

@dp.message_handler(commands=['start'], state="*")
async def cmd_start(message: types.Message, state: FSMContext):
    await message.reply("Choose what you want to order: "
                        "drinks (/drinks) or food (/food).", reply_markup=types.ReplyKeyboardRemove())

@dp.message_handler(commands="finish", state="*")
async def cmd_finish(message: types.Message, state: FSMContext):
    await message.answer("Thank you for ordering! If you want to order something else you need to write a command (/start).")

@dp.message_handler(commands="set_commands", state="*")
async def cmd_set_commands(message: types.Message):
    if message.from_user.id == 855783532:
        commands = [types.BotCommand(command="/drinks", description="Order drinks"),
                    types.BotCommand(command="/food", description="Order food")]
        await bot.set_my_commands(commands)
        await message.answer("The commands are set up.")
