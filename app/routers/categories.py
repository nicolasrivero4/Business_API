from fastapi import APIRouter, Depends

from sqlalchemy.orm import Session

from app.models.users import User
from app.schemas.categories import CategoryCreate, CategoryResponse, CategoryUpdate
from app.services.categories import CategoryService
from app.database.connection import get_db
from app.dependencies import require_admin

router = APIRouter()

service = CategoryService()

@router.post(
    "/",
    response_model=CategoryResponse,
    status_code=201,
    summary="Agregar categoria"
)
def category_create(category: CategoryCreate, _: User = Depends(require_admin), db: Session = Depends(get_db)):
    return service.category_create(db, category)

@router.get(
    "/{category_id}",
    response_model=CategoryResponse,
    status_code=200,
    summary="Consultar categoria"
)
def category_get(category_id: int, db: Session = Depends(get_db)):
    return service.category_get(db, category_id)

@router.get(
    "/",
    response_model=list[CategoryResponse],
    status_code=200,
    summary="Consultar todas las categorias"
)
def categories_get(db: Session = Depends(get_db)):
    return service.categories_get(db)

@router.put(
    "/",
    response_model=CategoryResponse,
    status_code=200,
    summary="Actualizar categoria"
)
def category_update(category: CategoryUpdate, category_id: int, _: User = Depends(require_admin), db: Session = Depends(get_db)):
    return service.category_udpate(db, category, category_id)

@router.delete(
    "/",
    status_code=204,
    summary="Eliminar categoria"
)
def category_delete(category_id: int, _: User = Depends(require_admin), db: Session = Depends(get_db)):
    service.category_delete(db, category_id)
