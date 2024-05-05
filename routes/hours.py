from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from models.models import Hour as HourModel
from schemas.hours import HourCreate
from db.db import get_db

router = APIRouter()

@router.get("")
def read_hours(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    hours = db.query(HourModel).offset(skip).limit(limit).all()
    return hours

@router.get("/{id_hour}")
def read_hour(id_hour: int, db: Session = Depends(get_db)):
    db_hours = db.query(HourModel).filter(HourModel.id_hours == id_hour).first()
    if not db_hours:
        raise HTTPException(status_code=404, detail="Hour not found")
    return db_hours

@router.post("")
def create_hour(hour: HourCreate, db: Session = Depends(get_db)):
    db_hour = HourModel(**hour.model_dump())
    db.add(db_hour)
    db.commit()
    db.refresh(db_hour)
    return db_hour

@router.put("/{id_hours}")
def update_hour(id_hours: int, hour: HourCreate, db: Session = Depends(get_db)):
    db_hour = db.query(HourModel).filter(HourModel.id_hours == id_hours).first()
    if not db_hour:
        raise HTTPException(status_code=404, detail="Hour not found")
    for key, value in hour.model_dump().items():
        setattr(db_hour, key, value)
    db.commit()
    return True