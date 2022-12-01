import random

CAT_URL = "https://http.cat/"
CAT_LIST = [100, 101, 102, 200, 201, 202, 204, 205, 206, 207,
            300, 301, 302, 303, 304, 305, 307, 308, 400, 401,
            402, 403, 404, 405, 406, 407, 408, 409, 410, 411,
            412, 413, 414, 415, 416, 417, 418, 420, 421, 422,
            423, 424, 425, 426, 429, 431, 444, 450, 451, 497,
            498, 499, 500, 501, 502, 503, 504, 506, 507, 508,
            509, 510, 511, 521, 522, 523, 525, 599]

QUESTION_URL = "https://yesno.wtf/api"

photo_src = "user_images/"

QUOTE_URL = "http://api.forismatic.com/api/1.0/"
QUOTE_PARAMS = {
    "method": "getQuote",
    "format": "json",
    "key": random.randint(1, 999999),
    "lang": "ru",
}

NEWS_URL = "https://ria.ru/world/"
