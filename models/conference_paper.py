from sqlalchemy import Column, Integer, String, ForeignKey, Text, DateTime, JSON
from sqlalchemy.orm import relationship
from database.db import Base
from datetime import datetime

class ConferencePaper(Base):
    __tablename__ = "conference_papers"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    conference_id = Column(Integer, ForeignKey("conferences.id", ondelete="CASCADE"), nullable=False)
    summary = Column(JSON, nullable=True)
    review_claude = Column(JSON, nullable=True)
    review_gemini = Column(JSON, nullable=True)
    review_openai = Column(JSON, nullable=True)
    review_perplexity = Column(JSON, nullable=True)
    review_deepseek = Column(JSON, nullable=True)
    status = Column(String, default="Pending")
    human_review = Column(Text, nullable=True)
    reviewer_name = Column(String, nullable=True)
    reviewer_id = Column(Integer, ForeignKey("users.id", ondelete="SET NULL"), nullable=True)
    date_of_review = Column(DateTime, default=datetime.utcnow)
    final_decision = Column(String, nullable=True)
    year = Column(Integer, nullable=False)

    # FIX: Use string-based references
    conference = relationship("Conference", back_populates="conference_papers", lazy="joined")
    reviewer = relationship("User", back_populates="reviews", lazy="joined")
