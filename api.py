import random
import requests
from config import cat_list, QUOTE_URL, QUOTE_PARAMS


def cat_status_code():
    return f'https://http.cat/{random.choice(cat_list)}.jpg'


def quote_text():
    return requests.get(QUOTE_URL, params=QUOTE_PARAMS).json()['quoteText'.strip()]


def quote_author():
    return requests.get(QUOTE_URL, params=QUOTE_PARAMS).json()['quoteAuthor']


def yes_no_maybe():
    return requests.get('https://yesno.wtf/api').json()['image']
