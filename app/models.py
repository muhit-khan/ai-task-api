from pydantic import BaseModel
from typing import Optional, Literal

class AITaskRequest(BaseModel):
    task: Literal["qa", "get_latest_answer", "generate_image", "generate_content"]
    prompt: Optional[str] = None
    platform: Optional[str] = None

class QAResponse(BaseModel):
    answer: str

class LatestAnswerResponse(BaseModel):
    question: str
    answer: str

class ImageResponse(BaseModel):
    image_url: Optional[str] = None
    image_base64: Optional[str] = None

class ContentResponse(BaseModel):
    content: str

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: Optional[str] = None

class User(BaseModel):
    username: str
    email: Optional[str] = None
    full_name: Optional[str] = None
    disabled: bool = False

class UserInDB(User):
    hashed_password: str

class UserCreate(BaseModel):
    username: str
    email: Optional[str] = None
    full_name: Optional[str] = None
    password: str