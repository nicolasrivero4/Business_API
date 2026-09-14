from datetime import datetime
from decimal import Decimal

from sqlalchemy import CheckConstraint, Numeric, DateTime, ForeignKey, Integer, String, Text, func
from sqlalchemy.orm import Mapped, mapped_column

from app.database.base import Base

class Product(Base):
    __tablename__ = "products"

    __table_args__= (
            CheckConstraint("stock >= 0", name="check_product_stock_nonnegative"),
            CheckConstraint("price >= 0", name="check_product_price_nonnegative"),
        )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(50), nullable=False, unique=True)
    description: Mapped[str | None] = mapped_column(Text)
    stock: Mapped[Decimal] = mapped_column(Numeric(10, 2), nullable=False, server_default="0")
    price: Mapped[Decimal] = mapped_column(Numeric(10, 2), nullable=False, server_default="0")
    category_id: Mapped[int] = mapped_column(ForeignKey("categories.id"), nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, nullable=False, server_default=func.now())
    