from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from models.models import Rol as RolModel
from db.db import get_db
from schemas.rol import RolCreate

router = APIRouter()

@router.get("")
def read_rols(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    rol = db.query(RolModel).offset(skip).limit(limit).all()
    return rol

@router.get("/{id_rol}")
def read_rol(id_rol: int, db: Session = Depends(get_db)):
    db_rol = db.query(RolModel).filter(RolModel.id_rol == id_rol).first()
    if not db_rol:
        raise HTTPException(status_code=404, detail="Rol not found")
    return db_rol

@router.post("")
def create_rol(rol: RolCreate, db: Session = Depends(get_db)):
    db_rol = RolModel(**rol.model_dump())
    db.add(db_rol)
    db.commit()
    db.refresh(db_rol)
    return db_rol

@router.put("/{id_rol}")
def update_rol(id_rol: int, rol: RolCreate, db: Session = Depends(get_db)):
    db_rol = db.query(RolModel).filter(RolModel.id_rol == id_rol).first()
    if not db_rol:
        raise HTTPException(status_code=404, detail="Rol not found")
    for key, value in rol.model_dump().items():
        setattr(db_rol, key, value)
    db.commit()
    return True