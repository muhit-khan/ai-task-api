import requests
import os
import base64
from io import BytesIO

HUGGINGFACE_API_KEY = os.getenv("HUGGINGFACE_API_KEY")
API_URL = "https://api-inference.huggingface.co/models/runwayml/stable-diffusion-v1-5"

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