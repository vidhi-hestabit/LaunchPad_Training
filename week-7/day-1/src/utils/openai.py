import os
import openai
from dotenv import load_dotenv

load_dotenv()

def get_openai_client():
    """
    Initialize and return a OpenAI client using API_KEY from .env
    """
    api_key = os.getenv("API_KEY")
    if not api_key:
        raise ValueError("API_KEY environment variable not set")

    client = openai.OpenAI(
        base_url="https://api.groq.com/openai/v1",
        api_key=api_key
    )
    return client
