import sqlite3

con = sqlite3.connect("travel_guide.db")

cur = con.cursor()

# cur.execute("CREATE TABLE user(id, name, email)")

res = cur.execute("SELECT name FROM sqlite_master")
print(res.fetchone())
