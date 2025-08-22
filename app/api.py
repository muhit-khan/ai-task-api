from fastapi import APIRouter, Depends, HTTPException, Body
from app.models import QATask, LatestAnswerTask, ImageGenerationTask, ContentGenerationTask, TaskResponse
from app.services.qa_service import perform_qa, get_latest_answer
from app.services.image_service import generate_image
from app.services.content_service import generate_content
from app.database import get_db
from sqlalchemy.orm import Session
from typing import Union

router = APIRouter(prefix="/ai-task")

@router.post("/", response_model=TaskResponse)
async def handle_ai_task(
    task_data: Union[QATask, LatestAnswerTask, ImageGenerationTask, ContentGenerationTask] = Body(..., discriminator="task"),
    db: Session = Depends(get_db)
):
    """
    Handle various AI tasks based on the task field
    """
    task_type = task_data.task
    
    if task_type == "qa":
        # task_data is already validated as QATask
        answer = perform_qa(task_data.question, task_data.context, db)
        return TaskResponse(task="qa", result=answer)
    
    elif task_type == "latest_answer":
        # task_data is already validated as LatestAnswerTask
        latest_answer = get_latest_answer(db)
        if not latest_answer:
            raise HTTPException(status_code=404, detail="No previous answers found")
        return TaskResponse(task="latest_answer", result=latest_answer)
    
    elif task_type == "image_generation":
        # task_data is already validated as ImageGenerationTask
        image_data = generate_image(task_data.prompt, db)
        return TaskResponse(task="image_generation", result=image_data)
    
    elif task_type == "content_generation":
        # task_data is already validated as ContentGenerationTask
        content = generate_content(task_data.prompt, task_data.platform, db)
        return TaskResponse(task="content_generation", result=content)
    
    else:
        raise HTTPException(status_code=400, detail=f"Unknown task type: {task_type}")