import requests
import os
import base64
from io import BytesIO
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

HUGGINGFACE_API_KEY = os.getenv("HUGGINGFACE_API_KEY", "your-huggingface-api-key")
IMAGE_GENERATION_MODEL_NAME = os.getenv("IMAGE_GENERATION_MODEL_NAME", "runwayml/stable-diffusion-v1-5")
API_URL = os.getenv("IMAGE_GENERATION_API_URL", f"https://api-inference.huggingface.co/models/{IMAGE_GENERATION_MODEL_NAME}")

def generate_image(prompt: str):
    headers = {"Authorization": f"Bearer {HUGGINGFACE_API_KEY}"}
    payload = {"inputs": prompt}
    response = requests.post(API_URL, headers=headers, json=payload)

    if response.status_code == 200:
        image_bytes = response.content
        buffered = BytesIO(image_bytes)
        img_str = base64.b64encode(buffered.getvalue()).decode("utf-8")
        return {"image_base64": img_str}
    else:
        return {"error": "Failed to generate image"}