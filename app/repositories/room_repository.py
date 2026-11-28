from typing import List, Optional
from uuid import UUID

from sqlalchemy.orm import Session

from app.models.participant import RoomParticipantORM
from app.models.room import RoomORM


class RoomRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_by_id(self, room_id: UUID) -> Optional[RoomORM]:
        return self.db.query(RoomORM).filter(RoomORM.id == room_id).first()

    def get_by_invite_code(self, invite_code: str) -> Optional[RoomORM]:
        return self.db.query(RoomORM).filter(RoomORM.invite_code == invite_code).first()

    def list_by_user_id(self, user_id: UUID) -> List[RoomORM]:
        return (
            self.db.query(RoomORM)
            .join(RoomParticipantORM, RoomParticipantORM.room_id == RoomORM.id)
            .filter(RoomParticipantORM.user_id == user_id)
            .all()
        )

    def get_participant(self, room_id: UUID, user_id: UUID) -> Optional[RoomParticipantORM]:
        return (
            self.db.query(RoomParticipantORM)
            .filter(
                RoomParticipantORM.room_id == room_id,
                RoomParticipantORM.user_id == user_id,
            )
            .first()
        )

    def add_room(self, room: RoomORM) -> RoomORM:
        self.db.add(room)
        self.db.flush()
        return room

    def add_participant(self, participant: RoomParticipantORM) -> RoomParticipantORM:
        self.db.add(participant)
        return participant

    def delete_room(self, room: RoomORM) -> None:
        self.db.delete(room)
