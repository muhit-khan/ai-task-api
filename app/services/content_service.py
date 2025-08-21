import requests
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

HUGGINGFACE_API_KEY = os.getenv("HUGGINGFACE_API_KEY", "your-huggingface-api-key")
CONTENT_GENERATION_MODEL_NAME = os.getenv("CONTENT_GENERATION_MODEL_NAME", "gpt2")
API_URL = os.getenv("CONTENT_GENERATION_API_URL", f"https://api-inference.huggingface.co/models/{CONTENT_GENERATION_MODEL_NAME}")

def generate_content(platform: str, prompt: str):
    headers = {"Authorization": f"Bearer {HUGGINGFACE_API_KEY}"}
    full_prompt = f"Create a {platform} post about: {prompt}"
    payload = {"inputs": full_prompt}
    response = requests.post(API_URL, headers=headers, json=payload)
    
    if response.status_code == 200 and isinstance(response.json(), list) and "generated_text" in response.json()[0]:
        return {"content": response.json()[0]["generated_text"]}
    else:
        return {"error": "Failed to generate content"}