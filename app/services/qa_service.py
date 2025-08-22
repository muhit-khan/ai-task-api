import httpx
from typing import Optional
from app.database import QAHistory, get_db
from app.settings import settings
from sqlalchemy.orm import Session
import json

# Get OpenRouter API key from settings
OPENROUTER_API_KEY = settings.openrouter_api_key
OPENROUTER_API_URL = "https://openrouter.ai/api/v1/chat/completions"

def perform_qa(question: str, context: Optional[str] = None, db: Optional[Session] = None) -> str:
    """
    Perform Q&A using OpenRouter API with DeepSeek model
    """
    # If no context provided, use a default one
    if not context:
        context = "Artificial intelligence (AI) is intelligence demonstrated by machines, in contrast to the natural intelligence displayed by humans and animals. Leading AI textbooks define the field as the study of \"intelligent agents\": any device that perceives its environment and takes actions that maximize its chance of successfully achieving its goals."
    
    # Prepare the payload for OpenRouter API
    payload = {
        "model": settings.chat_model,
        "messages": [
            {
                "role": "system",
                "content": f"You are a helpful AI assistant. Use the following context to answer questions accurately: {context}"
            },
            {
                "role": "user",
                "content": question
            }
        ],
        "temperature": settings.chat_temperature,
        "max_tokens": settings.chat_max_tokens
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
            response = client.post(OPENROUTER_API_URL, headers=headers, json=payload, timeout=30.0)
            response.raise_for_status()
            result = response.json()
            answer = result.get("choices", [{}])[0].get("message", {}).get("content", "No answer found")
    except Exception as e:
        # Try fallback model if primary model fails
        try:
            payload["model"] = settings.chat_model_alternative
            with httpx.Client() as client:
                response = client.post(OPENROUTER_API_URL, headers=headers, json=payload, timeout=30.0)
                response.raise_for_status()
                result = response.json()
                answer = result.get("choices", [{}])[0].get("message", {}).get("content", "No answer found")
                answer += f" (Generated using fallback model: {settings.chat_model_alternative})"
        except Exception as fallback_error:
            # Fallback answer if both API calls fail
            answer = f"Error occurred while fetching answer from AI: {str(e)}. Fallback model also failed: {str(fallback_error)}. This is a simulated answer based on the question: {question}"
    
    # Store in database
    if db:
        qa_record = QAHistory(question=question, answer=answer, context=context)
        db.add(qa_record)
        db.commit()
        db.refresh(qa_record)
    
    return answer

def get_latest_answer(db: Session) -> Optional[str]:
    """
    Retrieve the latest answer from the database
    """
    latest_qa = db.query(QAHistory).order_by(QAHistory.created_at.desc()).first()
    if latest_qa:
        return str(latest_qa.answer)
    return None