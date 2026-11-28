from datetime import datetime
from typing import Optional

from pydantic import BaseModel
from uuid import UUID


class CreateOptionRequest(BaseModel):
    title: str
    description: Optional[str] = ""


class OptionOut(BaseModel):
    id: UUID
    room_id: UUID
    participant_owner_id: Optional[UUID] = None
    title: str
    description: str
    created_at: datetime

    class Config:
        from_attributes = True