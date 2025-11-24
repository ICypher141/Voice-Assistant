from pydantic import BaseModel, EmailStr, Field
from typing import Optional

class ChatRequest(BaseModel):
    message: str = Field(..., description="The user's message to the assistant")

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "message": "Hello! Can you help me?"
                },
                {
                    "message": "What can you do?"
                }
            ]
        }
    }

class ChatResponse(BaseModel):
    reply: str = Field(..., description="The assistant's reply")

class TTSRequest(BaseModel):
    text: str = Field(..., description="The text to convert to speech")
    voice: Optional[str] = Field(None, description="Voice type (optional)")

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "text": "Hello, this is a test message",
                    "voice": "default"
                },
                {
                    "text": "Testing without voice parameter"
                }
            ]
        }
    }

class EmailRequest(BaseModel):
    to: EmailStr = Field(..., description="Recipient email address")
    subject: str = Field(..., description="Email subject")
    body: str = Field(..., description="Email body content")

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "to": "recipient@example.com",
                    "subject": "Test Email",
                    "body": "This is a test email from the voice assistant."
                },
                {
                    "to": "user@example.com",
                    "subject": "Meeting Reminder",
                    "body": "Hi,\n\nJust a reminder about our meeting tomorrow at 2 PM.\n\nBest regards"
                }
            ]
        }
    }
