import logging
from uuid import UUID

from fastapi import Depends, APIRouter, HTTPException

from app.api.dependecies import get_current_user, get_participant_service

from app.models.auth import UserORM
from app.schemas.auth import JoinRoomRequest
from app.schemas.errors import (
    AlreadyRoomMemberError,
    OwnerRemovalError,
    ParticipantNotFoundError,
    RoomAccessDeniedError,
    RoomClosedError,
    RoomFullError,
    RoomNotFoundError,
)

from app.schemas.room import RoomOut
from app.services.participant_service import ParticipantService

logger = logging.getLogger(__name__)

participant_router = APIRouter(
    prefix="/api/v1/rooms",
    tags=["participants"],
    responses={404: {"description": "Not found"}},
)

@participant_router.delete("/{room_id}/participants/{participant_id}", status_code=204, description="Удалить пользователя по participant_id")
def remove_participant(
    room_id: UUID,
    participant_id: UUID,
    user: UserORM = Depends(get_current_user),
    svc: ParticipantService = Depends(get_participant_service)
):
    try:
        svc.remove_participant(user, room_id, participant_id)
    except (RoomNotFoundError, ParticipantNotFoundError) as e:
        raise HTTPException(status_code=404, detail=str(e))
    except RoomAccessDeniedError as e:
        raise HTTPException(status_code=403, detail=str(e))
    except OwnerRemovalError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.error(f"Unexpected error removing participant {participant_id} from room {room_id}: {e}")
        raise HTTPException(status_code=500, detail="Внутренняя ошибка сервера")


@participant_router.post("/participants/join", response_model=RoomOut, description="Добавить пользователя в комнату по invite_code")
def join_room(
    body: JoinRoomRequest, 
    user: UserORM = Depends(get_current_user), 
    svc: ParticipantService = Depends(get_participant_service)
):
    try:
        return svc.join_room(user, body)
    except RoomNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except (RoomClosedError, AlreadyRoomMemberError, RoomFullError) as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.error(f"Unexpected error joining room: {e}")
        raise HTTPException(status_code=500, detail="Внутренняя ошибка сервера")