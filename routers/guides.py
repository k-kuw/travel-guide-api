from fastapi import APIRouter

router = APIRouter(
  prefix="/guides",
  tags=["guides"]
)

@router.get("/")
async def init_guides():
  return {"guide": "Tokyo"}
