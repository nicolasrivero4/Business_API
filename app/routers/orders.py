from fastapi import APIRouter, Depends

from sqlalchemy.orm import Session

from app.database.connection import get_db
from app.dependencies import get_current_user
from app.models.users import User
from app.schemas.orders import OrderCreate, OrderResponse, OrderUpdate
from app.services.orders import OrderService

router = APIRouter()

service = OrderService()

@router.post(
    "/",
    response_model=OrderResponse,
    status_code=201,
    summary="Crear una orden"
)
def order_create(order: OrderCreate, user_id: User = Depends(get_current_user), db: Session = Depends(get_db)):
    return service.order_create(db, user_id, order)

@router.get(
    "/",
    response_model=list[OrderResponse],
    status_code=200,
    summary="Obtener todas las ordenes"
)
def orders_get(_: User = Depends(get_current_user), db: Session = Depends(get_db)):
    return service.orders_get(db)

@router.get(
    "/{order_id}",
    response_model=OrderResponse,
    status_code=200,
    summary="Obtener la order"
)
def order_get(order_id: int, _: User = Depends(get_current_user), db: Session = Depends(get_db)):
    return service.order_get(db, order_id)

@router.put(
    "/",
    status_code=200,
    summary="Actualizar estado de orden"
)
def order_update(order: OrderUpdate, order_id: int, user_id: User = Depends(get_current_user), db: Session = Depends(get_db)):
    return service.order_update(db, order_id, user_id, order)
