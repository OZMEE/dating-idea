import secrets
import string
from typing import List

from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.models.auth import UserORM, RoomORM, RoomParticipantORM
from app.schemas.room import CreateRoomRequest, UpdateRoomRequest


def _generate_invite_code(length: int = 8) -> str:
    alphabet = string.ascii_uppercase + string.digits
    return "".join(secrets.choice(alphabet) for _ in range(length))


def create_room(db: Session, user: UserORM, body: CreateRoomRequest) -> RoomORM:
    invite_code = _generate_invite_code()
    while db.query(RoomORM).filter(RoomORM.invite_code == invite_code).first():
        invite_code = _generate_invite_code()

    new_room = RoomORM(
        owner_id=user.id,
        title=body.title,
        status="open",
        limit_participants=body.limit_participants,
        deadline=body.deadline,
        invite_code=invite_code,
    )
    db.add(new_room)
    db.flush()

    creator_participant = RoomParticipantORM(
        user_id=user.id,
        room_id=new_room.id,
    )
    db.add(creator_participant)
    db.commit()
    db.refresh(new_room)
    return new_room


def list_user_rooms(db: Session, user: UserORM) -> List[RoomORM]:
    return (
        db.query(RoomORM)
        .join(RoomParticipantORM, RoomParticipantORM.room_id == RoomORM.id)
        .filter(RoomParticipantORM.user_id == user.id)
        .all()
    )


def get_room_for_member(db: Session, user: UserORM, room_id: str) -> RoomORM:
    room = db.query(RoomORM).filter(RoomORM.id == room_id).first()
    if not room:
        raise HTTPException(status_code=404, detail="Комната не найдена")

    is_member = db.query(RoomParticipantORM).filter(
        RoomParticipantORM.room_id == room_id,
        RoomParticipantORM.user_id == user.id,
    ).first()
    if not is_member:
        raise HTTPException(status_code=403, detail="Вы не являетесь участником этой комнаты")

    return room


def update_room(db: Session, user: UserORM, room_id: str, body: UpdateRoomRequest) -> RoomORM:
    room = db.query(RoomORM).filter(RoomORM.id == room_id).first()
    if not room:
        raise HTTPException(status_code=404, detail="Комната не найдена")
    if room.owner_id != user.id:
        raise HTTPException(status_code=403, detail="Только владелец может изменять комнату")

    update_data = body.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(room, field, value)

    db.commit()
    db.refresh(room)
    return room


def delete_room(db: Session, user: UserORM, room_id: str) -> None:
    room = db.query(RoomORM).filter(RoomORM.id == room_id).first()
    if not room:
        raise HTTPException(status_code=404, detail="Комната не найдена")
    if room.owner_id != user.id:
        raise HTTPException(status_code=403, detail="Только владелец может удалить комнату")

    db.delete(room)
    db.commit()


def close_room(db: Session, user: UserORM, room_id: str) -> RoomORM:
    room = db.query(RoomORM).filter(RoomORM.id == room_id).first()
    if not room:
        raise HTTPException(status_code=404, detail="Комната не найдена")
    if room.owner_id != user.id:
        raise HTTPException(status_code=403, detail="Только владелец может закрыть комнату")

    room.status = "closed"
    db.commit()
    db.refresh(room)
    return room
