from  datetime import datetime

from pydantic import BaseModel, EmailStr
from uuid import UUID

class UserResponse(BaseModel):
    id: UUID
    username: str
    email: str
    #todo докинуть остальные поля если есть

class RegisterRequest(BaseModel):
    name: str
    email: EmailStr
    username: str
    password: str


class LoginRequest(BaseModel):
    email: EmailStr
    password: str


class RefreshRequest(BaseModel):
    refresh_token: str


class UserOut(BaseModel):
    id: UUID
    name: str
    email: str
    username: str
    created_at: datetime

    class Config:
        from_attributes = True


class CreateVoteRequest(BaseModel):
    option_id: UUID
    vote: str


class VoteOut(BaseModel):
    id: UUID
    room_participant_id: UUID
    option_id: UUID
    vote: str
    created_at: datetime

    class Config:
        from_attributes = True


class JoinRoomRequest(BaseModel):
    invite_code: str