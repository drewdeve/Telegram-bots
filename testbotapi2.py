import telebot
from telebot import types

bot = telebot.TeleBot("1269368677:AAEayTnxpNBQzCTCwxsfRKF4AcW4IMz0Gd4")

@bot.message_handler(content_types=["text"])
def any_msg(message):
    keyboard = types.InlineKeyboardMarkup()
    url_button = types.InlineKeyboardButton(text="Перейдите на мою страницу в ВК", url="https://vk.com/stimixx")
    callback_button = types.InlineKeyboardButton(text='Press me', callback_data='test')
    switch_button = types.InlineKeyboardButton(text='Нажми меня', switch_inline_query='Telegram')
    keyboard.add(url_button,callback_button, switch_button)
    bot.send_message(message.chat.id, 'Я – сообщение из обычного режима', reply_markup=keyboard)

@bot.callback_query_handler(func=lambda call: True)
def callback_inline(call):
    if call.message:
        if call.data == 'test':
            bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text='Пыщь')
            bot.answer_callback_query(callback_query_id=call.id, show_alert=True, text = 'Пыщь!')
    elif call.inline_message_id:
        if call.data == 'test':
            bot.edit_message_text(inline_message_id=call.inline_message_id, text='Бдыщь')

@bot.inline_handler(lambda query: len(query.query) > 0)
def query_text(query):
    kb = types.InlineKeyboardMarkup()
    kb.add(types.InlineKeyboardButton(text='Press me', callback_data='test'))
    results = []
    single_msg = types.InlineQueryResultArticle(
        id='1', title='Press me',
        input_message_content=types.InputTextMessageContent(message_text='Я – сообщение из инлайн-режима'),
        reply_markup=kb
    )
    results.append(single_msg)
    bot.answer_inline_query(query.id, results)


if __name__ == '__main__':
    bot.infinity_polling()