from typing import List, Tuple
from uuid import UUID

from sqlalchemy.orm import Session

from app.models.auth import UserORM
from app.models.option import OptionORM
from app.models.participant import RoomParticipantORM
from app.models.room import RoomORM
from app.models.vote import VoteORM
from app.repositories.swipe_repository import SwipeRepository
from app.schemas.auth import CreateVoteRequest
from app.schemas.errors import (
    OptionNotFoundError,
    RoomAccessDeniedError,
    RoomClosedError,
    RoomNotFoundError,
)

class SwipeService:
    def __init__(self, db: Session, repo: SwipeRepository):
        self.db = db
        self.repo = repo

    def _get_room_and_participant(self, room_id: UUID, user_id: UUID) -> Tuple[RoomORM, RoomParticipantORM]:
        room = self.repo.get_room_by_id(room_id)
        if not room:
            raise RoomNotFoundError("Комната не найдена")

        participant = self.repo.get_participant_by_user(room_id, user_id)
        if not participant:
            raise RoomAccessDeniedError("Вы не являетесь участником этой комнаты")

        return room, participant

    def get_my_swipes(self, user: UserORM, room_id: UUID) -> List[VoteORM]:
        _, participant = self._get_room_and_participant(room_id, user.id)
        return self.repo.list_votes_by_participant(participant.id)

    def get_deck(self, user: UserORM, room_id: UUID) -> List[OptionORM]:
        _, participant = self._get_room_and_participant(room_id, user.id)
        return self.repo.list_unvoted_options(room_id, participant.id)

    def swipe_option(self, user: UserORM, room_id: UUID, body: CreateVoteRequest) -> VoteORM:
        room, participant = self._get_room_and_participant(room_id, user.id)

        if room.status != "open":
            raise RoomClosedError("Комната закрыта, голосование завершено")

        option = self.repo.get_option_by_id(room_id, body.option_id)
        if not option:
            raise OptionNotFoundError("Вариант не найден в этой комнате")

        existing_vote = self.repo.get_vote(participant.id, body.option_id)
        if existing_vote:
            existing_vote.vote = body.vote
            self.db.commit()
            self.db.refresh(existing_vote)
            return existing_vote

        new_vote = VoteORM(
            room_participant_id=participant.id,
            option_id=body.option_id,
            vote=body.vote,
        )
        self.repo.add_vote(new_vote)
        self.db.commit()
        self.db.refresh(new_vote)
        return new_vote