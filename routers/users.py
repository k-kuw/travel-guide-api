from fastapi import APIRouter, HTTPException, status
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
  print("register user")
  hashed_password = get_password_hash(user.password)

  # データベース接続
  try: 
    if(not user.username or not user.email or not user.password):
      raise Exception("Insufficient input")
    con = connect_db()
    cursor = con.cursor()
    sql = "insert into user(name, email, password) values(:name, :email, :password) returning name"
    data = {"name": user.username, "email": user.email, "password": hashed_password}
    res = cursor.execute(sql, data).fetchone()[0]
    con.commit()
  except Exception as e:
    print(e)
    if("Insufficient" in e.args[0]):
      raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="insufficient input")
    elif("UNIQUE" in e.args[0]):
      raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="already used that name")
    else:
      raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="user register error") 
  return get_user_by_name(res)

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
