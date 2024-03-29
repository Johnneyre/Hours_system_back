from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from models.models import User as UserModel
from schemas.users import UserCreate
from db.db import get_db

router = APIRouter()

@router.get("")
def read_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    users = db.query(UserModel).offset(skip).limit(limit).all()
    return users

@router.get("/{id_user}")
def read_task(id_user: int, db: Session = Depends(get_db)):
    db_user = db.query(UserModel).filter(UserModel.id_user == id_user).first()
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user

@router.post("")
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    db_user = UserModel(**user.model_dump())
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

@router.put("/{id_user}")
def update_user(id_user: int, task: UserCreate, db: Session = Depends(get_db)):
    db_user = db.query(UserModel).filter(UserModel.id_user == id_user).first()
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")
    for key, value in task.model_dump().items():
        setattr(db_user, key, value)
    db.commit()
    return True

@router.delete("/{id_users}")
def delete_user(id_users: int, db: Session = Depends(get_db)):
    db_user = db.query(UserModel).filter(UserModel.id_user == id_users).first()
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")
    db.delete(db_user)
    db.commit()
    return {"detail": "User deleted successfully"}