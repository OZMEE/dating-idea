from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.models.auth import UserORM, RoomORM, RoomParticipantORM
from app.schemas.auth import JoinRoomRequest


def remove_participant(db: Session, user: UserORM, room_id: str, participant_id: str) -> None:
    room = db.query(RoomORM).filter(RoomORM.id == room_id).first()
    if not room:
        raise HTTPException(status_code=404, detail="Комната не найдена")

    participant = db.query(RoomParticipantORM).filter(
        RoomParticipantORM.id == participant_id,
        RoomParticipantORM.room_id == room_id,
    ).first()
    if not participant:
        raise HTTPException(status_code=404, detail="Участник не найден")

    if room.owner_id != user.id and participant.user_id != user.id:
        raise HTTPException(status_code=403, detail="Недостаточно прав для удаления участника")

    if participant.user_id == room.owner_id:
        raise HTTPException(status_code=400, detail="Владелец комнаты не может быть удален")

    db.delete(participant)
    db.commit()


def join_room(db: Session, user: UserORM, body: JoinRoomRequest) -> RoomORM:
    room = db.query(RoomORM).filter(RoomORM.invite_code == body.invite_code).first()
    if not room:
        raise HTTPException(status_code=404, detail="Комната с таким кодом приглашения не найдена")

    if room.status != "open":
        raise HTTPException(status_code=400, detail="Комната закрыта для вступления")

    already_member = db.query(RoomParticipantORM).filter(
        RoomParticipantORM.room_id == room.id,
        RoomParticipantORM.user_id == user.id,
    ).first()
    if already_member:
        raise HTTPException(status_code=400, detail="Вы уже состоите в этой комнате")

    if room.limit_participants is not None:
        current_count = db.query(RoomParticipantORM).filter(RoomParticipantORM.room_id == room.id).count()
        if current_count >= room.limit_participants:
            raise HTTPException(status_code=400, detail="Достигнут лимит участников комнаты")

    new_participant = RoomParticipantORM(
        user_id=user.id,
        room_id=room.id,
    )
    db.add(new_participant)
    db.commit()
    db.refresh(room)
    return room
