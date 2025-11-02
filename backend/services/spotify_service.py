import os
import requests
import base64
from typing import Dict, List, Optional
from fastapi import HTTPException
from dotenv import load_dotenv
import logging

load_dotenv()
logger = logging.getLogger(__name__)

class SpotifyService:
    def __init__(self):
        self.client_id = os.getenv("SPOTIFY_CLIENT_ID")
        self.client_secret = os.getenv("SPOTIFY_CLIENT_SECRET")
        
        base_url = os.getenv("BACKEND_URL", "http://127.0.0.1:8000")
        self.redirect_uri = f"{base_url}/api/spotify/callback"
        
        self.base_url = "https://api.spotify.com/v1"
        
        if not self.client_id or not self.client_secret:
            logger.error("Spotify credentials not configured")
            raise ValueError("Spotify CLIENT_ID and CLIENT_SECRET must be set")
        
    def get_auth_url(self) -> str:
        scopes = "playlist-modify-public playlist-modify-private user-read-private ugc-image-upload"
        auth_url = (
            f"https://accounts.spotify.com/authorize?"
            f"client_id={self.client_id}&"
            f"response_type=code&"
            f"redirect_uri={self.redirect_uri}&"
            f"scope={scopes}&"
            f"show_dialog=true"
        )
        return auth_url
    
    def exchange_code_for_token(self, code: str) -> Dict:
        token_url = "https://accounts.spotify.com/api/token"
        
        credentials = f"{self.client_id}:{self.client_secret}"
        encoded_credentials = base64.b64encode(credentials.encode()).decode()
        
        headers = {
            "Authorization": f"Basic {encoded_credentials}",
            "Content-Type": "application/x-www-form-urlencoded"
        }
        
        data = {
            "grant_type": "authorization_code",
            "code": code,
            "redirect_uri": self.redirect_uri
        }
        
        try:
            response = requests.post(token_url, headers=headers, data=data, timeout=10)
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            logger.error(f"Failed to exchange code for token: {e}")
            raise HTTPException(status_code=400, detail="Failed to get access token")
    
    def refresh_access_token(self, refresh_token: str) -> Dict:
        token_url = "https://accounts.spotify.com/api/token"
        
        credentials = f"{self.client_id}:{self.client_secret}"
        encoded_credentials = base64.b64encode(credentials.encode()).decode()
        
        headers = {
            "Authorization": f"Basic {encoded_credentials}",
            "Content-Type": "application/x-www-form-urlencoded"
        }
        
        data = {
            "grant_type": "refresh_token",
            "refresh_token": refresh_token
        }
        
        try:
            response = requests.post(token_url, headers=headers, data=data, timeout=10)
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            logger.error(f"Failed to refresh token: {e}")
            raise HTTPException(status_code=400, detail="Failed to refresh token")
    
    def get_user_profile(self, access_token: str) -> Dict:
        headers = {"Authorization": f"Bearer {access_token}"}
        
        try:
            response = requests.get(f"{self.base_url}/me", headers=headers, timeout=10)
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            logger.error(f"Failed to get user profile: {e}")
            raise HTTPException(status_code=401, detail="Invalid access token")
    
    def search_tracks(self, access_token: str, query: str, limit: int = 10) -> List[Dict]:
        headers = {"Authorization": f"Bearer {access_token}"}
        
        params = {
            "q": query,
            "type": "track",
            "limit": limit,
            "market": "DE"
        }
        
        try:
            response = requests.get(f"{self.base_url}/search", headers=headers, params=params, timeout=10)
            response.raise_for_status()
            return response.json()["tracks"]["items"]
        except requests.RequestException as e:
            logger.error(f"Failed to search tracks: {e}")
            raise HTTPException(status_code=400, detail="Failed to search tracks")
    
    def create_playlist(self, access_token: str, user_id: str, name: str, description: str = "") -> Dict:
        headers = {
            "Authorization": f"Bearer {access_token}",
            "Content-Type": "application/json"
        }
        
        data = {
            "name": name,
            "description": description,
            "public": False
        }
        
        try:
            response = requests.post(
                f"{self.base_url}/users/{user_id}/playlists",
                headers=headers,
                json=data,
                timeout=10
            )
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            logger.error(f"Failed to create playlist: {e}")
            raise HTTPException(status_code=400, detail="Failed to create playlist")
    
    def add_tracks_to_playlist(self, access_token: str, playlist_id: str, track_uris: List[str]) -> bool:
        headers = {
            "Authorization": f"Bearer {access_token}",
            "Content-Type": "application/json"
        }
        
        chunk_size = 100
        for i in range(0, len(track_uris), chunk_size):
            chunk = track_uris[i:i + chunk_size]
            data = {"uris": chunk}
            
            try:
                response = requests.post(
                    f"{self.base_url}/playlists/{playlist_id}/tracks",
                    headers=headers,
                    json=data,
                    timeout=10
                )
                response.raise_for_status()
            except requests.RequestException as e:
                logger.error(f"Failed to add tracks to playlist: {e}")
                return False
        
        return True
    
    def set_playlist_cover(self, access_token: str, playlist_id: str, image_base64: str) -> bool:
        headers = {
            "Authorization": f"Bearer {access_token}",
            "Content-Type": "image/jpeg"
        }
        
        try:
            response = requests.put(
                f"{self.base_url}/playlists/{playlist_id}/images",
                headers=headers,
                data=image_base64,
                timeout=10
            )
            response.raise_for_status()
            return True
        except requests.RequestException as e:
            return False
    
    def get_mindmate_cover_base64(self) -> Optional[str]:
        try:
            image_path = os.path.join(os.path.dirname(__file__), "img", "mindmate.jpeg")
            
            with open(image_path, "rb") as image_file:
                image_data = image_file.read()
                
                if len(image_data) > 256 * 1024:
                    logger.warning(f"Image is too large (max 256KB)")
                    return None
                
                base64_string = base64.b64encode(image_data).decode('utf-8')
                return base64_string
                
        except Exception as e:
            logger.error(f"Failed to load MindMate image: {e}")
            return None
    
    def generate_playlist_from_mood(self, access_token: str, user_id: str, mood: str, tracks_count: int = 20) -> Dict:
        mood_queries = {
            "gut": ["happy music", "upbeat songs", "positive vibes", "feel good", "energetic", "uplifting"],
            "schlecht": ["sad songs", "emotional music", "melancholy", "healing music", "comfort songs", "chill"],
            "neutral": ["chill music", "relaxed songs", "ambient", "calm music", "focus music", "background"]
        }
        
        queries = mood_queries.get(mood, mood_queries["neutral"])
        all_tracks = []
        tracks_per_query = max(1, tracks_count // len(queries))
        
        for query in queries:
            try:
                tracks = self.search_tracks(access_token, query, tracks_per_query + 5)
                all_tracks.extend(tracks)
            except Exception as e:
                logger.warning(f"Failed to search for '{query}': {e}")
                continue
        
        seen_ids = set()
        unique_tracks = []
        for track in all_tracks:
            if track["id"] not in seen_ids and track.get("uri"):
                seen_ids.add(track["id"])
                unique_tracks.append(track)
                if len(unique_tracks) >= tracks_count:
                    break
        
        # Create playlist
        mood_names = {"gut": "good", "schlecht": "bad", "neutral": "neutral"}
        playlist_name = f"MindMate {mood_names.get(mood, 'neutral').capitalize()} Mood"
        playlist_description = f"Your MindMate playlist for your {mood_names.get(mood, 'neutral')} mood."
        
        playlist = self.create_playlist(access_token, user_id, playlist_name, playlist_description)
        
        # Add tracks
        track_uris = [track["uri"] for track in unique_tracks]
        success = self.add_tracks_to_playlist(access_token, playlist["id"], track_uris)
        
        if not success:
            logger.warning("Some tracks may not have been added to the playlist")
        
        # Set playlist cover 
        try:
            mindmate_image_base64 = self.get_mindmate_cover_base64()
            if mindmate_image_base64:
                cover_success = self.set_playlist_cover(access_token, playlist["id"], mindmate_image_base64)
                if cover_success:
                    logger.info("MindMate image set as playlist cover")
                else:
                    logger.warning("Failed to set playlist cover")
        except Exception as e:
            logger.error(f"Error setting playlist cover: {e}")
        
        return {
            "playlist": playlist,
            "tracks_added": len(track_uris),
            "playlist_url": playlist["external_urls"]["spotify"],
            "tracks": unique_tracks[:10]
        }