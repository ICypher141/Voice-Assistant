# Swagger UI Testing Guide

## Access Swagger UI
1. Open your browser
2. Go to: **http://127.0.0.1:8000/docs**
3. You'll see all available endpoints with interactive testing

---

## Test 1: Health Check ✅

**Endpoint:** `GET /health`

**Steps:**
1. Find the `/health` endpoint in the Swagger UI
2. Click on it to expand
3. Click the **"Try it out"** button
4. Click **"Execute"**
5. Check the response

**Expected Response:**
```json
{
  "status": "ok"
}
```
**Status Code:** `200`

---

## Test 2: Chat Endpoint (Ollama) 💬

**Endpoint:** `POST /api/chat`

**Steps:**
1. Find the `/api/chat` endpoint
2. Click **"Try it out"**
3. Replace the example JSON with one of these test payloads:

### Test 2a: Simple Greeting
```json
{
  "message": "Hello! Can you hear me?"
}
```

### Test 2b: Question
```json
{
  "message": "What can you help me with?"
}
```

### Test 2c: Email Inquiry
```json
{
  "message": "I need to send an email"
}
```

4. Click **"Execute"**
5. Wait for response (may take a few seconds for Ollama to respond)

**Expected Response:**
```json
{
  "reply": "AI-generated response from Ollama"
}
```
**Status Code:** `200`

**Note:** If this fails, make sure:
- Ollama is running: `ollama serve`
- Model is pulled: `ollama pull llama3.2`
- Ollama host is correct in `.env` file

---

## Test 3: Text-to-Speech 🔊

**Endpoint:** `POST /api/tts`

**Steps:**
1. Find the `/api/tts` endpoint
2. Click **"Try it out"**
3. Use this test payload:

```json
{
  "text": "Hello, this is a test of the text to speech system",
  "voice": "default"
}
```

**Optional:** Test without voice parameter:
```json
{
  "text": "Testing without voice parameter"
}
```

4. Click **"Execute"**

**Expected Response:**
```json
{
  "content_type": "audio/wav",
  "audio_base64": "RIFF$...base64 encoded audio..."
}
```
**Status Code:** `200`

---

## Test 4: Speech-to-Text (Mock) 🎤

**Endpoint:** `POST /api/stt`

**Steps:**
1. Find the `/api/stt` endpoint
2. Click **"Try it out"**
3. Click **"Choose File"** button
4. Select any audio file (or create a dummy file):
   - Accepts: `.wav`, `.mp3`, `.m4a`, etc.
   - Note: This is currently a mock implementation
5. Click **"Execute"**

**Expected Response:**
```json
{
  "text": "Transcribed text from [filename]"
}
```
**Status Code:** `200`

**Note:** Currently returns a mock response based on filename. Real STT will be implemented later.

---

## Test 5: Email Sending 📧

**Endpoint:** `POST /api/email`

**Steps:**
1. Find the `/api/email` endpoint
2. Click **"Try it out"**
3. Use this test payload (replace with a real email for actual sending):

```json
{
  "to": "test@example.com",
  "subject": "Test Email from Voice Assistant",
  "body": "This is a test email sent from the voice assistant backend API."
}
```

4. Click **"Execute"**

**Expected Response:**
```json
{
  "status": "sent"
}
```
**Status Code:** `200`

**Note:** Make sure your `.env` file has correct SMTP credentials:
- `SMTP_HOST`
- `SMTP_PORT`
- `SMTP_USER`
- `SMTP_PASSWORD`

**Test with Real Email:**
Replace `test@example.com` with your actual email address to receive a test email.

---

## Test 6: Error Handling 🚨

### Test 6a: Empty Chat Message
**Endpoint:** `POST /api/chat`
```json
{
  "message": ""
}
```
**Expected:** Should handle gracefully or return an error message

### Test 6b: Invalid Email Format
**Endpoint:** `POST /api/email`
```json
{
  "to": "not-an-email",
  "subject": "Test",
  "body": "Test"
}
```
**Expected:** `422 Validation Error` (Pydantic validation)

### Test 6c: Missing Required Fields
**Endpoint:** `POST /api/email`
```json
{
  "to": "test@example.com"
}
```
**Expected:** `422 Validation Error` (missing subject/body)

---

## Quick Test Checklist ✅

- [ ] Health endpoint returns `{"status": "ok"}`
- [ ] Chat endpoint returns AI-generated response
- [ ] TTS endpoint returns base64 audio data
- [ ] STT endpoint accepts file upload
- [ ] Email endpoint validates email format
- [ ] Error cases return proper status codes

---

## Troubleshooting

### Chat endpoint not working?
- Check if Ollama is running: `ollama list`
- Verify model: `ollama pull llama3`
- Check server terminal for error messages

### Email endpoint failing?
- Verify `.env` file has SMTP credentials
- Check if SMTP server requires app-specific password
- Verify port and TLS settings match your email provider

### Server not starting?
- Check if port 8000 is already in use
- Verify virtual environment is activated
- Check for missing dependencies: `pip install -r requirements.txt`

---

## Pro Tips for Swagger UI

1. **Response Time:** Chat endpoint may take 5-10 seconds (Ollama processing)
2. **Copy Request:** Click "Example Value" to see JSON schema
3. **View Schema:** Click "Schema" tab to see request/response models
4. **Multiple Tests:** You can execute multiple requests without refreshing
5. **Download Response:** Right-click response to save/copy

---

## Next Steps After Testing

Once all endpoints work:
1. ✅ Backend is ready for frontend integration
2. ✅ Ready to replace STT/TTS mocks with real providers
3. ✅ Ready to add RAG functionality
4. ✅ Ready to set up CI/CD pipeline

