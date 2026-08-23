from fastapi import APIRouter, Depends

from sqlalchemy.orm import Session

from app.schemas.users import UserResponse, UserCreate, UserCreateAdmin, UserUpdate
from app.models.users import User
from app.services.users import UserService
from app.database.connection import get_db
from app.dependencies import get_current_user, require_admin

router = APIRouter()

service = UserService()

@router.post(
    "/employee",
    response_model=UserResponse,
    status_code=201,
    summary="Crear usuario"
)
def user_create_employee(user: UserCreate, db: Session = Depends(get_db)):
    return service.user_create(db, user)

@router.post(
    "/admin",
    response_model=UserResponse,
    status_code=201,
    summary="Crear usuario(Solo para admin)"
)
def user_create_admin(user: UserCreateAdmin, _: User = Depends(require_admin), db: Session = Depends(get_db)):
    return service.user_create(db, user)

@router.get(
    "/me",
    response_model=UserResponse,
    status_code=200,
    summary="Devolver usuario"
)
def user_get(current_user_id: int = Depends(get_current_user), db: Session = Depends(get_db)):
    return service.user_get(db, current_user_id)

@router.get(
    "/",
    response_model=list[UserResponse],
    status_code=200,
    summary="Devolver todos los usuarios"
)
def users_get(_: User = Depends(require_admin), db: Session = Depends(get_db)):
    return service.users_get(db)

@router.put(
    "/",
    response_model=UserResponse,
    status_code=200,
    summary="Modificar usuario"
)
def user_update(user: UserUpdate, current_user_id: int = Depends(get_current_user), db: Session = Depends(get_db)):
    return service.user_update(db, user, current_user_id)

@router.delete(
    "/me",
    status_code=204,
    summary="Eliminar usuario"
)
def user_delete(current_user_id: int = Depends(get_current_user), db: Session = Depends(get_db)):
    service.user_delete(db, current_user_id)

@router.delete(
    "/admin",
    status_code=204,
    summary="Eliminar usuario(Solo para admin)",
    description="Ingrese el id de la cuenta a eliminar"
)
def user_delete_admin(user_id: int, _: User = Depends(require_admin), db: Session = Depends(get_db)):
    service.user_delete(db, user_id)
