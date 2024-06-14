from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List
from database import connect_db

class Schedule(BaseModel):
  time: str
  place: str
  activity_content: str
  note: str

class Guide(BaseModel):
  title: str
  destinations: List[str]
  belongings: List[str]
  schedules: List[Schedule]


router = APIRouter(
  prefix="/guides",
  tags=["guides"]
)

@router.get("/")
async def init_guides():
  return {"guide": "Tokyo"}

@router.post("/register")
async def regist_guide(guide: Guide):
  result = create_guide(guide)
  if not result:
    raise HTTPException(status_code=400, detail="Guide regist error")
  return guide

def create_guide(guide):
  print("create title")
  try:
    cursor = connect_db()
    
  except:
    return False
  return True
