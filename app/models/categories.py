from datetime import datetime

from sqlalchemy import DateTime, Text, String, Integer, func
from sqlalchemy.orm import Mapped, mapped_column

from app.database.base import Base

class Category(Base):
    __tablename__ = "categories"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(50), nullable=False, unique=True)
    description: Mapped[str | None] = mapped_column(Text)
    created_at: Mapped[datetime] = mapped_column(DateTime, nullable=False, server_default=func.now())
