import requests
import base64
from io import BytesIO
from PIL import Image
from app.database import ImageRecord, get_db
from app.settings import settings
from sqlalchemy.orm import Session

# Get Hugging Face API key from settings
HUGGINGFACE_API_KEY = settings.huggingface_api_key
HF_API_URL = "https://api-inference.huggingface.co/models/stabilityai/stable-diffusion-2-1"

def generate_image(prompt: str, db: Session = None) -> str:
    """
    Generate an image based on a prompt using Hugging Face API and return as base64 string
    """
    # Set up headers
    headers = {"Authorization": f"Bearer {HUGGINGFACE_API_KEY}"}
    
    # Prepare the payload
    payload = {
        "inputs": prompt,
    }
    
    # Make the API call
    try:
        response = requests.post(HF_API_URL, headers=headers, json=payload)
        response.raise_for_status()
        
        # Convert image bytes to base64
        image_data = response.content
        img_str = base64.b64encode(image_data).decode()
    except Exception as e:
        # Create a placeholder image if API call fails
        image = Image.new('RGB', (512, 512), color=(73, 109, 137))
        buffered = BytesIO()
        image.save(buffered, format="PNG")
        img_str = base64.b64encode(buffered.getvalue()).decode()
    
    # Store in database
    if db:
        image_record = ImageRecord(prompt=prompt, image_data=img_str)
        db.add(image_record)
        db.commit()
        db.refresh(image_record)
    
    return img_str