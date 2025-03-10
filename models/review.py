from sqlalchemy import Column, Integer, String, ForeignKey, Text, JSON
from sqlalchemy.orm import relationship
from database.db import Base

class Review(Base):
    __tablename__ = "reviews"

    id = Column(Integer, primary_key=True, index=True)
    paper_id = Column(Integer, ForeignKey("papers.id", ondelete="CASCADE"), nullable=False)
    final_score = Column(String, nullable=False)  # Stores "7/10"
    decision = Column(String, nullable=False)  # Stores "Accept" or "Reject"
    numerical_ratings = Column(JSON, nullable=False)  # Stores ratings as JSON
    structured_review = Column(JSON, nullable=False)  # Stores structured review as JSON
    actionable_feedback = Column(JSON, nullable=False)  # Stores improvement suggestions & checklist

    paper = relationship("Paper", back_populates="reviews")
