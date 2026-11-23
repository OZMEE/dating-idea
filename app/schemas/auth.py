from  datetime import datetime

from pydantic import BaseModel, EmailStr


class UserResponse(BaseModel):
    id: int
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
    id: str
    name: str
    email: str
    username: str
    created_at: datetime

    class Config:
        from_attributes = True


class CreateVoteRequest(BaseModel):
    option_id: str
    vote: str


class VoteOut(BaseModel):
    id: str
    room_participant_id: str
    option_id: str
    vote: str
    created_at: datetime

    class Config:
        from_attributes = True


class JoinRoomRequest(BaseModel):
    invite_code: str