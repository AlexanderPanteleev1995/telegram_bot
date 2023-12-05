from aiogram import types, Dispatcher
from create_bot import dp, bot
from keyboards.client_kb import kb_client, kb_client2
from data_base2 import sqlite_db2
# from data_base3 import sqlite_db3
from keyboards.inline_kb import topUpMenu, buy_menu
from pyqiwip2p import QiwiP2P
import random
from aiogram.dispatcher.filters.state import StatesGroup, State
from aiogram.dispatcher import FSMContext
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


p2p = QiwiP2P(auth_key='', alt="example.com")

# @dp.message_handler(commands=['start'])
async def commands_start(message : types.Message):
    try:
        await bot.send_message(message.from_user.id, 'Приветствую в интернет-магазине кроссовок',reply_markup=kb_client)
        await message.delete()
    except:
        await message.reply('Напиши боту первый\nhttps://t.me/NewSanyaBot')

def is_number(_str):
    try:
        int(_str)
        return True
    except ValueError:
        return False

class Start(StatesGroup):
    start_name = State()
    finish_name = State()
# @dp.message_handler(commands=['Профиль'], state=None)
async def profil(message: types.Message):
    if not await sqlite_db2.user_exist(message.from_user.id):
        await sqlite_db2.add_user(message.from_user.id)
    a = await sqlite_db2.user_money(message.from_user.id)
    await bot.send_message(message.from_user.id, f'Ваш счет: {a} руб.', reply_markup=topUpMenu)
    await Start.start_name.set()

# @dp.message_handler(state=Start.finish_name)
async def bot_mess(message: types.Message, state: FSMContext):
    if message.chat.type == 'private':
        if is_number(message.text):
            message_money = int(message.text)
            if message_money >= 5:
                comment = str(message.from_user.id)+ '_' + str(random.randint(1000, 9999))
                bill = p2p.bill(amount=message_money, lifetime=15, comment=comment)
                await sqlite_db2.add_check(message.from_user.id, message_money, bill.bill_id)
                await bot.send_message(message.from_user.id, f'Вам нужно отправить {message_money} руб. на наш счет Qiwi\nСсылка: {bill.alt_url}\nУкажи комментарий к оплате: {comment}', reply_markup= buy_menu(url=bill.alt_url, bill=bill.bill_id))
            else:
                await bot.send_message(message.from_user.id, 'Минимальная сумма для пополнения 5 руб.')
        else:
            await bot.send_message(message.from_user.id, 'Введите целое число')
    await state.finish()

# @dp.callback_query_handler(text='top_up', state=Start.start_name)
async def top_up(callback: types.CallbackQuery):
    await bot.delete_message(callback.from_user.id, callback.message.message_id)
    await bot.send_message(callback.from_user.id, 'Введите сумму для пополнения!')
    await Start.next()

# @dp.callback_query_handler(text_contains = 'check_')
async def check(callback: types.CallbackQuery):
    bill = str(callback.data[6:])
    info = await sqlite_db2.get_check(bill)
    if info != False:
        if str(p2p.check(bill_id=bill).status) == 'PAID':
            user_money = await sqlite_db2.user_money(callback.from_user.id)
            money = int(info[2])
            await sqlite_db2.set_money(callback.from_user.id, user_money + money)
            await bot.send_message(callback.from_user.id, 'Ваш счет пополнен')
            await sqlite_db2.delete_check(callback.from_user.id)
        else:
            await bot.send_message(callback.from_user.id, 'Вы не оплатили счет!', reply_markup=buy_menu(False, bill=bill))
    else:
        await bot.send_message(callback.from_user.id, 'Счет не найден')

# @dp.message_handler(commands=['Режим_работы'])
async def open(message : types.Message):
    await bot.send_message(message.from_user.id, 'Пн-Пт с 8 до 17, Сб-Вс выходной')

# @dp.message_handler(commands=['Расположение'])
async def rasp(message : types.Message):
    await bot.send_message(message.from_user.id, 'г.Киров, ул.Володарского, д.159')

# @dp.callback_query_handler(lambda x: x.data and x.data.startswith('add '))
async def del_callback_run(callback_query: types.CallbackQuery):
    await sqlite_db2.sql_add_korzina_command(callback_query.data.replace('add ', ''))
    await callback_query.answer(text=f'{callback_query.data.replace("add ", "")} добавлена', show_alert=True)


# @dp.register_message_handler(commands=['Ассортимент'])
async def assort(message : types.Message):
    read = await sqlite_db2.sql_read()
    for ret in read:
        await bot.send_photo(message.from_user.id, ret[1], f'ID:{ret[0]}\nНазвание: {ret[2]}\nРазмер: {ret[3]}\nЦена: {ret[-1]}')
        await bot.send_message(message.from_user.id, text='Добавь в корзину:', reply_markup=InlineKeyboardMarkup(). \
                               add(InlineKeyboardButton(f'В корзину {ret[2]}', callback_data=f'add {ret[0]}')))

# @dp.callback_query_handler(lambda x: x.data and x.data.startswith('del '))
async def del_callback_run2(callback_query: types.CallbackQuery):
    await sqlite_db2.sql_delete_command2(callback_query.data.replace('del ', ''))
    await callback_query.answer(text=f'{callback_query.data.replace("del ", "")} удалена', show_alert=True)

# @dp.register_message_handler(commands=['Корзина'])
async def korzina(message : types.Message):
    await sqlite_db2.sql_read3()
    read = await sqlite_db2.sql_read3()
    for ret in read:
        await bot.send_photo(message.from_user.id, ret[1], f'ID:{ret[0]}\nНазвание: {ret[2]}\nРазмер: {ret[3]}\nЦена: {ret[-1]}', reply_markup=kb_client2)
        await bot.send_message(message.from_user.id, text='Убрать из корзины:', reply_markup=InlineKeyboardMarkup().\
                               add(InlineKeyboardButton(f'Убрать из корзины {ret[2]}', callback_data=f'del {ret[0]}')))

# @dp.register_message_handler(commands=['Купить'])
async def kypit(message : types.Message):
    a = await sqlite_db2.pok1()
    b = await sqlite_db2.pok2()
    if a - b < 0:
        await bot.send_message(message.from_user.id, f'Недостаточно средств')
    else:
        await sqlite_db2.pokyp()
        read = await sqlite_db2.sql_read3()
        for ret in read:
            await bot.send_message(message.from_user.id, f' Поздравляю! Вы купили:\nНазвание: {ret[2]}\nРазмер: {ret[3]}\nЦена: {ret[-1]}\nПокажи это для получения товара в пункте выдачи!', reply_markup=kb_client)
        await sqlite_db2.sql_delete_command3()




def register_handlers_client(dp : Dispatcher):
    dp.register_message_handler(commands_start, commands=['start'])
    dp.register_message_handler(open, lambda message: 'режим' in message.text.lower())
    dp.register_message_handler(rasp, lambda message: 'расположение' in message.text.lower())
    dp.register_callback_query_handler(del_callback_run, lambda x: x.data and x.data.startswith('add '))
    dp.register_message_handler(assort, lambda message: 'ассортимент' in message.text.lower())
    dp.register_message_handler(profil,lambda message: 'профиль' in message.text.lower(), state=None)
    dp.register_callback_query_handler(top_up, text='top_up', state=Start.start_name)
    dp.register_message_handler(bot_mess, state=Start.finish_name)
    dp.register_callback_query_handler(check, text_contains = 'check_')
    dp.register_callback_query_handler(del_callback_run2, lambda x: x.data and x.data.startswith('del '))
    dp.register_message_handler(korzina, lambda message: 'корзина' in message.text.lower())
    dp.register_message_handler(kypit, lambda message: 'купить' in message.text.lower())