import os
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.sessions import SessionMiddleware
from routers.spotify_router import router as spotify_router
from routers.chat_router import router as chat_router
from dotenv import load_dotenv

load_dotenv()

app = FastAPI()

ENVIRONMENT = os.getenv("ENVIRONMENT", "development")
FRONTEND_URL = os.getenv("FRONTEND_URL", "http://localhost:3000")

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://127.0.0.1:3000",  
        "http://127.0.0.1:8000",
    ],
    allow_credentials=True, 
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    allow_headers=["*"],
    expose_headers=["*"]
)

app.add_middleware(
    SessionMiddleware, 
    secret_key=os.getenv("SESSION_SECRET", "your-super-secret-development-key-12345"),
    session_cookie="mindmate_session", 
    max_age=7 * 24 * 60 * 60,  
    same_site="lax" 
)

app.include_router(chat_router)
app.include_router(spotify_router)

@app.get("/")
def root():
    return {"message": "MindMate Backend API", "environment": ENVIRONMENT}