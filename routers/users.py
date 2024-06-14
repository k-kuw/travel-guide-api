from fastapi import APIRouter
from database import connect_db

router = APIRouter()

@router.get("/users/", tags=["users"])
async def init_users():
  return [{"username": "Rick"}, {"username": "Morty"}]

# ユーザ情報取得処理
def get_user(name):
  sql = "select * from user where name=:name"
  cursor = connect_db()
  res = cursor.execute(sql, {"name": name})
  return res.fetchone()
