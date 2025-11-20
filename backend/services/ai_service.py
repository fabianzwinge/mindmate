import os
from dotenv import load_dotenv
import random
from openai import OpenAI
import re

load_dotenv()

class AIService:

    async def generate_response(self, user_message: str, sentiment: str) -> str:
        HF_TOKEN = os.environ.get("HF_API_KEY")
        if not HF_TOKEN:
            raise ValueError("HF_API_KEY environment variable is not set.")

        client = OpenAI(
            base_url="https://router.huggingface.co/v1",
            api_key=HF_TOKEN
        )

        model = "HuggingFaceTB/SmolLM3-3B:cheapest"

        system_prompt = """
        You are a highly empathetic and friendly AI assistant. 
        Your task is to respond to user messages in a way that matches their emotional state. 
        Always be warm, supportive, and encouraging. 
        For positive sentiments, express enthusiasm and genuine happiness. 
        For negative sentiments, be comforting and offer reassurance. 
        For neutral sentiments, be attentive, polite, and offer help if needed. 
        Never include internal thoughts, <think> tags, or any markup. 
        You may use emojis appropriately to enhance friendliness. 
        Keep responses concise, coherent, and natural. 
        Always maintain a human-like, friendly tone.
        IMPORTANT: Assume that the first user message you respond to is always an answer to this question: "Hi there! How are you feeling today? What have you been up to?" 
        Your response should directly address this and be relevant. 
        Limit your reply to a maximum of 3 sentences.
        """

        user_content = f"The user currently feels: {sentiment}. User message: \"{user_message}\""

        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_content}
        ]

        try:
            completion = client.chat.completions.create(
                model=model,
                messages=messages,
                temperature=0.7,
                max_tokens=300
            )

            if completion.choices and len(completion.choices) > 0:
                text = completion.choices[0].message.content.strip()

                text = re.sub(r"<think>.*?</think>", "", text, flags=re.DOTALL)
                text = re.sub(r"<.*?>", "", text)

                return text.strip()

        except Exception as e:
            print("AI error:", e)

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

        return random.choice(fallback_responses.get(sentiment, fallback_responses["neutral"]))