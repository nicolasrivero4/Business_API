from fastapi import APIRouter, Depends

from sqlalchemy.orm import Session

from app.models.users import User
from app.schemas.products import ProductResponse, ProductCreate, ProductUpdate
from app.database.connection import get_db
from app.dependencies import require_admin, get_current_user
from app.services.products import ProductService

router = APIRouter()

service = ProductService()

@router.post(
    "/",
    response_model=ProductResponse,
    status_code=201,
    summary="Crear producto"
)
def product_create(product: ProductCreate, _: User = Depends(require_admin) , db: Session = Depends(get_db)):
    return service.product_create(db, product)

@router.get(
    "/{product_id}",
    response_model=ProductResponse,
    status_code=200,
    summary="Mostrar producto"
)
def product_get(product_id: int, _: User = Depends(get_current_user), db: Session = Depends(get_db)):
    return service.product_get(db, product_id)

@router.get(
    "/",
    response_model=list[ProductResponse],
    status_code=200,
    summary="Mostrar productos"
)
def products_get(_: User = Depends(get_current_user), db: Session = Depends(get_db)):
    return service.products_get(db)

@router.put(
    "/",
    response_model=ProductResponse,
    status_code=200,
    summary="Actualizar producto"
)
def product_update(product_id: int, product: ProductUpdate, _: User = Depends(require_admin), db: Session = Depends(get_db)):
    return service.product_update(db, product, product_id)

@router.delete(
    "/",
    status_code=204,
    summary="Eliminar producto"
)
def product_delete(product_id: int, _: User = Depends(require_admin), db: Session = Depends(get_db)):
    service.product_delete(db, product_id)
