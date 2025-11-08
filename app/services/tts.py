import base64
from typing import Optional, Tuple

class TextToSpeechService:
    async def synthesize(self, text: str, voice: Optional[str] = None) -> Tuple[str, str]:
        if not text:
            raise ValueError("Text is required for TTS")
        wav_header = b"RIFF$\x80\x00\x00WAVEfmt \x10\x00\x00\x00\x01\x00\x01\x00D\xac\x00\x00\x88X\x01\x00\x02\x00\x10\x00data\x00\x80\x00\x00"
        b64 = base64.b64encode(wav_header).decode("ascii")
        return b64, "audio/wav"