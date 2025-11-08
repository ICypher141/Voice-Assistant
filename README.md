# Voice Assistant Backend (FastAPI)

## Features
- Chat endpoint (Ollama-powered)
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
ollama pull llama3
```
3. Set `.env` values if needed:
```bash
OLLAMA_HOST=http://localhost:11434
OLLAMA_MODEL=llama3
OLLAMA_TEMPERATURE=0.4
```
4. The chat endpoint will use the local model automatically.

## Endpoints
- POST /api/chat { message }
- POST /api/stt (multipart/form-data, file)
- POST /api/tts { text, voice? }
- POST /api/email { to, subject, body }

## Roadmap
- Replace mock STT/TTS with providers
- Add RAG for knowledge grounding
- CI/CD pipeline