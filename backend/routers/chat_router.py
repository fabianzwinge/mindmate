from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Dict, Any
from services.sentiment_service import SentimentService
from services.ai_service import AIService

router = APIRouter(prefix="/api/chat")

class ChatMessage(BaseModel):
    message: str

class ChatResponse(BaseModel):
    response: str
    sentiment: str
    confidence: float

sentiment_service = SentimentService()
ai_service = AIService()

@router.post("/sentiment", response_model=ChatResponse)
async def process_message(chat_message: ChatMessage) -> ChatResponse:
  
    try:
        sentiment_result = await sentiment_service.analyze_sentiment(chat_message.message)

        ai_response = await ai_service.generate_response(
            chat_message.message,
            sentiment_result["sentiment"]
        )

        return ChatResponse(
            response=ai_response,
            sentiment=sentiment_result["sentiment"],
            confidence=sentiment_result["confidence"]
        )
        
    except Exception as e:
        raise HTTPException(500, f"Chat processing failed: {str(e)}")