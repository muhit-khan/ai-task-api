from pydantic import BaseModel, Field
from typing import Optional, Union, Literal

class QATask(BaseModel):
    task: Literal["qa"] = "qa"
    question: str
    context: Optional[str] = None

class LatestAnswerTask(BaseModel):
    task: Literal["latest_answer"] = "latest_answer"

class ImageGenerationTask(BaseModel):
    task: Literal["image_generation"] = "image_generation"
    prompt: str

class ContentGenerationTask(BaseModel):
    task: Literal["content_generation"] = "content_generation"
    prompt: str
    platform: str

class TaskResponse(BaseModel):
    task: str
    result: Union[str, dict]