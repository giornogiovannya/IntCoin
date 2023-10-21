import sqlite3

conn = sqlite3.connect('database.db')
c = conn.cursor()

c.execute('''
    CREATE TABLE if not exists users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nickname TEXT,
        avatar TEXT,
        intcoins INTEGER
    )
''')

c.execute('''
    CREATE TABLE if not exists goods (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        goods_hash TEXT,
        goods_category TEXT,
        goods_title TEXT,
        goods_description TEXT,
        goods_merch_size TEXT,
        goods_count INTEGER,
        goods_photo TEXT,
        goods_cost INTEGER
    )
''')

c.execute('''
    CREATE TABLE if not exists orders (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        goods_id INTEGER,
        date DATETIME,
        status INTEGER
    )
''')

c.execute('''
    CREATE TABLE if not exists tasks (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        task_title TEXT,
        task_category TEXT,
        task_description TEXT,
        task_cost INTEGER
    )
''')

conn.commit()
conn.close()
