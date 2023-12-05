from aiogram import types, Dispatcher
from create_bot import dp
from data_base import sqlite_db

# @dp.message_handler()
async def mat(message:types.Message):
    text = ''.join(filter(str.isalpha, message.text.lower()))
    if text in sqlite_db.mate():
        await message.reply('Маты запрещены')
        await message.delete()
    else:
        await message.answer('Нет такой команды')
        await message.delete()


def register_handlers_other(dp : Dispatcher):
    dp.register_message_handler(mat)
