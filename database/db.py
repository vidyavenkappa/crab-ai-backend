import os
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# SQLite database URL
DATABASE_URL = os.getenv("DATABASE_URL")

if not DATABASE_URL:
    raise ValueError("DATABASE_URL is not set in environment variables!")

# Ensure the correct format for PostgreSQL
if DATABASE_URL.startswith("postgres://"):
    DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql://", 1)



# Create PostgreSQL URL from Render environment variables
engine = create_engine(DATABASE_URL)

# Create SessionLocal class
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create Base class for declarative models
Base = declarative_base()

# Dependency to get database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Import models to ensure they're registered
def init_models():
    from models.user import User
    from models.paper import Paper  # Ensure this import is here
    from models.review import Review
    from models.conference import Conference  # Ensure this import is here
    from models.conference import ConferencePaper
    
    # Create all tables
    Base.metadata.create_all(bind=engine)

# Call this before starting the application
init_models()