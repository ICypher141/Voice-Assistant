from fastapi import UploadFile
import os
import tempfile
import asyncio
from app.core.config import get_settings

class SpeechToTextService:
    def __init__(self):
        self.settings = get_settings()
        self._whisper_model = None
    
    async def _load_whisper_model(self):
        """Load Whisper model (cached for performance)."""
        if self._whisper_model is None:
            try:
                import whisper
                # Load model in executor thread to avoid blocking
                loop = asyncio.get_event_loop()
                self._whisper_model = await loop.run_in_executor(
                    None, 
                    lambda: whisper.load_model("base")
                )
            except ImportError:
                raise ImportError(
                    "Whisper not installed. Install with: pip install openai-whisper"
                )
        return self._whisper_model
    
    async def transcribe(self, file: UploadFile) -> str:
        """
        Transcribe audio file using OpenAI Whisper.
        Supports various audio formats (mp3, wav, m4a, etc.).
        """
        contents = await file.read()
        if not contents:
            raise ValueError("Empty audio file")
        
        # Get file extension
        filename = file.filename or "audio.wav"
        ext = filename.split('.')[-1] if '.' in filename else 'wav'
        
        # Save uploaded file temporarily
        with tempfile.NamedTemporaryFile(delete=False, suffix=f".{ext}") as temp_file:
            temp_file.write(contents)
            temp_path = temp_file.name
        
        try:
            # Load Whisper model
            model = await self._load_whisper_model()
            
            # Run transcription in executor (it's CPU-intensive)
            def run_transcription():
                result = model.transcribe(temp_path, language="en")
                return result["text"].strip()
            
            loop = asyncio.get_event_loop()
            transcribed_text = await loop.run_in_executor(None, run_transcription)
            
            return transcribed_text
        except ImportError as e:
            raise ImportError(
                f"Whisper not installed. Install with: pip install openai-whisper. Error: {str(e)}"
            )
        except Exception as e:
            raise ValueError(f"Transcription failed: {str(e)}")
        finally:
            # Clean up temporary file
            if os.path.exists(temp_path):
                try:
                    os.unlink(temp_path)
                except:
                    pass
