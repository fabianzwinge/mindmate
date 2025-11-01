import re
import os, secrets, httpx, base64
from fastapi import APIRouter, Request, Response, HTTPException
from urllib.parse import urlencode
from dotenv import load_dotenv

load_dotenv()

SPOTIFY_CLIENT_ID = os.getenv("SPOTIFY_CLIENT_ID")
SPOTIFY_CLIENT_SECRET = os.getenv("SPOTIFY_CLIENT_SECRET")
SPOTIFY_REDIRECT_URI = os.getenv("SPOTIFY_REDIRECT_URI")
SESSION_SECRET = os.getenv("SESSION_SECRET", secrets.token_urlsafe(32))

SPOTIFY_AUTH = "https://accounts.spotify.com/authorize?"
SPOTIFY_TOKEN= "https://accounts.spotify.com/api/token"
SPOTIFY_ME= "https://api.spotify.com/v1/me"

router = APIRouter()

STATE_KEY = "spotify_auth_state"

@router.get("/login")
async def login(request: Request):
    state = secrets.token_urlsafe(16)
    request.session[STATE_KEY] = state
    params = {
        "response_type": "code",
        "client_id": SPOTIFY_CLIENT_ID,
        "scope": "user-read-email user-read-private playlist-modify-private playlist-modify-public",
        "redirect_uri": SPOTIFY_REDIRECT_URI,
        "state": state,
        "show_dialog": "true"
    }
    
    return Response(status_code=302, headers={"Location": f"{SPOTIFY_AUTH}{urlencode(params)}"})

@router.get("/callback")
async def callback(request: Request, code: str | None = None, state: str | None = None):
    if not code or not state:
        raise HTTPException(400, "missing code or state")
    if state != request.session.get(STATE_KEY):
        raise HTTPException(400, "invalid state")
    request.session.pop(STATE_KEY, None)

    data = {
        "grant_type": "authorization_code",
        "code": code,
        "redirect_uri": SPOTIFY_REDIRECT_URI
    }

    headers = {
        "Content-Type": "application/x-www-form-urlencoded",
        "Authorization": f"Basic {base64.b64encode(f'{SPOTIFY_CLIENT_ID}:{SPOTIFY_CLIENT_SECRET}'.encode()).decode()}"
    }

    async with httpx.AsyncClient() as c:
        res = await c.post(SPOTIFY_TOKEN, data=data, headers=headers)
    if res.status_code != 200:
        raise HTTPException(400, f"token exchange failed: {res.text}")
    
    access_token = res.json()["access_token"]

    request.session["access_token"] = access_token

    return Response(status_code=302, headers={"Location": "http://127.0.0.1:3000/"}) 

@router.get("/playlists")
async def get_playlists(request: Request):
    access_token = request.session.get("access_token")
    if not access_token:
        raise HTTPException(401, "not authenticated")

    url = "https://api.spotify.com/v1/me/playlists"
    headers = {"Authorization": f"Bearer {access_token}"}

    async with httpx.AsyncClient() as c:
        r = await c.get(url, headers=headers)

    if r.status_code != 200:
        raise HTTPException(r.status_code, r.text)

    return Response(content=r.text, media_type="application/json")