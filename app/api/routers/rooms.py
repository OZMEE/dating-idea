from typing import List

from fastapi import Depends, APIRouter
from sqlalchemy.orm import Session

from app.api.dependecies import get_current_user, get_db

from app.models.auth import UserORM

from app.schemas.room import CreateRoomRequest, UpdateRoomRequest, RoomOut
from app.services import room_service

rooms_router = APIRouter(
    prefix="/api/v1/rooms",
    tags=["rooms"],
    responses={404: {"description": "Not found"}},
)

@rooms_router.post("", response_model=RoomOut, status_code=201, description="Создать новую комнату")
def create_room(body: CreateRoomRequest, user: UserORM = Depends(get_current_user), db: Session = Depends(get_db)):
    return room_service.create_room(db, user, body)


@rooms_router.get("", response_model=List[RoomOut], description="Получить все комнаты, в которых состоит пользователь")
def list_rooms(user: UserORM = Depends(get_current_user), db: Session = Depends(get_db)):
    return room_service.list_user_rooms(db, user)


@rooms_router.get("/{room_id}", response_model=RoomOut, description="Получить информации о комнате")
def get_room(room_id: str, user: UserORM = Depends(get_current_user), db: Session = Depends(get_db)):
    return room_service.get_room_for_member(db, user, room_id)


@rooms_router.patch("/{room_id}", response_model=RoomOut, description="Изменить информацию о комнате")
def update_room(
    room_id: str,
    body: UpdateRoomRequest,
    user: UserORM = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    return room_service.update_room(db, user, room_id, body)


@rooms_router.delete("/{room_id}", status_code=204, description="Удалить комнату")
def delete_room(room_id: str, user: UserORM = Depends(get_current_user), db: Session = Depends(get_db)):
    room_service.delete_room(db, user, room_id)


@rooms_router.post("/{room_id}/close", response_model=RoomOut, description="Закрыть комнату")
def close_room(room_id: str, user: UserORM = Depends(get_current_user), db: Session = Depends(get_db)):
    return room_service.close_room(db, user, room_id)