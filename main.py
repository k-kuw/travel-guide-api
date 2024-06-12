from fastapi import FastAPI
from routers import users, guides

app = FastAPI()

app.include_router(users.router)
app.include_router(guides.router)

@app.get("/")
def read_root():
    return {"Hello": "World"}
