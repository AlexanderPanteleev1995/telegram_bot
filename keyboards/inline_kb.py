from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

btnTopUp = InlineKeyboardButton(text='Пополнить', callback_data='top_up')
topUpMenu = InlineKeyboardMarkup(row_width=1)
topUpMenu.insert(btnTopUp)

def buy_menu(isUrl = True, url = '', bill =''):
    qiwiMenu = InlineKeyboardMarkup(row_width=1)
    if isUrl:
        btnUrlQiwi = InlineKeyboardButton(text='Ссылка на оплату', url=url)
        qiwiMenu.insert(btnUrlQiwi)

    btnCheckQIWI = InlineKeyboardButton(text ='Проверить оплату', callback_data='check_' + bill)
    qiwiMenu.insert(btnCheckQIWI)
    return qiwiMenu