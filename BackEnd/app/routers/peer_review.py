from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from datetime import datetime
from pydantic import BaseModel
from typing import List, Optional

from ..database import get_db
from ..models import PeerReview, Score, Assignment, User
from ..deps import get_api_token

router = APIRouter(prefix="/peer-reviews", tags=["peer-reviews"])

# Schemas
class PeerReviewCreate(BaseModel):
    reviewer_id: int
    submission_id: int
    rating: int  # 1-5
    comment: Optional[str] = None

class PeerReviewUpdate(BaseModel):
    rating: int
    comment: Optional[str] = None

class PeerReviewResponse(BaseModel):
    id: int
    reviewer_id: int
    submission_id: int
    rating: int
    comment: Optional[str]
    created_at: Optional[datetime]

    class Config:
        from_attributes = True

# GET all peer reviews for a submission
@router.get("", response_model=List[PeerReviewResponse])
def get_peer_reviews(
    submission_id: Optional[int] = Query(None),
    assignment_id: Optional[int] = Query(None),
    db: Session = Depends(get_db)
):
    """Get peer reviews - filter by submission_id or assignment_id"""
    query = db.query(PeerReview)
    
    if submission_id:
        query = query.filter(PeerReview.submission_id == submission_id)
    
    if assignment_id:
        # Get all scores for this assignment, then their reviews
        scores = db.query(Score).filter(Score.assignment_id == assignment_id).all()
        score_ids = [s.id for s in scores]
        query = query.filter(PeerReview.submission_id.in_(score_ids))
    
    return query.all()

# GET single peer review
@router.get("/{review_id}", response_model=PeerReviewResponse)
def get_peer_review(review_id: int, db: Session = Depends(get_db)):
    """Get single peer review by ID"""
    review = db.query(PeerReview).filter(PeerReview.id == review_id).first()
    if not review:
        raise HTTPException(status_code=404, detail="Peer review not found")
    return review

# CREATE peer review
@router.post("", response_model=PeerReviewResponse)
def create_peer_review(
    review: PeerReviewCreate,
    db: Session = Depends(get_db),
    token: str = Depends(get_api_token)
):
    """Create a new peer review"""
    # Check if submission exists
    submission = db.query(Score).filter(Score.id == review.submission_id).first()
    if not submission:
        raise HTTPException(status_code=404, detail="Submission not found")
    
    # Check if reviewer exists
    reviewer = db.query(User).filter(User.id == review.reviewer_id).first()
    if not reviewer:
        raise HTTPException(status_code=404, detail="Reviewer not found")
    
    # Check if reviewer is not the same as submitter
    if review.reviewer_id == submission.user_id:
        raise HTTPException(status_code=400, detail="Cannot review your own submission")
    
    # Validate rating
    if review.rating < 1 or review.rating > 5:
        raise HTTPException(status_code=400, detail="Rating must be between 1 and 5")
    
    # Check if already reviewed
    existing = db.query(PeerReview).filter(
        PeerReview.reviewer_id == review.reviewer_id,
        PeerReview.submission_id == review.submission_id
    ).first()
    if existing:
        raise HTTPException(status_code=400, detail="Already reviewed this submission")
    
    new_review = PeerReview(
        reviewer_id=review.reviewer_id,
        submission_id=review.submission_id,
        rating=review.rating,
        comment=review.comment,
        created_at=datetime.now()
    )
    db.add(new_review)
    db.commit()
    db.refresh(new_review)
    return new_review

# UPDATE peer review
@router.put("/{review_id}", response_model=PeerReviewResponse)
def update_peer_review(
    review_id: int,
    review_update: PeerReviewUpdate,
    db: Session = Depends(get_db),
    token: str = Depends(get_api_token)
):
    """Update a peer review"""
    review = db.query(PeerReview).filter(PeerReview.id == review_id).first()
    if not review:
        raise HTTPException(status_code=404, detail="Peer review not found")
    
    # Validate rating
    if review_update.rating < 1 or review_update.rating > 5:
        raise HTTPException(status_code=400, detail="Rating must be between 1 and 5")
    
    review.rating = review_update.rating
    if review_update.comment is not None:
        review.comment = review_update.comment
    
    db.commit()
    db.refresh(review)
    return review

# DELETE peer review
@router.delete("/{review_id}")
def delete_peer_review(
    review_id: int,
    db: Session = Depends(get_db),
    token: str = Depends(get_api_token)
):
    """Delete a peer review"""
    review = db.query(PeerReview).filter(PeerReview.id == review_id).first()
    if not review:
        raise HTTPException(status_code=404, detail="Peer review not found")
    
    db.delete(review)
    db.commit()
    return {"message": "Peer review deleted successfully"}

# GET average rating for a submission
@router.get("/submission/{submission_id}/average-rating")
def get_average_rating(submission_id: int, db: Session = Depends(get_db)):
    """Get average rating for a submission"""
    reviews = db.query(PeerReview).filter(PeerReview.submission_id == submission_id).all()
    if not reviews:
        return {"average_rating": 0, "count": 0}
    
    avg = sum(r.rating for r in reviews) / len(reviews)
    return {"average_rating": round(avg, 2), "count": len(reviews)}
