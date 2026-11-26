from typing import List

from fastapi import Depends, APIRouter, HTTPException

from app.api.dependecies import get_current_user, get_db
from sqlalchemy.orm import Session

from app.models.auth import User, Room, RoomParticipant, Option, Vote
from app.schemas.auth import CreateVoteRequest, VoteOut
from app.schemas.option import OptionOut

swipes_router = APIRouter(
    prefix="/api/v1/rooms/{room_id}",
    tags=["swipes"],
    responses={404: {"description": "Not found"}},
)

def _get_room_and_participant(room_id: str, user_id: str, db: Session) -> tuple[Room, RoomParticipant]:
    room = db.query(Room).filter(Room.id == room_id).first()
    if not room:
        raise HTTPException(status_code=404, detail="Комната не найдена")

    participant = db.query(RoomParticipant).filter(
        RoomParticipant.room_id == room_id,
        RoomParticipant.user_id == user_id,
    ).first()
    if not participant:
        raise HTTPException(status_code=403, detail="Вы не являетесь участником этой комнаты")

    return room, participant

@swipes_router.get("/me", response_model=List[VoteOut], description="Получить варианты, которые уже свайпнул")
def my_swipes(room_id: str, user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    _, participant = _get_room_and_participant(room_id, user.id, db)

    return db.query(Vote).filter(Vote.room_participant_id == participant.id).all()


@swipes_router.get("/deck", response_model=List[OptionOut], description="Получить варианты, которые еще не свайпнул")
def deck(room_id: str, user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    _, participant = _get_room_and_participant(room_id, user.id, db)

    voted_option_ids = (
        db.query(Vote.option_id)
        .filter(Vote.room_participant_id == participant.id)
        .subquery()
    )

    return (
        db.query(Option)
        .filter(
            Option.room_id == room_id,
            ~Option.id.in_(voted_option_ids),
        )
        .all()
    )


@swipes_router.patch("/swipes", status_code=201, description="Свайпнуть вариант по swipe_id")
def swipe(
    room_id: str,
    body: CreateVoteRequest,
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    room, participant = _get_room_and_participant(room_id, user.id, db)

    if room.status != "open":
        raise HTTPException(status_code=400, detail="Комната закрыта, голосование завершено")

    option = db.query(Option).filter(
        Option.id == body.option_id,
        Option.room_id == room_id,
    ).first()
    if not option:
        raise HTTPException(status_code=404, detail="Вариант не найден в этой комнате")

    existing_vote = db.query(Vote).filter(
        Vote.room_participant_id == participant.id,
        Vote.option_id == body.option_id,
    ).first()

    if existing_vote:
        existing_vote.vote = body.vote
        db.commit()
        db.refresh(existing_vote)
        return existing_vote

    new_vote = Vote(
        room_participant_id=participant.id,
        option_id=body.option_id,
        vote=body.vote,
    )
    db.add(new_vote)
    db.commit()
    db.refresh(new_vote)
    return new_vote