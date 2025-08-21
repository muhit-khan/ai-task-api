from sqlalchemy.orm import Session
from app.database import QARecord
import requests
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

HUGGINGFACE_API_KEY = os.getenv("HUGGINGFACE_API_KEY", "your-huggingface-api-key")
QA_MODEL_NAME = os.getenv("QA_MODEL_NAME", "deepset/roberta-base-squad2")
API_URL = os.getenv("QA_API_URL", f"https://api-inference.huggingface.co/models/{QA_MODEL_NAME}")

def perform_qa(db: Session, question: str, context: str):
    headers = {"Authorization": f"Bearer {HUGGINGFACE_API_KEY}"}
    payload = {
        "inputs": {
            "question": question,
            "context": context,
        },
    }
    response = requests.post(API_URL, headers=headers, json=payload)
    answer = response.json().get("answer", "No answer found.")

    db_record = QARecord(question=question, answer=answer)
    db.add(db_record)
    db.commit()
    db.refresh(db_record)
    return answer

def get_latest_answer(db: Session):
    latest_record = db.query(QARecord).order_by(QARecord.id.desc()).first()
    if latest_record:
        return {"question": latest_record.question, "answer": latest_record.answer}
    return None