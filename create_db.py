import sqlite3

conn = sqlite3.connect("users.db")
cur = conn.cursor()
print("connected to db file")

sqlcommand = """CREATE TABLE userdata (
uid INTEGER PRIMARY KEY,
gender CHAR(1),
premium CHAR(1),
preference CHAR(1),
matches INTEGER,
joining DATE);"""

cur.execute(sqlcommand)
print("table created")

conn.close()