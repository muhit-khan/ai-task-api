from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app import models, database
from app.services import qa_service, image_service, content_service, auth_service
from typing import Union

router = APIRouter()

@router.post("/register", response_model=models.User)
def register_user(user: models.UserCreate, db: Session = Depends(database.get_db)):
    # Check if user already exists
    db_user = db.query(database.User).filter(database.User.username == user.username).first()
    if db_user:
        raise HTTPException(status_code=400, detail="Username already registered")
    
    # Create new user
    hashed_password = auth_service.get_password_hash(user.password)
    db_user = database.User(
        username=user.username,
        email=user.email,
        full_name=user.full_name,
        hashed_password=hashed_password
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

@router.post("/ai-task", response_model=Union[models.QAResponse, models.LatestAnswerResponse, models.ImageResponse, models.ContentResponse])
async def ai_task(
    request: models.AITaskRequest,
    db: Session = Depends(database.get_db),
    current_user: dict = Depends(auth_service.get_current_user)
):
    if request.task == "qa":
        if not request.prompt:
            raise HTTPException(status_code=400, detail="Prompt is required for Q&A task")
        # For simplicity, using a generic context. In a real app, this would be dynamic.
        context = "The weather in London is usually rainy."
        answer = qa_service.perform_qa(db, request.prompt, context)
        return {"answer": answer}

    elif request.task == "get_latest_answer":
        latest = qa_service.get_latest_answer(db)
        if not latest:
            raise HTTPException(status_code=404, detail="No previous answers found")
        return latest

    elif request.task == "generate_image":
        if not request.prompt:
            raise HTTPException(status_code=400, detail="Prompt is required for image generation")
        return image_service.generate_image(request.prompt)

    elif request.task == "generate_content":
        if not request.prompt or not request.platform:
            raise HTTPException(status_code=400, detail="Prompt and platform are required for content generation")
        return content_service.generate_content(request.platform, request.prompt)

    else:
        raise HTTPException(status_code=400, detail="Invalid task type")