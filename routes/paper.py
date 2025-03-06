from fastapi import APIRouter, UploadFile, File, Depends
from sqlalchemy.orm import Session
from database.db import SessionLocal
from models.paper import Paper

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/upload_paper")
def upload_paper(author_id: int, conference: str, file: UploadFile = File(...), db: Session = Depends(get_db)):
    file_path = f"uploads/{file.filename}"
    with open(file_path, "wb") as buffer:
        buffer.write(file.file.read())

    paper = Paper(title=file.filename, author_id=author_id, conference=conference, file_path=file_path)
    db.add(paper)
    db.commit()
    return {"message": "Paper uploaded successfully"}

@router.get("/papers/{conference}")
def get_papers(conference: str, db: Session = Depends(get_db)):
    papers = db.query(Paper).filter(Paper.conference == conference).all()
    return papers
