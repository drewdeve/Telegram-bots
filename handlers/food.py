from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup

from misc import dp 

available_food_names = ["🍣 sushi 🍣", "🍝 spaghetti 🍝", "🍕 pizza 🍕"]
available_food_sizes = ["small", "medium", "large"]

class OrderFood(StatesGroup):
    waiting_for_food_name = State()
    waiting_for_food_size = State()

@dp.message_handler(commands="food", state="*")
async def food_step_1(message: types.Message):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    for name in available_food_names:
        keyboard.add(name)
    await message.answer("Choose a dish:", reply_markup=keyboard)
    await OrderFood.waiting_for_food_name.set()

@dp.message_handler(state=OrderFood.waiting_for_food_name, content_types=types.ContentTypes.TEXT)
async def food_step_2(message: types.Message, state: FSMContext):
    if message.text.lower() not in available_food_names:
        await message.reply("Please choose the dish using the keyboard below.")
        return
    await state.update_data(chosen_food=message.text.lower())

    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    for size in available_food_sizes:
        keyboard.add(size)
    await OrderFood.next()
    await message.answer("Now choose the portion size:", reply_markup=keyboard)

@dp.message_handler(state=OrderFood.waiting_for_food_size, content_types=types.ContentTypes.TEXT)
async def food_step_3(message: types.Message, state: FSMContext):
    if message.text.lower() not in available_food_sizes:
        await message.reply("Please choose the portion size using the keyboard below.")
        return
    user_data = await state.get_data()
    await message.answer(f"You ordered {message.text.lower()} portion {user_data['chosen_food']}.\n"
                         f"Try to order drinks now: /drinks\n"
                         f"Or you can complete orders: /finish", reply_markup=types.ReplyKeyboardRemove())
    await state.finish()