from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from database.db import get_db
from models.user import User, UserRole
from pydantic import BaseModel, validator, constr
import bcrypt
from logging_config import logger  # Import the logger
from typing import Optional
from utils.auth import create_access_token

router = APIRouter()

class UserSignup(BaseModel):
    username: constr(min_length=3, max_length=50)  # Constrained string
    password: constr(min_length=6, max_length=100)  # Constrained string
    role: UserRole  # Ensures only valid enum values
    conference:  Optional[str] = None

    @validator('username')
    def validate_username(cls, v):
        v = v.strip()  # Remove whitespace
        if not v:
            raise ValueError('Username cannot be empty')
        if not v.replace('_', '').isalnum():
            raise ValueError('Username must be alphanumeric (can include underscores)')
        return v


    @validator('conference', always=True)
    def validate_conference(cls, v, values):
        # If role is reviewer, conference is required
        if values.get('role') == UserRole.REVIEWER and not v:
            raise ValueError('Conference is required for reviewers')
        return v

class UserLogin(BaseModel):
    username: constr(min_length=3, max_length=50)
    password: constr(min_length=6, max_length=100)

    @validator('username')
    def username_not_empty(cls, v):
        if not v or len(v.strip()) == 0:
            raise ValueError('Username cannot be empty')
        return v.strip()

    @validator('password')
    def password_not_empty(cls, v):
        if not v or len(v.strip()) == 0:
            raise ValueError('Password cannot be empty')
        return v



@router.post("/signup")
def signup(user: UserSignup, db: Session = Depends(get_db)):
    try:
        # Log signup attempt
        logger.info(f"Signup attempt for username: {user.username}")

        # Check if user exists
        existing_user = db.query(User).filter(User.username == user.username).first()
        if existing_user:
            logger.warning(f"Signup attempt with existing username: {user.username}")
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, 
                detail="Username already exists"
            )

        # Hash password
        hashed_password = bcrypt.hashpw(user.password.encode('utf-8'), bcrypt.gensalt())

        # Create new user
        new_user = User(
            username=user.username, 
            password=hashed_password.decode('utf-8'), 
            role=user.role,
            conference=user.conference
        )

        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        
        logger.info(f"User {user.username} created successfully")
        return {"message": "User created successfully"}

    except HTTPException:
        # Re-raise HTTP exceptions
        raise
    except Exception as e:
        # Log unexpected errors
        logger.error(f"Unexpected error during signup: {str(e)}", exc_info=True)
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, 
            detail="An unexpected error occurred"
        )

@router.post("/login")
def login(user: UserLogin, db: Session = Depends(get_db)):
    try:
        # Log the incoming username for debugging
        logger.info(f"Login attempt for username: {user.username}")

        # Find user
        db_user = db.query(User).filter(User.username == user.username).first()
        
        if not db_user:
            logger.warning(f"Login attempt with non-existent username: {user.username}")
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED, 
                detail="Invalid credentials"
            )

        # Verify password
        if not bcrypt.checkpw(user.password.encode('utf-8'), db_user.password.encode('utf-8')):
            logger.warning(f"Failed login attempt for username: {user.username}")
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED, 
                detail="Invalid credentials"
            )


        logger.info(f"Successful login for username: {user.username}")
        # Create access token
        access_token = create_access_token(
            data={"sub": db_user.username}
        )

        return {
            "access_token": access_token, 
            "token_type": "bearer", 
            "role": db_user.role
        }

    except HTTPException:
        # Re-raise HTTP exceptions
        raise
    except Exception as e:
        # Log unexpected errors
        logger.error(f"Unexpected error during login: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, 
            detail="An unexpected error occurred"
        )



