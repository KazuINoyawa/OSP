from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel
from ..database import get_db
from .. import models

router = APIRouter(prefix="/auth", tags=["auth"])

class LoginRequest(BaseModel):
    username: str
    password: str

@router.post("/login")
def login(data: LoginRequest, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.username == data.username).first()
    if not user or user.hashed_password != data.password:
        raise HTTPException(status_code=401, detail="Sai tài khoản hoặc mật khẩu")
    return {
        "id": user.id,
        "username": user.username,
        "full_name": user.full_name,
        "role": user.role
    }
