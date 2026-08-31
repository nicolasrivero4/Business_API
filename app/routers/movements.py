from fastapi import APIRouter, Depends

from sqlalchemy.orm import Session

from app.dependencies import require_admin
from app.database.connection import get_db
from app.models.users import User
from app.schemas.movements import MovementCreate, MovementResponse
from app.services.movements import MovementService

router = APIRouter()

service = MovementService()

@router.post(
    "/",
    response_model=MovementResponse,
    status_code=201,
    summary="Agregar movimiento"
)
def movement_create(movement: MovementCreate, user: User = Depends(require_admin), db: Session = Depends(get_db)):
    return service.movement_create(db, movement, user.id)

@router.get(
    "/{movement_id}",
    response_model=MovementResponse,
    status_code=200,
    summary="Consultar movimiento por id de movimiento"
)
def movement_get_by_movement_id(movement_id: int, _: User = Depends(require_admin), db: Session = Depends(get_db)):
    return service.movement_get_by_movement_id(db, movement_id)

@router.get(
    "/user/{user_id}",
    response_model=list[MovementResponse],
    status_code=200,
    summary="Consultar movimiento por id de usuario"
)
def movement_get_by_user_id(user_id: int, _: User = Depends(require_admin), db: Session = Depends(get_db)):
    return service.movement_get_by_user_id(db, user_id)

@router.get(
    "/product/{product_id}",
    response_model=list[MovementResponse],
    status_code=200,
    summary="Consultar moivimientos por id de producto"
)
def movement_get_by_product_id(product_id, _: User = Depends(require_admin), db: Session = Depends(get_db)):
    return service.movement_get_by_product_id(db, product_id)

@router.get(
    "/",
    response_model=list[MovementResponse],
    status_code=200,
    summary="Consultar movimientos"
)
def movements_get(_: User = Depends(require_admin), db: Session = Depends(get_db)):
    return service.movements_get(db)
