import os
from fastapi import APIRouter, HTTPException, Request
from fastapi.responses import RedirectResponse, HTMLResponse
from pydantic import BaseModel
from services.spotify_service import SpotifyService
from typing import Dict, Any
import logging

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/spotify")

class PlaylistRequest(BaseModel):
    mood: str
    tracks_count: int = 20

spotify_service = SpotifyService()

def get_frontend_url() -> str:
    """Get frontend URL based on environment"""
    return os.getenv("FRONTEND_URL", "http://localhost:3000")

def get_spotify_tokens(request: Request) -> Dict[str, str]:
    """Holt Spotify-Tokens aus der Session"""
    access_token = request.session.get("spotify_access_token")
    refresh_token = request.session.get("spotify_refresh_token")
    
    if not access_token:
        raise HTTPException(status_code=401, detail="Not authenticated with Spotify")
    
    return {
        "access_token": access_token,
        "refresh_token": refresh_token
    }

def refresh_token_if_needed(request: Request, tokens: Dict[str, str]) -> str:
    """Erneuert Token falls nötig und gibt gültigen Access Token zurück"""
    try:
        # Test if token is still valid
        spotify_service.get_user_profile(tokens["access_token"])
        return tokens["access_token"]
    except HTTPException:
        # Token expired, try refresh
        if not tokens.get("refresh_token"):
            logger.warning("Access token expired and no refresh token available")
            raise HTTPException(status_code=401, detail="Token expired and no refresh token available")
        
        try:
            logger.info("Refreshing access token")
            new_tokens = spotify_service.refresh_access_token(tokens["refresh_token"])
            request.session["spotify_access_token"] = new_tokens["access_token"]

            if "refresh_token" in new_tokens:
                request.session["spotify_refresh_token"] = new_tokens["refresh_token"]
            
            return new_tokens["access_token"]
        except Exception as e:
            logger.error(f"Failed to refresh token: {e}")
            raise HTTPException(status_code=401, detail="Failed to refresh token")

@router.post("/generatePlaylist")
async def generate_playlist(playlist_request: PlaylistRequest, request: Request):
    """
    Generiert eine Spotify-Playlist. 
    Handhabt automatisch Authentifizierung und Token-Refresh.
    """
    try:
        logger.info(f"Generating playlist for mood: {playlist_request.mood}")
        
        # Versuche Tokens zu holen
        try:
            tokens = get_spotify_tokens(request)
            access_token = refresh_token_if_needed(request, tokens)
        except HTTPException as e:
            if e.status_code == 401:
        
                auth_url = spotify_service.get_auth_url()
                logger.info("User not authenticated, opening Spotify login popup")
                
                request.session["pending_playlist_request"] = {
                    "mood": playlist_request.mood,
                    "tracks_count": playlist_request.tracks_count
                }
                
                return {
                    "action": "open_popup",
                    "popup_url": auth_url,
                    "message": "Spotify-Authentifizierung erforderlich"
                }
            raise e
    
        user_profile = spotify_service.get_user_profile(access_token)
        user_id = user_profile["id"]
        
        result = spotify_service.generate_playlist_from_mood(
            access_token,
            user_id,
            playlist_request.mood,
            playlist_request.tracks_count
        )
        
        logger.info(f"Successfully created playlist: {result['playlist']['name']}")
        
        return {
            "action": "playlist_created",
            "success": True,
            "playlist_name": result["playlist"]["name"],
            "playlist_url": result["playlist_url"],
            "tracks_added": result["tracks_added"],
            "message": f"Playlist '{result['playlist']['name']}' wurde erfolgreich erstellt!"
        }
        
    except Exception as e:
        logger.error(f"Error generating playlist: {e}")
        return {
            "action": "error",
            "success": False,
            "error": str(e),
            "message": f"Fehler beim Erstellen der Playlist: {str(e)}"
        }

@router.get("/callback")
async def spotify_callback(code: str, request: Request):
    """
    Callback für Spotify-Authentifizierung.
    Schließt das Popup automatisch nach erfolgreicher Authentifizierung.
    """
    try:
        logger.info("Processing Spotify callback")
        
        tokens = spotify_service.exchange_code_for_token(code)
        request.session["spotify_access_token"] = tokens["access_token"]

        if "refresh_token" in tokens:
            request.session["spotify_refresh_token"] = tokens["refresh_token"]
        
        logger.info("Successfully authenticated with Spotify")
        
        return HTMLResponse(content="""
        <html>
        <head><title>Authentifizierung erfolgreich</title></head>
        <body>
        <script>
        // Popup sofort schließen ohne Wartezeit
        window.close();
        </script>
        </body>
        </html>
        """)
        
    except Exception as e:
        logger.error(f"Spotify callback error: {e}")
        
        return HTMLResponse(content=f"""
        <html>
        <head><title>Authentifizierungsfehler</title></head>
        <body>
        <script>
        window.close();
        </script>
        <p>Authentifizierungsfehler: {str(e)}</p>
        </body>
        </html>
        """)

