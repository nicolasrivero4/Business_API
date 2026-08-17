from enum import Enum as PyEnum
from datetime import datetime

from sqlalchemy import Boolean, DateTime, Integer, String, Text, Enum, func
from sqlalchemy.orm import Mapped, mapped_column

from app.database.base import Base

class UserRole(PyEnum):
    ADMIM = "ADMIM"
    EMPLOYEE = "EMPLOYEE"

class User(Base):
    __tablename__ =  "users"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(50), nullable=False)
    email: Mapped[str] = mapped_column(String(100), nullable=False, unique=True)
    password_hash: Mapped[str] = mapped_column(Text, nullable=False)
    role: Mapped[UserRole] = mapped_column(Enum(UserRole, name="user_role", create_type=False), nullable=False, server_default=UserRole.EMPLOYEE.value)
    active: Mapped[bool] = mapped_column(Boolean, nullable=False, server_default="true")
    created_at: Mapped[datetime] = mapped_column(DateTime, nullable=False, server_default=func.now())
