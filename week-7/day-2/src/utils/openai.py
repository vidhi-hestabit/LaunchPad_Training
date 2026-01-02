import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

def get_openai_client():
    api_key = os.getenv("API_KEY")
    if not api_key:
        raise ValueError("API_KEY missing")

    return OpenAI(
        api_key=api_key,
        base_url="https://api.groq.com/openai/v1"
    )