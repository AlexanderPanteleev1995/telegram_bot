import sqlite3 as sq

def mate():
    con = sq.connect('bd.db')
    cur = con.cursor()
    if con:
        print('База данных N1 подключена')
    a = cur.execute('SELECT slova FROM mat').fetchall()
    k = []
    for i in a:
        k += i
    return k

