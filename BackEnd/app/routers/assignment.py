
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel
from datetime import datetime
from ..database import get_db
from .. import models

router = APIRouter(prefix="/assignments", tags=["assignments"])

@router.get("/{assignment_id}/submissions")
def get_submissions(assignment_id: int, db: Session = Depends(get_db)):
    # Lấy các file bài nộp (is_submission=1) cho assignment
    return db.query(models.Attachment).filter(models.Attachment.assignment_id == assignment_id, models.Attachment.is_submission == 1).all()

@router.get("/")
def get_assignments(db: Session = Depends(get_db)):
    return db.query(models.Assignment).all()

@router.get("/class/{class_id}")
def get_assignments_by_class(class_id: int, db: Session = Depends(get_db)):
    return db.query(models.Assignment).filter(models.Assignment.class_id == class_id).all()

class AssignmentRequest(BaseModel):
    title: str
    description: str = ""
    due_date: str = None
    class_id: int

@router.post("/")
def create_assignment(assignment_data: AssignmentRequest, db: Session = Depends(get_db)):
    payload = assignment_data.dict()
    if payload.get('due_date'):
        try:
            payload['due_date'] = datetime.fromisoformat(payload['due_date'])
        except Exception:
            payload['due_date'] = None
    db_assignment = models.Assignment(**payload)
    db.add(db_assignment)
    db.commit()
    db.refresh(db_assignment)
    return db_assignment

@router.delete("/{assignment_id}")
def delete_assignment(assignment_id: int, db: Session = Depends(get_db)):
    assignment = db.query(models.Assignment).filter(models.Assignment.id == assignment_id).first()
    if not assignment:
        raise HTTPException(status_code=404, detail="Assignment not found")
    db.delete(assignment)
    db.commit()
    return {"message": "Assignment deleted"}

@router.put("/{assignment_id}")
def update_assignment(assignment_id: int, assignment_data: AssignmentRequest, db: Session = Depends(get_db)):
    assignment = db.query(models.Assignment).filter(models.Assignment.id == assignment_id).first()
    if not assignment:
        raise HTTPException(status_code=404, detail="Assignment not found")
    for key, value in assignment_data.dict().items():
        if key == 'due_date' and value:
            try:
                value = datetime.fromisoformat(value)
            except Exception:
                value = None
        setattr(assignment, key, value)
    db.commit()
    db.refresh(assignment)
    return assignment
