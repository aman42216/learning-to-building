
import os
import time
import logging
from pathlib import Path

from groq import Groq
from dotenv import load_dotenv

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(name)s: %(message)s"
)

logger = logging.getLogger("shramiksathi")
logger.setLevel(logging.INFO)

BASE_DIR = Path(__file__).resolve().parents[1]
load_dotenv(BASE_DIR / ".env")

MODEL_NAME = os.getenv(
    "GROQ_MODEL",
    "llama-3.3-70b-versatile"
)

logger = logging.getLogger("shramiksathi")


def generate_response(prompt, system_prompt):
    api_key = os.getenv("GROQ_API_KEY")

    if not api_key:
        raise ValueError("Groq API key not found in Day-06/.env")

    client = Groq(api_key=api_key)

    start_time = time.perf_counter()

    response = client.chat.completions.create(
        model=MODEL_NAME,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": prompt}
        ],
        temperature=0.3
    )

    latency_ms = (time.perf_counter() - start_time) * 1000

    usage = response.usage

    prompt_tokens = usage.prompt_tokens if usage else 0
    completion_tokens = usage.completion_tokens if usage else 0
    total_tokens = usage.total_tokens if usage else 0

    logger.info(
        "LLM request | latency_ms=%.2f | prompt_tokens=%d | "
        "completion_tokens=%d | total_tokens=%d",
        latency_ms,
        prompt_tokens,
        completion_tokens,
        total_tokens
    )

    return response.choices[0].message.content
