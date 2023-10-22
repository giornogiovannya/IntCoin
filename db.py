import sqlite3

DEFAULT_AVATAR = "default_avatar.jpg"


def connection(func):
    def wrapper(*args, **kwargs):
        conn = sqlite3.connect('/home/aboba/intcoin/db_dir/intcoin.db')
        result = func(conn, *args, **kwargs)
        conn.commit()
        conn.close()
        return result

    return wrapper


@connection
def goods_get_nickname(conn, user_id):
    curs = conn.execute("SELECT nickname FROM users WHERE user_id=?", (user_id,))
    user_instance = curs.fetchone()
    return user_instance[0]


@connection
def goods_set_nickname(conn, nickname, user_id):
    conn.execute("UPDATE users SET nickname = ? WHERE user_id = ?", (nickname, user_id))



@connection
def goods_get_avatar(conn, user_id):
    curs = conn.execute("SELECT avatar FROM users WHERE user_id=?", (user_id,))
    user_instance = curs.fetchone()
    return user_instance[0]


@connection
def goods_set_avatar(conn, user_avatar_filename, user_id):
    conn.execute("UPDATE users SET avatar = ? WHERE user_id = ?", (user_avatar_filename, user_id))


@connection
def goods_get_intcoins(conn, user_id):
    curs = conn.execute("SELECT intcoins FROM users WHERE user_id=?", (user_id,))
    user_instance = curs.fetchone()
    return user_instance[0]


@connection
def goods_get_last_trades(conn, user_id):
    return "Список последних обменов коинами пуст"


@connection
def goods_new_user_first_time(conn, user_id, default_nickname):
    curs = conn.cursor()
    curs.execute("SELECT * FROM users WHERE user_id=?", (user_id,))
    existing_user = curs.fetchone()
    if existing_user is None:
        curs.execute("INSERT INTO users (user_id, nickname, avatar, intcoins) VALUES (?, ?, ?, ?)",
                     (user_id, default_nickname, DEFAULT_AVATAR, 1000))
