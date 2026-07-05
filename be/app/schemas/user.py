from datetime import datetime
from typing import Optional

from pydantic import BaseModel, EmailStr


class UserBase(BaseModel):
    username: str
    email: EmailStr
    full_name: str
    role: str


class UserCreate(BaseModel):
    username: str
    password: str
    email: EmailStr
    full_name: str
    role: str = "student"


class UserUpdate(BaseModel):
    email: Optional[EmailStr] = None
    full_name: Optional[str] = None
    role: Optional[str] = None


class UserResponse(UserBase):
    id: int
    created_at: datetime

    model_config = {"from_attributes": True}


class UserInDB(UserBase):
    id: int
    password_hash: str
    created_at: datetime

    model_config = {"from_attributes": True}
