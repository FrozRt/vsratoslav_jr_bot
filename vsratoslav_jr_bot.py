import os
import sys
import configparser
import random
from datetime import datetime

import telebot
from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont

config_path = os.path.join(sys.path[0], 'settings.ini')
config = configparser.ConfigParser()
config.read(config_path)

BOT_TOKEN = config.get('Telegram', 'BOT_TOKEN')
CHANNEL = config.get('Telegram', 'TG_CHANNEL')
PIC_PATH = config.get('Bot_settings', 'PIC_PATH')

bot = telebot.TeleBot(BOT_TOKEN)


@bot.message_handler(commands=['start'])
def handle_start(message):
    bot.send_message(message.chat.id,
                     f'''
Привет, {message.chat.first_name}!
Я бот Всратослав Джуниор.
Я могу создать для тебя мемас!
Просто отправь мне подходящую для мема картинку
я подпишу её
иии
посмотрим что получится!''')


@bot.message_handler(content_types=['photo'])
def memes_maker(message):
    """
    Получает отправленную пользователем картинку, сохраняет ее по указанному в настройках пути,
    отправляет в функцию-обработчик и отсылает готовый мемес обратно пользователю
    """
    fileID = message.photo[-1].file_id
    file_info = bot.get_file(fileID)
    downloaded_file = bot.download_file(file_info.file_path)
    image_name = f"{PIC_PATH}/{datetime.strftime(datetime.now(), '%Y-%m-%d_%H:%M')}_{message.from_user.id}.png"

    with open(image_name, 'wb') as new_file:
        new_file.write(downloaded_file)
    image = generate_signature(Image.open(image_name))
    image.save('test.jpg')
    bot.send_photo(message.chat.id, photo=open('test.jpg', 'rb'))


def generate_signature(image):
    """
    Выбирает подпись из файла сборника и рисует ее на картинке
    """

    with open('signature_collection.txt') as f:
        sign_list = f.read().splitlines()
    random_message = random.choice(sign_list)

    font = ImageFont.truetype('Lobster.ttf', 48)  # Загрузка шрифта и установка размера
    font_color = (0, 0, 0)  # Цвет шрифта
    signature_pos = (50, 50)  # Координаты первой буквы подписи на загруженной картинке

    drawing = ImageDraw.Draw(image)
    drawing.text(signature_pos, random_message, font=font, fill=font_color)
    return image


if __name__ == '__main__':
    bot.polling(none_stop=True)
