from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from models.models import Task as TaskModel
from db.db import get_db
from schemas.tasks import TaskCreate

router = APIRouter()

@router.get("")
def read_tasks(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    tasks = db.query(TaskModel).offset(skip).limit(limit).all()
    return tasks

@router.get("/{id_tasks}")
def read_task(id_tasks: int, db: Session = Depends(get_db)):
    db_task = db.query(TaskModel).filter(TaskModel.id_tasks == id_tasks).first()
    if not db_task:
        raise HTTPException(status_code=404, detail="Task not found")
    return db_task

@router.post("")
def create_task(task: TaskCreate, db: Session = Depends(get_db)):
    db_task = TaskModel(**task.model_dump())
    db.add(db_task)
    db.commit()
    db.refresh(db_task)
    return db_task

@router.put("/{id_tasks}")
def update_task(id_tasks: int, task: TaskCreate, db: Session = Depends(get_db)):
    db_task = db.query(TaskModel).filter(TaskModel.id_tasks == id_tasks).first()
    if not db_task:
        raise HTTPException(status_code=404, detail="Task not found")
    for key, value in task.model_dump().items():
        setattr(db_task, key, value)
    db.commit()
    return True

@router.delete("/{id_tasks}")
def delete_task(id_tasks: int, db: Session = Depends(get_db)):
    db_task = db.query(TaskModel).filter(TaskModel.id_tasks == id_tasks).first()
    if not db_task:
        raise HTTPException(status_code=404, detail="Task not found")
    db.delete(db_task)
    db.commit()
    return {"detail": "Task deleted successfully"}