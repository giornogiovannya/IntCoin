import sqlite3

def connection(func):
    def wrapper(*args, **kwargs):
        connection = sqlite3.connect('intcoin.db')
        result = func(connection, *args, **kwargs)
        connection.commit()
        connection.close()
        return result

    return wrapper

@connection
def selectAll(connection):
    goods = connection.execute("select * from goods")
    print(goods)
    return goods