# token = "721732720:AAEnxBRKwlkSAMWuZ0YvsF2joId-o1rDlRg"

import telebot
import logging
from telebot import types
import requests

API_TOKEN_BOT = '721732720:AAEnxBRKwlkSAMWuZ0YvsF2joId-o1rDlRg'
WEATHER_API_KEY = '1ff3202a2e5beed64fcdb7c307480a44'

bot = telebot.TeleBot(API_TOKEN_BOT, threaded=False)

logger = telebot.logger
telebot.logger.setLevel(logging.DEBUG)  # Outputs debug messages to console.


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


bot.infinity_polling(True)



# class BotHandler:

#     def __init__(self, token):
#         self.token = token
#         self.api_url = "https://api.telegram.org/bot{}/".format(token)

#     def get_updates(self, offset=None, timeout=30):
#         method = 'getUpdates'
#         params = {'timeout': timeout, 'offset': offset}
#         resp = requests.get(self.api_url + method, params)
#         result_json = resp.json()['result']
#         return result_json

#     def send_message(self, chat_id, text):
#         params = {'chat_id': chat_id, 'text': text}
#         method = 'sendMessage'
#         resp = requests.post(self.api_url + method, params)
#         return resp

#     def get_last_update(self):
#         get_result = self.get_updates()

#         if len(get_result) > 0:
#             last_update = get_result[-1]
#         else:
#             last_update = get_result[len(get_result)]

#         return last_update

# greet_bot = BotHandler(token)  
# greetings = ('здравствуй', 'привет', 'ку', 'здорово')  
# now = datetime.datetime.now()


# def main():  
#     new_offset = None
#     today = now.day
#     hour = now.hour

#     while True:
#         greet_bot.get_updates(new_offset)

#         last_update = greet_bot.get_last_update()

#         last_update_id = last_update['update_id']
#         last_chat_text = last_update['message']['text']
#         last_chat_id = last_update['message']['chat']['id']
#         last_chat_name = last_update['message']['chat']['first_name']

#         if last_chat_text.lower() in greetings and today == now.day and 6 <= hour < 12:
#             greet_bot.send_message(last_chat_id, 'Доброе утро, {}'.format(last_chat_name))
#             today += 1

#         elif last_chat_text.lower() in greetings and today == now.day and 12 <= hour < 17:
#             greet_bot.send_message(last_chat_id, 'Добрый день, {}'.format(last_chat_name))
#             today += 1

#         elif last_chat_text.lower() in greetings and today == now.day and 17 <= hour < 23:
#             greet_bot.send_message(last_chat_id, 'Добрый вечер, {}'.format(last_chat_name))
#             today += 1

#         new_offset = last_update_id + 1

# if __name__ == '__main__':  
#     try:
#         main()
#     except KeyboardInterrupt:
#         exit()
