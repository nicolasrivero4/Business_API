from enum import Enum as PyEnum
from datetime import datetime
from decimal import Decimal

from sqlalchemy import CheckConstraint, Numeric, DateTime, Integer, ForeignKey, Enum, Text, func
from sqlalchemy.orm import Mapped, mapped_column

from app.database.base import Base

class MovementType(PyEnum):
    IN = "IN"
    OUT = "OUT"

class Movement(Base):
    __tablename__ = "movements"

    __table_args__= (
        CheckConstraint("quantity > 0", name="check_movement_quantity_positive"),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    product_id: Mapped[int] = mapped_column(ForeignKey("products.id"), nullable=False)
    type: Mapped[MovementType] = mapped_column(Enum(MovementType, name="movement_type", create_type=False), nullable=False)
    quantity: Mapped[Decimal] = mapped_column(Numeric(10, 2), nullable=False)
    detail: Mapped[str | None] = mapped_column(Text)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, nullable=False, server_default=func.now())
    movement_date: Mapped[datetime] = mapped_column(DateTime, nullable=False)
