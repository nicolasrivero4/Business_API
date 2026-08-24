from fastapi import FastAPI

from app.routers.users import router as user_router
from app.routers.login import router as login_router
from app.routers.categories import router as category_router
from app.routers.products import router as product_router

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

app.include_router(
    category_router,
    prefix="/category",
    tags=["Category"]
)

app.include_router(
    product_router,
    prefix="/product",
    tags=["Product"]
)
