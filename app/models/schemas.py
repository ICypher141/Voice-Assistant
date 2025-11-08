from pydantic import BaseModel, EmailStr
from typing import Optional

class ChatRequest(BaseModel):
    message: str

class ChatResponse(BaseModel):
    reply: str

class TTSRequest(BaseModel):
    text: str
    voice: Optional[str] = None

class EmailRequest(BaseModel):
    to: EmailStr
    subject: str
    body: str