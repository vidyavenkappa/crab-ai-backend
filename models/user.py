from sqlalchemy import Column, Integer, String, Enum, ForeignKey
from sqlalchemy.orm import relationship
from database.db import Base
import enum

class UserRole(str, enum.Enum):
    STUDENT = "student"
    REVIEWER = "reviewer"

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    password = Column(String)
    role = Column(Enum(UserRole))
    conference = Column(String, nullable=True)

    # # Relationship with papers
    # papers = relationship("Paper", back_populates="owner", foreign_keys="[Paper.owner_id]")