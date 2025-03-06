# from fastapi import FastAPI
# from fastapi.middleware.cors import CORSMiddleware
# from database.db import Base, engine
# from routes import user, paper

# # Initialize FastAPI app
# app = FastAPI()

# # Allow frontend requests
# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=["*"],
#     allow_credentials=True,
#     allow_methods=["*"],
#     allow_headers=["*"],
# )

# # Create database tables
# Base.metadata.create_all(bind=engine)

# # Include routes
# app.include_router(user.router, prefix="/users", tags=["Users"])
# app.include_router(paper.router, prefix="/papers", tags=["Papers"])

# @app.get("/")
# def home():
#     return {"message": "Welcome to C.R.A.B. AI"}


from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2PasswordBearer
from routes.user import router as user_router
from routes.paper import router as paper_router
import uvicorn
from logging_config import logger
from dotenv import load_dotenv
import os 

# Load environment variables
load_dotenv()


app = FastAPI()

# CORS Configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=os.getenv("CORS_ORIGINS", "").split(","),
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

# Log application startup
logger.info("CRAB.AI Backend Application Starting...")

# Include routers
app.include_router(user_router, prefix="/users", tags=["users"])
app.include_router(paper_router, prefix="/papers", tags=["papers"])

# OAuth2 scheme
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

@app.get("/health")
def health_check():
    return {"status": "healthy"}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
