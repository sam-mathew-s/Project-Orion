import os 
from groq import Groq 
from dotenv import load_dotenv 

load_dotenv()
api_key = os.environ.get("GROQ_API_KEY")

if not api_key: 
    raise ValueError("❌ CRITICAL ERROR: GROQ_API_KEY is missing from .env")

client = Groq(api_key=api_key)

def get_ai_response(user_message, system_instruction="You are a helpful AI assistant."):
    try:
        completion = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {"role": "system", "content": system_instruction},
                {"role": "user", "content": user_message}
            ],
            temperature=0.7,
            max_tokens=1024
        )
        return completion.choices[0].message.content
    except Exception as e:
        return f"❌ AI ENGINE FAILURE: {e}"