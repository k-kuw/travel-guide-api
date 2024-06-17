from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List
from database import connect_db

class Destination(BaseModel):
  id: int
  name: str
class Belongings(BaseModel):
  id: int
  name: str
class Schedule(BaseModel):
  time: str
  place: str
  activity: str
  note: str

class Guide(BaseModel):
  user_id: int
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

# しおり登録処理
@router.post("/register")
async def regist_guide(guide: Guide):
  result = create_guide(guide)
  if not result:
    raise HTTPException(status_code=400, detail="Guide regist error")
  return guide

# しおりDB登録処理
def create_guide(guide):
  print("create title")
  try:
    # データベース接続
    con = connect_db()
    cursor = con.cursor()
    # しおり登録
    sql = "insert into guide(title, user_id) values(?,?) returning id"
    data = (guide.title, guide.user_id)
    # 登録したしおりのIDを取得
    guide_id = cursor.execute(sql, data).fetchone()[0]
    # 目的地登録
    # TODO 緯度経度追加予定
    sql = "insert into destination(guide_id, place) values(?,?)"
    data = []
    for place in guide.destinations:
      data.append((guide_id, place.name))
    cursor.executemany(sql, data)
    # 持ち物登録
    sql = "insert into belonging(guide_id, item) values(?,?)"
    data = []
    for item in guide.belongings:
      data.append((guide_id, item.name))
    cursor.executemany(sql, data)
    # スケジュール登録
    sql = "insert into schedule(guide_id, time, place, activity, note) values(?,?,?,?,?)"
    data = []
    for schedule in guide.schedules:
      data.append((guide_id, schedule.time, schedule.place, schedule.activity, schedule.note))
    cursor.executemany(sql, data)
    # 登録コミット
    con.commit()
  except Exception as e:
    print(e)
    return False
  return True
