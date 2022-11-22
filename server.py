import telebot
from config import TG_TOKEN
from bot_functions import cat_status_code, quote_text, quote_author, yes_no_maybe, last_news, create_meme

bot = telebot.TeleBot(TG_TOKEN)


class Meme:
    text: str
    photo: str


@bot.message_handler(commands=['start'])
def hello(message):
    keyboard = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
    button_quote = telebot.types.KeyboardButton('/quote 📜')
    button_cat = telebot.types.KeyboardButton('/cat 🐈')
    button_yes_no = telebot.types.KeyboardButton('/question ❓')
    button_news = telebot.types.KeyboardButton('/news 🌐')
    button_meme = telebot.types.KeyboardButton('/meme 🐸')
    keyboard.row(button_quote, button_cat, button_yes_no, button_news, button_meme)
    bot.send_message(message.chat.id, 'Тебя приветствует соседский бот!\nНиже приведены команды, которые я могу исполнить 😎', reply_markup=keyboard)


@bot.message_handler(commands=['cat'])
def cat_image(message):
    keyboard = telebot.types.InlineKeyboardMarkup()
    button_yes = telebot.types.InlineKeyboardButton('Да', callback_data='cat_yes')
    button_no = telebot.types.InlineKeyboardButton('Нет', callback_data='cat_no')
    keyboard.row(button_yes, button_no)
    bot.send_message(message.chat.id, 'Хочешь получить картинку статус кода с котиком?', reply_markup=keyboard)


@bot.message_handler(commands=['quote'])
def get_quote(message):
    keyboard = telebot.types.InlineKeyboardMarkup()
    button_yes = telebot.types.InlineKeyboardButton('Да', callback_data='quote_yes')
    button_no = telebot.types.InlineKeyboardButton('Нет', callback_data='quote_no')
    keyboard.row(button_yes, button_no)
    bot.send_message(message.chat.id, 'Хочешь получить цитату?', reply_markup=keyboard)


@bot.message_handler(commands=['news'])
def get_news(message):
    bot.send_message(message.chat.id, last_news())


@bot.message_handler(commands=['question'])
def yes_or_no(message):
    bot.send_message(message.chat.id, "Задай вопрос, на который можно ответить 'да' или 'нет' 😉")
    bot.register_next_step_handler(message, answer)


def answer(message):
    bot.send_animation(message.chat.id, yes_no_maybe())


@bot.message_handler(commands=['meme'])
def meme_hello(message):
    bot.send_message(message.chat.id, "Привет! Прикрепи картинку для создания мема.")
    bot.register_next_step_handler(message, get_photo)


@bot.message_handler(content_types=['photo'])
def get_photo(message):

    file_info = bot.get_file(message.photo[-1].file_id)
    downloaded_file = bot.download_file(file_info.file_path)

    src = f'user_images/{file_info.file_id}.jpg'
    with open(src, 'wb') as new_file:
        new_file.write(downloaded_file)

    Meme.photo = src

    bot.send_message(message.chat.id, "Далее напиши текст.")
    bot.register_next_step_handler(message, get_text)


def get_text(message):
    Meme.text = message.text
    bot.send_message(message.chat.id, "Вот твой мем!")
    bot.send_photo(message.chat.id, create_meme(Meme.photo, Meme.text))
    #bot.register_next_step_handler(message, send_meme)


#def send_meme(message):
    #bot.send_photo(message.chat.id, create_meme(Meme.photo, Meme.text))


@bot.callback_query_handler(func=lambda call: True)
def handle(call):
    if call.data == 'quote':
        bot.send_message(call.message.chat.id, get_quote(call.message))
    elif call.data == 'cat_image':
        bot.send_message(call.message.chat.id, cat_image(call.message))
    elif call.data == 'yes_no':
        bot.send_message(call.message.chat.id, yes_or_no(call.message))
    elif call.data == 'cat_yes':
        bot.send_photo(call.message.chat.id, cat_status_code())
    elif call.data == 'quote_yes':
        bot.send_message(call.message.chat.id, f"{quote_text()}\n{quote_author()}")
    else:
        bot.send_message(call.message.chat.id, 'Вы отказались! 😞')
    bot.answer_callback_query(call.id)


@bot.message_handler(content_types=['text'])
def hello(message):
    bot.send_message(message.chat.id, "Ты просишь невозможное 🙁 Лучше выбери команду из меню!")


print("Бот запущен!")
bot.infinity_polling()
