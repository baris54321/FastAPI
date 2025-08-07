from pydantic import BaseModel
from datetime import datetime

class TokenBase(BaseModel):
    access_token: str
    refresh_token: str

class TokenCreate(TokenBase):
    user_id: int

class TokenOut(TokenBase):
    id: int
    user_id: int
    created_at: datetime

    class Config:
        from_attributes = True
