from datetime import datetime
from decimal import Decimal

from pydantic import BaseModel, Field, ConfigDict

class ProductCreate(BaseModel):
    name: str = Field(min_length=1, max_length=50)
    description: str | None = None
    price: Decimal = Field(max_digits=10, decimal_places=2)
    category_id: int

class ProductResponse(BaseModel):
    id: int
    name: str
    description: str | None
    stock: Decimal
    price: Decimal
    category_id: int
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)

class ProductUpdate(BaseModel):
    name: str = Field(min_length=1, max_length=50)
    description: str | None = None
    price: Decimal = Field(max_digits=10, decimal_places=2)
    category_id: int
