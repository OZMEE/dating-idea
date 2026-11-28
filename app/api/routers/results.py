import logging
from uuid import UUID

from fastapi import Depends, APIRouter, HTTPException

from app.api.dependecies import get_current_user, get_result_service
from app.models.auth import UserORM
from app.schemas.errors import RoomAccessDeniedError, RoomNotFoundError
from app.services.result_service import ResultService

logger = logging.getLogger(__name__)

results_router = APIRouter(
    prefix="/api/v1/rooms/{room_id}",
    tags=["results"],
    responses={404: {"description": "Not found"}},
)

@results_router.get("/stats", description="Получить статистику - кто за что проголосовал")
def stats(
    room_id: UUID, 
    user: UserORM = Depends(get_current_user), 
    svc: ResultService = Depends(get_result_service)
):
    try:
        return svc.get_room_stats(user, room_id)
    except RoomNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except RoomAccessDeniedError as e:
        raise HTTPException(status_code=403, detail=str(e))
    except Exception as e:
        logger.error(f"Unexpected error getting stats for room {room_id}: {e}")
        raise HTTPException(status_code=500, detail="Внутренняя ошибка сервера")

@results_router.get("/results", description="Получить результат голосования")
def results(
    room_id: UUID, 
    user: UserORM = Depends(get_current_user), 
    svc: ResultService = Depends(get_result_service)
):
    try:
        return svc.get_room_results(user, room_id)
    except RoomNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except RoomAccessDeniedError as e:
        raise HTTPException(status_code=403, detail=str(e))
    except Exception as e:
        logger.error(f"Unexpected error getting results for room {room_id}: {e}")
        raise HTTPException(status_code=500, detail="Внутренняя ошибка сервера")