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

API_TOKEN = os.environ["TELEGRAM_API_TOKEN"]
bot = Bot(token=API_TOKEN, parse_mode=None)
dp = Dispatcher(bot)


@dp.message_handler(commands=['start', 'help'])
async def send_welcome(message: types.Message):
    """Отправляет приветственное сообщение и помощь по боту"""
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    buttons = ["Вывести курс Биткоина", "Вывести курс Эфириума"]
    keyboard.add(*buttons)
    await message.answer(
        "Привет!\n"
        "Могу показать тебе курс Биткоина и Эфириума на сегодняшний день\n",
        reply_markup=keyboard)
    

@dp.message_handler()
async def get_btc_eth_button_or_text_input_to_bot(message: types.Message):
    """Отправляет стоимость Эфира/Биткоина"""
    if message.text == "Вывести курс Биткоина":
        URL = 'https://www.google.ru/search?q=%D0%BA%D1%83%D1%80%D1%81+%D0%B1%D0%B8%D1%82%D0%BA%D0%BE%D0%B8%D0%BD%D0%B0+%D0%B2+%D0%B4%D0%BE%D0%BB%D0%BB%D0%B0%D1%80%D0%B0%D1%85&newwindow=1&sxsrf=APq-WBtBdKqkQi92if7GFoNVLmsBj0YTIw%3A1646135033894&ei=-QYeYuCbNvaGwPAP5_m82AM&oq=%D0%BA%D1%83%D1%80%D1%81+%D0%B1%D0%B8%D1%82%D0%BA%D0%BE%D0%B8%D0%BD%D0%B0+&gs_lcp=Cgdnd3Mtd2l6EAMYADIFCAAQgAQyBQgAEIAEMgsIABCABBCxAxCDATIFCAAQgAQyCwgAEIAEELEDEIMBMgsIABCABBCxAxCDATILCAAQgAQQsQMQgwEyBQgAEIAEMgUIABCABDIICAAQgAQQyQM6BwgAEEcQsAM6CggAEEcQsAMQyQM6BwgAELADEEM6EgguEMcBEKMCEMgDELADEEMYADoSCC4QxwEQ0QMQyAMQsAMQQxgASgUIPBIBMUoECEEYAEoECEYYAFD8B1j8B2CrF2gBcAF4AIABWYgBWZIBATGYAQCgAQHIAQ3AAQHaAQQIABgI&sclient=gws-wiz'
        HEADERS = {'user-agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:96.0) Gecko/20100101 Firefox/96.0', 'accept': 'application/json, text/javascript, */*; q=0.01'}
        html = requests.get(URL, headers=HEADERS)
        soup = BeautifulSoup(html.text, 'html.parser')
        btc_price = soup.findAll('span', class_='pclqee')
        for bt_price in btc_price:
            btc_price = bt_price
        await message.answer(f"Bitcoin: {btc_price.text}USD")
        
    if message.text == "Вывести курс Эфириума":
        URL = 'https://www.google.ru/search?q=%D0%BA%D1%83%D1%80%D1%81+%D1%8D%D1%84%D0%B8%D1%80%D0%B0+%D0%B2+%D0%B4%D0%BE%D0%BB%D0%BB%D0%B0%D1%80%D0%B0%D1%85&newwindow=1&sxsrf=APq-WBs4fiPng3SDNz21RPbRiLlkONm25g%3A1646135709828&ei=nQkeYveRMujrrgTloLSoDA&ved=0ahUKEwi31PGx7aT2AhXotYsKHWUQDcUQ4dUDCA0&uact=5&oq=%D0%BA%D1%83%D1%80%D1%81+%D1%8D%D1%84%D0%B8%D1%80%D0%B0+%D0%B2+%D0%B4%D0%BE%D0%BB%D0%BB%D0%B0%D1%80%D0%B0%D1%85&gs_lcp=Cgdnd3Mtd2l6EAMyBQgAEIAEMgUIABCABDIFCAAQgAQyBQgAEIAEMgUIABCABDIGCAAQBxAeOgcIIxCwAxAnOgcIABBHELADOgoIABBHELADEMkDOgcIABCwAxBDOhIILhDHARCjAhDIAxCwAxBDGAA6EgguEMcBENEDEMgDELADEEMYADoFCAAQxAI6CAgAEAgQBxAeSgUIPBIBMUoECEEYAEoECEYYAVCPBFiqF2DDHGgBcAF4AIABaYgBrwWSAQMzLjSYAQCgAQHIARHAAQHaAQYIABABGAg&sclient=gws-wiz'
        HEADERS = {'user-agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:96.0) Gecko/20100101 Firefox/96.0', 'accept': 'application/json, text/javascript, */*; q=0.01'}
        html = requests.get(URL, headers=HEADERS)
        soup = BeautifulSoup(html.text, 'html.parser')
        eth_price = soup.findAll('span', class_='pclqee')
        for et_price in eth_price:
            eth_price = et_price
        await message.answer(f"Ethereum: {eth_price.text}USD")
    
    if message.text != "Вывести курс Биткоина" and message.text != "Вывести курс Эфириума":
        """Обработчик некорректных сообщений пользователя"""
        await message.answer("Я вас не понимаю .. :(")


        
if __name__ == '__main__':
        executor.start_polling(dp)
