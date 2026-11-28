import secrets
import string
from typing import List
from uuid import UUID

from sqlalchemy.orm import Session

from app.models.auth import UserORM
from app.schemas.room import CreateRoomRequest, UpdateRoomRequest
from app.models.participant import RoomParticipantORM
from app.models.room import RoomORM
from app.repositories.room_repository import RoomRepository
from app.schemas.errors import RoomNotFoundError, RoomAccessDeniedError

class RoomService:
    def __init__(self, db: Session, repo: RoomRepository):
        self.db = db
        self.repo = repo

    @staticmethod
    def _generate_invite_code(length: int = 8) -> str:
        alphabet = string.ascii_uppercase + string.digits
        return "".join(secrets.choice(alphabet) for _ in range(length))

    def create_room(self, user: UserORM, body: CreateRoomRequest) -> RoomORM:
        invite_code = self._generate_invite_code()
        while self.repo.get_by_invite_code(invite_code):
            invite_code = self._generate_invite_code()

        new_room = RoomORM(
            owner_id=user.id,
            title=body.title,
            status="open",
            limit_participants=body.limit_participants,
            deadline=body.deadline,
            invite_code=invite_code,
        )
        self.repo.add_room(new_room)

        creator_participant = RoomParticipantORM(
            user_id=user.id,
            room_id=new_room.id,
        )
        self.repo.add_participant(creator_participant)

        self.db.commit()
        self.db.refresh(new_room)
        return new_room

    def list_user_rooms(self, user: UserORM) -> List[RoomORM]:
        return self.repo.list_by_user_id(user.id)

    def get_room_for_member(self, user: UserORM, room_id: UUID) -> RoomORM:
        room = self.repo.get_by_id(room_id)
        if not room:
            raise RoomNotFoundError("Комната не найдена")

        is_member = self.repo.get_participant(room_id, user.id)
        if not is_member:
            raise RoomAccessDeniedError("Вы не являетесь участником этой комнаты")

        return room

    def update_room(self, user: UserORM, room_id: UUID, body: UpdateRoomRequest) -> RoomORM:
        room = self.repo.get_by_id(room_id)
        if not room:
            raise RoomNotFoundError("Комната не найдена")
        if room.owner_id != user.id:
            raise RoomAccessDeniedError("Только владелец может изменять комнату")

        update_data = body.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(room, field, value)

        self.db.commit()
        self.db.refresh(room)
        return room

    def delete_room(self, user: UserORM, room_id: UUID) -> None:
        room = self.repo.get_by_id(room_id)
        if not room:
            raise RoomNotFoundError("Комната не найдена")
        if room.owner_id != user.id:
            raise RoomAccessDeniedError("Только владелец может удалить комнату")

        self.repo.delete_room(room)
        self.db.commit()

    def close_room(self, user: UserORM, room_id: UUID) -> RoomORM:
        room = self.repo.get_by_id(room_id)
        if not room:
            raise RoomNotFoundError("Комната не найдена")
        if room.owner_id != user.id:
            raise RoomAccessDeniedError("Только владелец может закрыть комнату")

        room.status = "closed"
        self.db.commit()
        self.db.refresh(room)
        return room
