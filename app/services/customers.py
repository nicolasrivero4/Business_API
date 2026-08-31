from fastapi import HTTPException

from sqlalchemy import select
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from app.models.customers import Customer
from app.core.logger import logger

class CustomerService:
    def customer_create(self, db: Session, user_id, customer):
        try:
            new_customer = Customer(
                name = customer.name,
                email = customer.email,
                phone = customer.phone
            )
            db.add(new_customer)
            db.commit()
            db.refresh(new_customer)

            logger.info("El usuario %s creo un nuevo cliente. ID: %s", user_id, new_customer.id)

            return new_customer
        
        except IntegrityError:
            db.rollback()

            raise HTTPException(
                status_code=400,
                detail="No se pudo crear el cliente"
            )

    def customer_get(self, db: Session, customer_id):
        statement = select(Customer).where(Customer.id == customer_id)
        result = db.execute(statement)

        customer = result.scalar_one_or_none()

        if not customer:
            raise HTTPException(
                status_code=404,
                detail="Cliente no encontrado"
            )

        return customer

    def customers_get(self, db: Session):
        statement = select(Customer)
        result = db.execute(statement)

        customers = result.scalars().all()

        if not customers:
            raise HTTPException(
                status_code=404,
                detail="Cliente no encontrado"
            )

        return customers

    def customer_update(self, db: Session, user_id, customer_id, customer):
        statement = select(Customer).where(Customer.id == customer_id)
        result = db.execute(statement)

        customer_upd = result.scalar_one_or_none()

        if not customer_upd:
            raise HTTPException(
                status_code=404,
                detail="Cliente no encontrado"
            )

        try:
            customer_upd.name = customer.name
            customer_upd.email = customer.email
            customer_upd.phone = customer.phone

            db.commit()
            db.refresh(customer_upd)

            logger.info("El usuario %s actualizo los datos del cliente. ID: %s", user_id, customer_upd.id)

            return customer_upd

        except IntegrityError:
            db.rollback()

            raise HTTPException(
                status_code=400,
                detail="No se pudo actualizar los datos del cliente"
            )

    def customer_delete(self, db: Session, user_id, customer_id):
        statement = select(Customer).where(Customer.id == customer_id)
        result = db.execute(statement)

        customer = result.scalar_one_or_none()

        if not customer:
            raise HTTPException(
                status_code=404,
                detail="Cliente no encontrado"
            )

        db.delete(customer)
        db.commit()

        logger.info("El usuario %s elimino al cliente. ID: %s", user_id, customer_id)
        