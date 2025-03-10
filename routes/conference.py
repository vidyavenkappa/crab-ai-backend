from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
from sqlalchemy.orm import Session
from database.db import get_db
from models.conference import Conference

router = APIRouter()

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
