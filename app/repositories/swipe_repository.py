from typing import List, Optional
from uuid import UUID

from sqlalchemy.orm import Session

from app.models.option import OptionORM
from app.models.participant import RoomParticipantORM
from app.models.room import RoomORM
from app.models.vote import VoteORM


class SwipeRepository:
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

    def list_votes_by_participant(self, participant_id: UUID) -> List[VoteORM]:
        return self.db.query(VoteORM).filter(VoteORM.room_participant_id == participant_id).all()

    def list_unvoted_options(self, room_id: UUID, participant_id: UUID) -> List[OptionORM]:
        voted_option_ids = (
            self.db.query(VoteORM.option_id)
            .filter(VoteORM.room_participant_id == participant_id)
            .subquery()
        )
        return (
            self.db.query(OptionORM)
            .filter(
                OptionORM.room_id == room_id,
                ~OptionORM.id.in_(voted_option_ids),
            )
            .all()
        )

    def get_option_by_id(self, room_id: UUID, option_id: UUID) -> Optional[OptionORM]:
        return (
            self.db.query(OptionORM)
            .filter(OptionORM.id == option_id, OptionORM.room_id == room_id)
            .first()
        )

    def get_vote(self, participant_id: UUID, option_id: UUID) -> Optional[VoteORM]:
        return (
            self.db.query(VoteORM)
            .filter(
                VoteORM.room_participant_id == participant_id,
                VoteORM.option_id == option_id,
            )
            .first()
        )

    def add_vote(self, vote: VoteORM) -> VoteORM:
        self.db.add(vote)
        return vote
