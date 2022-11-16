import telebot
from config import TG_TOKEN
from api import cat_status_code, quote_text, quote_author, yes_no_maybe

bot = telebot.TeleBot(TG_TOKEN)


@bot.message_handler(commands=['cat'])
def hello(message):
    keyboard = telebot.types.InlineKeyboardMarkup()
    button_yes = telebot.types.InlineKeyboardButton('Да', callback_data='cat_yes')
    button_no = telebot.types.InlineKeyboardButton('Нет', callback_data='cat_no')
    keyboard.row(button_yes, button_no)
    bot.send_message(message.chat.id, 'Хотите получить картинку статус кода с котиком?', reply_markup=keyboard)


@bot.message_handler(commands=['quote'])
def hello(message):
    keyboard = telebot.types.InlineKeyboardMarkup()
    button_yes = telebot.types.InlineKeyboardButton('Да', callback_data='quote_yes')
    button_no = telebot.types.InlineKeyboardButton('Нет', callback_data='quote_no')
    keyboard.row(button_yes, button_no)
    bot.send_message(message.chat.id, 'Хотите получить цитату?', reply_markup=keyboard)


@bot.message_handler(commands=['question'])
def question(message):
    bot.send_message(message.chat.id, "Задай вопрос, на который можно ответить 'да' или 'нет' :)")
    bot.register_next_step_handler(message, answer)


def answer(message):
    bot.send_animation(message.chat.id, yes_no_maybe())


@bot.callback_query_handler(func=lambda call: True)
def handle(call):
    if call.data == 'cat_yes':
        bot.send_photo(call.message.chat.id, cat_status_code())
    if call.data == 'quote_yes':
        bot.send_message(call.message.chat.id, f"{quote_text()}\n{quote_author()}")
    else:
        bot.send_message(call.message.chat.id, 'Вы отказались!')
    bot.answer_callback_query(call.id)


@bot.message_handler(content_types=['text'])
def hello(message):
    bot.send_message(message.chat.id, "Отвечаю на любой текст!")


print("Бот запущен!")
bot.infinity_polling()
