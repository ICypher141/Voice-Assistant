from fastapi import UploadFile

class SpeechToTextService:
    async def transcribe(self, file: UploadFile) -> str:
        contents = await file.read()
        if not contents:
            raise ValueError("Empty audio file")
        name = file.filename or "audio"
        return f"Transcribed text from {name}"