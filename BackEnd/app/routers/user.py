from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from pydantic import BaseModel
from ..database import get_db
from .. import models

router = APIRouter(prefix="/users", tags=["users"])

@router.get("/")
def get_users(q: str = Query(None, description="Tìm kiếm theo tên hoặc username"), db: Session = Depends(get_db)):
    query = db.query(models.User)
    if q:
        query = query.filter((models.User.username.ilike(f"%{q}%")) | (models.User.full_name.ilike(f"%{q}%")))
    return query.all()

class UserRequest(BaseModel):
    username: str
    password: str
    full_name: str
    role: str = "student"

@router.post("/")
def create_user(user: UserRequest, db: Session = Depends(get_db)):
    db_user = models.User(username=user.username, hashed_password=user.password, full_name=user.full_name, role=user.role)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

@router.delete("/{user_id}")
def delete_user(user_id: int, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    db.delete(user)
    db.commit()
    return {"message": "User deleted"}

@router.put("/{user_id}")
def update_user(user_id: int, user: UserRequest, db: Session = Depends(get_db)):
    db_user = db.query(models.User).filter(models.User.id == user_id).first()
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")
    db_user.username = user.username
    db_user.hashed_password = user.password
    db_user.full_name = user.full_name
    db_user.role = user.role
    db.commit()
    db.refresh(db_user)
    return db_user
