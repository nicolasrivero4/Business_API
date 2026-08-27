from datetime import datetime
from decimal import Decimal

from pydantic import BaseModel, Field, ConfigDict

from app.models.movements import MovementType

class MovementCreate(BaseModel):
    product_id: int
    type: MovementType
    quantity: Decimal = Field(gt=0, max_digits=10, decimal_places=2)
    detail: str | None = None
    movement_date: datetime

class MovementResponse(BaseModel):
    id: int
    product_id: int
    type: str
    quantity: Decimal
    detail: str
    user_id: int
    created_at: datetime
    movement_date: datetime

    model_config = ConfigDict(from_attributes=True)
