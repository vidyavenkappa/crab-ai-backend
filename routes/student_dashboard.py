from fastapi import APIRouter, Depends, HTTPException, UploadFile, File,Form
from sqlalchemy.orm import Session
from database.db import get_db
from models.paper import Paper
from models.user import User
from utils.gemini import validate_paper_with_gemini
import shutil
import os

router = APIRouter()

UPLOAD_FOLDER = "uploads"

# Ensure upload folder exists
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

@router.get("/students/{student_id}/papers")
def get_student_papers(student_id: int, db: Session = Depends(get_db)):
    """
    Fetch all papers uploaded by a student.
    """
    papers = db.query(Paper).filter(Paper.author_id == student_id).all()
    if not papers:
        raise HTTPException(status_code=404, detail="No papers found")
    return papers


@router.post("/students/{student_id}/upload")
async def upload_paper(student_id: int, conference: str = Form(...), file: UploadFile = File(...), db: Session = Depends(get_db)):
    """
    Upload a paper and validate it using Gemini API.
    """
    file_path = os.path.join(UPLOAD_FOLDER, file.filename)
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    # Validate the paper with Gemini API
    # validation_result = validate_paper_with_gemini(file_path)

    new_paper = Paper(
        title=file.filename,
        author_id=student_id,
        conference=conference,
        file_path=file_path,
        # review=validation_result["summary"],
        # score=validation_result["score"],
        status="In Review"
    )
    db.add(new_paper)
    db.commit()
    db.refresh(new_paper)

    # file_path = os.path.join(UPLOAD_FOLDER, file.filename)
    # with open(file_path, "wb") as buffer:
    #     shutil.copyfileobj(file.file, buffer)

    # new_paper = Paper(
    #     title=file.filename,
    #     author_id=student_id,
    #     conference=conference,
    #     file_path=file_path,
    #     status="In Review"
    # )
    # db.add(new_paper)
    # db.commit()
    # db.refresh(new_paper)
    return {"message": "Paper uploaded successfully", "paper_id": new_paper.id}
    # return {"message": "Paper uploaded successfully", "paper_id": new_paper.id,"validation": validation_result}
 


@router.delete("/students/{student_id}/papers/{paper_id}")
def delete_paper(student_id: int, paper_id: int, db: Session = Depends(get_db)):
    """
    Delete a student's paper and its associated file.
    """
    paper = db.query(Paper).filter(Paper.id == paper_id, Paper.author_id == student_id).first()
    
    if not paper:
        raise HTTPException(status_code=404, detail="Paper not found")  # ✅ Return 404 if paper doesn't exist
    
    # ✅ Check if file exists before deleting
    if paper.file_path and os.path.exists(paper.file_path):
        try:
            os.remove(paper.file_path)  # Remove the actual file
        except Exception as e:
            print(f"Error deleting file: {e}")  # ✅ Log error instead of crashing

    db.delete(paper)
    db.commit()
    
    return {"message": "Paper deleted successfully"}


@router.get("/students/{student_id}/papers/{paper_id}")
def get_paper_details(student_id: int, paper_id: int, db: Session = Depends(get_db)):
    """
    Get details of a specific paper.
    """
    paper = db.query(Paper).filter(Paper.id == paper_id, Paper.author_id == student_id).first()
    if not paper:
        raise HTTPException(status_code=404, detail="Paper not found")
    
    return paper
