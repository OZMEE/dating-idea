from fastapi import Depends, APIRouter
from sqlalchemy.orm import Session

from app.api.dependecies import get_current_user, get_db

from app.models.auth import UserORM
from app.schemas.auth import JoinRoomRequest
from app.schemas.room import RoomOut
from app.services import participant_service

participant_router = APIRouter(
    prefix="/api/v1/rooms",
    tags=["participants"],
    responses={404: {"description": "Not found"}},
)

@participant_router.delete("/{room_id}/participants/{participant_id}", status_code=204, description="Удалить пользователя по participant_id")
def remove_participant(
    room_id: str,
    participant_id: str,
    user: UserORM = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    participant_service.remove_participant(db, user, room_id, participant_id)

@participant_router.post("/participants/join", response_model=RoomOut, description="Добавить пользователя в комнату по invite_code")
def join_room(body: JoinRoomRequest, user: UserORM = Depends(get_current_user), db: Session = Depends(get_db)):
    return participant_service.join_room(db, user, body)