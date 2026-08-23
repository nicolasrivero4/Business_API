from fastapi import HTTPException

from sqlalchemy import select
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from app.models.categories import Category
from app.core.logger import logger

class CategoryService:

    def category_create(self, db: Session, category):
        try:
            new_category = Category(
                name = category.name,
                description = category.description
            )
            db.add(new_category)
            db.commit()
            db.refresh(new_category)

            logger.info("Categoria creada correctamente. ID: %s", new_category.id)

            return new_category

        except IntegrityError:
            db.rollback()

            logger.warning("Se intento crear una categoria repetida. Nombre: %s", category.name)

            raise HTTPException(
                status_code=400,
                detail="Nombre invalido"
            )

    def category_get(self, db: Session, category_id):
        statement = select(Category).where(Category.id == category_id)
        result = db.execute(statement)

        category = result.scalar_one_or_none()

        if not category:

            raise HTTPException(
                status_code=404,
                detail="Categoria no encontrada"
            )

        return category

    def categories_get(self, db:Session):
        statement = select(Category)
        result = db.execute(statement)

        categories = result.scalars().all()

        if not categories:
            raise HTTPException(
                status_code=404,
                detail="Categorias no encontradas"
            )

        return categories

    def category_udpate(self, db: Session, category, category_id):
        statement = select(Category).where(Category.id == category_id)
        result = db.execute(statement)

        category_upd = result.scalar_one_or_none()

        if not category_upd:
            raise HTTPException(
                status_code=404,
                detail="Categoria no encontrada"
            )

        try:
            category_upd.name = category.name
            category_upd.description = category.description

            db.commit()
            db.refresh(category_upd)

            logger.info("Se actualizo la categoria. ID: %s", category_upd.id)

            return category_upd

        except IntegrityError:
            db.rollback()

            raise HTTPException(
                status_code=400,
                detail="Ya existe una categoria con ese nombre"
            )

    def category_delete(self, db: Session, category_id):
        statement = select(Category).where(Category.id == category_id)
        result = db.execute(statement)

        category = result.scalar_one_or_none()

        if not category:
            raise HTTPException(
                status_code=404,
                detail="Categoria no encontrada"
            )

        db.delete(category)
        db.commit()

        logger.info("Se elimino una categoria. ID: %s", category.id)
    