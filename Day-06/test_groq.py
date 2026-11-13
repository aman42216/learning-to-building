
from app.llm import generate_response

system_prompt = """
You are ShramikSathi, an assistant for Indian workers.
Answer in simple language. Do not invent labour laws.
"""

user_prompt = "What is gratuity? Explain in simple words."

try:
    answer = generate_response(user_prompt, system_prompt)
    print("\nShramikSathi AI Response:")
    print(answer)

except Exception as e:
    print("Error:", e)
