import telebot
from telebot import types 
import os
import time

token = '1173464994:AAFiy8Rdc1cPEE8G-10ihcN7FGbSqcO3UrY'
bot = telebot.TeleBot(token)

@bot.message_handler(commands=['fileid'])
def file_id(message):
    for file in os.listdir('photo/'):
        if file.split('.')[-1] == 'jpg':
            f = open('photo/'+file, 'rb')
            msg = bot.send_photo(message.chat.id, f, None)
            bot.send_message(message.chat.id, msg.photo[-1].file_id, reply_to_message_id=msg.message_id)
        time.sleep(3)

@bot.message_handler(commands=['geophone'])
def geophone(messsage):
    keyboard = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
    button_phone = types.KeyboardButton(text='Send your phone number', request_contact=True)
    button_geo = types.KeyboardButton(text='Send a geolocation', request_location=True)
    keyboard.add(button_geo, button_phone)
    bot.send_message(messsage.chat.id, 'Send me your phone number or share your location, pathetic little man!', reply_markup=keyboard)

@bot.message_handler(func=lambda message: True)
def any_message(message):
    bot.reply_to(message, 'Himself {!s}'.format(message.text))

@bot.edited_message_handler(func=lambda message: True)
def edit_message(message):
    bot.edit_message_text(chat_id=message.chat.id,
                        text= 'Himself {!s}'.format(message.text),
                        message_id=message.message_id + 1)

@bot.inline_handler(func=lambda query: True)
def inline_mode(query):
    randphoto1 = types.InlineQueryResultCachedPhoto(
        id='1',
        photo_file_id='AgACAgQAAxkDAAMoXvPO2uFNYCQFTZVXhQlLfHEXZ0UAAsuwMRvUzqBTIccZX_COP5xKF3YjXQADAQADAgADbQADFUwBAAEaBA',
        caption='Random photo #1'
    )
    randphoto2 = types.InlineQueryResultCachedPhoto(
        id='2',
        photo_file_id='AgACAgQAAxkDAAMmXvPO1zdFrNnQlZedBdewIJneKvYAAsqwMRvUzqBT_z1SYtD9QJXOMkokXQADAQADAgADbQAD-UcBAAEaBA',
        caption='Random photo #2'
    )
    randphoto3 = types.InlineQueryResultCachedPhoto(
        id='3',
        photo_file_id='AgACAgQAAxkDAAMkXvPO00XrUfOUYuAsIxizcbvfNwIAAsmwMRvUzqBTeWOqakF8D4ymIuUiXQADAQADAgADbQADq4IDAAEaBA',
        caption='Random photo #3'
    )
    randphoto4 = types.InlineQueryResultCachedPhoto(
        id='4',
        photo_file_id='AgACAgQAAxkDAAMiXvPO0Jup0MwiX30DV-Pk3cg1F6UAAsiwMRvUzqBTEMyk2yJvZAshm-MiXQADAQADAgADbQAD3XwDAAEaBA',
        caption='Random photo #4'
    )
    randphoto5 = types.InlineQueryResultCachedPhoto(
        id='5',
        photo_file_id='AgACAgQAAxkDAAMgXvPOzTsggu7AIEg7t0J9ywtqklkAAsCwMRvUzqBTpOIAAW-WKqtFmqt6I10AAwEAAwIAA20AAzXuAgABGgQ',
        caption='Random photo #5'
    )
    randphoto6 = types.InlineQueryResultCachedPhoto(
        id='6',
        photo_file_id='AgACAgQAAxkDAAMeXvPOys6gvtUqFIhz75FM1TXCRbwAAsewMRvUzqBTFl1WKpW4nHaeyZUiXQADAQADAgADbQADZ-UEAAEaBA',
        caption='Random photo #6'
    )
    bot.answer_inline_query(query.id, [randphoto1, randphoto2, randphoto3, randphoto4, randphoto5, randphoto6])

if __name__ == '__main__':
    bot.infinity_polling()