from decimal import Decimal

from pydantic import Field, BaseModel, ConfigDict

class OrderItemCreate(BaseModel):
    product_id: int
    quantity: Decimal = Field(gt=0, max_digits=10, decimal_places=2)

class OrderItemResponse(BaseModel):
    id: int
    order_id: int
    product_id: int
    quantity: Decimal
    unit_price: Decimal

    model_config = ConfigDict(from_attributes=True)
