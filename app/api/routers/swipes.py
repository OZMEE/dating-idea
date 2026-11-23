from typing import List

from fastapi import Depends, APIRouter

from app.api.dependecies import get_current_user, get_db
from sqlalchemy.orm import Session

from app.models.auth import User
from app.schemas.auth import CreateVoteRequest, VoteOut
from app.schemas.option import OptionOut

swipes_router = APIRouter(
    prefix="/api/v1/rooms/{room_id}",
    tags=["swipes"],
    responses={404: {"description": "Not found"}},
)

@swipes_router.get("/me", response_model=List[VoteOut], description="Получить варианты, которые уже свайпнул")
def my_swipes(room_id: str, user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    raise NotImplementedError


@swipes_router.get("/deck", response_model=List[OptionOut], description="Получить варианты, которые еще не свайпнул")
def deck(room_id: str, user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    raise NotImplementedError


@swipes_router.patch("/swipes", status_code=201, description="Свайпнуть вариант по swipe_id")
def swipe(
    room_id: str,
    body: CreateVoteRequest,
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    raise NotImplementedError