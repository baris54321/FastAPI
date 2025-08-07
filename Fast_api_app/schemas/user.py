from pydantic import BaseModel, EmailStr
from typing import List, Optional
from datetime import datetime


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

class UserWithTokens(BaseModel):
    data: UserOut
    # tokens: List[TokenOut] = []
    access_token: Optional[str] = None
    refresh_token: Optional[str] = None
    message: str
    status: str


class LoginRequest(BaseModel):
    username: str
    password: str


class ResponseModel(BaseModel):
    data: UserOut
    message: str
    status: str

class ApproveUser(BaseModel):
    is_admin_approved: bool
    message: str
    status: str
