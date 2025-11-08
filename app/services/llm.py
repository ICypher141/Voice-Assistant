from __future__ import annotations
from typing import Optional
import ollama
from app.core.config import get_settings

class LLMService:
    def __init__(self, model: Optional[str] = None, temperature: Optional[float] = None) -> None:
        settings = get_settings()
        # The Ollama python client uses OLLAMA_HOST env var; we rely on env for host
        self.model = model or settings.ollama_model
        self.temperature = temperature if temperature is not None else settings.ollama_temperature

    def generate(self, prompt: str) -> str:
        if not prompt or not prompt.strip():
            return ""
        response = ollama.generate(
            model=self.model,
            prompt=prompt,
            options={"temperature": self.temperature},
        )
        # Response dict contains key 'response'
        return response.get("response", "")