from pydantic_settings import BaseSettings
from pydantic import Field
from functools import lru_cache

class Settings(BaseSettings):
    app_name: str = "Voice Assistant API"
    smtp_host: str = Field(..., env="SMTP_HOST")
    smtp_port: int = Field(587, env="SMTP_PORT")
    smtp_user: str = Field(..., env="SMTP_USER")
    smtp_password: str = Field(..., env="SMTP_PASSWORD")
    smtp_use_tls: bool = Field(True, env="SMTP_USE_TLS")
    # Ollama configuration
    ollama_host: str = Field("http://localhost:11434", env="OLLAMA_HOST")
    ollama_model: str = Field("llama3.2", env="OLLAMA_MODEL")
    ollama_temperature: float = Field(0.4, env="OLLAMA_TEMPERATURE")
    # Retrieval-Augmented Generation (RAG)
    rag_documents_dir: str = Field("knowledge_base", env="RAG_DOCUMENTS_DIR")
    rag_embedding_model: str = Field("nomic-embed-text", env="RAG_EMBEDDING_MODEL")
    rag_top_k: int = Field(3, ge=1, le=10, env="RAG_TOP_K")
    rag_min_score: float = Field(0.25, ge=0.0, le=1.0, env="RAG_MIN_SCORE")

    class Config:
        env_file = ".env"
        case_sensitive = False

@lru_cache(maxsize=1)
def get_settings() -> Settings:
    return Settings()