from pydantic_settings import BaseSettings
import os
from dotenv import dotenv_values

# Load environment variables from .env file only
env_vars = dotenv_values(".env")

class Settings(BaseSettings):
    # Database settings
    database_url: str = env_vars.get("DATABASE_URL") or "sqlite:///./app/database/app.db"
    
    # API Keys
    openrouter_api_key: str = env_vars.get("OPENROUTER_API_KEY") or ""
    
    # AI Model Configuration
    chat_model: str = env_vars.get("CHAT_MODEL") or "deepseek/deepseek-r1-0528:free"
    chat_model_alternative: str = env_vars.get("CHAT_MODEL_ALTERNATIVE") or "google/gemini-2.0-flash-exp:free"
    image_model: str = env_vars.get("IMAGE_MODEL") or ""
    image_model_alternative: str = env_vars.get("IMAGE_MODEL_ALTERNATIVE") or ""
    
    # Model Parameters
    chat_temperature: float = float(env_vars.get("CHAT_TEMPERATURE") or "0.7")
    chat_max_tokens: int = int(env_vars.get("CHAT_MAX_TOKENS") or "500")
    content_temperature: float = float(env_vars.get("CONTENT_TEMPERATURE") or "0.8")
    content_max_tokens: int = int(env_vars.get("CONTENT_MAX_TOKENS") or "300")
    image_size: str = env_vars.get("IMAGE_SIZE") or "1024x1024"
    
    # Server settings
    host: str = env_vars.get("HOST") or "127.0.0.1"  # Default to localhost for security
    port: int = int(env_vars.get("PORT") or os.environ.get("PORT", "8000"))
    debug: bool = (env_vars.get("DEBUG") or "True").lower() == "true"
    
    class Config:
        # Don't load from system environment variables
        env_file = None

# Create a settings instance
settings = Settings()

# Validate that required environment variables are set
if not settings.openrouter_api_key:
    raise ValueError("OPENROUTER_API_KEY environment variable is not set. Please check your .env file.")