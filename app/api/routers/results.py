from fastapi import Depends, APIRouter
from sqlalchemy.orm import Session

from app.api.dependecies import get_current_user, get_db
from app.main import app
from app.models.auth import User

results_router = APIRouter(
    prefix="/api/v1/rooms/{room_id}",
    tags=["results"],
    responses={404: {"description": "Not found"}},
)

@results_router.get("/stats", description="Получить статистику - кто за что проголосовал")
def stats(room_id: str, user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    raise NotImplementedError


@results_router.get("/results", description="Получить результат голосования")
def results(room_id: str, user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    raise NotImplementedError