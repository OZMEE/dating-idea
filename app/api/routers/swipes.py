import logging
from typing import List
from uuid import UUID

from fastapi import Depends, APIRouter, HTTPException

from app.api.dependecies import get_current_user, get_swipe_service

from app.models.auth import UserORM
from app.schemas.auth import CreateVoteRequest, VoteOut
from app.schemas.errors import (
    OptionNotFoundError,
    RoomAccessDeniedError,
    RoomClosedError,
    RoomNotFoundError,
)
from app.schemas.option import OptionOut
from app.services.swipe_service import SwipeService

logger = logging.getLogger(__name__)

swipes_router = APIRouter(
    prefix="/api/v1/rooms/{room_id}",
    tags=["swipes"],
    responses={404: {"description": "Not found"}},
)

@swipes_router.get("/me", response_model=List[VoteOut], description="Получить варианты, которые уже свайпнул")
def my_swipes(
    room_id: UUID, 
    user: UserORM = Depends(get_current_user), 
    svc: SwipeService = Depends(get_swipe_service)
):
    try:
        return svc.get_my_swipes(user, room_id)
    except RoomNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except RoomAccessDeniedError as e:
        raise HTTPException(status_code=403, detail=str(e))
    except Exception as e:
        logger.error(f"Unexpected error getting user swipes in room {room_id}: {e}")
        raise HTTPException(status_code=500, detail="Внутренняя ошибка сервера")


@swipes_router.get("/deck", response_model=List[OptionOut], description="Получить варианты, которые еще не свайпнул")
def deck(
    room_id: UUID, 
    user: UserORM = Depends(get_current_user), 
    svc: SwipeService = Depends(get_swipe_service)
):
    try:
        return svc.get_deck(user, room_id)
    except RoomNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except RoomAccessDeniedError as e:
        raise HTTPException(status_code=403, detail=str(e))
    except Exception as e:
        logger.error(f"Unexpected error getting deck in room {room_id}: {e}")
        raise HTTPException(status_code=500, detail="Внутренняя ошибка сервера")


@swipes_router.patch("/swipes", response_model=VoteOut, status_code=200, description="Свайпнуть вариант по swipe_id")
def swipe(
    room_id: UUID,
    body: CreateVoteRequest,
    user: UserORM = Depends(get_current_user),
    svc: SwipeService = Depends(get_swipe_service)
):
    try:
        return svc.swipe_option(user, room_id, body)
    except (RoomNotFoundError, OptionNotFoundError) as e:
        raise HTTPException(status_code=404, detail=str(e))
    except RoomAccessDeniedError as e:
        raise HTTPException(status_code=403, detail=str(e))
    except RoomClosedError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.error(f"Unexpected error swiping in room {room_id}: {e}")
        raise HTTPException(status_code=500, detail="Внутренняя ошибка сервера")