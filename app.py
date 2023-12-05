from aiogram.utils import executor
from create_bot import dp
from data_base2 import sqlite_db2
from data_base import sqlite_db
from aiogram import types
from create_bot import dp, bot


async def on_startup(_):
    print('Бот онлайн')
    sqlite_db.mate()
    sqlite_db2.sql_start()


from handlers import client, admin, other

client.register_handlers_client(dp)
admin.register_handlers_admin(dp)
other.register_handlers_other(dp)



executor.start_polling(dp, skip_updates=True, on_startup=on_startup)