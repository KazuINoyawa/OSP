from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel
from ..database import get_db
from .. import models

router = APIRouter(prefix="/scores", tags=["scores"])

@router.get("/")
def get_scores(db: Session = Depends(get_db)):
    return db.query(models.Score).all()

@router.get("/student/{user_id}")
def get_scores_by_student(user_id: int, db: Session = Depends(get_db)):
    return db.query(models.Score).filter(models.Score.user_id == user_id).all()

@router.get("/assignment/{assignment_id}")
def get_scores_by_assignment(assignment_id: int, db: Session = Depends(get_db)):
    return db.query(models.Score).filter(models.Score.assignment_id == assignment_id).all()

class ScoreRequest(BaseModel):
    user_id: int
    assignment_id: int
    score: float

@router.post("/")
def create_score(score_data: ScoreRequest, db: Session = Depends(get_db)):
    db_score = models.Score(**score_data.dict())
    db.add(db_score)
    db.commit()
    db.refresh(db_score)
    return db_score

@router.put("/{score_id}")
def update_score(score_id: int, score_data: ScoreRequest, db: Session = Depends(get_db)):
    db_score = db.query(models.Score).filter(models.Score.id == score_id).first()
    if not db_score:
        raise HTTPException(status_code=404, detail="Score not found")
    db_score.user_id = score_data.user_id
    db_score.assignment_id = score_data.assignment_id
    db_score.score = score_data.score
    db.commit()
    db.refresh(db_score)
    return db_score
