import os

from fastapi import Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session

from app.db.session import SessionLocal
from app.models.auth import UserORM

from dotenv import load_dotenv

from app.repositories.option_repository import OptionRepository
from app.repositories.participant_repository import ParticipantRepository
from app.repositories.result_repository import ResultRepository
from app.repositories.room_repository import RoomRepository
from app.repositories.swipe_repository import SwipeRepository
from app.services.option_service import OptionService
from app.services.participant_service import ParticipantService
from app.services.result_service import ResultService
from app.services.room_service import RoomService
from app.services.swipe_service import SwipeService

security = HTTPBearer(auto_error=False)

load_dotenv()  # внедряет переменные из .env в окружение процесса
DEV_MODE = os.getenv("ENV") == "development"

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def get_current_user(
    creds: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db),
) -> UserORM:
    if DEV_MODE:
        user = UserORM()
        user.name = "dev_user"
        print(user)
        return user
    raise NotImplementedError

def get_room_service(db: Session = Depends(get_db)) -> RoomService:
    return RoomService(db=db, repo=RoomRepository(db))


def get_participant_service(db: Session = Depends(get_db)) -> ParticipantService:
    return ParticipantService(db=db, repo=ParticipantRepository(db))


def get_option_service(db: Session = Depends(get_db)) -> OptionService:
    return OptionService(db=db, repo=OptionRepository(db))


def get_swipe_service(db: Session = Depends(get_db)) -> SwipeService:
    return SwipeService(db=db, repo=SwipeRepository(db))


def get_result_service(db: Session = Depends(get_db)) -> ResultService:
    return ResultService(db=db, repo=ResultRepository(db))