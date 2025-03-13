from sqlalchemy import Column, Integer, String, Text
from sqlalchemy.orm import relationship
from database.db import Base

class Conference(Base):
    __tablename__ = "conferences"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    guidelines = Column(Text, nullable=True)

    # FIX: Use string reference
    conference_papers = relationship("ConferencePaper", back_populates="conference", cascade="all, delete-orphan", lazy="joined")
