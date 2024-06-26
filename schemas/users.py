from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class UserBase(BaseModel):
    username: Optional[str] = None
    password: Optional[str] = None
    fullName: Optional[str] = None
    C_I: Optional[int] = None
    bithdate: Optional[datetime] = None
    position: Optional[str] = None
    status: Optional[bool] = None
    id_rol: int

class UserCreate(UserBase):
    pass

class User(UserBase):
    id_user: Optional[int] = None
    created_at: Optional[datetime] = None

    class Config:
        from_attributes = True

class UserInDB(User):
    hashed_password: str
    disabled: Optional[bool] = False