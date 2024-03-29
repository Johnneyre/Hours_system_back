from pydantic import BaseModel
from typing import Optional

class RolBase(BaseModel):
    description: str

class RolCreate(RolBase):
    pass

class Rol(RolBase):
    id_rol: Optional[int] = None

    class Config:
        from_attributes = True
