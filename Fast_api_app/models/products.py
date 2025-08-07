from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime

from db.base import Base

class Product(Base):
    __tablename__ = 'products'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    description = Column(String, nullable=True)
    price = Column(Integer, nullable=False)

    owner_id = Column(Integer, ForeignKey('users.id'))
    owner = relationship(
        "User",
        back_populates="products",
        foreign_keys=[owner_id]  # ✅ THIS FIXES THE ERROR
    )

    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    deleted_at = Column(DateTime, nullable=True)

    updated_by = Column(Integer, ForeignKey('users.id'), nullable=True)
    updated_by_user = relationship(
        "User",
        foreign_keys=[updated_by],
        back_populates="updated_products"
    )

    deleted_by = Column(Integer, ForeignKey('users.id'), nullable=True)
    deleted_by_user = relationship(
        "User",
        foreign_keys=[deleted_by],
        back_populates="deleted_products"
    )

    def __repr__(self):
        return f"<Product(id={self.id}, name='{self.name}', price={self.price})>"

