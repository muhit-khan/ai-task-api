from fastapi import APIRouter, Depends, HTTPException, Body
from app.models import QATask, LatestAnswerTask, ImageGenerationTask, ContentGenerationTask, TaskResponse
from app.services.qa_service import perform_qa, get_latest_answer
from app.services.image_service import generate_image
from app.services.content_service import generate_content
from app.database import get_db
from app.model_utils import get_available_models, get_model_status, get_popular_models, validate_model_config
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
    
    if task_type == "qa" and isinstance(task_data, QATask):
        # task_data is validated as QATask
        answer = perform_qa(task_data.question, task_data.context, db)
        return TaskResponse(task="qa", result=answer)
    
    elif task_type == "latest_answer" and isinstance(task_data, LatestAnswerTask):
        # task_data is validated as LatestAnswerTask
        latest_answer = get_latest_answer(db)
        if not latest_answer:
            raise HTTPException(status_code=404, detail="No previous answers found")
        return TaskResponse(task="latest_answer", result=latest_answer)
    
    elif task_type == "image_generation" and isinstance(task_data, ImageGenerationTask):
        # task_data is validated as ImageGenerationTask
        image_data = generate_image(task_data.prompt, db)
        return TaskResponse(task="image_generation", result=image_data)
    
    elif task_type == "content_generation" and isinstance(task_data, ContentGenerationTask):
        # task_data is validated as ContentGenerationTask
        content = generate_content(task_data.prompt, task_data.platform, db)
        return TaskResponse(task="content_generation", result=content)
    
    else:
        raise HTTPException(status_code=400, detail=f"Unknown task type: {task_type}")

@router.get("/models/info")
async def get_models_info():
    """
    Get information about all available models
    """
    return get_available_models()

@router.get("/models/status")
async def get_models_status():
    """
    Get current model configuration status
    """
    return get_model_status()

@router.get("/models/popular")
async def get_popular_models_list():
    """
    Get a list of popular models that can be used
    """
    return get_popular_models()

@router.get("/models/validate")
async def validate_models_config():
    """
    Validate current model configuration
    """
    return validate_model_config()