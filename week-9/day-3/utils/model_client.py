import os
from autogen_ext.models.openai import OpenAIChatCompletionClient
from dotenv import load_dotenv

load_dotenv() 

def get_model_client():
    return OpenAIChatCompletionClient(
        model="llama-3.1-8b-instant",
        api_key=os.getenv(
            "GROQ_API_KEY"
        ),
        base_url="https://api.groq.com/openai/v1",
        temperature=0.7,
        max_tokens=2048,
        model_info={
            "type": "openai",
            "json_output": False,
            "vision": False,
            "function_calling": False,
            "family":"llama"
        }
    )
