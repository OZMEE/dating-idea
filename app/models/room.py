import uuid
from datetime import datetime, timezone

from sqlalchemy import Column, String, Integer, DateTime, ForeignKey, Uuid

from app.models.base import Base


class RoomORM(Base):
    __tablename__ = "rooms"

    id = Column(
        Uuid,
        primary_key=True,
        default=uuid.uuid4,
    )
    owner_id = Column(
        Uuid,
        ForeignKey("users.id"),
        nullable=False,
    )
    title = Column(
        String,
        nullable=False,
    )
    status = Column(
        String,
        default="open",
        nullable=False,
    )
    limit_participants = Column(
        Integer,
        nullable=True,
    )
    deadline = Column(
        DateTime,
        nullable=True,
    )
    invite_code = Column(
        String,
        unique=True,
        nullable=False,
    )
    created_at = Column(
        DateTime,
        default=lambda: datetime.now(timezone.utc),
    )
