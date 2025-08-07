from pydantic import BaseModel
from datetime import datetime

class BlacklistedTokenBase(BaseModel):
    token: str

class BlacklistedTokenCreate(BlacklistedTokenBase):
    pass

class BlacklistedTokenOut(BlacklistedTokenBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True
