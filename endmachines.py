import telebot
import config2
import dbworker

bot = telebot.TeleBot(config2.token)

@bot.message_handler(commands=["start"])
def cmd_start(message):
    state = dbworker.get_current_state(message.chat.id)
    if state == config2.States.S_ENTER_NAME.value:
        bot.send_message(message.chat.id, "I think someone promised to send his name, but he never did it :( Waiting...")
    elif state == config2.States.S_ENTER_AGE.value:
        bot.send_message(message.chat.id, "It seems that someone promised to send his age, but never did it :( Waiting...")
    elif state == config2.States.S_SEND_PIC.value:
        bot.send_message(message.chat.id, "It seems that someone promised to send a picture, but never did it :( Waiting...")
    else: 
        bot.send_message(message.chat.id, "Hi! How can I address you?")
        dbworker.set_state(message.chat.id, config2.States.S_ENTER_NAME.value)

@bot.message_handler(commands=["reset"])
def cmd_reset(message):
    bot.send_message(message.chat.id, "Well, let's start a new way. What is your name?")
    dbworker.set_state(message.chat.id, config2.States.S_ENTER_NAME.value)

@bot.message_handler(func=lambda message: dbworker.get_current_state(message.chat.id) == config2.States.S_ENTER_NAME.value)
def user_entering_name(message):
    bot.send_message(message.chat.id, "That's a great name, I'll remember! Now please tell me your age.")
    dbworker.set_state(message.chat.id, config2.States.S_ENTER_AGE.value)

@bot.message_handler(func=lambda message: dbworker.get_current_state(message.chat.id) == config2.States.S_ENTER_AGE.value)
def user_entering_age(message):
    if not message.text.isdigit():
        bot.send_message(message.chat.id, "Something's wrong, try again!")
        return
    if int(message.text) < 5 or int(message.text) > 100:
        bot.send_message(message.chat.id, "It's a strange age. I don't believe it! Answer honestly.")
        return
    else:
        bot.send_message(message.chat.id, "I used to be so old... Eh... However, let's not be distracted."
                                          "Send me a picture.")
        dbworker.set_state(message.chat.id, config2.States.S_SEND_PIC.value)

@bot.message_handler(content_types=["photo"],
                    func=lambda message: dbworker.get_current_state(message.chat.id) == config2.States.S_SEND_PIC.value)
def user_sending_photo(message):
    bot.send_message(message.chat.id, "It's cool! Nothing more is required of you. If you want to talk again -"
                                      "send a command /start.")    
    dbworker.set_state(message.chat.id, config2.States.S_START.value)             

if __name__ == "__main__":
    bot.infinity_polling()
    
