from pydantic_settings import BaseSettings
import os
from dotenv import dotenv_values

# Load environment variables from .env file only
env_vars = dotenv_values(".env")

class Settings(BaseSettings):
    # Database settings
    database_url: str = env_vars.get("DATABASE_URL", "sqlite:///./app/database/app.db")
    
    # API Keys
    huggingface_api_key: str = env_vars.get("HUGGINGFACE_API_KEY", "")
    
    # Server settings
    host: str = env_vars.get("HOST", "127.0.0.1")  # Default to localhost for security
    port: int = int(env_vars.get("PORT", "8000"))
    debug: bool = env_vars.get("DEBUG", "True").lower() == "true"
    
    class Config:
        # Don't load from system environment variables
        env_file = None

# Create a settings instance
settings = Settings()

# Validate that required environment variables are set
if not settings.huggingface_api_key:
    raise ValueError("HUGGINGFACE_API_KEY environment variable is not set. Please check your .env file.")