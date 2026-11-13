
import os
from pathlib import Path
from groq import Groq
from dotenv import load_dotenv

# Load Day-06 environment variables
BASE_DIR = Path(__file__).resolve().parents[1]
load_dotenv(BASE_DIR / ".env")

API_KEY = os.getenv("GROQ_API_KEY")
MODEL_NAME = os.getenv(
    "GROQ_MODEL",
    "llama-3.3-70b-versatile"
)

# Create Groq client
if not API_KEY:
    raise ValueError("Groq API key not found in Day-06/.env")

client = Groq(api_key=API_KEY)


def generate_response(prompt, system_prompt):
    response = client.chat.completions.create(
        model=MODEL_NAME,
        messages=[
            {
                "role": "system",
                "content": system_prompt
            },
            {
                "role": "user",
                "content": prompt
            }
        ],
        temperature=0.3
    )

    return response.choices[0].message.content
