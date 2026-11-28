import uuid
from datetime import datetime, timezone

from sqlalchemy import Column, String, DateTime, ForeignKey, UniqueConstraint, Uuid

from app.models.base import Base


class VoteORM(Base):
    __tablename__ = "votes"
    __table_args__ = (
        UniqueConstraint("room_participant_id", "option_id", name="uq_participant_option"),
    )

    id = Column(
        Uuid,
        primary_key=True,
        default=uuid.uuid4,
    )
    room_participant_id = Column(
        Uuid,
        ForeignKey("room_participants.id", ondelete="CASCADE"),
        nullable=False,
    )
    option_id = Column(
        Uuid,
        ForeignKey("options.id", ondelete="CASCADE"),
        nullable=False,
    )
    vote = Column(
        String,
        nullable=False,
    )
    created_at = Column(
        DateTime,
        default=lambda: datetime.now(timezone.utc),
    )
