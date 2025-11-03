from fastapi import APIRouter, HTTPException, Request
from pydantic import BaseModel
import logging

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/model")

class TextInput(BaseModel):
    text: str

class SentimentPrediction(BaseModel):
    sentiment: str
    confidence: float

@router.post("/predict", response_model=SentimentPrediction)
async def predict_sentiment(input_data: TextInput): 
    try:
        # Placeholder
        return SentimentPrediction(
            sentiment="negative",
            confidence=0.9
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Prediction failed: {str(e)}")