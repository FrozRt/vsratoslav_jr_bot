import os
import sys
import configparser
import random
from datetime import datetime
from io import BytesIO

import telebot
from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
CHANNEL = os.getenv("TG_CHANNEL")
PIC_PATH = os.getenv("PIC_PATH")

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
    imgByteArr = BytesIO()
    image.save(imgByteArr, format='PNG')

    keyboard1 = telebot.types.ReplyKeyboardMarkup(True, True)
    keyboard1.row('Да', 'Нет')

    if bot.send_photo(message.chat.id, imgByteArr.getvalue(), reply_markup=keyboard1):
        bot.send_message(message.chat.id, "Как насчет того, чтобы разместить мем на нашем канале?")


def generate_signature(image):
    """
    Выбирает подпись из файла сборника и рисует ее на картинке
    """
    with open('signature_collection.txt') as f:
        sign_list = f.read().splitlines()
    random_message = random.choice(sign_list)

    font = ImageFont.truetype('Lobster.ttf', 42)  # Загрузка шрифта и установка размера
    font_color = (0, 0, 0)  # Цвет шрифта
    signature_pos = (50, 50)  # Координаты первой буквы подписи на загруженной картинке

    drawing = ImageDraw.Draw(image)
    drawing.text(signature_pos, random_message, font=font, fill=font_color)

    return image


@bot.message_handler(content_types=['text'])
def send_text(message):
    if message.text == 'Да':
        bot.forward_message(CHANNEL, message.chat.id, message_id=message.message_id - 2)
    else:
        bot.send_message(message.chat.id, "Заглядывай за новыми мемами!")


if __name__ == '__main__':
    bot.polling(none_stop=True)
