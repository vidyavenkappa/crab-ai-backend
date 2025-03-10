from fastapi import APIRouter, Depends, HTTPException, UploadFile, File,Form
from sqlalchemy.orm import Session
from database.db import get_db
from models.paper import Paper
from models.user import User
from models.review import Review
from utils.gemini import generate_summary_using_gemini,get_student_reviews
import shutil
import os
from datetime import datetime

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

    # get summary and review from gemini
    summary_result = generate_summary_using_gemini(file_path)
    review_result = get_student_reviews(conference,file_path)
    
    try:
        score_arr = review_result["final_score"].split("/")
        new_paper = Paper(
            title=summary_result['title'],
            author_id=student_id,
            conference=conference,
            file_path=file_path,
            summary=summary_result['summary'],
            score=float(score_arr[0]),
            max_score = float(score_arr[1]),
            status=review_result['decision'] if review_result['decision'] else "Pending",
            date = datetime.today().date()
        )

        db.add(new_paper)
        db.commit()
        db.refresh(new_paper)

        print(review_result['review'][0])
        # Store the review in the Review model
        new_review = Review(
            paper_id=new_paper.id,
            content=review_result['review'][0].get("content",""),
            strengths=review_result['review'][0].get("strengths", []),
            weaknesses=review_result['review'][0].get("weaknesses", [])
        )
        
        db.add(new_review)
        db.commit()
        return {
            "message": "Paper uploaded successfully",
            "paper_id": new_paper.id
        }

    except Exception as e:
        db.rollback()  # ✅ Rollback to prevent database corruption
        print(f"Error in upload_paper: {e}")  # ✅ Log the error for debugging
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")

    finally:
        db.close()

@router.delete("/students/{student_id}/papers/{paper_id}")
def delete_paper(student_id: int, paper_id: int, db: Session = Depends(get_db)):
    """
    Delete a student's paper along with its associated reviews and file.
    """
    try:
        paper = db.query(Paper).filter(Paper.id == paper_id, Paper.author_id == student_id).first()
        
        if not paper:
            raise HTTPException(status_code=404, detail="Paper not found")
        
        # Delete associated reviews first
        db.query(Review).filter(Review.paper_id == paper_id).delete(synchronize_session=False)
        db.commit()
        
        # Check if file exists before deleting
        if paper.file_path and os.path.exists(paper.file_path):
            try:
                os.remove(paper.file_path)  # Remove the actual file
            except Exception as e:
                print(f"Error deleting file: {e}")  # Log error instead of crashing
        
        db.delete(paper)
        db.commit()
        
        return {"message": "Paper and associated reviews deleted successfully"}

    except Exception as e:
        db.rollback()  # ✅ Rollback to prevent database corruption
        print(f"Error in upload_paper: {e}")  # ✅ Log the error for debugging
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")

    finally:
        db.close()


@router.get("/students/{student_id}/papers/{paper_id}")
def get_paper_details(student_id: int, paper_id: int, db: Session = Depends(get_db)):
    """
    Get details of a specific paper.
    """

    paper = db.query(Paper).filter(Paper.id == paper_id, Paper.author_id == student_id).first()
    
    if not paper:
        raise HTTPException(status_code=404, detail="Paper not found")
    
    reviews = db.query(Review).filter(Review.paper_id == paper_id).all()
    
    return {"paper": paper, "reviews": reviews}
