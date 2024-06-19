from fastapi import APIRouter, Depends, HTTPException
from geopy.geocoders import Nominatim

from auth import get_current_user
from routers.users import User
from pydantic import BaseModel

class Location(BaseModel):
  name: str

router = APIRouter(
  prefix="/map",
  tags=["map"]
)

@router.post("/search-address")
async def search_address(location: Location, user: User = Depends(get_current_user)):
  geolocator = Nominatim(user_agent="travel-guide")
  location = geolocator.geocode(location.name)
  if not location:
    raise HTTPException(status_code=400, detail="Not Found Location")
  else:
    return location.raw
