from enum import Enum as PyEnum
from decimal import Decimal
from datetime import datetime

from sqlalchemy import CheckConstraint, Integer, ForeignKey, Enum, Numeric, DateTime, text, func
from sqlalchemy.orm import Mapped, mapped_column

from app.database.base import Base

class OrderStatus(PyEnum):
    PENDING = "PENDING"
    COMPLETED = "COMPLETED"
    CANCELLED = "CANCELLED"

class Order(Base):
    __tablename__ = "orders"

    __table_args__= (
        CheckConstraint("total >= 0", name="check_order_total_nonnegative"),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    customer_id: Mapped[int] = mapped_column(ForeignKey("customers.id"), nullable=False)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)
    status: Mapped[OrderStatus] = mapped_column(Enum(OrderStatus, name="order_status", create_type=False), nullable=False, server_default=OrderStatus.PENDING.value)
    total: Mapped[Decimal] = mapped_column(Numeric(10, 2), nullable=False, server_default=text("0"))
    created_at: Mapped[datetime] = mapped_column(DateTime, nullable=False, server_default=func.now())
