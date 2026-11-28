from uuid import UUID
from sqlalchemy.orm import Session

from app.models.auth import UserORM
from app.models.room import RoomORM
from app.repositories.result_repository import ResultRepository
from app.schemas.errors import RoomAccessDeniedError, RoomNotFoundError

POSITIVE_VOTES = {"like", "yes", "true", "1", "right"}

class ResultService:
    def __init__(self, db: Session, repo: ResultRepository):
        self.db = db
        self.repo = repo

    def _check_room_access(self, room_id: UUID, user_id: UUID) -> RoomORM:
        room = self.repo.get_room_by_id(room_id)
        if not room:
            raise RoomNotFoundError("Комната не найдена")

        is_member = self.repo.get_participant_by_user(room_id, user_id)
        if not is_member:
            raise RoomAccessDeniedError("Вы не являетесь участником этой комнаты")

        return room

    def get_room_stats(self, user: UserORM, room_id: UUID) -> dict:
        self._check_room_access(room_id, user.id)

        options = self.repo.list_options_by_room(room_id)
        participants = self.repo.list_participants_with_users(room_id)
        participant_map = {
            rp.id: {"participant_id": str(rp.id), "user_id": str(u.id), "username": u.username, "name": u.name}
            for rp, u in participants
        }

        option_ids = [opt.id for opt in options]
        votes = self.repo.list_votes_by_option_ids(option_ids)

        votes_by_option: dict[UUID, list] = {opt.id: [] for opt in options}
        for v in votes:
            voter_info = participant_map.get(v.room_participant_id, {"participant_id": str(v.room_participant_id)})
            votes_by_option[v.option_id].append({
                **voter_info,
                "vote": v.vote,
                "created_at": v.created_at,
            })

        return {
            "room_id": str(room_id),
            "options": [
                {
                    "option_id": str(opt.id),
                    "title": opt.title,
                    "description": opt.description,
                    "votes": votes_by_option[opt.id],
                }
                for opt in options
            ],
        }

    def get_room_results(self, user: UserORM, room_id: UUID) -> dict:
        room = self._check_room_access(room_id, user.id)

        options = self.repo.list_options_by_room(room_id)
        option_ids = [opt.id for opt in options]
        votes = self.repo.list_votes_by_option_ids(option_ids)

        likes_count = {opt.id: 0 for opt in options}
        dislikes_count = {opt.id: 0 for opt in options}

        for v in votes:
            if v.vote.strip().lower() in POSITIVE_VOTES:
                likes_count[v.option_id] += 1
            else:
                dislikes_count[v.option_id] += 1

        ranking = [
            {
                "option_id": str(opt.id),
                "title": opt.title,
                "description": opt.description,
                "likes": likes_count[opt.id],
                "dislikes": dislikes_count[opt.id],
                "total_votes": likes_count[opt.id] + dislikes_count[opt.id],
            }
            for opt in options
        ]
        ranking.sort(key=lambda item: (item["likes"], -item["dislikes"]), reverse=True)

        winner = ranking[0] if ranking and ranking[0]["likes"] > 0 else None

        return {
            "room_id": str(room_id),
            "status": room.status,
            "winner": winner,
            "ranking": ranking,
        }