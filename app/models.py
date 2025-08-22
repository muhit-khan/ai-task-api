from pydantic import BaseModel
from typing import Optional, Union

class QATask(BaseModel):
    task: str = "qa"
    question: str
    context: Optional[str] = None

class LatestAnswerTask(BaseModel):
    task: str = "latest_answer"

class ImageGenerationTask(BaseModel):
    task: str = "image_generation"
    prompt: str

class ContentGenerationTask(BaseModel):
    task: str = "content_generation"
    prompt: str
    platform: str

class TaskResponse(BaseModel):
    task: str
    result: Union[str, dict]

class QARequest(BaseModel):
    task: str
    question: str
    context: Optional[str] = None

class ImageRequest(BaseModel):
    task: str
    prompt: str

class ContentRequest(BaseModel):
    task: str
    prompt: str
    platform: str

TaskRequest = Union[QARequest, ImageRequest, ContentRequest]