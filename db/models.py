from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, Float
from sqlalchemy.orm import relationship
from .database import Base

# SQLAlchemyモデル定義

# ユーザテーブル
class User(Base):
  __tablename__ = "users"

  id = Column(Integer, primary_key =True)
  name = Column(String, unique=True, index=True)
  email = Column(String)
  hashed_password = Column(String)

  guides = relationship("Guide", back_populates="user")

# しおりテーブル
class Guide(Base):
  __tablename__ = "guides"

  id = Column(Integer, primary_key =True)
  title = Column(String)
  user_id = Column(Integer, ForeignKey("users.id"))

  user = relationship("User", back_populates="guides")
  destinations = relationship("Destination", back_populates="guide")
  belongings = relationship("Belonging", back_populates="guide")
  schedules = relationship("Schedule", back_populates="guide")

# 目的地テーブル
class Destination(Base): 
  __tablename__ = "destinations"
  
  id = Column(Integer, primary_key =True)
  name = Column(String)
  lon = Column(Float)
  lat = Column(Float)
  guide_id = Column(Integer, ForeignKey("guides.id"))

  guide = relationship("Guide", back_populates="destinations")

# 持ち物テーブル
class Belonging(Base): 
  __tablename__ = "belongings"
  id = Column(Integer, primary_key =True)
  name = Column(String)
  guide_id = Column(Integer, ForeignKey("guides.id"))

  guide = relationship("Guide", back_populates="belongings")

# スケジュールテーブル
class Schedule(Base): 
  __tablename__ = "schedules"
  id = Column(Integer, primary_key =True)
  time = Column(String)
  place = Column(String)
  activity = Column(String)
  note = Column(String)
  guide_id = Column(Integer, ForeignKey("guides.id"))

  guide = relationship("Guide", back_populates="schedules")



  
