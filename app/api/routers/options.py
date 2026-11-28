import logging
from typing import List
from uuid import UUID

from fastapi import Depends, APIRouter, HTTPException

from app.api.dependecies import get_current_user, get_option_service
from app.models.auth import UserORM
from app.schemas.errors import (
    OptionAccessDeniedError,
    OptionNotFoundError,
    RoomAccessDeniedError,
    RoomNotFoundError,
)
from app.schemas.option import CreateOptionRequest, OptionOut
from app.services.option_service import OptionService

logger = logging.getLogger(__name__)

options_router = APIRouter(
    prefix="/api/v1/rooms/{room_id}",
    tags=["options"],
    responses={404: {"description": "Not found"}},
)

@options_router.post("/options", response_model=OptionOut, status_code=201, description="Добавить свой вариант в комнату")
def add_option(
    room_id: UUID,
    body: CreateOptionRequest,
    user: UserORM = Depends(get_current_user),
    svc: OptionService = Depends(get_option_service)
):
    try:
        return svc.add_option(user, room_id, body)
    except RoomNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except RoomAccessDeniedError as e:
        raise HTTPException(status_code=403, detail=str(e))
    except Exception as e:
        logger.error(f"Unexpected error adding option to room {room_id}: {e}")
        raise HTTPException(status_code=500, detail="Внутренняя ошибка сервера")


@options_router.get("/options", response_model=List[OptionOut], description="Получить все варианты в комнате")
def list_options(
    room_id: UUID, 
    user: UserORM = Depends(get_current_user), 
    svc: OptionService = Depends(get_option_service)
):
    try:
        return svc.list_options(user, room_id)
    except RoomNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except RoomAccessDeniedError as e:
        raise HTTPException(status_code=403, detail=str(e))
    except Exception as e:
        logger.error(f"Unexpected error listing options in room {room_id}: {e}")
        raise HTTPException(status_code=500, detail="Внутренняя ошибка сервера")


@options_router.delete("/options/{option_id}", status_code=204, description="Удалить вариант в комнате по option_id")
def delete_option(
    room_id: UUID,
    option_id: UUID,
    user: UserORM = Depends(get_current_user),
    svc: OptionService = Depends(get_option_service)
):
    try:
        svc.delete_option(user, room_id, option_id)
    except OptionNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except OptionAccessDeniedError as e:
        raise HTTPException(status_code=403, detail=str(e))
    except Exception as e:
        logger.error(f"Unexpected error deleting option {option_id} in room {room_id}: {e}")
        raise HTTPException(status_code=500, detail="Внутренняя ошибка сервера")