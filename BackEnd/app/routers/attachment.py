from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form
from sqlalchemy.orm import Session
from pydantic import BaseModel
from ..database import get_db
from .. import models
import shutil
import os

router = APIRouter(prefix="/attachments", tags=["attachments"])
UPLOAD_DIR = "uploaded_files"
os.makedirs(UPLOAD_DIR, exist_ok=True)

class AttachmentResponse(BaseModel):
    id: int
    filename: str
    file_url: str
    uploaded_by: int
    assignment_id: int
    is_submission: int

@router.post("/upload", response_model=AttachmentResponse)
def upload_attachment(
    file: UploadFile = File(...),
    uploaded_by: int = Form(...),
    assignment_id: int = Form(...),
    is_submission: int = Form(0),
    db: Session = Depends(get_db)
):
    file_path = os.path.join(UPLOAD_DIR, file.filename)
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    file_url = f"/{UPLOAD_DIR}/{file.filename}"
    attachment = models.Attachment(
        filename=file.filename,
        file_url=file_url,
        uploaded_by=uploaded_by,
        assignment_id=assignment_id,
        is_submission=is_submission
    )
    db.add(attachment)
    db.commit()
    db.refresh(attachment)
    return attachment

@router.get("/assignment/{assignment_id}")
def get_attachments_by_assignment(assignment_id: int, db: Session = Depends(get_db)):
    return db.query(models.Attachment).filter(models.Attachment.assignment_id == assignment_id).all()

@router.get("/{attachment_id}")
def get_attachment(attachment_id: int, db: Session = Depends(get_db)):
    attachment = db.query(models.Attachment).filter(models.Attachment.id == attachment_id).first()
    if not attachment:
        raise HTTPException(status_code=404, detail="Attachment not found")
    return attachment
