from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel
from ..database import get_db
from .. import models

router = APIRouter(prefix="/classes", tags=["classes"])

@router.get("/")
def get_classes(db: Session = Depends(get_db)):
    return db.query(models.Class).all()

@router.post("/")
def create_class(class_data: dict, db: Session = Depends(get_db)):
    db_class = models.Class(**class_data)
    db.add(db_class)
    db.commit()
    db.refresh(db_class)
    return db_class

@router.get("/{class_id}/students")
def get_students_in_class(class_id: int, db: Session = Depends(get_db)):
    classroom = db.query(models.Class).filter(models.Class.id == class_id).first()
    if not classroom:
        raise HTTPException(status_code=404, detail="Class not found")
    return classroom.users

class AddStudentRequest(BaseModel):
    user_id: int

@router.post("/{class_id}/students")
def add_student_to_class(class_id: int, req: AddStudentRequest, db: Session = Depends(get_db)):
    classroom = db.query(models.Class).filter(models.Class.id == class_id).first()
    user = db.query(models.User).filter(models.User.id == req.user_id).first()
    if not classroom or not user:
        raise HTTPException(status_code=404, detail="Class or user not found")
    if user not in classroom.users:
        classroom.users.append(user)
        db.commit()
    return {"message": "Student added to class"}
