from fastapi import Depends, APIRouter, HTTPException
from sqlalchemy.orm import Session

from app.api.dependecies import get_current_user, get_db

from app.models.auth import User, Room, RoomParticipant
from app.schemas.auth import JoinRoomRequest
from app.schemas.room import RoomOut

participant_router = APIRouter(
    prefix="/api/v1/rooms",
    tags=["participants"],
    responses={404: {"description": "Not found"}},
)

@participant_router.delete("/{room_id}/participants/{participant_id}", status_code=204, description="Удалить пользователя по participant_id")
def remove_participant(
    room_id: str,
    participant_id: str,
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    room = db.query(Room).filter(Room.id == room_id).first()
    if not room:
        raise HTTPException(status_code=404, detail="Комната не найдена")

    participant = db.query(RoomParticipant).filter(
        RoomParticipant.id == participant_id,
        RoomParticipant.room_id == room_id,
    ).first()
    if not participant:
        raise HTTPException(status_code=404, detail="Участник не найден")

    if room.owner_id != user.id and participant.user_id != user.id:
        raise HTTPException(status_code=403, detail="Недостаточно прав для удаления участника")

    if participant.user_id == room.owner_id:
        raise HTTPException(status_code=400, detail="Владелец комнаты не может быть удален")

    db.delete(participant)
    db.commit()

@participant_router.post("/participants/join", response_model=RoomOut, description="Добавить пользователя в комнату по invite_code")
def join_room(body: JoinRoomRequest, user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    room = db.query(Room).filter(Room.invite_code == body.invite_code).first()
    if not room:
        raise HTTPException(status_code=404, detail="Комната с таким кодом приглашения не найдена")

    if room.status != "open":
        raise HTTPException(status_code=400, detail="Комната закрыта для вступления")

    already_member = db.query(RoomParticipant).filter(
        RoomParticipant.room_id == room.id,
        RoomParticipant.user_id == user.id,
    ).first()
    if already_member:
        raise HTTPException(status_code=400, detail="Вы уже состоите в этой комнате")

    if room.limit_participants is not None:
        current_count = db.query(RoomParticipant).filter(RoomParticipant.room_id == room.id).count()
        if current_count >= room.limit_participants:
            raise HTTPException(status_code=400, detail="Достигнут лимит участников комнаты")

    new_participant = RoomParticipant(
        user_id=user.id,
        room_id=room.id,
    )
    db.add(new_participant)
    db.commit()
    db.refresh(room)
    return room