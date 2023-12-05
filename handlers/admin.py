from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram import types, Dispatcher
from create_bot import dp, bot
from aiogram.dispatcher.filters import Text
from data_base2 import sqlite_db2
from keyboards.admin_kb import kb_admin
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

ID = None

class FSMAdmin(StatesGroup):
    photo = State()
    name = State()
    size = State()
    price = State()

# @dp.register_message_handler(commands='модератор', is_chat_admin = True)
async def make_changes_command(message : types.Message):
    global ID
    ID = message.from_user.id
    await bot.send_message(message.from_user.id, 'Вы администратор, выполните действия', reply_markup=kb_admin)
    await message.delete()

# @dp.message_handler(commands=['Загрузить'], state = None)
async def cm_start(message : types.Message):
    if message.from_user.id == ID:
        await FSMAdmin.photo.set()
        await message.reply('Загрузи фото')

# @dp.register_message_handler(state="*", commands=['Отмена'])
# @dp.register_message_handler(Text(equals=['Отмена'], ignore_case=True), state="*")
async def cancel(message : types.Message, state : FSMContext):
    if message.from_user.id == ID:
        current_state = await state.get_state()
        if current_state is None:
            return
        await state.finish()
        await message.reply('Ок')

# @dp.message_handler(content_types=['photo'], state=FSMAdmin.photo)
async def load_photo(message : types.Message, state:FSMContext):
    if message.from_user.id == ID:
        async with state.proxy() as data:
            data['photo'] = message.photo[0].file_id
        await FSMAdmin.next()
        await message.reply('Введи название')

# @dp.message_handler(state=FSMAdmin.name)
async def load_name(message : types.Message, state:FSMContext):
    if message.from_user.id == ID:
        async with state.proxy() as data:
            data['name'] = message.text
        await FSMAdmin.next()
        await message.reply('Теперь введи размер')

# @dp.message_handler(state=FSMAdmin.size)
async def load_size(message : types.Message, state:FSMContext):
    if message.from_user.id == ID:
        async with state.proxy() as data:
            data['size'] = message.text
        await FSMAdmin.next()
        await message.reply('Укажи цену')

# @dp.message_handler(state=FSMAdmin.price)
async def load_price(message : types.Message, state:FSMContext):
    if message.from_user.id == ID:
        async with state.proxy() as data:
            data['price'] = message.text
        await sqlite_db2.sql_add_command(state)
        await state.finish()

# @dp.callback_query_handler(lambda x: x.data and x.data.startswith('del '))
async def del_callback_run(callback_query: types.CallbackQuery):
    await sqlite_db2.sql_delete_command(callback_query.data.replace('del ', ''))
    await callback_query.answer(text=f'{callback_query.data.replace("del ", "")} удалена', show_alert=True)

# @dp.message_handler(commands=['Удалить'])
async def delete_item(message:types.Message):
    if message.from_user.id == ID:
        read = await sqlite_db2.sql_read2()
        for ret in read:
            await bot.send_photo(message.from_user.id, ret[0], f'{ret[1]}\nОписание: {ret[2]}\nЦена: {ret[-1]}')
            await bot.send_message(message.from_user.id,text='Удали товар:', reply_markup= InlineKeyboardMarkup().\
                add(InlineKeyboardButton(f'Удалить {ret[1]}', callback_data=f'del {ret[1]}')))


def register_handlers_admin(dp : Dispatcher):
    dp.register_message_handler(make_changes_command,lambda message: 'модератор' in message.text.lower(), is_chat_admin = True)
    dp.register_message_handler(cm_start,lambda message: 'загрузить' in message.text.lower(), state = None)
    dp.register_callback_query_handler(del_callback_run, lambda x: x.data and x.data.startswith('del '))
    dp.register_message_handler(delete_item, lambda message: 'удалить' in message.text.lower())
    dp.register_message_handler(cancel, state="*", commands=['отмена'])
    dp.register_message_handler(cancel, Text(equals='отмена', ignore_case=True), state="*")
    dp.register_message_handler(load_photo,content_types=['photo'], state=FSMAdmin.photo)
    dp.register_message_handler(load_name,state=FSMAdmin.name)
    dp.register_message_handler(load_size, state=FSMAdmin.size)
    dp.register_message_handler(load_price,state=FSMAdmin.price)




