import cherrypy
import requests
import telebot

WEBHOOK_HOST = '83.99.185.157'
WEBHOOK_PORT = 443
WEBHOOK_LISTEN = '0.0.0.0'
WEBHOOK_SSL_CERT = 'C:/telegram-bot/webhook_cert.pem'  
WEBHOOK_SSL_PRIV = 'C:/telegram-bot/webhook_pkey.pem' 
WEBHOOK_URL_BASE = "https://{!s}:{!s}".format(WEBHOOK_HOST, WEBHOOK_PORT)

BOT_1_TOKEN = "1338564247:AAHO9EId3t3pnUCb7VtQ3vYHb3fAqzUIDIE"
BOT_2_TOKEN = "1386787789:AAG7xlU0ct2gR9ocnI5YO6TKbJIt-JwZ3fA"

BOT_1_ADDRES = "http://127.0.0.1:7771"
BOT_2_ADDRES = "http://127.0.0.1:7772"

bot_1 = telebot.TeleBot(BOT_1_TOKEN)
bot_2 = telebot.TeleBot(BOT_2_TOKEN)

class WebhookServer(object):

    @cherrypy.expose
    def AAAA(self):
        if 'content-length' in cherrypy.request.headers and \
           'content-type' in cherrypy.request.headers and \
            cherrypy.request.headers['content-type'] == 'application/json':
             length = int(cherrypy.request.headers['content-length'])
             json_string = cherrypy.request.body.read(length).decode("utf-8")
             requests.post(BOT_1_ADDRES, data=json_string)
             return ''
        else:
            raise cherrypy.HTTPError(403)

    @cherrypy.expose
    def ZZZZ(self):
        if 'content-length' in cherrypy.request.headers and \
           'content-type' in cherrypy.request.headers and \
            cherrypy.request.headers['content-type'] == 'application/json':
             length = int(cherrypy.request.headers['content-length'])
             json_string = cherrypy.request.body.read(length).decode("utf-8")
             requests.post(BOT_2_ADDRES, data=json_string)
             return ''
        else:
            raise cherrypy.HTTPError(403)

if __name__ == '__main__':

    bot_1.remove_webhook()
    bot_1.set_webhook(url='https://83.99.185.157/AAAA',
                      certificate=open(WEBHOOK_SSL_CERT, 'r'))

    bot_2.remove_webhook()
    bot_2.set_webhook(url='https://83.99.185.157/ZZZZ',
                      certificate=open(WEBHOOK_SSL_CERT, 'r'))

    cherrypy.config.update({
        'server.socket_host': WEBHOOK_LISTEN,
        'server.socket_port': WEBHOOK_PORT,
        'server.ssl_module': 'builtin',
        'server.ssl_certificate': WEBHOOK_SSL_CERT,
        'server.ssl_private_key': WEBHOOK_SSL_PRIV,
        'engine.autoreload.on': False
    })
    cherrypy.quickstart(WebhookServer(), '/', {'/': {}})
