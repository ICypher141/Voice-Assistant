from fastapi import APIRouter, HTTPException
from fastapi import UploadFile, File
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
    service = TextToSpeechService()
    try:
        audio_bytes, content_type = await service.synthesize(request.text, request.voice)
        return {"content_type": content_type, "audio_base64": audio_bytes}
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