from fastapi import Depends, APIRouter
from sqlalchemy.orm import Session

from app.api.dependecies import get_current_user, get_db

from app.models.auth import User
from app.schemas.auth import JoinRoomRequest
from app.schemas.room import RoomOut

participant_router = APIRouter(
    prefix="/api/v1/rooms/{room_id}",
    tags=["participants"],
    responses={404: {"description": "Not found"}},
)

@participant_router.delete("/participants/{participant_id}", status_code=204, description="Удалить пользователя по participant_id")
def remove_participant(
    room_id: str,
    participant_id: str,
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    raise NotImplementedError

@participant_router.post("/participants/join", response_model=RoomOut, description="Добавить пользователя в комнату по invite_code")
def join_room(body: JoinRoomRequest, user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    raise NotImplementedError