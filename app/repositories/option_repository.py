from typing import List, Optional
from uuid import UUID

from sqlalchemy.orm import Session

from app.models.option import OptionORM
from app.models.participant import RoomParticipantORM
from app.models.room import RoomORM


class OptionRepository:
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

    def get_option_by_id(self, room_id: UUID, option_id: UUID) -> Optional[OptionORM]:
        return (
            self.db.query(OptionORM)
            .filter(OptionORM.id == option_id, OptionORM.room_id == room_id)
            .first()
        )

    def list_options_by_room(self, room_id: UUID) -> List[OptionORM]:
        return self.db.query(OptionORM).filter(OptionORM.room_id == room_id).all()

    def add_option(self, option: OptionORM) -> OptionORM:
        self.db.add(option)
        return option

    def delete_option(self, option: OptionORM) -> None:
        self.db.delete(option)
