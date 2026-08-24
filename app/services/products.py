from fastapi import HTTPException

from sqlalchemy import select
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from app.models.products import Product
from app.models.categories import Category
from app.core.logger import logger

class ProductService:

    def _category_get(self, db: Session, category_id):
        statement = select(Category).where(Category.id == category_id)
        result = db.execute(statement)

        category = result.scalar_one_or_none()

        if not category:
            raise HTTPException(
                status_code=404,
                detail="Categoria no encontrada"
            )

    def product_create(self, db: Session, product):

        self._category_get(db, product.category_id)
        
        try:
            new_product = Product(
                name = product.name,
                description = product.description,
                price = product.price,
                category_id = product.category_id
            )
            db.add(new_product)
            db.commit()
            db.refresh(new_product)

            logger.info("Se agrego un nuevo producto. ID: %s", new_product.id)

            return new_product

        except IntegrityError:
            db.rollback()

            logger.warning("Se intento crear un producto repetido. Nombre: %s", product.name)

            raise HTTPException(
                status_code=400,
                detail="Nombre invalido"
            )

    def product_get(self, db: Session, product_id):
        statement = select(Product).where(Product.id == product_id)
        result = db.execute(statement)

        product = result.scalar_one_or_none()

        if not product:
            raise HTTPException(
                status_code=404,
                detail="Producto no encontrado"
            )

        return product

    def products_get(self, db: Session):
        statement = select(Product)
        result = db.execute(statement)

        products = result.scalars().all()

        if not products:
            raise HTTPException(
                status_code=404,
                detail="Productos no encontrados"
            )

        return products

    def product_update(self, db: Session, product, product_id):

        self._category_get(db, product.category_id)

        statement = select(Product).where(Product.id == product_id)
        result = db.execute(statement)

        product_upd = result.scalar_one_or_none()

        if not product_upd:
            raise HTTPException(
                status_code=404,
                detail="Producto no encontrado"
            )

        try:
            product_upd.name = product.name
            product_upd.description = product.description
            product_upd.price = product.price
            product_upd.category_id = product.category_id

            db.commit()
            db.refresh(product_upd)

            logger.info("Se actualizo el producto. ID: %s", product_upd.id)

            return product_upd

        except IntegrityError:
            db.rollback()

            logger.warning("Se intento utilizar el nombre de un producto existente. Nombre: %s", product.name)

            raise HTTPException(
                status_code=400,
                detail="Nombre invalido"
            )

    def product_delete(self, db: Session, product_id):
        statement = select(Product).where(Product.id == product_id)
        result = db.execute(statement)

        product = result.scalar_one_or_none()

        if not product:
            raise HTTPException(
                status_code=404,
                detail="Producto no encontrado"
            )

        db.delete(product)
        db.commit()

        logger.info("Producto eliminado. ID: %s", product_id)
        