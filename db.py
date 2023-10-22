import sqlite3


def connection(func):
    def wrapper(*args, **kwargs):
        conn = sqlite3.connect('/home/aboba/intcoin/db_dir/intcoin.db')
        #conn = sqlite3.connect('intcoin.db')
        result = func(conn, *args, **kwargs)
        conn.commit()
        conn.close()
        return result

    return wrapper


def addnew_goods_to_db(conn, goods_item):
    conn.execute('''
                    INSERT INTO goods (goods_hash, goods_category, goods_title, goods_merch_size, goods_count, goods_description, goods_cost, goods_photo)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                ''', (
        goods_item["goods_hash"],
        goods_item["goods_category"],
        goods_item["goods_title"],
        goods_item["goods_merch_size"],
        goods_item["goods_count"],
        goods_item["goods_description"],
        goods_item["goods_cost"],
        goods_item["goods_photo"]
    ))


def addnew_goods_to_unique_db(conn, goods_item, total_count):
    conn.execute('''
                    INSERT INTO unique_goods (goods_hash, goods_category, goods_title, goods_merch_size, goods_count, goods_description, goods_cost, goods_photo)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                ''', (
        goods_item["goods_hash"],
        goods_item["goods_category"],
        goods_item["goods_title"],
        "",
        total_count,
        goods_item["goods_description"],
        goods_item["goods_cost"],
        goods_item["goods_photo"]
    ))


@connection
def admin_addnew_goods(conn, goods_info):
    if type(goods_info) == list:
        for goods_item in goods_info:
            addnew_goods_to_db(conn, goods_item)
    else:
        addnew_goods_to_db(conn, goods_info)


@connection
def admin_addnew_unique_goods(conn, goods_info, total_count):
    if type(goods_info) == list:
        addnew_goods_to_unique_db(conn, goods_info[0], total_count)
    else:
        addnew_goods_to_unique_db(conn, goods_info, total_count)


@connection
def admin_get_orders(conn):
    curs = conn.cursor()
    curs.execute('''
        SELECT orders.id, unique_goods.goods_title, unique_goods.goods_category, orders.size, orders.cost, orders.status
        FROM orders
        INNER JOIN unique_goods ON orders.goods_id = unique_goods.goods_hash
    ''')
    formatted_orders = []
    for row in curs.fetchall():
        order_id, goods_name, goods_category, size, cost, status = row
        status_text = "в процессе" if status == 1 else ("готово" if status == 2 else "")
        size_text = f", Размер: {size}" if size else ""
        formatted_orders.append(
            f"id: {order_id}, Товар: {goods_name}, Категория: {goods_category}{size_text}, Инткоинов потрачено: {cost}, Статус: {status_text}"
        )
    return formatted_orders
