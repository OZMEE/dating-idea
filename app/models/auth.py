import uuid
from datetime import datetime, timezone

from sqlalchemy import Column, String, DateTime, Uuid

from app.models.base import Base


class UserORM(Base):
    __tablename__ = "users"
    
    id = Column(
        Uuid, 
        primary_key=True, 
        default=uuid.uuid4
    )
    name = Column(
        String, 
        nullable=False
    )
    email = Column(
        String, 
        unique=True, 
        nullable=False, 
        index=True
    )
    username = Column(
        String, 
        unique=True, 
        nullable=False, 
        index=True
    )
    password_hash = Column(
        String, 
        nullable=False
    )
    created_at = Column(
        DateTime, 
        default=lambda: datetime.now(timezone.utc)
    )

