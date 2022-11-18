import telebot
from config import TG_TOKEN
from api import cat_status_code, quote_text, quote_author, yes_no_maybe

bot = telebot.TeleBot(TG_TOKEN)


@bot.message_handler(commands=['start'])
def hello(message):
    keyboard = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
    button_quote = telebot.types.KeyboardButton('/quote')
    button_cat = telebot.types.KeyboardButton('/cat')
    button_yes_no = telebot.types.KeyboardButton('/question')
    keyboard.row(button_quote, button_cat, button_yes_no)
    bot.send_message(message.chat.id, 'Тебя приветствует соседский бот!\nНиже приведены команды, которые я могу исполнить :)', reply_markup=keyboard)


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


@bot.message_handler(commands=['question'])
def yes_or_no(message):
    bot.send_message(message.chat.id, "Задай вопрос, на который можно ответить 'да' или 'нет' :)")
    bot.register_next_step_handler(message, answer)


def answer(message):
    bot.send_animation(message.chat.id, yes_no_maybe())


@bot.callback_query_handler(func=lambda call: True)
def handle(call):
    if call.data == 'quote':
        bot.send_message(call.message.chat.id, get_quote(call.message))
    elif call.data == 'cat_image':
        bot.send_message(call.message.chat.id, cat_image(call.message))
    elif call.data == 'yes_no':
        bot.send_message(call.message.chat.id, yes_or_no(call.message))
    elif call.data == 'cat_yes':
        print(cat_status_code())
        bot.send_photo(call.message.chat.id, cat_status_code())
    elif call.data == 'quote_yes':
        bot.send_message(call.message.chat.id, f"{quote_text()}\n{quote_author()}")
    else:
        bot.send_message(call.message.chat.id, 'Вы отказались!')
    bot.answer_callback_query(call.id)


@bot.message_handler(content_types=['text'])
def hello(message):
    bot.send_message(message.chat.id, "Отвечаю на любой текст!")


print("Бот запущен!")
bot.infinity_polling()
