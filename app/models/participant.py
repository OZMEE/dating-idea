import uuid
from datetime import datetime, timezone

from sqlalchemy import Column, DateTime, ForeignKey, UniqueConstraint, Uuid

from app.models.base import Base


class RoomParticipantORM(Base):
    __tablename__ = "room_participants"
    __table_args__ = (
        UniqueConstraint("user_id", "room_id", name="uq_user_room"),
    )

    id = Column(
        Uuid,
        primary_key=True,
        default=uuid.uuid4,
    )
    user_id = Column(
        Uuid,
        ForeignKey("users.id"),
        nullable=False,
    )
    room_id = Column(
        Uuid,
        ForeignKey("rooms.id", ondelete="CASCADE"),
        nullable=False,
    )
    joined_at = Column(
        DateTime,
        default=lambda: datetime.now(timezone.utc),
    )
