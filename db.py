import sqlite3

def connection(func):
    def wrapper(*args, **kwargs):
        conn = sqlite3.connect('intcoin.db')
        result = func(conn, *args, **kwargs)
        conn.commit()
        conn.close()
        return result

    return wrapper

@connection
def selectAll(conn):
    goods = conn.execute("select * from goods")
    return goods.fetchall()

@connection
def selectWithFilter(conn, filter, value):
    goods = conn.execute(f"select * from goods where {filter}='{value}'")
    return goods.fetchall()

@connection
def selectSearch(conn, filter, filterValue, value):
    goods = []
    if (filter != None and filterValue != None):
        print(123)
        goods = conn.execute(f"select * from goods where name like '%{value}%' and {filter}='{filterValue}'")
    else:
        print(456)
        goods = conn.execute(f"select * from goods where name like '%{value}%'")
    return goods.fetchall()

@connection
def addGoods(conn, goods):
    query = """insert into goods (name, price, description, type, img_link) values ("""
    for g in goods:
        if (type(goods[g]) == int):
            query += f"{goods[g]},"
        else:
            query += f"'{goods[g]}',"

    query = query[:-1] + ")"

    print(query)

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

    print(query)

    res = conn.execute(query)
    return res.fetchall()

@connection
def deleteGoods(conn, filters):
    query = "delete from goods where "

    for filter in filters:
        f = filter.split("=")
        print(f)
        query += f"{f[0]}='{f[1]}',"

    query = query[:-1]
    res = conn.execute(query)
    return res.fetchall()