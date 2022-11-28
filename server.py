import telebot
from telebot.types import Message, ReplyKeyboardMarkup

from bot_functions import (
    create_meme,
    get_answer,
    get_cat_status_code,
    get_last_new,
    get_quote_author,
    get_quote_text,
)
from config import TG_TOKEN, photo_src

bot = telebot.TeleBot(TG_TOKEN)
user_meme = {}


def navigation_keyboard() -> ReplyKeyboardMarkup:
    """
    Создание клавиатуры для выбора действия.
    :return: ReplyKeyboardMarkup
    """
    keyboard = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
    button_quote = telebot.types.KeyboardButton("/quote 📜")
    button_cat = telebot.types.KeyboardButton("/cat 🐈")
    button_yes_no = telebot.types.KeyboardButton("/question ❓")
    button_news = telebot.types.KeyboardButton("/news 🌐")
    button_meme = telebot.types.KeyboardButton("/meme 🐸")
    return keyboard.add(
        button_quote, button_cat, button_yes_no, button_news, button_meme, row_width=2
    )


@bot.message_handler(commands=["start"])
def hello(message: Message) -> None:
    """
    Начало работы с ботом.
    :param message: Message
    :return: None
    """
    bot.send_message(
        message.chat.id,
        "Тебя приветствует соседский бот!\nНиже приведены команды, которые я могу исполнить 😎",
        reply_markup=navigation_keyboard(),
    )


@bot.message_handler(commands=["cat"])
def cat_image(message: Message) -> None:
    """
    Функция для работы с картинкой, в которой создается клавиатура для дальнейшей работы.
    :param message: Message
    :return: None
    """
    bot.send_message(message.chat.id, get_cat_status_code())


@bot.message_handler(commands=["quote"])
def quote(message: Message) -> None:
    """
    Функция для работы с цитатой, в которой создается клавиатура для дальнейшей работы.
    :param message: Message
    :return: None
    """
    bot.send_message(message.chat.id, f"{get_quote_text()}\n{get_quote_author()}")


@bot.message_handler(commands=["news"])
def last_new(message: Message) -> None:
    """
    Функция, в которой отправляется сообщение с последней новостью.
    :param message: Message
    :return: None
    """
    bot.send_message(message.chat.id, get_last_new())


@bot.message_handler(commands=["question"])
def yes_or_no(message: Message) -> None:
    """
    Функция, в которой требуется отправить вопрос для бота.
    :param message: Message
    :return: None
    """
    bot.send_message(
        message.chat.id, "Задай вопрос, на который можно ответить 'да' или 'нет' 😉"
    )
    bot.register_next_step_handler(message, answer)


def answer(message: Message) -> None:
    """
    Функция для выдачи ответа на вопрос пользователя.
    :param message: Message
    :return: None
    """
    bot.send_animation(message.chat.id, get_answer())


@bot.message_handler(commands=["meme"])
def meme_hello(message: Message) -> None:
    """
    Функция приветствия с пользователем.
    :param message: Message
    :return: None
    """
    bot.send_message(message.chat.id, "Привет! Прикрепи картинку для создания мема.")
    user_meme[message.chat.id] = {}
    bot.register_next_step_handler(message, get_info)


@bot.message_handler(content_types=["photo"])
def get_info(message: Message) -> None:
    """
    Функция для получения картинки для создания мема.
    :param message: Message
    :return: None
    """

    file_info = bot.get_file(message.photo[-1].file_id)
    downloaded_file = bot.download_file(file_info.file_path)

    user_meme[message.chat.id]["photo"] = f"{photo_src}{file_info.file_id}.jpg"
    with open(user_meme[message.chat.id]["photo"], "wb") as new_file:
        new_file.write(downloaded_file)

    bot.send_message(message.chat.id, "Далее напиши текст.")
    bot.register_next_step_handler(message, get_text)


def get_text(message: Message) -> None:
    """
    Функция для получения текста.
    :param message: Message
    :return: None
    """
    user_meme[message.chat.id]["text"] = message.text
    bot.send_message(message.chat.id, "Вот твой мем!")
    send_meme(message)


def send_meme(message: Message) -> None:
    """
    Функция для отправки мема.
    :param message: Message
    :return: None
    """
    bot.send_photo(
        message.chat.id,
        create_meme(
            user_meme[message.chat.id]["photo"], user_meme[message.chat.id]["text"]
        ),
    )
    clear_content(message.chat.id)


def clear_content(user_id):
    user_meme[user_id] = {}


@bot.message_handler(content_types=["text"])
def wrong_answer(message: Message) -> None:
    """
    Функция, которая выдает ответ на любое сообщение, которого нет в функциях.
    :param message: Message
    :return: None
    """
    bot.send_message(
        message.chat.id, "Ты просишь невозможное 🙁 Лучше выбери команду из меню!"
    )


print("Бот запущен!")
bot.infinity_polling()
