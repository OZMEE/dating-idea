import uuid
from datetime import datetime, timezone

from sqlalchemy import Column, String, DateTime, ForeignKey, Uuid

from app.models.base import Base


class OptionORM(Base):
    __tablename__ = "options"

    id = Column(
        Uuid,
        primary_key=True,
        default=uuid.uuid4,
    )
    room_id = Column(
        Uuid,
        ForeignKey("rooms.id", ondelete="CASCADE"),
        nullable=False,
    )
    participant_owner_id = Column(
        Uuid,
        ForeignKey("room_participants.id", ondelete="SET NULL"),
        nullable=True,
    )
    title = Column(
        String,
        nullable=False,
    )
    description = Column(
        String,
        default="",
        nullable=False,
    )
    created_at = Column(
        DateTime,
        default=lambda: datetime.now(timezone.utc),
    )
