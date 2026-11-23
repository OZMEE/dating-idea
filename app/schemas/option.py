from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class CreateOptionRequest(BaseModel):
    title: str
    description: Optional[str] = ""


class OptionOut(BaseModel):
    id: str
    room_id: str
    participant_owner_id: Optional[str] = None
    title: str
    description: str
    created_at: datetime

    class Config:
        from_attributes = True