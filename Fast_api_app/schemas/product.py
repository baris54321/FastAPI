from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class ProductBase(BaseModel):
    name: str
    description: Optional[str] = None
    price: int

class ProductCreate(ProductBase):
    pass

class ProductOut(ProductBase):
    id: int
    owner_id: int
    created_at: datetime
    updated_at: datetime
    deleted_at: Optional[datetime] = None

    class Config:
        from_attributes = True


class ProductResponse(BaseModel):
    data : ProductOut
    message: str
    status: str

class DeleteProduct(BaseModel):
    message: str
    status: str

class ProductUpdate(BaseModel):
    name: Optional[str] = None
    price: Optional[int]  = None 
    description: Optional[str]  = None
