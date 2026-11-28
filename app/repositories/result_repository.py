from typing import List, Optional, Tuple
from uuid import UUID

from sqlalchemy.orm import Session

from app.models.auth import UserORM
from app.models.option import OptionORM
from app.models.participant import RoomParticipantORM
from app.models.room import RoomORM
from app.models.vote import VoteORM


class ResultRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_room_by_id(self, room_id: UUID) -> Optional[RoomORM]:
        return self.db.query(RoomORM).filter(RoomORM.id == room_id).first()

    def get_participant_by_user(self, room_id: UUID, user_id: UUID) -> Optional[RoomParticipantORM]:
        return (
            self.db.query(RoomParticipantORM)
            .filter(
                RoomParticipantORM.room_id == room_id,
                RoomParticipantORM.user_id == user_id,
            )
            .first()
        )

    def list_options_by_room(self, room_id: UUID) -> List[OptionORM]:
        return self.db.query(OptionORM).filter(OptionORM.room_id == room_id).all()

    def list_participants_with_users(self, room_id: UUID) -> List[Tuple[RoomParticipantORM, UserORM]]:
        return (
            self.db.query(RoomParticipantORM, UserORM)
            .join(UserORM, UserORM.id == RoomParticipantORM.user_id)
            .filter(RoomParticipantORM.room_id == room_id)
            .all()
        )

    def list_votes_by_option_ids(self, option_ids: List[UUID]) -> List[VoteORM]:
        if not option_ids:
            return []
        return self.db.query(VoteORM).filter(VoteORM.option_id.in_(option_ids)).all()
