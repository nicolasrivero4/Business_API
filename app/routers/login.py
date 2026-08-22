from fastapi import APIRouter, Depends

from sqlalchemy.orm import Session

from app.schemas.login import UserLogin
from app.services.login import LoginService
from app.database.connection import get_db

router = APIRouter()

service = LoginService()

@router.post(
    "/",
    status_code=200,
    summary="Iniciar sesion"
)
def user_login(user: UserLogin, db: Session = Depends(get_db)):
    return service.login(db, user)
