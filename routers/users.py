from fastapi import APIRouter, Depends, HTTPException, status
from passlib.context import CryptContext
from db.database import get_db
from db import models, schemas
from sqlalchemy.orm import Session
from config import settings
from fastapi.security import APIKeyHeader


router = APIRouter(
  prefix="/users",
  tags=["users"]
)

header_scheme = APIKeyHeader(name="x-api-key")

# apiキー認証処理
def verify_api_key(api_key):
    if api_key != settings.api_key:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Invalid API Key"
        )
    return

# ユーザDB登録処理
@router.post("/register", response_model=schemas.User)
async def register_user(user: schemas.UserCreate, api_key: str = Depends(header_scheme), db: Session = Depends(get_db)):
  verify_api_key(api_key)
  try: 
    if(not user.name or not user.email or not user.password):
      raise Exception("Insufficient input")
    if(len(user.password) <= 4):
      raise Exception("Password needs more than 5 characters")
    # パスワードのハッシュ化
    hashed_password = get_password_hash(user.password)
    # ユーザ登録
    db_user = models.User(name=user.name, email=user.email, hashed_password=hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user
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

# パスワードハッシュ化処理
def get_password_hash(password):
  pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
  return pwd_context.hash(password)

# ユーザ情報取得処理
def get_user_by_name(db: Session, name: str):
  return db.query(models.User).filter(models.User.name == name).first()

def get_user_by_id(db: Session, id: int):
  return db.query(models.User).filter(models.User.id == id).first()
