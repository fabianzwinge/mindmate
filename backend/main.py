from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# CORS konfigurieren, damit das Frontend zugreifen kann
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # später besser nur die Frontend-URL eintragen
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/api/hello")
def read_root():
    return {"message": "Hello from Python backend!"}
