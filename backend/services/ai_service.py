import os
from typing import Dict, Any
from dotenv import load_dotenv
import random

load_dotenv()

class AIService:
    def __init__(self):
        # Für jetzt nur lokale Antworten verwenden
        self.model = None
        
    async def generate_response(self, user_message: str, sentiment: str) -> str:
        """
        Generiert eine empathische Antwort basierend auf der erkannten Stimmung
        """
        
        fallback_responses = {
            "gut": [
                "Das freut mich zu hören! Es ist schön, dass es dir gut geht.",
                "Toll, dass du in guter Stimmung bist! Genieße diesen Moment.",
                "Es ist wunderbar, wenn man sich gut fühlt. Was macht dich heute besonders glücklich?",
                "Deine positive Energie ist spürbar! Was bereitet dir heute so viel Freude?"
            ],
          
            "schlecht": [
                "Es tut mir leid zu hören, dass es dir nicht gut geht. Ich bin für dich da.",
                "Schwere Zeiten gehören zum Leben dazu. Du schaffst das, ich glaube an dich.",
                "Manchmal ist es okay, sich schlecht zu fühlen. Möchtest du darüber reden?",
                "Du bist stark, auch wenn es sich gerade nicht so anfühlt. Ich höre dir zu."
            ],
            "neutral": [
                "Danke, dass du deine Gedanken mit mir teilst. Wie kann ich dir helfen?",
                "Ich bin hier, um dir zuzuhören. Was beschäftigt dich heute?",
                "Es ist schön, dass wir uns unterhalten. Was möchtest du besprechen?",
                "Ich freue mich auf unser Gespräch. Erzähl mir, was dich bewegt."
            ]
        }

        responses = fallback_responses.get(sentiment, fallback_responses["gut"]) #Placehoder - always positive for now
        return random.choice(responses)