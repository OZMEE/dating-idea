from typing import List

from fastapi import Depends, APIRouter, HTTPException
from sqlalchemy.orm import Session

from app.api.dependecies import get_current_user, get_db
from app.models.auth import User, Room, RoomParticipant, Option
from app.schemas.option import CreateOptionRequest, OptionOut

options_router = APIRouter(
    prefix="/api/v1/rooms/{room_id}",
    tags=["options"],
    responses={404: {"description": "Not found"}},
)

@options_router.post("/options", response_model=OptionOut, status_code=201, description="Добавить свой вариант в комнату")
def add_option(
    room_id: str,
    body: CreateOptionRequest,
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    room = db.query(Room).filter(Room.id == room_id).first()
    if not room:
        raise HTTPException(status_code=404, detail="Комната не найдена")

    participant = db.query(RoomParticipant).filter(
        RoomParticipant.room_id == room_id,
        RoomParticipant.user_id == user.id,
    ).first()
    if not participant:
        raise HTTPException(status_code=403, detail="Вы не являетесь участником этой комнаты")

    new_option = Option(
        room_id=room_id,
        participant_owner_id=participant.id,
        title=body.title,
        description=body.description or "",
    )
    db.add(new_option)
    db.commit()
    db.refresh(new_option)
    return new_option


@options_router.get("/options", response_model=List[OptionOut], description="Получить все варианты в комнате")
def list_options(room_id: str, user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    room = db.query(Room).filter(Room.id == room_id).first()
    if not room:
        raise HTTPException(status_code=404, detail="Комната не найдена")

    participant = db.query(RoomParticipant).filter(
        RoomParticipant.room_id == room_id,
        RoomParticipant.user_id == user.id,
    ).first()
    if not participant:
        raise HTTPException(status_code=403, detail="Вы не являетесь участником этой комнаты")

    return db.query(Option).filter(Option.room_id == room_id).all()


@options_router.delete("/options/{option_id}", status_code=204, description="Удалить вариант в комнате по option_id")
def delete_option(
    room_id: str,
    option_id: str,
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    option = db.query(Option).filter(Option.id == option_id, Option.room_id == room_id).first()
    if not option:
        raise HTTPException(status_code=404, detail="Вариант не найден")

    participant = db.query(RoomParticipant).filter(
        RoomParticipant.room_id == room_id,
        RoomParticipant.user_id == user.id,
    ).first()
    if not participant or option.participant_owner_id != participant.id:
        raise HTTPException(status_code=403, detail="Нельзя удалить чужой вариант")

    db.delete(option)
    db.commit()