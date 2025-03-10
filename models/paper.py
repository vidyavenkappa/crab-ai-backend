from sqlalchemy import Column, Integer, String, ForeignKey, Text, DateTime,Float
from sqlalchemy.orm import relationship
from database.db import Base
from datetime import datetime

class Paper(Base):
    __tablename__ = "papers"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    author_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    conference = Column(String, nullable=False)
    file_path = Column(String, nullable=False)
    summary = Column(Text, default="No summary available")
    score = Column(Float, default=0)
    max_score = Column(Float, default=10)
    status = Column(String, default="Pending")  # "Accepted" or "Rejected"
    date = Column(DateTime, default=datetime.utcnow)  # Timestamp for upload
   
    # Relationship to reviews
    reviews = relationship("Review", back_populates="paper", cascade="all, delete-orphan")