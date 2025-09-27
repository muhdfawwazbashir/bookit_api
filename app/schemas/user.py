from datetime import datetime
from pydantic import BaseModel, EmailStr
from typing import Optional
from enum import Enum
import uuid

class RoleEnum(str, Enum):
    user = "user"
    admin = "admin"

class UserBase(BaseModel):
    name: str
    email:EmailStr
    role: RoleEnum = RoleEnum.user

class UserCreate(UserBase):
    password: str

class UserUpdate(BaseModel):
    name: Optional[str] = None
    email: Optional[EmailStr] = None
    password: Optional[str] = None

class UserOut(UserBase):
    id: uuid.UUID
    role: RoleEnum
    created_at: datetime

    class Config:
        from_attributes = True


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"

class LoginRequest(BaseModel):
    email: EmailStr
    password: str






