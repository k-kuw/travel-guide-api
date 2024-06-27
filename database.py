# DB構築用ファイル

import sqlite3

def connect_db():
  con = sqlite3.connect("travel_guide.db", check_same_thread=False)
  return con

con = sqlite3.connect("travel_guide.db", check_same_thread=False)
cur = con.cursor()

# cur.execute("delete from user where id=5")
# cur.execute("delete from guide")
# cur.execute("delete from destination")
# cur.execute("delete from belonging")
# cur.execute("delete from schedule")

# cur.execute("DROP TABLE guide")
# cur.execute("DROP TABLE destination")
# cur.execute("DROP TABLE belonging")
# cur.execute("DROP TABLE schedule")

# cur.execute("CREATE TABLE guide(id integer primary key autoincrement, title, user_id)")
# cur.execute("CREATE TABLE destination(id integer primary key autoincrement, guide_id, place)")
# cur.execute("CREATE TABLE belonging(id integer primary key autoincrement, guide_id, item)")
# cur.execute("CREATE TABLE schedule(id integer primary key autoincrement, guide_id, time, place, activity, note)")
# cur.execute("CREATE TABLE new_user(id integer primary key autoincrement, name text not null, email text not null, password text not null)")
# cur.execute("CREATE TABLE new_user(id integer primary key autoincrement, name text unique, email text not null, password text not null)")
# cur.execute("drop table new_user")


# cur.execute("insert into new_user select * from user")
# cur.execute("drop table user")
# cur.execute("alter table new_user rename to user")
# cur.execute('insert into user(name, email, password) values("旅", "", "")')

# sql = "insert into user(name, email, password) values(?, ?, ?)"
# data = [('旅栞', 'tabi@example.com', '$2b$12$QdST9d/V9JObamcsCLDeMOQ1v5RGtooJBHSVaOXjqzK130cJBhYRq'), ('塩栞', 'shio@example.com', '$2b$12$Ii/fMuCx40PJyBINu1Tm0uVoTk9iXtOn/1UiT8fiKC3WMrevkoMfu')]
# cur.executemany(sql, data)
# con.commit()

# cur.execute("alter table destination add lon")
# cur.execute("alter table destination add lat")

# res = cur.execute("SELECT name FROM user")

con.commit()

cur.close()
con.close()
