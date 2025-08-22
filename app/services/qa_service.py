import requests
from typing import Optional
from app.database import QAHistory, get_db
from app.settings import settings
from sqlalchemy.orm import Session

# Get Hugging Face API key from settings
HUGGINGFACE_API_KEY = settings.huggingface_api_key
HF_API_URL = "https://api-inference.huggingface.co/models/deepset/roberta-base-squad2"

def perform_qa(question: str, context: Optional[str] = None, db: Session = None) -> str:
    """
    Perform Q&A using Hugging Face API
    """
    # If no context provided, use a default one
    if not context:
        context = "Artificial intelligence (AI) is intelligence demonstrated by machines, in contrast to the natural intelligence displayed by humans and animals. Leading AI textbooks define the field as the study of \"intelligent agents\": any device that perceives its environment and takes actions that maximize its chance of successfully achieving its goals."
    
    # Prepare the payload
    payload = {
        "inputs": {
            "question": question,
            "context": context
        }
    }
    
    # Set up headers
    headers = {"Authorization": f"Bearer {HUGGINGFACE_API_KEY}"}
    
    # Make the API call
    try:
        response = requests.post(HF_API_URL, headers=headers, json=payload)
        response.raise_for_status()
        result = response.json()
        answer = result.get("answer", "No answer found")
    except Exception as e:
        # Fallback answer if API call fails
        answer = f"Error occurred while fetching answer from AI: {str(e)}. This is a simulated answer."
    
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
    return latest_qa.answer if latest_qa else None