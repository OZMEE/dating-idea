from sqlalchemy.orm import Session
from uuid import UUID

from app.models.auth import UserORM
from app.models.participant import RoomParticipantORM
from app.models.room import RoomORM
from app.repositories.participant_repository import ParticipantRepository
from app.schemas.auth import JoinRoomRequest
from app.schemas.errors import (
    AlreadyRoomMemberError,
    OwnerRemovalError,
    ParticipantNotFoundError,
    RoomAccessDeniedError,
    RoomClosedError,
    RoomFullError,
    RoomNotFoundError,
)

class ParticipantService:
    def __init__(self, db: Session, repo: ParticipantRepository):
        self.db = db
        self.repo = repo

    def remove_participant(self, user: UserORM, room_id: UUID, participant_id: UUID) -> None:
        room = self.repo.get_room_by_id(room_id)
        if not room:
            raise RoomNotFoundError("Комната не найдена")

        participant = self.repo.get_participant_by_id(room_id, participant_id)
        if not participant:
            raise ParticipantNotFoundError("Участник не найден")

        if room.owner_id != user.id and participant.user_id != user.id:
            raise RoomAccessDeniedError("Недостаточно прав для удаления участника")

        if participant.user_id == room.owner_id:
            raise OwnerRemovalError("Владелец комнаты не может быть удален")

        self.repo.delete_participant(participant)
        self.db.commit()

    def join_room(self, user: UserORM, body: JoinRoomRequest) -> RoomORM:
        room = self.repo.get_room_by_invite_code(body.invite_code)
        if not room:
            raise RoomNotFoundError("Комната с таким кодом приглашения не найдена")

        if room.status != "open":
            raise RoomClosedError("Комната закрыта для вступления")

        already_member = self.repo.get_participant_by_user(room.id, user.id)
        if already_member:
            raise AlreadyRoomMemberError("Вы уже состоите в этой комнате")

        if room.limit_participants is not None:
            current_count = self.repo.count_participants(room.id)
            if current_count >= room.limit_participants:
                raise RoomFullError("Достигнут лимит участников комнаты")

        new_participant = RoomParticipantORM(
            user_id=user.id,
            room_id=room.id,
        )
        self.repo.add_participant(new_participant)
        self.db.commit()
        self.db.refresh(room)
        return room