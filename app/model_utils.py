"""
Model utilities for AI Task API
Provides functions to get model information and manage model configurations
"""

from app.settings import settings
from typing import Dict, List, Any

def get_available_models() -> Dict[str, Any]:
    """
    Get information about all available models configured in the system
    """
    return {
        "chat_models": {
            "primary": {
                "id": settings.chat_model,
                "description": "Primary chat model for Q&A and content generation",
                "temperature": settings.chat_temperature,
                "max_tokens": settings.chat_max_tokens
            },
            "alternative": {
                "id": settings.chat_model_alternative,
                "description": "Fallback chat model",
                "temperature": settings.chat_temperature,
                "max_tokens": settings.chat_max_tokens
            }
        },
        "content_generation": {
            "model": settings.chat_model,
            "temperature": settings.content_temperature,
            "max_tokens": settings.content_max_tokens
        },
        "image_models": {
            "primary": {
                "id": settings.image_model,
                "description": "Primary image generation model",
                "size": settings.image_size
            },
            "alternative": {
                "id": settings.image_model_alternative,
                "description": "Fallback image generation model",
                "size": settings.image_size
            }
        }
    }

def get_model_status() -> Dict[str, str]:
    """
    Get the current status/configuration of all models
    """
    return {
        "primary_chat_model": settings.chat_model,
        "fallback_chat_model": settings.chat_model_alternative,
        "primary_image_model": settings.image_model,
        "fallback_image_model": settings.image_model_alternative,
        "image_size": settings.image_size,
        "chat_temperature": str(settings.chat_temperature),
        "content_temperature": str(settings.content_temperature)
    }

def get_popular_models() -> Dict[str, List[str]]:
    """
    Get a list of popular models that can be used as alternatives
    """
    return {
        "chat_models": [
            "deepseek/deepseek-chat",
            "anthropic/claude-3.5-sonnet",
            "openai/gpt-4o",
            "openai/gpt-4o-mini", 
            "anthropic/claude-3-opus",
            "google/gemini-pro-1.5",
            "meta-llama/llama-3.1-405b-instruct",
            "mistralai/mixtral-8x7b-instruct"
        ],
        "image_models": [
            "openai/dall-e-3",
            "openai/dall-e-2",
            "stabilityai/stable-diffusion-xl-base-1.0",
            "stabilityai/stable-diffusion-3-large",
            "midjourney/midjourney",
            "runwayml/stable-diffusion-v1-5"
        ]
    }

def validate_model_config() -> Dict[str, Any]:
    """
    Validate the current model configuration
    """
    issues = []
    warnings = []
    
    # Check if API key is set
    if not settings.openrouter_api_key or settings.openrouter_api_key == "your_openrouter_api_key_here":
        issues.append("OpenRouter API key is not set or using placeholder value")
    
    # Check if models are different (recommended)
    if settings.chat_model == settings.chat_model_alternative:
        warnings.append("Primary and alternative chat models are the same")
    
    if settings.image_model == settings.image_model_alternative:
        warnings.append("Primary and alternative image models are the same")
    
    # Check temperature values
    if not 0.0 <= settings.chat_temperature <= 2.0:
        issues.append(f"Chat temperature ({settings.chat_temperature}) should be between 0.0 and 2.0")
    
    if not 0.0 <= settings.content_temperature <= 2.0:
        issues.append(f"Content temperature ({settings.content_temperature}) should be between 0.0 and 2.0")
    
    # Check image size format
    valid_sizes = ["256x256", "512x512", "1024x1024", "1792x1024", "1024x1792"]
    if settings.image_size not in valid_sizes:
        warnings.append(f"Image size ({settings.image_size}) may not be supported by all models. Valid sizes: {valid_sizes}")
    
    return {
        "valid": len(issues) == 0,
        "issues": issues,
        "warnings": warnings,
        "config": get_model_status()
    }