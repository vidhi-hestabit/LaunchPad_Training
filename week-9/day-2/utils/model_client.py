import os
from autogen_ext.models.openai import OpenAIChatCompletionClient
from dotenv import load_dotenv

load_dotenv() 


def get_model_client():
    return OpenAIChatCompletionClient(
        model="llama-3.3-70b-versatile",
        api_key=os.getenv(
            "OPENAI_API_KEY"
        ),
        base_url="https://api.groq.com/openai/v1",
        temperature=0.2,
        max_tokens=2048,
        model_info={
            "type": "openai",
            "json_output": False,
            "vision": False,
            "function_calling": False,
            "family":"llama"
        }
    )
