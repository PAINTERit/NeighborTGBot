import telebot
from telebot.types import Message, CallbackQuery

from bot_functions import (create_meme, get_answer, get_cat_status_code,
                           get_last_new, get_quote_author, get_quote_text)
from config import TG_TOKEN

bot = telebot.TeleBot(TG_TOKEN)


class Meme:
    """
    Класс для сохранения параметров для создания мема.
    """
    text: str
    photo: str


@bot.message_handler(commands=["start"])
def hello(message: Message) -> None:
    """
    Начало работы с ботом. Создание клавиатуры для удобной работы.
    :param message: Message
    :return: None
    """
    keyboard = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
    button_quote = telebot.types.KeyboardButton("/quote 📜")
    button_cat = telebot.types.KeyboardButton("/cat 🐈")
    button_yes_no = telebot.types.KeyboardButton("/question ❓")
    button_news = telebot.types.KeyboardButton("/news 🌐")
    button_meme = telebot.types.KeyboardButton("/meme 🐸")
    keyboard.row(button_quote, button_cat, button_yes_no, button_news, button_meme)
    bot.send_message(
        message.chat.id,
        "Тебя приветствует соседский бот!\nНиже приведены команды, которые я могу исполнить 😎",
        reply_markup=keyboard,
    )


@bot.message_handler(commands=["cat"])
def cat_image(message: Message) -> None:
    """
    Функция для работы с картинкой, в которой создается клавиатура для дальнейшей работы.
    :param message: Message
    :return: None
    """
    keyboard = telebot.types.InlineKeyboardMarkup()
    button_yes = telebot.types.InlineKeyboardButton("Да", callback_data="cat_yes")
    button_no = telebot.types.InlineKeyboardButton("Нет", callback_data="cat_no")
    keyboard.row(button_yes, button_no)
    bot.send_message(
        message.chat.id,
        "Хочешь получить картинку статус кода с котиком?",
        reply_markup=keyboard,
    )


@bot.message_handler(commands=["quote"])
def quote(message: Message) -> None:
    """
    Функция для работы с цитатой, в которой создается клавиатура для дальнейшей работы.
    :param message: Message
    :return: None
    """
    keyboard = telebot.types.InlineKeyboardMarkup()
    button_yes = telebot.types.InlineKeyboardButton("Да", callback_data="quote_yes")
    button_no = telebot.types.InlineKeyboardButton("Нет", callback_data="quote_no")
    keyboard.row(button_yes, button_no)
    bot.send_message(message.chat.id, "Хочешь получить цитату?", reply_markup=keyboard)


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


def answer(message:  Message) -> None:
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

    src = f"user_images/{file_info.file_id}.jpg"
    with open(src, "wb") as new_file:
        new_file.write(downloaded_file)

    Meme.photo = src

    bot.send_message(message.chat.id, "Далее напиши текст.")
    bot.register_next_step_handler(message, get_text)


def get_text(message: Message) -> None:
    """
    Функция для получения текста.
    :param message: Message
    :return: None
    """
    Meme.text = message.text
    bot.send_message(message.chat.id, "Вот твой мем!")
    send_meme(message)


def send_meme(message: Message) -> None:
    """
    Функция для отправки мема.
    :param message: Message
    :return: None
    """
    bot.send_photo(message.chat.id, create_meme(Meme.photo, Meme.text))


@bot.callback_query_handler(func=lambda call: True)
def handle(call: CallbackQuery) -> None:
    """
    Функция, содержащая ответы на определенные кнопки в клавиатуре.
    :param call: CallbackQuery
    :return: None
    """
    if call.data == "quote":
        quote()
    elif call.data == "cat_image":
        cat_image()
    elif call.data == "yes_no":
        yes_or_no()
    elif call.data == "cat_yes":
        bot.send_photo(call.message.chat.id, get_cat_status_code())
    elif call.data == "quote_yes":
        bot.send_message(
            call.message.chat.id, f"{get_quote_text()}\n{get_quote_author()}"
        )
    else:
        bot.send_message(call.message.chat.id, "Вы отказались! 😞")
    bot.answer_callback_query(call.id)


@bot.message_handler(content_types=["text"])
def hello(message: Message) -> None:
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
