import httpx
import base64
from io import BytesIO
from typing import Optional
from PIL import Image
from app.database import ImageRecord, get_db
from app.settings import settings
from sqlalchemy.orm import Session
import json

# Get OpenRouter API key from settings
OPENROUTER_API_KEY = settings.openrouter_api_key
OPENROUTER_IMAGE_API_URL = "https://openrouter.ai/api/v1/images/generations"

def generate_image(prompt: str, db: Optional[Session] = None) -> str:
    """
    Generate an image based on a prompt using OpenRouter API with DALL-E model and return as base64 string
    """
    # Prepare the payload for OpenRouter API
    payload = {
        "model": settings.image_model,
        "prompt": prompt,
        "n": 1,
        "size": settings.image_size,
        "response_format": "b64_json"
    }
    
    # Set up headers
    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "Content-Type": "application/json",
        "HTTP-Referer": "http://localhost:8000",
        "X-Title": "AI Task API"
    }
    
    # Make the API call using httpx
    try:
        with httpx.Client() as client:
            response = client.post(OPENROUTER_IMAGE_API_URL, headers=headers, json=payload, timeout=60.0)
            response.raise_for_status()
            result = response.json()
            
            # Extract base64 image data
            if "data" in result and len(result["data"]) > 0:
                img_str = result["data"][0].get("b64_json", "")
                if not img_str:
                    raise Exception("No image data received from API")
            else:
                raise Exception("Invalid response format from API")
                
    except Exception as e:
        print(f"Primary image model ({settings.image_model}) failed: {str(e)}")
        # Try fallback model if primary model fails
        try:
            payload["model"] = settings.image_model_alternative
            with httpx.Client() as client:
                response = client.post(OPENROUTER_IMAGE_API_URL, headers=headers, json=payload, timeout=60.0)
                response.raise_for_status()
                result = response.json()
                
                # Extract base64 image data
                if "data" in result and len(result["data"]) > 0:
                    img_str = result["data"][0].get("b64_json", "")
                    if not img_str:
                        raise Exception("No image data received from fallback API")
                    print(f"Image generated successfully using fallback model: {settings.image_model_alternative}")
                else:
                    raise Exception("Invalid response format from fallback API")
                    
        except Exception as fallback_error:
            print(f"Fallback image model ({settings.image_model_alternative}) also failed: {str(fallback_error)}")
            # Create a placeholder image if both API calls fail
            try:
                # Create a colorful placeholder with text
                image = Image.new('RGB', (512, 512), color=(64, 128, 255))  # type: ignore
                
                # Try to add text if PIL supports it
                try:
                    from PIL import ImageDraw, ImageFont
                    draw = ImageDraw.Draw(image)
                    
                    # Try to use a default font
                    try:
                        font = ImageFont.truetype("arial.ttf", 32)
                    except:
                        font = ImageFont.load_default()
                    
                    # Add text to image
                    text_lines = [
                        "AI Generated Image",
                        f"Prompt: {prompt[:30]}...",
                        "(Placeholder - API Unavailable)"
                    ]
                    
                    y_offset = 150
                    for line in text_lines:
                        bbox = draw.textbbox((0, 0), line, font=font)
                        text_width = bbox[2] - bbox[0]
                        x = (512 - text_width) // 2
                        draw.text((x, y_offset), line, fill=(255, 255, 255), font=font)
                        y_offset += 60
                        
                except ImportError:
                    # If PIL doesn't support text drawing, just use plain color
                    pass
                
                # Convert to base64
                buffered = BytesIO()
                image.save(buffered, format="PNG")
                img_str = base64.b64encode(buffered.getvalue()).decode()
                
            except Exception as final_fallback_error:
                # Ultimate fallback - return error message
                return f"Error generating image: Primary model ({settings.image_model}) failed: {str(e)}. Fallback model ({settings.image_model_alternative}) failed: {str(fallback_error)}. Placeholder generation failed: {str(final_fallback_error)}"
    
    # Store in database
    if db:
        image_record = ImageRecord(prompt=prompt, image_data=img_str)
        db.add(image_record)
        db.commit()
        db.refresh(image_record)
    
    return img_str