import io
from typing import Optional
from gtts import gTTS
import asyncio
from app.core.config import get_settings

class TextToSpeechService:
    def __init__(self):
        self.settings = get_settings()
    
    async def synthesize(self, text: str, voice: Optional[str] = None, lang: str = "en") -> bytes:
        """
        Convert text to speech using Google Text-to-Speech (gTTS).
        Returns audio bytes in MP3 format.
        """
        if not text or not text.strip():
            raise ValueError("Text is required for TTS")
        
        # Run gTTS in executor since it makes HTTP requests
        def generate_audio():
            tts = gTTS(text=text, lang=lang, slow=False)
            audio_buffer = io.BytesIO()
            tts.write_to_fp(audio_buffer)
            audio_buffer.seek(0)
            return audio_buffer.read()
        
        loop = asyncio.get_event_loop()
        audio_bytes = await loop.run_in_executor(None, generate_audio)
        
        return audio_bytes
    
    def get_content_type(self) -> str:
        """Return the content type for the audio format."""
        return "audio/mpeg"  # MP3 format
