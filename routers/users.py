from fastapi import APIRouter, Depends, HTTPException, status
from db.database import get_db
from db import models, schemas
from sqlalchemy.orm import Session
from auth import header_scheme, verify_api_key, get_password_hash

router = APIRouter(
  prefix="/users",
  tags=["users"]
)

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
