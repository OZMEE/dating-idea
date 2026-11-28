from datetime import datetime
from typing import Optional

from pydantic import BaseModel
from uuid import UUID

class RoomOut(BaseModel):
    id: UUID
    owner_id: UUID
    title: str
    status: str
    limit_participants: Optional[int] = None
    deadline: Optional[datetime] = None
    invite_code: str
    created_at: datetime

    class Config:
        from_attributes = True


class CreateRoomRequest(BaseModel):
    title: str
    limit_participants: Optional[int] = None
    deadline: Optional[datetime] = None


class UpdateRoomRequest(BaseModel):
    title: Optional[str] = None
    limit_participants: Optional[int] = None
    deadline: Optional[datetime] = None