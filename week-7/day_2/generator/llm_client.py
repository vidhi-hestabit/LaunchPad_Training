import os
from dotenv import load_dotenv
import openai

load_dotenv()

def get_openai_client():
    api_key = os.getenv("API_KEY")
    if not api_key:
        raise ValueError("API_KEY env variable not set")
    client = openai.OpenAI(
        base_url="https://api.groq.com/openai/v1",
        api_key=api_key
    )
    return client
