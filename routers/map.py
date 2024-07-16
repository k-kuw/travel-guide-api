from fastapi import APIRouter, Depends, HTTPException, status
from geopy.geocoders import Nominatim
from auth import get_current_user, header_scheme, verify_api_key
from db import schemas
from pydantic import BaseModel

# 位置クラス
class Location(BaseModel):
  name: str

router = APIRouter(
  prefix="/map",
  tags=["map"]
)

# 地点情報取得処置
@router.post("/search-address")
async def search_address(location: Location, user: schemas.User = Depends(get_current_user), api_key: str = Depends(header_scheme)):
  verify_api_key(api_key)
  geo_locator = Nominatim(user_agent="travel-guide")
  location = geo_locator.geocode(location.name)
  # 地点が見つからなかった場合
  if not location:
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Not Found Location")
  else:
    return location.raw
