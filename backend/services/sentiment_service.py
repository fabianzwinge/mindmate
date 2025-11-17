import os
import httpx
from typing import Dict, Any
from enum import Enum
from dotenv import load_dotenv

load_dotenv()

class SentimentType(Enum):
    POSITIVE = "good"
    NEGATIVE = "bad" 
    NEUTRAL = "neutral"

class SentimentService:
    def __init__(self):
        self.ml_backend_url = os.getenv("ML_BACKEND_URL")
        self.predict_endpoint = f"{self.ml_backend_url}/api/model/predict"

    async def analyze_sentiment(self, text: str) -> Dict[str, Any]:
        async with httpx.AsyncClient() as client:
            response = await client.post(
                self.predict_endpoint,
                json={"text": text},
                timeout=30.0
            )
            
            response.raise_for_status() 
    
            result = response.json()
            
            sentiment_mapping = {
                "positive": SentimentType.POSITIVE.value,
                "negative": SentimentType.NEGATIVE.value,
                "neutral": SentimentType.NEUTRAL.value
            }
            
            predicted_sentiment = result.get("sentiment")
            confidence = result.get("confidence")
            
            return {
                "sentiment": sentiment_mapping.get(predicted_sentiment),
                "confidence": confidence
            }