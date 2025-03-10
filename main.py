from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2PasswordBearer

import uvicorn
from logging_config import logger
from dotenv import load_dotenv
import os 


from routes.user import router as user_router
from routes.conference import router as conference_router
from routes.student_dashboard import router as student_router
from routes.reviewer import router as reviewer_router


# Load environment variables
load_dotenv()


app = FastAPI()

# CORS Configuration
app.add_middleware(
    CORSMiddleware,
    #allow_origins=["http://localhost:3000"],
    allow_origins=["https://crabai.vercel.app"],
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

# Log application startup
logger.info("CRAB.AI Backend Application Starting...")

# Include routers
app.include_router(user_router, prefix="/users", tags=["users"])
app.include_router(conference_router, prefix="/conference", tags=["conference"])
app.include_router(conference_router, prefix="/reviewer", tags=["reviewer"])
app.include_router(student_router, prefix="/api", tags=["student"])

# OAuth2 scheme
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

@app.get("/health")
def health_check():
    return {"status": "healthy"}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=10000)
