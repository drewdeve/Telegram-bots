from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup

from misc import dp

available_drinks_names = ["🍵 tea 🍵", "☕️ coffee ☕️", "🍺 beer 🍺"]
available_drinks_sizes = ["0.25l", "0.5l", "1l"]

class OrderDrinks(StatesGroup):
    waiting_for_drink_name = State()
    waiting_for_drink_size = State()

@dp.message_handler(commands="drinks", state="*")
async def food_step_1(message: types.Message):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    for name in available_drinks_names:
        keyboard.add(name)
    await message.answer("Choose a drink:", reply_markup=keyboard)
    await OrderDrinks.waiting_for_drink_name.set()

@dp.message_handler(state=OrderDrinks.waiting_for_drink_name, content_types=types.ContentTypes.TEXT)
async def food_step_2(message: types.Message, state: FSMContext):
    if message.text.lower() not in available_drinks_names:
        await message.reply("Please choose the drink using the keyboard below")
        return
    await state.update_data(chosen_drink=message.text.lower())

    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    for size in available_drinks_sizes:
        keyboard.add(size)
    await OrderDrinks.next()
    await message.answer("Now choose the size of the drink: ", reply_markup=keyboard)

@dp.message_handler(state=OrderDrinks.waiting_for_drink_size, content_types=types.ContentTypes.TEXT)
async def food_step_3(message: types.Message, state: FSMContext):
    if message.text.lower() not in available_drinks_sizes:
        await message.reply("Please choose the size of the drink using the keyboard below.")
        return
    user_data = await state.get_data()
    await message.answer(f"You ordered {user_data['chosen_drink']} the volume {message.text.lower()}.\n"
                         f"Try to order food now: /food\n"
                         f"Or you can complete orders: /finish", reply_markup=types.ReplyKeyboardRemove())
    await state.finish()