import telebot
import os
import random
from telebot import types

bot_token = '6214483932:AAGgcQFBKayhRpEbCuiNiX7gMggdA46264k'

class Bot:
    def __init__(self, token, images_folder, sounds_folder):
        self.bot = telebot.TeleBot(token)
        self.images_folder = images_folder
        self.sounds_folder = sounds_folder

        @self.bot.message_handler(commands=['start'])
        def start(message):
            markup = types.ReplyKeyboardMarkup(resize_keyboard = True)
            item1 = types.KeyboardButton('Звук')
            item2 = types.KeyboardButton('Репозиторий')

            markup.add(item1,item2)

            self.bot.send_message(message.chat.id, 'Привет! Чем могу помочь?',reply_markup=markup)

        @self.bot.message_handler(func=lambda message: message.text == 'отправь мне фото')
        def photo(message):
            # Получаем список файлов в папке "photo"
            photo_files = os.listdir(self.images_folder)
            if photo_files:
                # Выбираем случайное изображение из списка
                random_photo = random.choice(photo_files)

                # Создаем полный путь к выбранному изображению
                photo_path = os.path.join(self.images_folder, random_photo)

                # Отправляем изображение пользователю
                with open(photo_path, 'rb') as photo_file:
                    self.bot.send_photo(message.chat.id, photo_file)
            else:
                self.bot.send_message(message.chat.id, 'В папке "photo" нет изображений.')

        @self.bot.message_handler(func=lambda message: message.text == 'Звук')
        def send_random_sound(message):
            # Получаем список файлов в папке "sounds"
            sound_files = os.listdir(self.sounds_folder)

            if sound_files:
                # Выбираем случайное звуковое сообщение из списка
                random_sound = random.choice(sound_files)

                # Создаем полный путь к выбранному звуковому сообщению
                sound_path = os.path.join(self.sounds_folder, random_sound)

                # Отправляем звуковое сообщение пользователю
                with open(sound_path, 'rb') as sound_file:
                    self.bot.send_voice(message.chat.id, sound_file)
            else:
                self.bot.send_message(message.chat.id, 'В папке "sounds" нет звуковых сообщений.')

        @self.bot.message_handler(func=lambda message: message.text == 'Репозиторий')
        def send_github_link(message):
            github_repo_url = 'https://github.com/MetelevaV/Chat_Bot'  # Замените на актуальную ссылку на ваш репозиторий
            self.bot.send_message(message.chat.id, f'Ссылка на репозиторий бота: {github_repo_url}')

        @self.bot.message_handler(commands=['stop'])
        def stop(message):
            hide_markup = types.ReplyKeyboardRemove()
            self.bot.send_message(message.chat.id, 'Пока!', reply_markup=hide_markup)

    def start(self):
        self.bot.polling(none_stop=True)

if __name__ == "__main__":
    my_bot = Bot(bot_token, 'photo', 'sounds')
    my_bot.start()