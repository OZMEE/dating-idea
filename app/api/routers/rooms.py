from typing import List
import logging
from uuid import UUID

from fastapi import Depends, APIRouter, HTTPException

from app.api.dependecies import get_current_user, get_room_service

from app.models.auth import UserORM

from app.schemas.errors import RoomAccessDeniedError, RoomNotFoundError
from app.schemas.room import CreateRoomRequest, UpdateRoomRequest, RoomOut
from app.services.room_service import RoomService

logger = logging.getLogger(__name__)

rooms_router = APIRouter(
    prefix="/api/v1/rooms",
    tags=["rooms"],
    responses={404: {"description": "Not found"}},
)

@rooms_router.post("", response_model=RoomOut, status_code=201, description="Создать новую комнату")
def create_room(
    body: CreateRoomRequest, 
    user: UserORM = Depends(get_current_user), 
    svc: RoomService = Depends(get_room_service)
):
    try:
        return svc.create_room(user, body)
    except Exception as e:
        logger.error(f"Unexpected error creating room: {e}")
        raise HTTPException(status_code=500, detail="Внутренняя ошибка сервера")


@rooms_router.get("", response_model=List[RoomOut], description="Получить все комнаты, в которых состоит пользователь")
def list_rooms(
    user: UserORM = Depends(get_current_user), 
    svc: RoomService = Depends(get_room_service)
):
    try:
        return svc.list_user_rooms(user)
    except Exception as e:
        logger.error(f"Unexpected error listing rooms: {e}")
        raise HTTPException(status_code=500, detail="Внутренняя ошибка сервера")


@rooms_router.get("/{room_id}", response_model=RoomOut, description="Получить информации о комнате")
def get_room(
    room_id: UUID, 
    user: UserORM = Depends(get_current_user), 
    svc: RoomService = Depends(get_room_service)
):
    try:
        return svc.get_room_for_member(user, room_id)
    except RoomNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except RoomAccessDeniedError as e:
        raise HTTPException(status_code=403, detail=str(e))
    except Exception as e:
        logger.error(f"Unexpected error getting room {room_id}: {e}")
        raise HTTPException(status_code=500, detail="Внутренняя ошибка сервера")


@rooms_router.patch("/{room_id}", response_model=RoomOut, description="Изменить информацию о комнате")
def update_room(
    room_id: UUID,
    body: UpdateRoomRequest,
    user: UserORM = Depends(get_current_user),
    svc: RoomService = Depends(get_room_service)
):
    try:
        return svc.update_room(user, room_id, body)
    except RoomNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except RoomAccessDeniedError as e:
        raise HTTPException(status_code=403, detail=str(e))
    except Exception as e:
        logger.error(f"Unexpected error updating room {room_id}: {e}")
        raise HTTPException(status_code=500, detail="Внутренняя ошибка сервера")


@rooms_router.delete("/{room_id}", status_code=204, description="Удалить комнату")
def delete_room(
    room_id: UUID, 
    user: UserORM = Depends(get_current_user), 
    svc: RoomService = Depends(get_room_service)
):
    try:
        svc.delete_room(user, room_id)
    except RoomNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except RoomAccessDeniedError as e:
        raise HTTPException(status_code=403, detail=str(e))
    except Exception as e:
        logger.error(f"Unexpected error deleting room {room_id}: {e}")
        raise HTTPException(status_code=500, detail="Внутренняя ошибка сервера")


@rooms_router.post("/{room_id}/close", response_model=RoomOut, description="Закрыть комнату")
def close_room(
    room_id: UUID, 
    user: UserORM = Depends(get_current_user), 
    svc: RoomService = Depends(get_room_service)
):
    try:
        return svc.close_room(user, room_id)
    except RoomNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except RoomAccessDeniedError as e:
        raise HTTPException(status_code=403, detail=str(e))
    except Exception as e:
        logger.error(f"Unexpected error closing room {room_id}: {e}")
        raise HTTPException(status_code=500, detail="Внутренняя ошибка сервера")