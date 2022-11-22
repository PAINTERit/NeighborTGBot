import random
import requests
from bs4 import BeautifulSoup
from config import cat_list, QUOTE_URL, QUOTE_PARAMS, NEWS_URL, NEWS_HEADERS
from PIL import Image, ImageFont, ImageDraw


def cat_status_code():
    return f'https://http.cat/{random.choice(cat_list)}.jpg'


def quote_text():
    return requests.get(QUOTE_URL, params=QUOTE_PARAMS).json()['quoteText'.strip()]


def quote_author():
    return requests.get(QUOTE_URL, params=QUOTE_PARAMS).json()['quoteAuthor']


def yes_no_maybe():
    return requests.get('https://yesno.wtf/api').json()['image']


def last_news():
    response = requests.get(NEWS_URL, headers=NEWS_HEADERS)
    soup = BeautifulSoup(response.text, 'lxml')
    news = soup.find('a', class_='list-item__title color-font-hover-only').text
    link = soup.find('a', class_='list-item__title color-font-hover-only').get('href')
    return f'{news}\nСсылка: {link}'


def create_meme(photo, text):
    image = Image.open(photo)

    font = ImageFont.truetype("C:/Windows/Fonts/cour.ttf", 30)
    drawer = ImageDraw.Draw(image)
    drawer.text((100, 100), text, font=font, fill='white')

    image.save('meme_image.jpg')
    return image
