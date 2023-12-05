from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
b1 = KeyboardButton('Загрузить')
b2 = KeyboardButton('Удалить')
b3 = KeyboardButton('Отмена')


kb_admin = ReplyKeyboardMarkup(resize_keyboard=True)
kb_admin.add(b1).add(b2).add(b3)
