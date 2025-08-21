import requests
import os

HUGGINGFACE_API_KEY = os.getenv("HUGGINGFACE_API_KEY")
API_URL = "https://api-inference.huggingface.co/models/gpt2"

def generate_content(platform: str, prompt: str):
    headers = {"Authorization": f"Bearer {HUGGINGFACE_API_KEY}"}
    full_prompt = f"Create a {platform} post about: {prompt}"
    payload = {"inputs": full_prompt}
    response = requests.post(API_URL, headers=headers, json=payload)
    
    if response.status_code == 200 and isinstance(response.json(), list) and "generated_text" in response.json()[0]:
        return {"content": response.json()[0]["generated_text"]}
    else:
        return {"error": "Failed to generate content"}