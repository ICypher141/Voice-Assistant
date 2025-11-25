from fastapi import APIRouter, HTTPException
from fastapi import UploadFile, File
from fastapi.responses import Response
from app.models.schemas import ChatRequest, ChatResponse, TTSRequest, EmailRequest
from app.services.chat import ChatService
from app.services.stt import SpeechToTextService
from app.services.tts import TextToSpeechService
from app.services.email_service import EmailService
import asyncio

router = APIRouter()

@router.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    service = ChatService()
    # Offload blocking LLM call to a worker thread
    reply = await asyncio.get_event_loop().run_in_executor(None, service.generate_reply, request.message)
    return ChatResponse(reply=reply)

@router.post("/stt")
async def stt(file: UploadFile = File(...)):
    service = SpeechToTextService()
    try:
        text = await service.transcribe(file)
        return {"text": text}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/tts")
async def tts(request: TTSRequest):
    """
    Convert text to speech and return audio file that can be played directly.
    Returns MP3 audio that browsers can play automatically.
    """
    service = TextToSpeechService()
    try:
        audio_bytes = await service.synthesize(request.text, request.voice)
        content_type = service.get_content_type()
        
        # Return audio file directly as streaming response
        return Response(
            content=audio_bytes,
            media_type=content_type,
            headers={
                "Content-Disposition": 'inline; filename="speech.mp3"',
                "Accept-Ranges": "bytes"
            }
        )
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/email")
async def send_email(request: EmailRequest):
    service = EmailService()
    try:
        service.send_email(request.to, request.subject, request.body)
        return {"status": "sent"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))