import sqlite3

conn = sqlite3.connect('login.db')
# conn.execute('create table users (ID text, PW text)')
conn.execute('insert into users values (?,?)',('habeen','jih4412'))
conn.commit()
conn.close()