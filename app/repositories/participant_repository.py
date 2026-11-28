from typing import Optional
from uuid import UUID

from sqlalchemy.orm import Session

from app.models.participant import RoomParticipantORM
from app.models.room import RoomORM


class ParticipantRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_room_by_id(self, room_id: UUID) -> Optional[RoomORM]:
        return self.db.query(RoomORM).filter(RoomORM.id == room_id).first()

    def get_room_by_invite_code(self, invite_code: str) -> Optional[RoomORM]:
        return self.db.query(RoomORM).filter(RoomORM.invite_code == invite_code).first()

    def get_participant_by_id(self, room_id: UUID, participant_id: UUID) -> Optional[RoomParticipantORM]:
        return (
            self.db.query(RoomParticipantORM)
            .filter(
                RoomParticipantORM.id == participant_id,
                RoomParticipantORM.room_id == room_id,
            )
            .first()
        )

    def get_participant_by_user(self, room_id: UUID, user_id: UUID) -> Optional[RoomParticipantORM]:
        return (
            self.db.query(RoomParticipantORM)
            .filter(
                RoomParticipantORM.room_id == room_id,
                RoomParticipantORM.user_id == user_id,
            )
            .first()
        )

    def count_participants(self, room_id: UUID) -> int:
        return self.db.query(RoomParticipantORM).filter(RoomParticipantORM.room_id == room_id).count()

    def add_participant(self, participant: RoomParticipantORM) -> RoomParticipantORM:
        self.db.add(participant)
        return participant

    def delete_participant(self, participant: RoomParticipantORM) -> None:
        self.db.delete(participant)
