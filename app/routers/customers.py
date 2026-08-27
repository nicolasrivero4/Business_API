from fastapi import APIRouter, Depends

from sqlalchemy.orm import Session

from app.schemas.customers import CustomerCreate, CustomerResponse, CustomerUpdate
from app.models.users import User
from app.dependencies import get_current_user
from app.database.connection import get_db
from app.services.customers import CustomerService

router = APIRouter()

service = CustomerService()

@router.post(
    "/",
    response_model=CustomerResponse,
    status_code=201,
    summary="Crear cuenta de cliente"
)
def customer_create(customer: CustomerCreate, user_id: User = Depends(get_current_user), db: Session = Depends(get_db)):
    return service.customer_create(db, user_id, customer)

@router.get(
    "/{customer_id}",
    response_model=CustomerResponse,
    status_code=200,
    summary="Devolver datos de cliente"
)
def customer_get(customer_id: int , _: User = Depends(get_current_user), db: Session = Depends(get_db)):
    return service.customer_get(db, customer_id)

@router.get(
    "/",
    response_model=list[CustomerResponse],
    status_code=200,
    summary="Devolver datos de los clientes"
)
def customers_get(_: User = Depends(get_current_user), db: Session = Depends(get_db)):
    return service.customers_get(db)

@router.put(
    "/",
    response_model=CustomerResponse,
    status_code=200,
    summary="Actualizar datos de usuario"
)
def customer_update(customer: CustomerUpdate, customer_id: int, user_id: User = Depends(get_current_user), db: Session = Depends(get_db)):
    return service.customer_update(db, user_id, customer_id, customer)

@router.delete(
    "/",
    status_code=204,
    summary="Eliminar cliente"
)
def customer_delete(customer_id: int, user_id: User = Depends(get_current_user), db: Session = Depends(get_db)):
    service.customer_delete(db, user_id, customer_id)
