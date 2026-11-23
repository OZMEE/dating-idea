from typing import List

from fastapi import Depends, APIRouter
from sqlalchemy.orm import Session

from app.api.dependecies import get_current_user, get_db
from app.models.auth import User
from app.schemas.option import CreateOptionRequest, OptionOut

options_router = APIRouter(
    prefix="/api/v1/rooms/{room_id}",
    tags=["options"],
    responses={404: {"description": "Not found"}},
)

@options_router.post("/options", response_model=OptionOut, status_code=201, description="Добавить свой вариант в комнату")
def add_option(
    room_id: str,
    body: CreateOptionRequest,
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    raise NotImplementedError


@options_router.get("/options", response_model=List[OptionOut], description="Получить все варианты в комнате")
def list_options(room_id: str, user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    raise NotImplementedError


@options_router.delete("/options/{option_id}", status_code=204, description="Удалить вариант в комнате по option_id")
def delete_option(
    room_id: str,
    option_id: str,
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    raise NotImplementedError