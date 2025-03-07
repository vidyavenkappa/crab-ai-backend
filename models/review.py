from sqlalchemy import Column, Integer, String, ForeignKey, ARRAY,Text
from sqlalchemy.orm import relationship
from database.db import Base

class Review(Base):
    __tablename__ = "reviews"

    id = Column(Integer, primary_key=True, index=True)
    paper_id = Column(Integer, ForeignKey("papers.id", ondelete="CASCADE"), nullable=False)
    content = Column(String, nullable=False)
    strengths = Column(ARRAY(Text), default=[])  # Stored as an array of text
    weaknesses = Column(ARRAY(Text), default=[])  # Stored as an array of text

    paper = relationship("Paper", back_populates="reviews")
