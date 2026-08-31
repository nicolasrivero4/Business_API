from datetime import datetime
from decimal import Decimal

from pydantic import BaseModel, ConfigDict

from app.models.orders import OrderStatus
from app.schemas.order_items import OrderItemCreate, OrderItemResponse

class OrderCreate(BaseModel):
    customer_id: int
    items: list[OrderItemCreate]

class OrderResponse(BaseModel):
    id: int
    customer_id: int
    user_id: int
    status: str
    total: Decimal
    created_at: datetime
    items: list[OrderItemResponse]

    model_config = ConfigDict(from_attributes=True)

class OrderUpdate(BaseModel):
    status: OrderStatus
