from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class TaskBase(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None

class TaskCreate(TaskBase):
    pass

class Task(TaskBase):
    id_tasks: int
    created_at: Optional[datetime] = None

    class Config:
        from_attributes = True
