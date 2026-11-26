from typing import List

from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.models.auth import UserORM, RoomORM, RoomParticipantORM, OptionORM, VoteORM
from app.schemas.auth import CreateVoteRequest


def _get_room_and_participant(db: Session, room_id: str, user_id: str) -> tuple[RoomORM, RoomParticipantORM]:
    room = db.query(RoomORM).filter(RoomORM.id == room_id).first()
    if not room:
        raise HTTPException(status_code=404, detail="Комната не найдена")

    participant = db.query(RoomParticipantORM).filter(
        RoomParticipantORM.room_id == room_id,
        RoomParticipantORM.user_id == user_id,
    ).first()
    if not participant:
        raise HTTPException(status_code=403, detail="Вы не являетесь участником этой комнаты")

    return room, participant


def get_my_swipes(db: Session, user: UserORM, room_id: str) -> List[VoteORM]:
    _, participant = _get_room_and_participant(db, room_id, user.id)
    return db.query(VoteORM).filter(VoteORM.room_participant_id == participant.id).all()


def get_deck(db: Session, user: UserORM, room_id: str) -> List[OptionORM]:
    _, participant = _get_room_and_participant(db, room_id, user.id)

    voted_option_ids = (
        db.query(VoteORM.option_id)
        .filter(VoteORM.room_participant_id == participant.id)
        .subquery()
    )

    return (
        db.query(OptionORM)
        .filter(
            OptionORM.room_id == room_id,
            ~OptionORM.id.in_(voted_option_ids),
        )
        .all()
    )


def swipe_option(db: Session, user: UserORM, room_id: str, body: CreateVoteRequest) -> VoteORM:
    room, participant = _get_room_and_participant(db, room_id, user.id)

    if room.status != "open":
        raise HTTPException(status_code=400, detail="Комната закрыта, голосование завершено")

    option = db.query(OptionORM).filter(
        OptionORM.id == body.option_id,
        OptionORM.room_id == room_id,
    ).first()
    if not option:
        raise HTTPException(status_code=404, detail="Вариант не найден в этой комнате")

    existing_vote = db.query(VoteORM).filter(
        VoteORM.room_participant_id == participant.id,
        VoteORM.option_id == body.option_id,
    ).first()

    if existing_vote:
        existing_vote.vote = body.vote
        db.commit()
        db.refresh(existing_vote)
        return existing_vote

    new_vote = VoteORM(
        room_participant_id=participant.id,
        option_id=body.option_id,
        vote=body.vote,
    )
    db.add(new_vote)
    db.commit()
    db.refresh(new_vote)
    return new_vote
