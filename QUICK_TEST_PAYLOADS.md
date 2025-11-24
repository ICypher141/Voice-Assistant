# Quick Test Payloads - Copy & Paste for Swagger UI

## 🔗 Access Swagger UI: http://127.0.0.1:8000/docs

---

## 1️⃣ Chat Endpoint - POST /api/chat

### Test 1: Simple Greeting
```json
{
  "message": "Hello! Can you hear me?"
}
```

### Test 2: Question
```json
{
  "message": "What can you help me with?"
}
```

### Test 3: Email Request
```json
{
  "message": "I need to send an email to my colleague"
}
```

### Test 4: Complex Query
```json
{
  "message": "Explain what a voice assistant is in one sentence"
}
```

---

## 2️⃣ Text-to-Speech - POST /api/tts

### Test 1: Basic TTS
```json
{
  "text": "Hello, this is a test of the text to speech system",
  "voice": "default"
}
```

### Test 2: Without Voice Parameter
```json
{
  "text": "Testing without voice parameter"
}
```

### Test 3: Short Message
```json
{
  "text": "Hi there!",
  "voice": "default"
}
```

---

## 3️⃣ Email - POST /api/email

### Test 1: Simple Email (Use Real Email Address)
```json
{
  "to": "your-email@example.com",
  "subject": "Test Email from Voice Assistant",
  "body": "This is a test email sent from the voice assistant backend API."
}
```

### Test 2: Detailed Email
```json
{
  "to": "recipient@example.com",
  "subject": "Meeting Reminder",
  "body": "Hi,\n\nJust a reminder about our meeting tomorrow at 2 PM.\n\nBest regards,\nVoice Assistant"
}
```

### Test 3: HTML-like Email
```json
{
  "to": "test@example.com",
  "subject": "Project Update",
  "body": "Project Status:\n- Task 1: Complete\n- Task 2: In Progress\n- Task 3: Pending"
}
```

---

## 4️⃣ Error Testing - Expected Validation Errors

### Invalid Email Format
```json
{
  "to": "not-an-email-address",
  "subject": "Test",
  "body": "Test body"
}
```
**Expected:** `422 Unprocessable Entity`

### Missing Fields - Email
```json
{
  "to": "test@example.com"
}
```
**Expected:** `422 Unprocessable Entity` (missing subject/body)

### Empty Message - Chat
```json
{
  "message": ""
}
```
**Expected:** Should handle gracefully

---

## 📋 Quick Copy-Paste Checklist

Copy each payload above and paste into Swagger UI:

1. ✅ Open http://127.0.0.1:8000/docs
2. ✅ Click on endpoint (e.g., `/api/chat`)
3. ✅ Click **"Try it out"**
4. ✅ Delete the example JSON
5. ✅ Paste one of the payloads above
6. ✅ Click **"Execute"**
7. ✅ Check response status and content

---

## 🎯 Expected Status Codes

- ✅ **200 OK** - Request successful
- ❌ **400 Bad Request** - Invalid request data
- ❌ **422 Unprocessable Entity** - Validation error (Pydantic)
- ❌ **500 Internal Server Error** - Server-side error

---

## 💡 Tips

- **Chat responses** may take 5-10 seconds (Ollama processing)
- **Email tests** require valid SMTP credentials in `.env`
- **STT endpoint** - Use "Choose File" button (no JSON payload)
- **All endpoints** show response schema in Swagger UI

