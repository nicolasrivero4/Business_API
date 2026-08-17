from fastapi import APIRouter, Depends

from sqlalchemy.orm import Session

from app.schemas.users import UsersResponse, UsersCreate
from app.services.users import UserService
from app.database.connection import get_db

router = APIRouter()

service = UserService()

@router.post(
    "/",
    status_code=201,
    summary="Crear usuario"
)
def user_create(user: UsersCreate, db: Session = Depends(get_db)):
    return service.user_create(db, user)

@router.get(
    "/",
    response_model=UsersResponse,
    status_code=200,
    summary="Devolver usuarios"
)
def user_get(user_id: int, db: Session = Depends(get_db)):
    return service.user_get(db, user_id)
