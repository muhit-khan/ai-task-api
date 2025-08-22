import requests
from app.database import ContentRecord, get_db
from app.settings import settings
from sqlalchemy.orm import Session

# Get Hugging Face API key from settings
HUGGINGFACE_API_KEY = settings.huggingface_api_key
HF_API_URL = "https://api-inference.huggingface.co/models/google/flan-t5-base"

def generate_content(prompt: str, platform: str, db: Session = None) -> str:
    """
    Generate platform-specific content based on a prompt using Hugging Face API
    """
    # Create platform-specific instructions
    platform_instructions = {
        "twitter": f"Write a concise, engaging tweet (under 280 characters) about: {prompt}",
        "facebook": f"Write a Facebook post about: {prompt}",
        "linkedin": f"Write a professional LinkedIn post about: {prompt}",
        "instagram": f"Write a catchy Instagram caption about: {prompt}",
        "default": f"Write content about: {prompt}"
    }
    
    # Get the instruction for the platform
    instruction = platform_instructions.get(platform.lower(), platform_instructions["default"])
    
    # Set up headers
    headers = {"Authorization": f"Bearer {HUGGINGFACE_API_KEY}"}
    
    # Prepare the payload
    payload = {
        "inputs": instruction,
        "parameters": {
            "max_new_tokens": 100,
            "temperature": 0.7
        }
    }
    
    # Make the API call
    try:
        response = requests.post(HF_API_URL, headers=headers, json=payload)
        response.raise_for_status()
        result = response.json()
        content = result[0]["generated_text"] if result else f"Generated {platform} content about: {prompt}"
    except Exception as e:
        # Fallback to template-based content if API call fails
        platform_templates = {
            "twitter": f"🐦 {prompt} #AI #Tech",
            "facebook": f"📢 {prompt}\n\nCheck out this amazing AI content!\n\n#AI #Technology",
            "linkedin": f"🚀 {prompt}\n\nAs professionals in the tech industry, we're excited about the potential of AI.\n\n#ArtificialIntelligence #TechInnovation",
            "instagram": f"✨ {prompt} ✨\n\n#AI #TechLife #Innovation",
            "default": f"{prompt}\n\nGenerated content for {platform}"
        }
        content = platform_templates.get(platform.lower(), platform_templates["default"])
    
    # Store in database
    if db:
        content_record = ContentRecord(prompt=prompt, platform=platform, content=content)
        db.add(content_record)
        db.commit()
        db.refresh(content_record)
    
    return content