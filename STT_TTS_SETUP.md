# Speech-to-Text (STT) & Text-to-Speech (TTS) Setup Guide

## ✅ What's Implemented

### 🎤 **Speech-to-Text (STT)**
- **Real transcription** using OpenAI Whisper
- Supports multiple audio formats (mp3, wav, m4a, flac, etc.)
- High accuracy transcription
- Async processing for better performance

### 🔊 **Text-to-Speech (TTS)**
- **Real audio generation** using Google Text-to-Speech (gTTS)
- Returns MP3 audio file that can be played directly in browsers
- Supports multiple languages
- Streaming audio response

---

## 📦 Installation

### 1. Install New Dependencies

```bash
pip install -r requirements.txt
```

This will install:
- `openai-whisper` - For speech-to-text transcription
- `gtts` - For text-to-speech audio generation

### 2. Install Whisper Dependencies

Whisper requires `ffmpeg` for audio processing:

**Windows:**
```powershell
# Using chocolatey
choco install ffmpeg

# Or download from: https://ffmpeg.org/download.html
# Add to PATH after installation
```

**Linux/Mac:**
```bash
sudo apt-get install ffmpeg  # Ubuntu/Debian
brew install ffmpeg           # Mac
```

**Verify installation:**
```bash
ffmpeg -version
```

---

## 🚀 Usage

### **Speech-to-Text Endpoint**

**Endpoint:** `POST /api/stt`

**In Swagger UI:**
1. Go to http://127.0.0.1:8000/docs
2. Find `/api/stt` endpoint
3. Click "Try it out"
4. Click "Choose File" and upload an audio file
5. Click "Execute"

**Response:**
```json
{
  "text": "Transcribed text from your audio file"
}
```

**Supported Formats:**
- MP3 (.mp3)
- WAV (.wav)
- M4A (.m4a)
- FLAC (.flac)
- OGG (.ogg)
- And more...

**Example with curl:**
```bash
curl -X POST "http://127.0.0.1:8000/api/stt" \
  -F "file=@audio.mp3"
```

---

### **Text-to-Speech Endpoint**

**Endpoint:** `POST /api/tts`

**In Swagger UI:**
1. Go to http://127.0.0.1:8000/docs
2. Find `/api/tts` endpoint
3. Click "Try it out"
4. Use this payload:
```json
{
  "text": "Hello, this is a test message",
  "voice": "default"
}
```
5. Click "Execute"
6. **The audio will play automatically in the browser!** 🎵

**Response:**
- Returns MP3 audio file directly (not JSON)
- Browser will play it automatically
- You can also download the audio

**Example with curl:**
```bash
curl -X POST "http://127.0.0.1:8000/api/tts" \
  -H "Content-Type: application/json" \
  -d '{"text": "Hello world"}' \
  --output speech.mp3

# Play the file
# Windows:
start speech.mp3
# Mac:
afplay speech.mp3
# Linux:
mpg123 speech.mp3
```

---

## 🎯 Testing Tips

### **Test STT:**
1. Record a short audio message (30 seconds or less)
2. Save as MP3 or WAV
3. Upload via Swagger UI or curl
4. Check transcribed text

### **Test TTS:**
1. Send any text message via `/api/tts`
2. Audio will stream back as MP3
3. Browser will play it automatically
4. Or save the response as `.mp3` file

---

## ⚙️ Configuration

### **Whisper Model Size**

By default, uses `base` model for good balance of speed/accuracy.

To change model size, edit `app/services/stt.py`:
- `tiny` - Fastest, least accurate
- `base` - Default, good balance
- `small` - Better accuracy
- `medium` - High accuracy
- `large` - Best accuracy, slowest

**Note:** Larger models take more time and memory.

### **TTS Language**

Default is English (`en`). To change:

Edit `app/services/tts.py` in the `synthesize` method:
```python
tts = gTTS(text=text, lang="es", slow=False)  # Spanish
```

Supported languages: https://gtts.readthedocs.io/en/latest/module.html#languages-gtts-lang

---

## 🔧 Troubleshooting

### **STT Issues:**

**Error: "Whisper not installed"**
```bash
pip install openai-whisper
```

**Error: "ffmpeg not found"**
- Install ffmpeg (see Installation section above)
- Make sure it's in your PATH

**Transcription is slow:**
- First run downloads the model (base model ~150MB)
- Subsequent runs are faster
- Use `tiny` model for faster transcription

**No audio transcribed:**
- Check audio file format (must be supported format)
- Ensure audio has actual speech (not silence)
- Try a different audio file

### **TTS Issues:**

**Error: "gTTS not installed"**
```bash
pip install gtts
```

**No audio playback in browser:**
- Check browser audio settings
- Try downloading the audio file
- Check network connection (gTTS requires internet)

**Audio quality issues:**
- gTTS quality is limited by Google's free service
- For better quality, consider paid services (Azure, AWS Polly, etc.)

---

## 📝 Next Steps

For production, consider:
1. **Better TTS:** Azure Cognitive Services, AWS Polly, or ElevenLabs
2. **Caching:** Cache TTS results for common phrases
3. **Streaming:** Stream audio chunks for real-time playback
4. **Language Detection:** Auto-detect language in STT

---

## 🎉 You're All Set!

Now you have:
- ✅ Real speech-to-text transcription
- ✅ Real text-to-speech generation
- ✅ Playable audio responses
- ✅ Multiple audio format support

Test both endpoints in Swagger UI to see them in action!

