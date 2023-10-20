import sqlite3

con = sqlite3.connect("intcoin.db")
cursor = con.cursor()

cursor.execute("""create table if not exists goods (
            id serial primary key,
            name varchar, 
            price integer, 
            description varchar, 
            type varchar
            )""")

