# Voice Assistant Backend (FastAPI)

## Features
- Chat endpoint (Ollama-powered)
- Retrieval-Augmented Generation (RAG) endpoint grounded in local docs
- Speech-to-Text (mock)
- Text-to-Speech (mock)
- Send Email via SMTP

## Requirements
- Python 3.11+

## Setup
1. Create and fill .env based on .env.example
2. Install deps:
```bash
pip install -r requirements.txt
```
3. Run server:
```bash
uvicorn app.main:app --reload
```

## Ollama (Local LLM)
1. Install Ollama and start the server (OLLAMA_HOST defaults to http://localhost:11434)
2. Pull a model, e.g.:
```bash
ollama pull llama3.2
```
3. Set `.env` values if needed:
```bash
OLLAMA_HOST=http://localhost:11434
OLLAMA_MODEL=llama3.2
OLLAMA_TEMPERATURE=0.4
```
4. The chat endpoint will use the local model automatically.

## Endpoints
- POST /api/chat { message }
- POST /api/rag { query }
- POST /api/stt (multipart/form-data, file)
- POST /api/tts { text, voice? }
- POST /api/email { to, subject, body }

### RAG Workflow
1. Place `.md` or `.txt` files inside `knowledge_base/` (configurable with `RAG_DOCUMENTS_DIR`).
2. Each file is chunked (~1,200 chars) and embedded via Ollama's `nomic-embed-text` model.
3. The `/api/rag` endpoint retrieves the top `RAG_TOP_K` chunks above `RAG_MIN_SCORE` and feeds them to the chat model.
4. Responses include `sources` with short previews so clients can display citations.

Environment overrides:
```
RAG_DOCUMENTS_DIR=knowledge_base
RAG_EMBEDDING_MODEL=nomic-embed-text
RAG_TOP_K=3
RAG_MIN_SCORE=0.25
```

Restart the FastAPI server after modifying the knowledge base to rebuild embeddings.

## Roadmap
- Replace mock STT/TTS with providers
- Expand knowledge base management tooling
- CI/CD pipeline