from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
from typing import List
from auth import get_current_user, header_scheme, verify_api_key
from routers.users import get_user_by_name
from db.database import get_db
from db import models, schemas
from sqlalchemy.orm import Session

# 目的地クラス
class Destination(BaseModel):
  id: int
  name: str
  lon: str
  lat: str

# 持ち物クラス
class Belongings(BaseModel):
  id: int
  name: str

# スケジュールクラス
class Schedule(BaseModel):
  time: str
  place: str
  activity: str
  note: str


router = APIRouter(
  prefix="/guides",
  tags=["guides"]
)

# しおり取得処理
@router.get("/search", response_model=List[schemas.Guide])
async def search_guides(user: schemas.User = Depends(get_current_user), api_key: str = Depends(header_scheme), db: Session = Depends(get_db)):
  verify_api_key(api_key)
  # ユーザがDBに存在しない場合
  if not user.id:
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Not User Found")
  # DB情報取得
  return db.query(models.Guide).filter(models.Guide.user_id == user.id).all()

# しおり詳細取得処理
@router.get("/search/{guide_id}")
async def search_guide(guide_id: int, user: schemas.User = Depends(get_current_user), api_key: str = Depends(header_scheme), db: Session = Depends(get_db)):
  verify_api_key(api_key)
  # しおり情報取得
  guide_result = db.query(models.Guide).filter(models.Guide.id == guide_id, models.Guide.user_id == user.id).first()
  # しおり情報が取得できなかった場合
  if not guide_result:
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Not Found Guide")
  # しおり情報が取得できた場合
  else:
    return {
      "title": guide_result.title, 
      "destinations": guide_result.destinations, 
      "belongings": guide_result.belongings,
      "schedules": guide_result.schedules
    }

# しおり登録処理
@router.post("/register")
async def register_guide(guide: schemas.GuideCreate, user: schemas.User = Depends(get_current_user), api_key: str = Depends(header_scheme), db: Session = Depends(get_db)):
  verify_api_key(api_key)
  # タイトル入力内容がなかった場合
  if (not guide.title):
    raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Insufficient input")
  
  user = get_user_by_name(db, guide.username)
  # ユーザが見つからなかった場合
  if not user:
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Not Found User")
  
  # しおり登録
  db_guide = models.Guide(title=guide.title, user_id=user.id)
  db.add(db_guide)
  # しおりを登録し、しおりIDをdb_guideに格納
  db.commit()
  db.refresh(db_guide)

  # 目的地登録
  destinations = []
  for place in guide.destinations:
    destinations.append(models.Destination(name=place.name, lat=place.lat, lon=place.lon, guide_id=db_guide.id))
  db.add_all(destinations)
  
  # 持ち物登録
  belongings = []
  for item in guide.belongings:
    belongings.append(models.Belonging(name=item.name, guide_id=db_guide.id))
  db.add_all(belongings)

  # スケジュール登録
  schedules = []
  for schedule in guide.schedules:
    schedules.append(models.Schedule(time=schedule.time, place=schedule.place, activity=schedule.activity, note=schedule.note, guide_id=db_guide.id))
  db.add_all(schedules)

  # 登録コミット
  db.commit()
  return {"ok": True}

# しおり更新処理
@router.put("/update")
async def update_guide(guide: schemas.GuideUpdate, user: schemas.User = Depends(get_current_user), api_key: str = Depends(header_scheme), db: Session = Depends(get_db)):
  verify_api_key(api_key)
  # タイトル入力内容がなかった場合
  if (not guide.title):
    raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Insufficient input")
  
  user = get_user_by_name(db, guide.username)
  # ユーザが見つからなかった場合
  if not user:
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Not Found User")

  # DBのしおり情報取得
  db_guide = db.get(models.Guide, guide.id)
  if not db_guide:
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Not Found Guide")
  
  # しおり更新
  db_guide.title = guide.title
  db.add(db_guide)

  # 目的地更新
  prev_destinations = db.query(models.Destination).filter(models.Destination.guide_id == guide.id).all()
  for prev_destination in prev_destinations:
    db.delete(prev_destination)
  new_destinations = []
  for place in guide.destinations:
    new_destinations.append(models.Destination(name=place.name, lat=place.lat, lon=place.lon, guide_id=guide.id))
  db.add_all(new_destinations)

  # 持ち物更新
  prev_belongings = db.query(models.Belonging).filter(models.Belonging.guide_id == guide.id).all()
  for prev_belonging in prev_belongings:
    db.delete(prev_belonging)
  new_belongings = []
  for item in guide.belongings:
    new_belongings.append(models.Belonging(name=item.name, guide_id=guide.id))
  db.add_all(new_belongings)

  # スケジュール更新
  prev_schedules = db.query(models.Schedule).filter(models.Schedule.guide_id == guide.id).all()
  for prev_schedule in prev_schedules:
    db.delete(prev_schedule)
  new_schedules = []
  for schedule in guide.schedules:
    new_schedules.append(models.Schedule(time=schedule.time, place=schedule.place, activity=schedule.activity, note=schedule.note, guide_id=guide.id))
  db.add_all(new_schedules)

  db.commit()
  return {"ok": True}

# しおり削除処理
@router.delete("/delete/{guide_id}")
async def delete_guide(guide_id: int, user: schemas.User = Depends(get_current_user), api_key: str = Depends(header_scheme), db: Session = Depends(get_db)):
  verify_api_key(api_key)
  guide = db.get(models.Guide, guide_id)
  if not guide:
    raise HTTPException(status_code=404, detail="Guide not found")
  db.delete(guide)
  db.commit()
  return {"ok": True}
