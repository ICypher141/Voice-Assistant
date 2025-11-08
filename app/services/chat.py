from app.services.llm import LLMService

SYSTEM_PROMPT = (
    "You are a concise, helpful voice assistant. "
    "Answer briefly, and ask for missing details when sending emails."
)


class ChatService:
    def __init__(self) -> None:
        self.llm = LLMService()

    def generate_reply(self, message: str) -> str:
        message = (message or "").strip()
        if not message:
            return "Please provide a message."
        prompt = f"{SYSTEM_PROMPT}\n\nUser: {message}\nAssistant:"
        reply = self.llm.generate(prompt)
        return reply or "I'm not sure how to answer that."