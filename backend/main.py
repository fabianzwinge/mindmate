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
FRONTEND_URL = os.getenv("FRONTEND_URL", "http://127.0.0.1:3000")

if ENVIRONMENT == "production":
    allowed_origins = [FRONTEND_URL]
    same_site_setting = "none"   
    https_only = True             
    secure_flag = True     
else:
    allowed_origins = [
        "http://127.0.0.1:3000",
        "http://127.0.0.1:8000",
        "http://localhost:3000",
        "http://localhost:8000"
    ]
    same_site_setting = "lax"     
    https_only = False            
    secure_flag = False    

app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
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
    same_site=same_site_setting,  
    https_only=https_only,        
    secure=secure_flag   
)

app.include_router(chat_router)
app.include_router(spotify_router)

@app.get("/")
def root():
    return {
        "message": "MindMate Backend API", 
        "environment": ENVIRONMENT,
        "frontend_url": FRONTEND_URL,
        "cookie_config": {
            "same_site": same_site_setting,
            "https_only": https_only,
            "secure": secure_flag
        }
    }