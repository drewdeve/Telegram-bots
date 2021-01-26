import cherrypy
import telebot

BOT_TOKEN = "1338564247:AAHO9EId3t3pnUCb7VtQ3vYHb3fAqzUIDIE"

bot = telebot.TeleBot(BOT_TOKEN)

@bot.message_handler(commands=["start"])
def command_start(message):
    bot.send_message(message.chat.id, "Hello! I'm bot number one")

class WebhookServer(object):
    @cherrypy.expose
    def index(self):
        length = int(cherrypy.request.headers['content-length'])
        json_string = cherrypy.request.body.read(length).decode("utf-8")
        update = telebot.types.Update.de_json(json_string)
        bot.process_new_updates([update])
        return ''

if __name__ == '__main__':
    cherrypy.config.update({
        'server.socket_host': '127.0.0.1',
        'server.socket_port': 7771,
        'engine.autoreload.on': False
    })
    cherrypy.quickstart(WebhookServer(), '/', {'/': {}})