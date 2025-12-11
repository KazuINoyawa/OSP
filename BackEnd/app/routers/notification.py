from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel
from datetime import datetime
from ..database import get_db
from .. import models
from ..deps import get_api_token

router = APIRouter(prefix="/notifications", tags=["notifications"])


class NotificationCreate(BaseModel):
    user_id: int
    title: str
    message: str | None = None
    class_name: str | None = None


@router.get("/")
def list_notifications(user_id: int, limit: int = 10, db: Session = Depends(get_db)):
    return db.query(models.Notification).filter(models.Notification.user_id == user_id).order_by(models.Notification.timestamp.desc()).limit(limit).all()


@router.post("/{notification_id}/mark-read", dependencies=[Depends(get_api_token)])
def mark_notification_read(notification_id: int, db: Session = Depends(get_db)):
    notif = db.query(models.Notification).filter(models.Notification.id == notification_id).first()
    if not notif:
        raise HTTPException(status_code=404, detail="Notification not found")
    notif.is_read = 1
    db.add(notif)
    db.commit()
    return {"status": "ok", "notification_id": notification_id}


@router.post("/mark-read-bulk", dependencies=[Depends(get_api_token)])
def mark_notifications_bulk(ids: list[int], db: Session = Depends(get_db)):
    items = db.query(models.Notification).filter(models.Notification.id.in_(ids)).all()
    for it in items:
        it.is_read = 1
        db.add(it)
    db.commit()
    return {"status": "ok", "marked": [i.id for i in items]}
