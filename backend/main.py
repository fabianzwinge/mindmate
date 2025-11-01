import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.sessions import SessionMiddleware
from routers.auth_router import router as auth_router


app = FastAPI(host="0.0.0.0", port=8000)

# CORS konfigurieren, damit das Frontend zugreifen kann
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # später besser nur die Frontend-URL eintragen
    allow_methods=["*"],
    allow_headers=["*"],
)
app.add_middleware(
    SessionMiddleware, 
    secret_key=os.getenv("SESSION_SECRET"), 
    same_site="lax"
)
app.include_router(auth_router)

@app.get("/api/hello")
def read_root():
    return {"message": "Hello from Python backend!"}

