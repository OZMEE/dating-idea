from typing import List

from fastapi import Depends, APIRouter
from sqlalchemy.orm import Session

from app.api.dependecies import get_current_user, get_db

from app.models.auth import User

from app.schemas.room import CreateRoomRequest, UpdateRoomRequest, RoomOut

rooms_router = APIRouter(
    prefix="/api/v1/rooms",
    tags=["rooms"],
    responses={404: {"description": "Not found"}},
)

@rooms_router.post("", response_model=RoomOut, status_code=201, description="Создать новую комнату")
def create_room(body: CreateRoomRequest, user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    raise NotImplementedError


@rooms_router.get("", response_model=List[RoomOut], description="Получить все комнаты, в которых состоит пользователь")
def list_rooms(user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    raise NotImplementedError


@rooms_router.get("/{room_id}", response_model=RoomOut, description="Получить информации о комнате")
def get_room(room_id: str, user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    raise NotImplementedError


@rooms_router.patch("/{room_id}", response_model=RoomOut, description="Изменить информацию о комнате")
def update_room(
    room_id: str,
    body: UpdateRoomRequest,
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    raise NotImplementedError


@rooms_router.delete("/{room_id}", status_code=204, description="Удалить комнату")
def delete_room(room_id: str, user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    raise NotImplementedError


@rooms_router.post("/{room_id}/close", description="Закрыть комнату")
def close_room(room_id: str, user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    raise NotImplementedError