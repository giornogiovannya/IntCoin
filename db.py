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