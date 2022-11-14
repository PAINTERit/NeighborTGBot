import telebot
from config import TG_TOKEN
from api import cat_img

bot = telebot.TeleBot(TG_TOKEN)


@bot.message_handler(commands=['cat'])
def hello(message):
    keyboard = telebot.types.InlineKeyboardMarkup()
    button_yes = telebot.types.InlineKeyboardButton('Да', callback_data='cat_yes')
    button_no = telebot.types.InlineKeyboardButton('Нет', callback_data='cat_no')
    keyboard.row(button_yes, button_no)
    bot.send_message(message.chat.id, 'Хотите получить картинку статус кода с котиком?', reply_markup=keyboard)


def send_cat_img(message):
    bot.send_photo(message.chat.id, cat_img)


@bot.message_handler(content_types=['text'])
def hello(message):
    bot.send_message(message.chat.id, 'Отвечаю на любой текст!')


@bot.callback_query_handler(func=lambda call: True)
def handle(call):
    if call.data == 'cat_yes':
        send_cat_img(call.message)
    else:
        bot.send_message(call.message.chat.id, 'Вы отказались!')
    bot.answer_callback_query(call.id)


print("Бот запущен!")
bot.infinity_polling()
