from fastapi import HTTPException
from decimal import Decimal
from datetime import datetime

from sqlalchemy import select
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from app.models.orders import Order, OrderStatus
from app.models.order_items import OrderItem
from app.models.products import Product
from app.models.movements import Movement
from app.core.logger import logger

class OrderService:
    def _get_order_item(self, db: Session, order_id):
        statement = select(OrderItem).where(OrderItem.order_id == order_id)
        result = db.execute(statement)

        return result.scalars().all()

    def _order_cancelled(self, db: Session, order_id, current_user_id):
        
        statement = select(OrderItem).where(OrderItem.order_id == order_id)
        result = db.execute(statement)

        order_item = result.scalars().all()

        movement_date = datetime.now().strftime(
            "%Y-%m-%d %H:%M:%S"
        )
        
        for item in order_item:
            self._add_stock(db, item)
            new_movement = Movement (
                product_id = item.product_id,
                type = "IN",
                quantity = item.quantity,
                detail = "Movimiento debido a la cancelación de una orden",
                user_id = current_user_id,
                movement_date = movement_date
            )
            db.add(new_movement)

    def _add_stock(self, db: Session, item):
        statement = select(Product).where(Product.id == item.product_id)
        result = db.execute(statement)

        product = result.scalar_one_or_none()

        product.stock += item.quantity
    
    def _order_item_create(self, db: Session, current_order_id, item):
        statement = select(Product).where(Product.id == item.product_id)
        result = db.execute(statement)

        product = result.scalar_one_or_none()

        if not product:
            raise HTTPException(
                status_code=404,
                detail="Producto no encontrado"
            )

        if product.stock >= item.quantity:
            product.stock -= item.quantity

        else:
            raise HTTPException(
                status_code=400,
                detail="Stock insuficiente"
            )

        new_order_item = OrderItem(
            order_id = current_order_id,
            product_id = item.product_id,
            quantity = item.quantity,
            unit_price = product.price
        )
        db.add(new_order_item)
        db.flush()
        
        return new_order_item

    def order_create(self, db: Session, current_user_id, order):
        try:
            new_order = Order(
                customer_id = order.customer_id,
                user_id = current_user_id,
            )
            db.add(new_order)
            db.flush()

            total = Decimal("0")
            items = []

            for item in order.items:
                order_item = self._order_item_create(db, new_order.id, item)
                new_movement = Movement(
                    product_id = item.product_id,
                    type = "OUT",
                    quantity = item.quantity,
                    detail = "Movimiento debido al registro de una orden",
                    user_id = current_user_id,
                    movement_date = new_order.created_at
                )
                db.add(new_movement)

                items.append(order_item)

                product_price = order_item.unit_price * order_item.quantity
                total += product_price

            new_order.total = total

            db.commit()
            db.refresh(new_order)

            logger.info("El usuario %s agrego un nuevo movimiento. ID: %s", new_order.user_id, new_order.id)

            return {
                "id": new_order.id,
                "customer_id": new_order.customer_id,
                "user_id": new_order.user_id,
                "status": new_order.status,
                "total": new_order.total,
                "created_at": new_order.created_at,
                "items": items
            }

        except HTTPException:
            db.rollback()

            raise

        except IntegrityError:
            db.rollback()

            logger.warning("No se pudo generar la orden proporcionada por el usuario. ID: %s", current_user_id)

            raise HTTPException(
                status_code=400,
                detail="No se pudo generar la orden"
            )

    def orders_get(self, db: Session):
        statement = select(Order)
        result = db.execute(statement)

        orders = result.scalars().all()

        if not orders:
            raise HTTPException(
                status_code=404,
                detail="No hay ordenes"
            )

        list_orders = []

        for order in orders:
            order_item = self._get_order_item(db, order.id)

            list_orders.append({
                "id": order.id,
                "customer_id": order.customer_id,
                "user_id": order.user_id,
                "status": order.status,
                "total": order.total,
                "created_at": order.created_at,
                "items": order_item
                }
            )

        return list_orders

    def order_get(self, db: Session, order_id):
        statement = select(Order).where(Order.id == order_id)
        result = db.execute(statement)

        order = result.scalar_one_or_none()

        if not order:
            raise HTTPException(
                status_code=404,
                detail="Orden no encontrada"
            )

        order_item = self._get_order_item(db, order_id)

        return {
            "id": order.id,
            "customer_id": order.customer_id,
            "user_id": order.user_id,
            "status": order.status,
            "total": order.total,
            "created_at": order.created_at,
            "items": order_item
        }

    def order_update(self, db: Session, order_id, user_id, order):
        statement = select(Order).where(Order.id == order_id)
        result = db.execute(statement)

        order_upd = result.scalar_one_or_none()

        if not order_upd:
            raise HTTPException(
                status_code=404,
                detail="Orden no encontrada"
            )

        if order_upd.status == OrderStatus.CANCELLED:
            raise HTTPException(
                status_code=400,
                detail="Una orden cancelada no puede modificarse"
            )

        if order_upd.status == OrderStatus.PENDING:
            try:
                order_upd.status = order.status
                
                if order_upd.status == OrderStatus.CANCELLED:
                    self._order_cancelled(db, order_upd.id, user_id)

                db.commit()
                db.refresh(order_upd)

                logger.info("El usuario %s cambio el estado de la orden %s.  Status:%s", user_id, order_upd.id, order_upd.status.value)
                
                return {
                    "message": f"Estado modificado correctamente a {order_upd.status.value}"
                }

            except IntegrityError:
                db.rollback()

                logger.warning("El usuario %s intento cambiar el estado de la orden %s con valores invalidos", user_id, order_upd.id)

                raise HTTPException(
                    status_code=400,
                    detail="No se pudo actualizar el estado de la orden"
                )

        else:
            raise HTTPException(
                status_code=400,
                detail="No se puede modificar el estado de la orden"
            )
