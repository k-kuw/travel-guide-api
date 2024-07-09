from pydantic import BaseModel
from typing import List

# Pydanticモデル定義
# ユーザ
class UserBase(BaseModel):
  name: str
  email: str

class UserCreate(UserBase):
  password: str

class User(UserBase): 
  id: int
  
  class Config:
    from_attributes = True

# 目的地
class DestinationBase(BaseModel):
  name: str
  lon: float
  lat: float

class DestinationCreate(DestinationBase):
  pass

class Destination(DestinationBase): 
  id: int
  guide_id: int
  
  class Config:
    from_attributes = True

# 持ち物
class BelongingBase(BaseModel):
  name: str

class BelongingCreate(BelongingBase):
  pass

class Belonging(BelongingBase): 
  id: int
  guide_id: int
  
  class Config:
    from_attributes = True

# スケジュール
class ScheduleBase(BaseModel):
  time: str
  place: str
  activity: str
  note: str

class ScheduleCreate(ScheduleBase):
  pass

class Schedule(ScheduleBase): 
  id: int
  guide_id: int
  
  class Config:
    from_attributes = True

# しおり
class GuideBase(BaseModel):
  title: str

class GuideCreate(GuideBase):
  id: int | None = None
  username: str
  destinations: List[DestinationCreate]
  belongings: List[BelongingCreate]
  schedules: List[ScheduleCreate]

class Guide(GuideBase): 
  id: int
  user_id: int
  
  class Config:
    from_attributes = True

class GuideUpdate(GuideBase):
  id: int
  username: str | None = None
  destinations: List[DestinationCreate] | None = None
  belongings: List[BelongingCreate] | None = None
  schedules: List[ScheduleCreate] | None = None
