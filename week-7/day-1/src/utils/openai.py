import os
import openai

def get_openai_client():
    """
    Initialize and return a OpenAI client using the API_KEY environment variable.
    """
    api_key = "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"
    if not api_key:
        raise ValueError("API_KEY environment variable not set")

    client = openai.OpenAI(
        base_url="https://api.groq.com/openai/v1",
        api_key=api_key
    )
    return client
