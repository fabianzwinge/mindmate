import os
from typing import Dict, Any
from dotenv import load_dotenv
import random

load_dotenv()

class AIService:

    async def generate_response(self, user_message: str, sentiment: str) -> str:
       
        fallback_responses = {
            "good": [
            "I'm glad to hear that you're feeling good!",
            "That's great! Enjoy this positive moment.",
            "It's wonderful to feel well. What made you happy today?",
            "Your positive energy is contagious! What's bringing you joy today?"
            ],
            "bad": [
            "I'm sorry to hear you're not feeling well. I'm here for you.",
            "Tough times are part of life. You can get through this, I believe in you.",
            "It's okay to feel down sometimes. Would you like to talk about it?",
            "You're strong, even if it doesn't feel like it right now. I'm listening."
            ],
            "neutral": [
            "Thank you for sharing your thoughts. How can I help you?",
            "I'm here to listen. What's on your mind today?",
            "It's nice to have this conversation. What would you like to discuss?",
            "I'm looking forward to our chat. Tell me what's on your mind."
            ]
        }

        responses = fallback_responses.get(sentiment)
        return random.choice(responses)