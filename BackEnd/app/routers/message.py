from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel
from datetime import datetime
from ..database import get_db
from .. import models
from ..deps import get_api_token

router = APIRouter(prefix="/messages", tags=["messages"])

class MessageRequest(BaseModel):
    sender_id: int
    receiver_id: int
    content: str

@router.post("/")
def send_message(msg: MessageRequest, db: Session = Depends(get_db)):
    message = models.Message(
        sender_id=msg.sender_id,
        receiver_id=msg.receiver_id,
        content=msg.content,
        timestamp=datetime.now()
    )
    db.add(message)
    db.commit()
    db.refresh(message)
    return message

@router.get("/")
def get_messages(sender_id: int, receiver_id: int, db: Session = Depends(get_db)):
    return db.query(models.Message).filter(
        ((models.Message.sender_id == sender_id) & (models.Message.receiver_id == receiver_id)) |
        ((models.Message.sender_id == receiver_id) & (models.Message.receiver_id == sender_id))
    ).order_by(models.Message.timestamp.asc()).all()


@router.post("/{message_id}/mark-read", dependencies=[Depends(get_api_token)])
def mark_message_read(message_id: int, db: Session = Depends(get_db)):
    message = db.query(models.Message).filter(models.Message.id == message_id).first()
    if not message:
        raise HTTPException(status_code=404, detail="Message not found")
    message.is_read = 1
    db.add(message)
    db.commit()
    return {"status": "ok", "message_id": message_id}
