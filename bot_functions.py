import random

import requests
from bs4 import BeautifulSoup
from PIL import Image, ImageDraw, ImageFont

from config import CAT_LIST, NEWS_HEADERS, NEWS_URL, QUOTE_PARAMS, QUOTE_URL


def get_cat_status_code() -> str:
    """
    Функция для выдачи картинки.
    :return: str
    """
    return f"https://http.cat/{random.choice(CAT_LIST)}.jpg"


def get_quote_text() -> str:
    """
    Функция для выдачи текста цитаты.
    :return: str
    """
    return requests.get(QUOTE_URL, params=QUOTE_PARAMS).json()["quoteText".strip()]


def get_quote_author() -> str:
    """
    Функция для выдачи автора цитаты.
    :return: str
    """
    return requests.get(QUOTE_URL, params=QUOTE_PARAMS).json()["quoteAuthor"]


def get_answer() -> str:
    """
    Функция которая выдает ответ-gif.
    :return: str
    """
    return requests.get("https://yesno.wtf/api").json()["image"]


def get_last_new() -> str:
    """
    Функция, которая выдает последнюю новость и ссылку на нее.
    :return: str
    """
    response = requests.get(NEWS_URL, headers=NEWS_HEADERS)
    soup = BeautifulSoup(response.text, "lxml")
    news = soup.find("a", class_="list-item__title color-font-hover-only").text
    link = soup.find("a", class_="list-item__title color-font-hover-only").get("href")
    return f"{news}\nСсылка: {link}"


def create_meme(photo, text) -> Image:
    """
    Функция, которая создает мем и возвращает картинку.
    :param photo: str
    :param text: str
    :return: Image
    """
    image = Image.open(photo)

    font = ImageFont.truetype("C:/Windows/Fonts/cour.ttf", 30)
    drawer = ImageDraw.Draw(image)
    drawer.text((100, 100), text, font=font, fill="white")

    image.save("meme_image.jpg")
    return image
