import telebot
from time import time

token = "1124201362:AAEbI1nZSRmaBg1RetdYDwG5EKTMaZVDVyg"
bot = telebot.TeleBot(token)

GROUP_ID = -1001345959636

strings = {
    "ru": {
        "ro_msg": "Вам запрещено отправлять сюда сообщения в течение 10 минут."
    }, 
    "en": {
        "ro_msg": "You're not allowed to send messages here for 10 minutes."
    }
}

def get_language(lang_code):
    if not lang_code:
        return "en"
    if "-" in lang_code:
        lang_code = lang_code.split("-")[0]
    if lang_code == "ru":
        return "ru"
    else:
        return "en"

@bot.message_handler(func=lambda message: message.entities and message.chat.id == GROUP_ID)
def del_links(message):
    for entity in message.entities:
        if entity.type in ["url", "text_link"]:
            bot.delete_message(message.chat.id, message.message_id)


restricted_messages = ["я веган", "i am vegan"]

@bot.message_handler(func=lambda message: message.text and message.text.lower() in restricted_messages and message.chat.id == GROUP_ID)
def set_ro(message):
    print(message.from_user.language_code)
    bot.restrict_chat_member(message.chat.id, message.from_user.id, until_date=time()+600)
    bot.send_message(message.chat.id, strings.get(get_language(message.from_user.language_code)).get("ro_msg"),
                     reply_to_message_id=message.message_id)


if __name__ == "__main__":
    bot.infinity_polling()