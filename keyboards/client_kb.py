from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
b1 = KeyboardButton('Режим работы')
b2 = KeyboardButton('Расположение')
b3 = KeyboardButton('Ассортимент')
b4 = KeyboardButton('Профиль')
b5 = KeyboardButton('Корзина')
b6 = KeyboardButton('Купить')

kb_client = ReplyKeyboardMarkup(resize_keyboard=True)
kb_client.add(b1).add(b2).add(b3).add(b4).insert(b5)

kb_client2 = ReplyKeyboardMarkup(resize_keyboard=True)
kb_client2.add(b6)