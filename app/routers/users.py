from fastapi import APIRouter, Depends

from sqlalchemy.orm import Session

from app.schemas.users import UserResponse, UserCreate, UserUpdate
from app.services.users import UserService
from app.database.connection import get_db
from app.dependencies import get_current_user

router = APIRouter()

service = UserService()

@router.post(
    "/",
    status_code=201,
    summary="Crear usuario"
)
def user_create(user: UserCreate, db: Session = Depends(get_db)):
    return service.user_create(db, user)

@router.get(
    "/me",
    response_model=UserResponse,
    status_code=200,
    summary="Devolver usuario"
)
def user_get(current_user_id: int = Depends(get_current_user), db: Session = Depends(get_db)):
    return service.user_get(db, current_user_id)

@router.put(
    "/",
    response_model=UserResponse,
    status_code=200,
    summary="Modificar usuario"
)
def user_update(user: UserUpdate, current_user_id: int = Depends(get_current_user), db: Session = Depends(get_db)):
    return service.user_update(db, user, current_user_id)

@router.delete(
    "/",
    status_code=204,
    summary="Eliminar usuario"
)
def user_delete(current_user_id: int = Depends(get_current_user), db: Session = Depends(get_db)):
    service.user_delete(db, current_user_id)
