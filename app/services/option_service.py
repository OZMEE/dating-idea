from typing import List
from uuid import UUID

from sqlalchemy.orm import Session

from app.models.auth import UserORM
from app.models.option import OptionORM
from app.repositories.option_repository import OptionRepository
from app.schemas.errors import (
    OptionAccessDeniedError,
    OptionNotFoundError,
    RoomAccessDeniedError,
    RoomNotFoundError,
)
from app.schemas.option import CreateOptionRequest

class OptionService:
    def __init__(self, db: Session, repo: OptionRepository):
        self.db = db
        self.repo = repo

    def add_option(self, user: UserORM, room_id: UUID, body: CreateOptionRequest) -> OptionORM:
        room = self.repo.get_room_by_id(room_id)
        if not room:
            raise RoomNotFoundError("Комната не найдена")

        participant = self.repo.get_participant_by_user(room_id, user.id)
        if not participant:
            raise RoomAccessDeniedError("Вы не являетесь участником этой комнаты")

        new_option = OptionORM(
            room_id=room_id,
            participant_owner_id=participant.id,
            title=body.title,
            description=body.description or "",
        )
        self.repo.add_option(new_option)
        self.db.commit()
        self.db.refresh(new_option)
        return new_option

    def list_options(self, user: UserORM, room_id: UUID) -> List[OptionORM]:
        room = self.repo.get_room_by_id(room_id)
        if not room:
            raise RoomNotFoundError("Комната не найдена")

        participant = self.repo.get_participant_by_user(room_id, user.id)
        if not participant:
            raise RoomAccessDeniedError("Вы не являетесь участником этой комнаты")

        return self.repo.list_options_by_room(room_id)

    def delete_option(self, user: UserORM, room_id: UUID, option_id: UUID) -> None:
        option = self.repo.get_option_by_id(room_id, option_id)
        if not option:
            raise OptionNotFoundError("Вариант не найден")

        participant = self.repo.get_participant_by_user(room_id, user.id)
        if not participant or option.participant_owner_id != participant.id:
            raise OptionAccessDeniedError("Нельзя удалить чужой вариант")

        self.repo.delete_option(option)
        self.db.commit()