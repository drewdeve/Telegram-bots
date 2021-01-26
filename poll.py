import logging
from aiogram import Bot, Dispatcher, executor, types
from aiogram.utils import deep_linking

from quizzer import Quiz


bot = Bot(token="1388836709:AAH7VTzwi6Lc7lPOUL2vdjcNfGq0VXO70xg")
dp = Dispatcher(bot)
logging.basicConfig(level=logging.INFO)

quizzes_database = {}
quizzes_owners = {}

@dp.poll_answer_handler()
async def handle_poll_answer(quiz_answer: types.PollAnswer):
    quiz_owner = quizzes_owners.get(quiz_answer.poll_id)
    if not quiz_owner:
        logging.error(f"I can't find the author of the quiz with quiz_answer.poll_id = {quiz_answer.poll_id}")
        return
    for saved_quiz in quizzes_database[quiz_owner]:
        if saved_quiz.quiz_id == quiz_answer.poll_id:
            if saved_quiz.correct_option_id == quiz_answer.option_ids[0]:
                saved_quiz.winners.append(quiz_answer.user.id)
                if len(saved_quiz.winners) == 2:
                    await bot.stop_poll(saved_quiz.chat_id, saved_quiz.message_id)

@dp.poll_handler(lambda active_quiz: active_quiz.is_closed is True)
async def just_poll_answer(active_quiz: types.Poll):
    quiz_owner = quizzes_owners.get(active_quiz.id)
    if not quiz_owner:
        logging.error(f"I can't find the author of the quiz with active_quiz.id = {active_quiz.id}")
        return
    for num, saved_quiz in enumerate(quizzes_database[quiz_owner]):
        if saved_quiz.quiz_id == active_quiz.id:
            congrats_text = []
            for winner in saved_quiz.winners:
                chat_member_info = await bot.get_chat_member(saved_quiz.chat_id, winner)
                congrats_text.append(chat_member_info.user.get_mention(as_html=True))
            await bot.send_message(saved_quiz.chat_id, "The quiz is over, thank you all! Here are our winners:\n\n"
                                   + "\n".join(congrats_text), parse_mode="HTML")
            del quizzes_owners[active_quiz.id]
            del quizzes_database[quiz_owner][num]



@dp.message_handler(commands=["start"])
async def cmd_start(messsage: types.Message):
    if messsage.chat.type == types.ChatType.PRIVATE:
        poll_keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
        poll_keyboard.add(types.KeyboardButton(text="Create a quiz",
                                            request_poll=types.KeyboardButtonPollType(type=types.PollType.QUIZ)))
        poll_keyboard.add(types.KeyboardButton(text="Cancel"))
        await messsage.answer("Click on the button below and create a quiz!"
                              "Warning: in the future it will be public (non-anonymym).", reply_markup=poll_keyboard)
    else:
        words = messsage.text.split()
        if len(words) == 1:
            bot_info = await bot.get_me()
            keyboard = types.InlineKeyboardMarkup()
            move_to_dm_button = types.InlineKeyboardButton(text="Move to private messages",
                                                           url=f"t.me/{bot_info.username}?start=anything")
            keyboard.add(move_to_dm_button)
            await messsage.reply("No quiz selected. Please move to private messages with the bot "
                                 "to create a new quiz.", reply_markup=keyboard)
        else:
            quiz_owner = quizzes_owners.get(words[1])
            if not quiz_owner:
                await messsage.reply("The quiz has been removed, invalid, or already running in another group. Try to create a new quiz.")
                return
            for saved_quiz in quizzes_database[quiz_owner]:
                if saved_quiz.quiz_id == words[1]:
                    msg = await bot.send_poll(chat_id=messsage.chat.id, question=saved_quiz.question,
                                        is_anonymous=False, options=saved_quiz.options, type="quiz",
                                        correct_option_id=saved_quiz.correct_option_id)
                    quizzes_owners[msg.poll.id] = quiz_owner
                    del quizzes_owners[words[1]]
                    saved_quiz.quiz_id = msg.poll.id
                    saved_quiz.chat_id = msg.chat.id
                    saved_quiz.message_id = msg.message_id

@dp.message_handler(lambda message: message.text == "Cancel")
async def action_cancel(message: types.Message):
    remove_keyboard = types.ReplyKeyboardRemove()
    await message.answer("Action cancelled. Enter /start to start again.", reply_markup=remove_keyboard)

@dp.message_handler(content_types=["poll"])
async def msg_with_poll(message: types.Message):
    if not quizzes_database.get(str(message.from_user.id)):
        quizzes_database[str(message.from_user.id)] = []

    if message.poll.type != "quiz":
        await message.reply("Sorry, I only take quizzes (quiz)!")
        return

    quizzes_database[str(message.from_user.id)].append(Quiz(
        quiz_id=message.poll.id,
        question=message.poll.question,
        options=[o.text for o in message.poll.options],
        correct_option_id=message.poll.correct_option_id,
        owner_id=message.from_user.id)
    )

    quizzes_owners[message.poll.id] = str(message.from_user.id)

    await message.reply(
        f"The quiz is saved. Total number of quizzes saved: {len(quizzes_database[str(message.from_user.id)])}")

@dp.inline_handler()
async def inline_query(query: types.InlineQuery):
    results = []
    user_quizzes = quizzes_database.get(str(query.from_user.id))
    if user_quizzes:
        for quiz in user_quizzes:
            keyboard = types.InlineKeyboardMarkup()
            start_quiz_button = types.InlineKeyboardButton(
                text="Send to the group",
                url=await deep_linking.get_startgroup_link(quiz.quiz_id)
            )
            keyboard.add(start_quiz_button)
            results.append(types.InlineQueryResultArticle(
                id=quiz.quiz_id,
                title=quiz.question,
                input_message_content=types.InputTextMessageContent(
                    message_text="Click the button below to send the quiz to the group."),
                reply_markup=keyboard
            ))
    await query.answer(switch_pm_text="Create a quiz", switch_pm_parameter="_",
                       results=results, cache_time=120, is_personal=True)

if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)
