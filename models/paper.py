from sqlalchemy import Column, Integer, String, ForeignKey, Text, Boolean
from sqlalchemy.orm import relationship
from database.db import Base

class Paper(Base):
    __tablename__ = "papers"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    author_id = Column(Integer, ForeignKey("users.id"))
    conference = Column(String)
    file_path = Column(String)
    review = Column(Text, default="Pending Review")
    summary = Column(Text, default="No summary available")
    score = Column(Integer, default=0)
    status = Column(String, default="Pending")  # "Accepted" or "Rejected"
    
