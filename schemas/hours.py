from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class HourBase(BaseModel):
    hours: Optional[int] = None
    date: Optional[datetime] = None
    description: Optional[str] = None
    id_user: int
    id_tasks: int

class HourCreate(HourBase):
    pass

class Hour(HourBase):
    id_hours: int
    created_at: Optional[datetime] = None

    class Config:
        from_attributes = True
