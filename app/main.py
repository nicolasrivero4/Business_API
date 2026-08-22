from fastapi import FastAPI

from app.routers.users import router as user_router
from app.routers.login import router as login_router

app = FastAPI()

app.include_router(
    user_router,
    prefix="/user",
    tags=["User"]
)

app.include_router(
    login_router,
    prefix="/login",
    tags=["Login"]
)
