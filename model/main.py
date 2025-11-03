import os
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from routers.model_router import router as model_router
from dotenv import load_dotenv

load_dotenv()

app = FastAPI()

ENVIRONMENT = os.getenv("ENVIRONMENT")
BACKEND_URL = os.getenv("BACKEND_URL")

allowed_origins = [BACKEND_URL]

app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=False,
    allow_methods=["GET", "POST", "OPTIONS"],
    allow_headers=["*"],
    expose_headers=["*"]
)

app.include_router(model_router)

@app.get("/")
def root():
    return {
        "message": "MindMate Model Backend API",
        "environment": ENVIRONMENT,
        "backend_url": BACKEND_URL,
        "allowed_origins": allowed_origins
    }