from pydantic_settings import BaseSettings
from typing import Optional
import os

# Load environment variables from .env file
from dotenv import load_dotenv
load_dotenv()


class Settings(BaseSettings):
    # Database settings
    database_url: str = os.getenv("DATABASE_URL", "sqlite:///./app/database/app.db")
    
    # API Keys
    huggingface_api_key: str = os.getenv("HUGGINGFACE_API_KEY", "")
    
    # Server settings
    host: str = os.getenv("HOST", "0.0.0.0")
    port: int = int(os.getenv("PORT", "8001"))  # Changed default to 8001 to avoid conflicts
    debug: bool = os.getenv("DEBUG", "True").lower() == "true"
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


# Create a settings instance
settings = Settings()

# Validate that required environment variables are set
# Only validate if we're not in a test environment
if not settings.huggingface_api_key and not os.getenv("TESTING_ENV"):
    raise ValueError("HUGGINGFACE_API_KEY environment variable is not set. Please check your .env file.")