import logging
import time

import flask

import telebot

API_TOKEN = "721732720:AAEnxBRKwlkSAMWuZ0YvsF2joId-o1rDlRg"

WEBHOOK_HOST = "https://pacific-sea-51251.herokuapp.com/"
WEBHOOK_PORT = 8443  # 443, 80, 88 or 8443 (port need to be 'open')
WEBHOOK_LISTEN = 'https://test-weather-the-best.herokuapp.com/'  # In some VPS you may need to put here the IP addr

WEBHOOK_SSL_CERT = './webhook_cert.pem'  # Path to the ssl certificate
WEBHOOK_SSL_PRIV = './webhook_pkey.pem'  # Path to the ssl private key

# Quick'n'dirty SSL certificate generation:
#
# openssl genrsa -out webhook_pkey.pem 2048
# openssl req -new -x509 -days 3650 -key webhook_pkey.pem -out webhook_cert.pem
#
# When asked for "Common Name (e.g. server FQDN or YOUR name)" you should reply
# with the same value in you put in WEBHOOK_HOST

WEBHOOK_URL_BASE = "https://%s:%s" % (WEBHOOK_HOST, WEBHOOK_PORT)
WEBHOOK_URL_PATH = "/%s/" % (API_TOKEN)

# logger = telebot.logger
# telebot.logger.setLevel(logging.INFO)

bot = telebot.TeleBot(API_TOKEN)

app = flask.Flask(__name__)


@bot.message_handler(commands=['start'])
def send_welcome(message):
   bot.reply_to(message, "Дороу")


@bot.message_handler(commands=['help'])
def send_welcome(message):
   bot.reply_to(message, "Бог в помощь")


@bot.message_handler(commands=['location'])
def location(message):
   keyboard = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
   button_geo = types.KeyboardButton(text="Send de way", request_location=True)
   keyboard.add(button_geo)
   bot.send_message(message.chat.id, "Do u now de way", reply_markup=keyboard)


@bot.message_handler(content_types=["location"])
def location(message):
   url = requests.get(f'http://api.openweathermap.org/data/2.5/weather?'
                      f'lat={message.location.latitude}&lon={message.location.longitude}&appid={WEATHER_API_KEY}').json()
   bot.send_message(message.chat.id, text=f'{url.get("name")}, {url.get("main").get("temp")}')

   #f'{url.get("name")}, {url.get("main").get("temp")}


@bot.message_handler(func=lambda message: True)
def echo_message(message):
   bot.reply_to(message, message.text)


# Remove webhook, it fails sometimes the set if there is a previous webhook
bot.remove_webhook()

time.sleep(0.1)

# Set webhook
bot.set_webhook(url=WEBHOOK_URL_BASE + WEBHOOK_URL_PATH,
                certificate=open(WEBHOOK_SSL_CERT, 'r'))

# Start flask server
app.run(host=WEBHOOK_LISTEN,
        port=WEBHOOK_PORT,
        ssl_context=(WEBHOOK_SSL_CERT, WEBHOOK_SSL_PRIV),
debug=True)

