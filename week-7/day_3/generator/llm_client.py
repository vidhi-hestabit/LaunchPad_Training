import os
import base64
from io import BytesIO
from dotenv import load_dotenv
import openai
from PIL import Image

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

def generate_image(prompt: str, n_images=1, size="1024x1024"):
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("OPENAI_API_KEY not set in .env")

    client = openai.OpenAI(api_key=api_key)

    response = client.images.generate(
        model="gpt-image-1",
        prompt=prompt,
        n=n_images,
        size=size
    )

    images = []
    for data in response.data:
        img_bytes = base64.b64decode(data.b64_json)
        img = Image.open(BytesIO(img_bytes))
        images.append(img)
    return images
