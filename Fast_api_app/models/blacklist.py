from sqlalchemy import Column, Integer, String, DateTime
from datetime import datetime

from db.base import Base

class BlacklistedToken(Base):
    __tablename__ = 'blacklisted_tokens'

    id = Column(Integer, primary_key=True, index=True)
    token = Column(String, unique=True, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"<BlacklistedToken(id={self.id}, token='{self.token}')>"
