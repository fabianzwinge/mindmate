from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from transformers import AutoModelForSequenceClassification, AutoTokenizer
import torch
import torch.nn.functional as F

router = APIRouter(prefix="/api/model")

class TextRequest(BaseModel):
    text: str

class SentimentPrediction(BaseModel):
    sentiment: str
    confidence: float

model_name = "sentiment_model"
model = AutoModelForSequenceClassification.from_pretrained(model_name)
tokenizer = AutoTokenizer.from_pretrained(model_name)

@router.post("/predict", response_model=SentimentPrediction)
async def predict_sentiment(request: TextRequest): 
    try:
        text = request.text

        inputs = tokenizer(
            text,
            return_tensors="pt",
            truncation=True,
            padding=True
        )

        with torch.no_grad():  
            outputs = model(**inputs)
        
        logits = outputs.logits
        probs = F.softmax(logits, dim=-1) 
        prediction = torch.argmax(probs, dim=1).item()
        confidence = torch.max(probs, dim=1).values.item()
    
        sentiment_map = {0: "negative", 1: "neutral", 2: "positive"}
        sentiment = sentiment_map.get(prediction)
        
        return {
            "sentiment": sentiment,
            "confidence": confidence
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Prediction failed: {str(e)}")