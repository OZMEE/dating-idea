from fastapi import Depends, APIRouter
from sqlalchemy.orm import Session

from app.api.dependecies import get_current_user, get_db
from app.models.auth import UserORM
from app.services import result_service

results_router = APIRouter(
    prefix="/api/v1/rooms/{room_id}",
    tags=["results"],
    responses={404: {"description": "Not found"}},
)

@results_router.get("/stats", description="Получить статистику - кто за что проголосовал")
def stats(room_id: str, user: UserORM = Depends(get_current_user), db: Session = Depends(get_db)):
    return result_service.get_room_stats(db, user, room_id)

@results_router.get("/results", description="Получить результат голосования")
def results(room_id: str, user: UserORM = Depends(get_current_user), db: Session = Depends(get_db)):
    return result_service.get_room_results(db, user, room_id)