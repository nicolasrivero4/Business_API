from fastapi import HTTPException

from sqlalchemy import select
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from app.models.products import Product
from app.models.movements import Movement, MovementType
from app.core.logger import logger

class MovementService:

    def _modify_stock(self, db: Session, product_id, movement_type, quantity):
        statement = select(Product).where(Product.id == product_id)
        result = db.execute(statement)
        
        product = result.scalar_one_or_none()
        
        if not product:
            raise HTTPException(
                status_code=404,
                detail="Producto no encontrado"
            )
        
        if movement_type == MovementType.IN:
            product.stock += quantity

        elif movement_type == MovementType.OUT:
            if product.stock >= quantity:
                product.stock -= quantity
            else:
                raise HTTPException(
                    status_code=400,
                    detail="Stock insuficiente"
                )
            
    def movement_create(self, db: Session, movement, current_user_id):
        try:
            new_movement = Movement(
                product_id = movement.product_id,
                type = movement.type,
                quantity = movement.quantity,
                detail = movement.detail,
                user_id = current_user_id,
                movement_date = movement.movement_date
            )
            self._modify_stock(db, movement.product_id, movement.type, movement.quantity)
            db.add(new_movement)
            db.commit()
            db.refresh(new_movement)

            logger.info("Se agrego un nuevo movimiento. ID: %s", new_movement.id)

            return new_movement

        except IntegrityError:
            db.rollback()

            logger.warning("Se intento crear un movimiento invalido")

            raise HTTPException(
                status_code=400,
                detail="No se pudo crear el movimiento"
            )

    def movement_get_by_movement_id(self, db: Session, movement_id):
        statement = select(Movement).where(Movement.id == movement_id)
        result = db.execute(statement)

        movement = result.scalar_one_or_none()

        if not movement:
            raise HTTPException(
                status_code=404,
                detail="Movimiento no encontrado"
            )

        return movement

    def movement_get_by_user_id(self, db: Session, user_id):
        statement = select(Movement).where(Movement.user_id == user_id)
        result = db.execute(statement)
    
        movement = result.scalars().all()
    
        if not movement:
            raise HTTPException(
                status_code=404,
                detail="Movimiento no encontrado"
            )
        return movement

    def movement_get_by_product_id(self, db: Session, product_id):
        statement = select(Movement).where(Movement.product_id == product_id)
        result = db.execute(statement)
    
        movement = result.scalars().all()
    
        if not movement:
            raise HTTPException(
                status_code=404,
                detail="Movimiento no encontrado"
            )
    
        return movement

    def movements_get(self, db: Session):
        statement = select(Movement)
        result = db.execute(statement)

        movements = result.scalars().all()

        if not movements:
            raise HTTPException(
                status_code=404,
                detail="Movimiento no encontrado"
            )

        return movements
