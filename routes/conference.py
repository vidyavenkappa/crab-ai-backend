from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database.db import get_db
from models.conference import Conference
from models.user import User
from pydantic import BaseModel

router = APIRouter()

class GuidelinesRequest(BaseModel):
    user_id: int
    conference_id: str
    text: str



@router.get("/get-list")
def get_conference_names(db: Session = Depends(get_db)):
    """Fetch a list of all conference names and their IDs."""
    conferences = db.query(Conference.id, Conference.name).all()
    if not conferences:
        raise HTTPException(status_code=404, detail="No conferences found")
    result = []
    for conference in conferences :
        result.append({"value": conference.id, "label": conference.name})
    return result


@router.post("/upload_guidelines")
def upload_guidelines(payload: GuidelinesRequest, db: Session = Depends(get_db)):
    """Upload or update conference guidelines as text."""
    reviewer = db.query(User).filter(User.id == payload.user_id, User.role == "reviewer").first()
    if not reviewer:
        raise HTTPException(status_code=403, detail="User not authorized")
    
    conference = db.query(Conference).filter(Conference.id == payload.conference_id).first()
    if not conference:
        raise HTTPException(status_code=404, detail="Conference not found")
    
    conference.guidelines = payload.text  # Directly save input text
    db.commit()
    
    return {"message": "Guidelines uploaded successfully"}
