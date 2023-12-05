import sqlite3 as sq
from create_bot import bot

def sql_start():
    global con, cur
    con = sq.connect('assort.db')
    cur = con.cursor()
    if con:
        print('База данных N2 подключена')
    cur.execute('CREATE TABLE IF NOT EXISTS assort(id INTEGER PRIMARY KEY AUTOINCREMENT, img TEXT, name TEXT, size INTEGER, price INTEGER)')
    cur.execute('CREATE TABLE IF NOT EXISTS korzina(id INTEGER, img TEXT, name TEXT, size INTEGER, price INTEGER, user_id INTEGER)')
    cur.execute('CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY AUTOINCREMENT, user_id INTEGER NOT NULL, money INTEGER NOT NULL DEFAULT 0)')
    cur.execute('CREATE TABLE IF NOT EXISTS ololo (id INTEGER PRIMARY KEY AUTOINCREMENT, user_id INTEGER NOT NULL, money INTEGER NOT NULL, bill_id INTEGER NOT NULL)')
    con.commit()

async def sql_add_command(state):
    async with state.proxy() as data:
        cur.execute('INSERT INTO assort (img, name, size, price) VALUES (?, ?, ?, ?)', tuple(data.values()))
        con.commit()

async def sql_read():
    return cur.execute('SELECT * FROM assort').fetchall()


# async def sql_read2():
#     return cur.execute('SELECT * FROM assort').fetchall()

async def sql_delete_command(data):
    cur.execute('DELETE FROM assort WHERE id == ?', (data,))
    con.commit()

async def sql_read3():
    return cur.execute('SELECT * FROM korzina').fetchall()

async def pokyp():
    cur.execute('UPDATE users SET money = money - SUM(korzina.price) FROM korzina')
    con.commit()

async def pok1():
    return cur.execute('SELECT money FROM users').fetchone()[0]

async def pok2():
    return cur.execute('SELECT SUM(price) FROM korzina').fetchone()[0]

async def sql_add_korzina_command(data):
    cur.execute('INSERT INTO korzina(id, img, name, size, price) SELECT id, img, name, size, price FROM assort WHERE id == ?', (data,))
    con.commit()


async def sql_delete_command2(data):
    cur.execute('DELETE FROM korzina WHERE id == ?', (data,))
    con.commit()

async def sql_delete_command3():
    cur.execute('DELETE FROM korzina')
    con.commit()

async def user_exist(user_id):
    with con:
        result = cur.execute('SELECT * FROM users WHERE user_id = ?', (user_id,)).fetchall()
        return bool(len(result))

async def add_user(user_id):
    with con:
        return cur.execute('INSERT INTO users(user_id) VALUES (?)', (user_id,))

async def user_money(user_id):
    with con:
        result = cur.execute('SELECT money FROM users WHERE user_id = ?', (user_id,)).fetchmany(1)
        return int(result[0][0])

async def set_money(user_id, money):
    with con:
        return cur.execute('UPDATE users SET money = ? WHERE user_id = ?', (money, user_id))

async def add_check(user_id, money, bill_id):
    with con:
        cur.execute('INSERT INTO ololo (user_id, money, bill_id) VALUES(?,?,?)', (user_id, money, bill_id,))

async def get_check(bill_id):
    with con:
        result = cur.execute('SELECT * FROM ololo WHERE bill_id = ?', (bill_id,)).fetchmany(1)
        if not bool(len(result)):
            return False
        return True

async def delete_check(bill_id):
    with con:
        return cur.execute('DELETE FROM ololo WHERE bill_id = ?', (bill_id,))


