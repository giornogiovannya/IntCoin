import sqlite3, config
from datetime import datetime

def connection(func):
    def wrapper(*args, **kwargs):
        conn = sqlite3.connect(config.db)
        result = func(conn, *args, **kwargs)
        conn.commit()
        conn.close()
        return result

    return wrapper

@connection
def select_user(conn, user_id):
    users = conn.execute(f"select * from users where user_id={user_id}")
    return users.fetchall()

@connection
def add_user(conn, user):
    query = """insert into users (
                user_id, 
                nickname, 
                avatar, 
                intcoins) values ("""
    for u in user:
        if (type(user[u]) == int):
            query += f"{user[u]},"
        else:
            query += f"'{user[u]}',"

    query = query[:-1] + ")"

    return conn.execute(query).fetchall()

@connection
def select_all_tasks(conn):
    tasks = conn.execute("select * from tasks")
    return tasks.fetchall()

@connection
def select_tasks_with_filter(conn, filter, value):
    tasks = conn.execute(f"select * from tasks where {filter}='{value}'")
    return tasks.fetchall()

@connection
def select_tasks_with_search(conn, filter, filterValue, value):
    tasks = []
    if (filter != None and filterValue != None):
        tasks = conn.execute(f"select * from tasks where name like '%{value}%' and {filter}='{filterValue}'")
    else:
        tasks = conn.execute(f"select * from tasks where name like '%{value}%'")
    return tasks.fetchall()

@connection
def add_tasks(conn, tasks):
    query = """insert into tasks (
                task_title, 
                task_category, 
                task_description, 
                task_cost) values ("""
    for t in tasks:
        if (type(tasks[t]) == int):
            query += f"{tasks[t]},"
        else:
            query += f"'{tasks[t]}',"

    query = query[:-1] + ")"

    return conn.execute(query).fetchall()

@connection
def update_tasks(conn, updates, filters):
    query = "update tasks set "

    for update in updates:
        query += f"{update}='{updates[update]}',"

    query = query[:-1]

    query += " where"

    for filter in filters:
        if (type(filters[filter]) == int):
            query += f" {filter}={filters[filter]} and"
        else:
            query += f" {filter}='{filters[filter]}' and"

    query = query.rsplit(' ', 1)[0]

    res = conn.execute(query)
    return res.fetchall()

@connection
def delete_tasks(conn, filters):
    query = "delete from tasks where "

    for filter in filters:
        f = filter.split("=")
        query += f"{f[0]}='{f[1]}',"

    query = query[:-1]
    res = conn.execute(query)
    return res.fetchall()
@connection
def selectAll(conn):
    goods = conn.execute("select * from goods")
    return goods.fetchall()

@connection
def selectWithFilter(conn, filter, value):
    if (type(value) == int):
        goods = conn.execute(f"select * from goods where {filter}={value}")
    else:
        goods = conn.execute(f"select * from goods where {filter}='{value}'")
    return goods.fetchall()

@connection
def selectSearch(conn, filter, filterValue, value):
    goods = []
    if (filter != None and filterValue != None):
        goods = conn.execute(f"select * from goods where name like '%{value}%' and {filter}='{filterValue}'")
    else:
        goods = conn.execute(f"select * from goods where name like '%{value}%'")
    return goods.fetchall()

@connection
def addGoods(conn, goods):
    query = """insert into goods (
                goods_hash, 
                goods_category, 
                goods_title, 
                goods_description,
                goods_merch_size, 
                goods_count, 
                goods_photo, 
                goods_cost 
                ) values ("""
    for g in goods:
        if (type(goods[g]) == int):
            query += f"{goods[g]},"
        else:
            query += f"'{goods[g]}',"

    query = query[:-1] + ")"

    return conn.execute(query).fetchall()

@connection
def updateGoods(conn, updates, filters):
    query = "update goods set "

    for update in updates:
        query += f"{update}='{updates[update]}',"

    query = query[:-1]

    query += " where"

    for filter in filters:
        if (type(filters[filter]) == int):
            query += f" {filter}={filters[filter]} and"
        else:
            query += f" {filter}='{filters[filter]}' and"

    query = query.rsplit(' ', 1)[0]

    res = conn.execute(query)
    return res.fetchall()

@connection
def deleteGoods(conn, filters):
    query = "delete from goods where "

    for filter in filters:
        f = filter.split("=")
        query += f"{f[0]}='{f[1]}',"

    query = query[:-1]
    res = conn.execute(query)
    return res.fetchall()

@connection
def add_order(conn, data):
    conn.execute("SELECT * FROM goods WHERE goods_hash = ? AND goods_merch_size = ?", (data['goods_hash'], data["size"],))
    conn.execute(f"UPDATE goods SET goods_count = goods_count - 1 WHERE goods_hash = ? AND goods_merch_size = ?", (data['goods_hash'], data["size"],) )
    current_datetime = datetime.now()
    conn.execute("UPDATE users SET intcoins = intcoins - ? WHERE user_id = ?", (data['cost'], data['user_id'],))
    res = conn.execute("INSERT INTO orders (user_id, goods_id, size, cost, date, status) VALUES (?, ?, ?, ?, ?, ?)", (data['user_id'],data['goods_hash'],data['size'],data['cost'],current_datetime,1,))
    return res