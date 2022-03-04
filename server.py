"""Сервер Telegram бота, запускаемый непосредственно"""
import os
import logging
from aiogram import Bot, Dispatcher, executor, types
import requests
from bs4 import BeautifulSoup
from aiogram.types import ReplyKeyboardRemove, \
    ReplyKeyboardMarkup, KeyboardButton, \
    InlineKeyboardMarkup, InlineKeyboardButton


logging.basicConfig(level=logging.INFO)
#API_TOKEN = os.environ["TELEGRAM_API_TOKEN"]
API_TOKEN = "5176489970:AAGc_b8KRthxbU460_73EdkUBcX-7AZZxI4"
bot = Bot(token=API_TOKEN, parse_mode=None)
dp = Dispatcher(bot)


async def get_headers():
    """Функция, возвращающая headers для request-запроса"""
    headers = {"user-agent": "Mozilla/5.0 (X11; Linux x86_64; rv:96.0) Gecko/20100101 Firefox/96.0", "accept": "application/json, text/javascript, */*; q=0.01"}
    return headers 


async def get_url(crypto_name):
    """Функция автоматического определения нужного URL по каждой отдельно взятой монете"""
    urls = f"https://www.google.ru/search?q=курс+{crypto_name}а+в+долларах"
    return urls


async def get_soup(URL, HEADERS):
    """Получаем html-страничку, получаем объект супа"""
    html = requests.get(URL, headers=HEADERS)
    soup = BeautifulSoup(html.text, 'html.parser')
    return soup


async def get_price(soup):
    """Парсим полученный объект, находим нужную строчку цены"""
    crypto_price = soup.findAll('span', class_='pclqee')
    [crypto_price for price in crypto_price]
    return crypto_price[0]


async def go_crypto(name_of_crypto: str):
    """Автоматизация запуска для каждой отдельно взятой монеты \
        На Вход функция ожидает аргумент формата строки \
        (сокращенное название криптомонеты, которое есть в словаре с готовыми URL для запроса в Гугл) \
        Возвращает переменную price, содержащую цену для данной криптовалюты \
        Перед выводом извлечь из текст из price -> price.text"""
    URL = await get_url(name_of_crypto)
    HEADERS = await get_headers()
    soup = await get_soup(URL, HEADERS)
    price = await get_price(soup)
    return price 


@dp.message_handler(commands=['start', 'help'])
async def send_welcome(message: types.Message):
    """Отправляет приветственное сообщение и помощь по боту"""
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    buttons = ["Вывести курс Биткоина", "Вывести курс Эфириума", "Вывести курс Дэша"]
    keyboard.add(*buttons)
    await message.answer(
        "Привет, я Konvik ❤️\n\n"
        "Могу показать тебе курс интересующих тебя криптовалют на сегодняшний день 🌍\n\n\n"
        "Просто выбери нужную кнопку, с нужной тебе криптовалютой 💬 ⬇",
        reply_markup=keyboard)
    

@dp.message_handler()
async def get_btc_eth_button_or_text_input_to_bot(message: types.Message):
    """Отправляет котировку криптоваюты"""
    try:
        await get_url(message["text"].split(" ")[2][0:-1])
        crypto_name = message["text"].split(" ")[2][0:-1]
        price = await go_crypto(crypto_name)
        await message.answer(f"{crypto_name}: {price.text}USD")
    except: await message.answer("Я вас не понимаю 😓")
    
    
if __name__ == '__main__':
        executor.start_polling(dp)
