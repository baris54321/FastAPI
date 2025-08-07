from sqlalchemy import Column, Integer, String, Boolean, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from passlib.context import CryptContext
from db.base import Base

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, nullable=False, index=True)
    email = Column(String, unique=True, nullable=False, index=True)
    hashed_password = Column(String, nullable=False)

    is_active = Column(Boolean, default=True)
    is_admin = Column(Boolean, default=False)
    is_admin_approved = Column(Boolean, default=False)

    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    deleted_at = Column(DateTime, nullable=True)

    tokens = relationship("Token", back_populates="user", cascade="all, delete")

    products = relationship(
        "Product",
        back_populates="owner",
        cascade="all, delete",
        foreign_keys='Product.owner_id'  # 🔥 THIS IS THE FIX
    )


    # Define relationships for updated_by and deleted_by products
    updated_products = relationship(
        "Product",
        foreign_keys='Product.updated_by',
        back_populates="updated_by_user"
    )

    deleted_products = relationship(
        "Product",
        foreign_keys='Product.deleted_by',
        back_populates="deleted_by_user"
    )


    def __repr__(self):
        return f"<User(id={self.id}, username='{self.username}', email='{self.email}')>"
    
    def set_password(self, raw_password: str):
        self.hashed_password = pwd_context.hash(raw_password)

    def verify_password(self, raw_password: str):
        return pwd_context.verify(raw_password, self.hashed_password)
