from pydantic import BaseModel, EmailStr
from typing import List, Optional
from datetime import datetime

from .product import ProductOut
from .token import TokenOut

class UserBase(BaseModel):
    username: str
    email: EmailStr

class UserCreate(UserBase):
    password: str  # Plain password for input

class UserOut(UserBase):
    id: int
    is_active: bool
    is_admin: bool
    is_admin_approved: bool
    created_at: datetime
    updated_at: datetime
    deleted_at: Optional[datetime] = None

    class Config:
        from_attributes = True

class UserWithProducts(UserOut):
    products: List[ProductOut] = []

class UserWithTokens(BaseModel):
    data: UserOut
    # tokens: List[TokenOut] = []
    access_token: Optional[str] = None
    refresh_token: Optional[str] = None
    message: str
    status: str

class UserUpdate(BaseModel):
    username: Optional[str] = None
    email: Optional[EmailStr] = None
    is_active: Optional[bool] = None
    is_admin: Optional[bool] = None
    is_admin_approved: Optional[bool] = None

    class Config:
        from_attributes = True


class LoginRequest(BaseModel):
    username: str
    password: str


class ResponseModel(BaseModel):
    data: UserOut
    message: str
    status: str