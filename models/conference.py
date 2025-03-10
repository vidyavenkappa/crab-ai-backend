from sqlalchemy import Column, Integer, String, ForeignKey, Text, DateTime, ARRAY
from sqlalchemy.orm import relationship
from database.db import Base
from datetime import datetime

class Conference(Base):
    __tablename__ = "conferences"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    guidelines = Column(Text, nullable=True)

    # Relationship with conference papers
    conference_papers = relationship("ConferencePaper", back_populates="conference", cascade="all, delete-orphan")
    
class ConferencePaper(Base):
    __tablename__ = "conference_papers"

    id = Column(Integer, primary_key=True, index=True)
    paper_id = Column(Integer, nullable=False)
    title = Column(String, nullable=False)
    conference_id = Column(Integer, ForeignKey("conferences.id", ondelete="CASCADE"), nullable=False)
    summary = Column(Text, nullable=True)
    review_claude = Column(Text, nullable=True)
    review_gemini = Column(Text, nullable=True)
    review_openai = Column(Text, nullable=True)
    review_perplexity = Column(Text, nullable=True)
    review_deepseek = Column(Text, nullable=True)
    status = Column(String, default="Pending")
    human_review = Column(Text, nullable=True)
    reviewer_name = Column(String, nullable=True)
    reviewer_id = Column(Integer, ForeignKey("users.id", ondelete="SET NULL"), nullable=True)
    date_of_review = Column(DateTime, default=datetime.utcnow)
    final_decision = Column(String, nullable=True)
    year = Column(Integer, nullable=False)

    conference = relationship("Conference", back_populates="conference_papers")
    reviewer = relationship("User", back_populates="reviews")  # This ensures proper linking
