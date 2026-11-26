import secrets
import string
from typing import List

from fastapi import Depends, APIRouter, HTTPException
from sqlalchemy.orm import Session

from app.api.dependecies import get_current_user, get_db

from app.models.auth import User, Room, RoomParticipant

from app.schemas.room import CreateRoomRequest, UpdateRoomRequest, RoomOut

rooms_router = APIRouter(
    prefix="/api/v1/rooms",
    tags=["rooms"],
    responses={404: {"description": "Not found"}},
)

def _generate_invite_code(length: int = 8) -> str:
    alphabet = string.ascii_uppercase + string.digits
    return "".join(secrets.choice(alphabet) for _ in range(length))

@rooms_router.post("", response_model=RoomOut, status_code=201, description="Создать новую комнату")
def create_room(body: CreateRoomRequest, user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    invite_code = _generate_invite_code()
    while db.query(Room).filter(Room.invite_code == invite_code).first():
        invite_code = _generate_invite_code()

    new_room = Room(
        owner_id=user.id,
        title=body.title,
        status="open",
        limit_participants=body.limit_participants,
        deadline=body.deadline,
        invite_code=invite_code,
    )
    db.add(new_room)
    db.flush()

    creator_participant = RoomParticipant(
        user_id=user.id,
        room_id=new_room.id,
    )
    db.add(creator_participant)
    db.commit()
    db.refresh(new_room)
    return new_room


@rooms_router.get("", response_model=List[RoomOut], description="Получить все комнаты, в которых состоит пользователь")
def list_rooms(user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    return (
        db.query(Room)
        .join(RoomParticipant, RoomParticipant.room_id == Room.id)
        .filter(RoomParticipant.user_id == user.id)
        .all()
    )


@rooms_router.get("/{room_id}", response_model=RoomOut, description="Получить информации о комнате")
def get_room(room_id: str, user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    room = db.query(Room).filter(Room.id == room_id).first()
    if not room:
        raise HTTPException(status_code=404, detail="Комната не найдена")

    is_member = db.query(RoomParticipant).filter(
        RoomParticipant.room_id == room_id,
        RoomParticipant.user_id == user.id,
    ).first()
    if not is_member:
        raise HTTPException(status_code=403, detail="Вы не являетесь участником этой комнаты")

    return room


@rooms_router.patch("/{room_id}", response_model=RoomOut, description="Изменить информацию о комнате")
def update_room(
    room_id: str,
    body: UpdateRoomRequest,
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    room = db.query(Room).filter(Room.id == room_id).first()
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


@rooms_router.delete("/{room_id}", status_code=204, description="Удалить комнату")
def delete_room(room_id: str, user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    room = db.query(Room).filter(Room.id == room_id).first()
    if not room:
        raise HTTPException(status_code=404, detail="Комната не найдена")
    if room.owner_id != user.id:
        raise HTTPException(status_code=403, detail="Только владелец может удалить комнату")

    db.delete(room)
    db.commit()


@rooms_router.post("/{room_id}/close", description="Закрыть комнату")
def close_room(room_id: str, user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    room = db.query(Room).filter(Room.id == room_id).first()
    if not room:
        raise HTTPException(status_code=404, detail="Комната не найдена")
    if room.owner_id != user.id:
        raise HTTPException(status_code=403, detail="Только владелец может закрыть комнату")

    room.status = "closed"
    db.commit()
    db.refresh(room)
    return room