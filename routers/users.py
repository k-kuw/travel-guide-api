from fastapi import APIRouter
from pydantic import BaseModel
from passlib.context import CryptContext
from database import connect_db

class User(BaseModel):
    username: str
    email: str
    password: str

router = APIRouter(
  prefix="/users",
  tags=["users"]
)

# ユーザ登録処理
@router.post("/register")
async def register_user(user: User):
  print("regist user")
  hashed_password = get_password_hash(user.password)
  # データベース接続
  con = connect_db()
  cursor = con.cursor()
  sql = "insert into user(name, email, password) values(:name, :email, :password)"
  data = {"name": user.username, "email": user.email, "password": hashed_password}
  res = cursor.execute(sql, data)
  con.commit()
  return get_user_by_name(user.username)

# パスワードハッシュ化処理
def get_password_hash(password):
  pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
  return pwd_context.hash(password)

# ユーザ情報取得処理
def get_user_by_name(name):
  # データベース接続
  con = connect_db()
  cursor = con.cursor()
  sql = "select * from user where name=:name"
  res = cursor.execute(sql, {"name": name})
  return res.fetchone()

def get_user_by_id(id):
  # データベース接続
  con = connect_db()
  cursor = con.cursor()
  sql = "select * from user where id=:id"
  res = cursor.execute(sql, {"id": id})
  return res.fetchone()
