from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field, EmailStr

from app.schemas.enum import UserRole

class UserResponse(BaseModel):
    id: int
    name: str
    email: str
    role: str
    active: bool
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)

class UserCreate(BaseModel):
    name: str = Field(min_length=1, max_length=50)
    email: EmailStr
    password: str
    role: UserRole

class UserUpdate(BaseModel):
    name: str = Field(min_length=1, max_length=50)
    email: EmailStr
