from datetime import datetime

from pydantic import Field, BaseModel, ConfigDict, EmailStr

class CustomerCreate(BaseModel):
    name: str = Field(min_length=1, max_length=50)
    email: EmailStr
    phone: str = Field(min_length=10, max_length=25)

class CustomerResponse(BaseModel):
    id: int
    name: str
    email: str
    phone: str
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)

class CustomerUpdate(BaseModel):
    name: str = Field(min_length=1, max_length=50)
    email: EmailStr
    phone: str = Field(min_length=10, max_length=25)
