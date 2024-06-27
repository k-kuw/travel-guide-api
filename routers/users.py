from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel
from passlib.context import CryptContext
from database import connect_db

# ユーザクラス
class User(BaseModel):
    username: str
    email: str
    password: str

router = APIRouter(
  prefix="/users",
  tags=["users"]
)

# ユーザDB登録処理
@router.post("/register")
async def register_user(user: User):
  try: 
    if(not user.username or not user.email or not user.password):
      raise Exception("Insufficient input")
    if(len(user.password) <= 4):
      raise Exception("Password needs more than 5 characters")
    # パスワードのハッシュ化
    hashed_password = get_password_hash(user.password)
    # ユーザ登録
    con = connect_db()
    cursor = con.cursor()
    sql = "insert into user(name, email, password) values(:name, :email, :password) returning name"
    data = {"name": user.username, "email": user.email, "password": hashed_password}
    res = cursor.execute(sql, data).fetchone()[0]
    con.commit()
  except Exception as e:
    # 入力内容が不十分な場合
    if("Insufficient" in e.args[0]):
      raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="insufficient input")
    # パスワードの入力文字数が不足していた場合
    elif("Password" in e.args[0]):
      raise HTTPException(status_code=status.HTTP_411_LENGTH_REQUIRED, detail="password needs more than 5 characters")
    # ユーザ名が既に使用されている場合
    elif("UNIQUE" in e.args[0]):
      raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="already used that name")
    # その他例外発生時
    else:
      raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="user register error") 
  return get_user_by_name(res)

# パスワードハッシュ化処理
def get_password_hash(password):
  pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
  return pwd_context.hash(password)

# ユーザ情報取得処理
def get_user_by_name(name):
  con = connect_db()
  cursor = con.cursor()
  sql = "select * from user where name=:name"
  res = cursor.execute(sql, {"name": name})
  return res.fetchone()

def get_user_by_id(id):
  con = connect_db()
  cursor = con.cursor()
  sql = "select * from user where id=:id"
  res = cursor.execute(sql, {"id": id})
  return res.fetchone()
