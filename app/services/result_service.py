from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.models.auth import UserORM, RoomORM, RoomParticipantORM, OptionORM, VoteORM

POSITIVE_VOTES = {"like", "yes", "true", "1", "right"}


def _check_room_access(db: Session, room_id: str, user_id: str) -> RoomORM:
    room = db.query(RoomORM).filter(RoomORM.id == room_id).first()
    if not room:
        raise HTTPException(status_code=404, detail="Комната не найдена")

    is_member = db.query(RoomParticipantORM).filter(
        RoomParticipantORM.room_id == room_id,
        RoomParticipantORM.user_id == user_id,
    ).first()
    if not is_member:
        raise HTTPException(status_code=403, detail="Вы не являетесь участником этой комнаты")

    return room


def get_room_stats(db: Session, user: UserORM, room_id: str) -> dict:
    _check_room_access(db, room_id, user.id)

    options = db.query(OptionORM).filter(OptionORM.room_id == room_id).all()
    participants = (
        db.query(RoomParticipantORM, UserORM)
        .join(UserORM, UserORM.id == RoomParticipantORM.user_id)
        .filter(RoomParticipantORM.room_id == room_id)
        .all()
    )
    participant_map = {
        rp.id: {"participant_id": rp.id, "user_id": u.id, "username": u.username, "name": u.name}
        for rp, u in participants
    }

    option_ids = [opt.id for opt in options]
    votes = db.query(VoteORM).filter(VoteORM.option_id.in_(option_ids)).all() if option_ids else []

    votes_by_option: dict[str, list] = {opt.id: [] for opt in options}
    for v in votes:
        voter_info = participant_map.get(v.room_participant_id, {"participant_id": v.room_participant_id})
        votes_by_option[v.option_id].append({
            **voter_info,
            "vote": v.vote,
            "created_at": v.created_at,
        })

    return {
        "room_id": room_id,
        "options": [
            {
                "option_id": opt.id,
                "title": opt.title,
                "description": opt.description,
                "votes": votes_by_option[opt.id],
            }
            for opt in options
        ],
    }


def get_room_results(db: Session, user: UserORM, room_id: str) -> dict:
    room = _check_room_access(db, room_id, user.id)

    options = db.query(OptionORM).filter(OptionORM.room_id == room_id).all()
    option_ids = [opt.id for opt in options]
    votes = db.query(VoteORM).filter(VoteORM.option_id.in_(option_ids)).all() if option_ids else []

    likes_count = {opt.id: 0 for opt in options}
    dislikes_count = {opt.id: 0 for opt in options}

    for v in votes:
        if v.vote.strip().lower() in POSITIVE_VOTES:
            likes_count[v.option_id] += 1
        else:
            dislikes_count[v.option_id] += 1

    ranking = [
        {
            "option_id": opt.id,
            "title": opt.title,
            "description": opt.description,
            "likes": likes_count[opt.id],
            "dislikes": dislikes_count[opt.id],
            "total_votes": likes_count[opt.id] + dislikes_count[opt.id],
        }
        for opt in options
    ]
    ranking.sort(key=lambda item: (item["likes"], -item["dislikes"]), reverse=True)

    winner = ranking if ranking and ranking["likes"] > 0 else None

    return {
        "room_id": room_id,
        "status": room.status,
        "winner": winner,
        "ranking": ranking,
    }
