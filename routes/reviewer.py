from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
from sqlalchemy.orm import Session
from database.db import get_db
from models.conference import Conference, ConferencePaper
from models.user import User
from datetime import datetime
import shutil
import os

router = APIRouter()
UPLOAD_FOLDER = "uploads/guidelines"
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)



@router.get("/reviewer/papers")
def get_conference_papers(user_id: int, conference_id: int, db: Session = Depends(get_db)):
    """Fetch all papers for the specified conference and year where the reviewer is assigned."""
    reviewer = db.query(User).filter(User.id == user_id, User.role == "reviewer").first()
    if not reviewer:
        raise HTTPException(status_code=403, detail="User not authorized")
    
    current_year = datetime.utcnow().year
    conference = db.query(Conference).filter(Conference.id == conference_id, Conference.year == current_year).first()
    if not conference:
        raise HTTPException(status_code=404, detail="Conference not found for the current year")
    
    papers = db.query(ConferencePaper).filter(ConferencePaper.conference_id == conference.id).all()
    return papers

@router.post("/reviewer/review_paper")
def submit_review(user_id: int, conference_id: int, paper_id: int, review_text: str, status: str, db: Session = Depends(get_db)):
    """Submit a human review and update the paper status for a specific conference and year."""
    reviewer = db.query(User).filter(User.id == user_id, User.role == "reviewer").first()
    if not reviewer:
        raise HTTPException(status_code=403, detail="User not authorized")
    
    current_year = datetime.utcnow().year
    conference = db.query(Conference).filter(Conference.id == conference_id, Conference.year == current_year).first()
    if not conference:
        raise HTTPException(status_code=404, detail="Conference not found for the current year")
    
    paper = db.query(ConferencePaper).filter(ConferencePaper.id == paper_id, ConferencePaper.conference_id == conference.id).first()
    if not paper:
        raise HTTPException(status_code=404, detail="Paper not found")
    
    paper.human_review = review_text
    paper.status = status
    paper.reviewer_id = reviewer.id
    paper.reviewer_name = reviewer.name
    paper.date_of_review = datetime.utcnow()
    db.commit()
    return {"message": "Review submitted successfully", "paper_id": paper.id}
