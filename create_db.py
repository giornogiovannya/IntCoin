import sqlite3

conn = sqlite3.connect('intcoin.db')
c = conn.cursor()

c.execute('''
    CREATE TABLE users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        nickname TEXT,
        avatar TEXT,
        intcoins INTEGER
    )
''')

c.execute('''
    CREATE TABLE goods (
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
    CREATE TABLE unique_goods (
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
    CREATE TABLE orders (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        goods_id INTEGER,
        size TEXT,
        cost INTEGER,
        date DATETIME,
        status INTEGER
    )
''')

c.execute('''
    CREATE TABLE tasks (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        task_title TEXT,
        task_category TEXT,
        task_description TEXT,
        task_cost INTEGER,
        task_status integer
    )
''')

c.execute('''
    CREATE TABLE history (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        from_user_id INTEGER,
        to_user_id INTEGER,
        cost INTEGER,
        date DATETIME
    )
''')

conn.commit()
conn.close()
