# DB構築用ファイル

import sqlite3

def connect_db():
  con = sqlite3.connect("travel_guide.db", check_same_thread=False)
  return con.cursor()

# cur.execute("CREATE TABLE user(id, name, email)")

# res = cur.execute("ALTER TABLE user ADD password")

# sql = "insert into user(name, email, password) values(?, ?, ?)"
# data = [('旅栞', 'tabi@example.com', 'tabi'), ('塩栞', 'shio@example.com', 'shio')]
# cur.executemany(sql, data)
# sql = "update user set password='$2b$12$Ii/fMuCx40PJyBINu1Tm0uVoTk9iXtOn/1UiT8fiKC3WMrevkoMfu' where password='shio'"
# cur.execute(sql)
# con.commit()

# res = cur.execute("SELECT name FROM user")
