from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
from typing import List
from auth import get_current_user
from database import connect_db
from routers.users import User, get_user_by_name

class Destination(BaseModel):
  id: int
  name: str
  lon: str
  lat: str

class Belongings(BaseModel):
  id: int
  name: str

class Schedule(BaseModel):
  time: str
  place: str
  activity: str
  note: str

class Guide(BaseModel):
  username: str
  title: str
  destinations: List[Destination]
  belongings: List[Belongings]
  schedules: List[Schedule]

router = APIRouter(
  prefix="/guides",
  tags=["guides"]
)

@router.get("/")
async def init_guides():
  return {"guide": "Tokyo"}

# しおり取得処理
@router.get("/search")
async def search_guides(user: User = Depends(get_current_user)):
  user_id = user[0]
  if not user_id:
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Not User Found")
  con = connect_db()
  cursor = con.cursor()
  sql = "select id, title from guide where user_id=:user_id"
  data = {"user_id": user_id}
  result = cursor.execute(sql, data).fetchall()
  guide_list = []
  for guide in result:
    guide_list.append({"id": guide[0], "title": guide[1]})
  return guide_list

# しおり詳細取得処理ret
@router.get("/search/{guide_id}")
async def search_guide(guide_id: int, user: User = Depends(get_current_user)):
  user_id = user[0]
  con = connect_db()
  cursor = con.cursor()
  # しおり情報取得
  sql = "select id, title from guide where id=:guide_id and user_id=:user_id"
  data = {"guide_id": guide_id, "user_id": user_id}
  guide_result = cursor.execute(sql, data).fetchone()
  if not guide_result:
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Not Found Guide")
  # 目的地情報取得
  sql = "select place, lon, lat from destination where guide_id=:guide_id"
  data = {"guide_id": guide_id}
  destinations_result = cursor.execute(sql, data).fetchall()
  destination_list = []
  for destination in destinations_result:
    destination_list.append({"name": destination[0], "lon": destination[1], "lat": destination[2]})
  # 持ち物情報取得
  sql = "select item from belonging where guide_id=:guide_id"
  data = {"guide_id": guide_id}
  belongings_result = cursor.execute(sql, data).fetchall()
  belonging_list = []
  for belonging in belongings_result:
    belonging_list.append({"name": belonging[0]})
  # スケジュール情報取得
  sql = "select time, place, activity, note from schedule where guide_id=:guide_id"
  data = {"guide_id": guide_id}
  schedules_result = cursor.execute(sql, data).fetchall()
  schedule_list = []
  for schedule in schedules_result:
    schedule_list.append({"time": schedule[0], "place": schedule[1], "activity": schedule[2], "note": schedule[3]})

  return {
    "title": guide_result[1], 
    "destinations": destination_list, 
    "belongings": belonging_list,
    "schedules": schedule_list
  }


# しおり登録処理
@router.post("/register")
async def register_guide(guide: Guide, user: User = Depends(get_current_user)):
  if (not guide.title):
    raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Insufficient input")
  result = create_guide(guide)
  if not result:
    raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Guide register error")
  return guide

# しおりDB登録処理
def create_guide(guide):
  print("create title")
  try:
    user_id = get_user_by_name(guide.username)[0]
    # データベース接続
    con = connect_db()
    cursor = con.cursor()
    # しおり登録
    sql = "insert into guide(title, user_id) values(:title, :user_id) returning id"
    data = {"title": guide.title, "user_id": user_id}
    # 登録したしおりのIDを取得
    guide_id = cursor.execute(sql, data).fetchone()[0]
    # 目的地登録
    sql = "insert into destination(guide_id, place, lon, lat) values(:guide_id, :place, :lon, :lat)"
    data = []
    for place in guide.destinations:
      data.append({"guide_id": guide_id, "place": place.name, "lon": place.lon, "lat": place.lat})
    cursor.executemany(sql, data)
    # 持ち物登録
    sql = "insert into belonging(guide_id, item) values(:guide_id, :item)"
    data = []
    for item in guide.belongings:
      data.append({"guide_id": guide_id, "item": item.name})
    cursor.executemany(sql, data)
    # スケジュール登録
    sql = "insert into schedule(guide_id, time, place, activity, note) values(:guide_id, :time, :place, :activity, :note)"
    data = []
    for schedule in guide.schedules:
      data.append({"guide_id": guide_id, "time": schedule.time, "place": schedule.place, "activity": schedule.activity, "note": schedule.note})
    cursor.executemany(sql, data)
    # 登録コミット
    con.commit()
  except Exception as e:
    print(e)
    return False
  return True
