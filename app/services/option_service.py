from typing import List

from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.models.auth import UserORM, RoomORM, RoomParticipantORM, OptionORM
from app.schemas.option import CreateOptionRequest


def add_option(db: Session, user: UserORM, room_id: str, body: CreateOptionRequest) -> OptionORM:
    room = db.query(RoomORM).filter(RoomORM.id == room_id).first()
    if not room:
        raise HTTPException(status_code=404, detail="Комната не найдена")

    participant = db.query(RoomParticipantORM).filter(
        RoomParticipantORM.room_id == room_id,
        RoomParticipantORM.user_id == user.id,
    ).first()
    if not participant:
        raise HTTPException(status_code=403, detail="Вы не являетесь участником этой комнаты")

    new_option = OptionORM(
        room_id=room_id,
        participant_owner_id=participant.id,
        title=body.title,
        description=body.description or "",
    )
    db.add(new_option)
    db.commit()
    db.refresh(new_option)
    return new_option


def list_options(db: Session, user: UserORM, room_id: str) -> List[OptionORM]:
    room = db.query(RoomORM).filter(RoomORM.id == room_id).first()
    if not room:
        raise HTTPException(status_code=404, detail="Комната не найдена")

    participant = db.query(RoomParticipantORM).filter(
        RoomParticipantORM.room_id == room_id,
        RoomParticipantORM.user_id == user.id,
    ).first()
    if not participant:
        raise HTTPException(status_code=403, detail="Вы не являетесь участником этой комнаты")

    return db.query(OptionORM).filter(OptionORM.room_id == room_id).all()


def delete_option(db: Session, user: UserORM, room_id: str, option_id: str) -> None:
    option = db.query(OptionORM).filter(OptionORM.id == option_id, OptionORM.room_id == room_id).first()
    if not option:
        raise HTTPException(status_code=404, detail="Вариант не найден")

    participant = db.query(RoomParticipantORM).filter(
        RoomParticipantORM.room_id == room_id,
        RoomParticipantORM.user_id == user.id,
    ).first()
    if not participant or option.participant_owner_id != participant.id:
        raise HTTPException(status_code=403, detail="Нельзя удалить чужой вариант")

    db.delete(option)
    db.commit()
