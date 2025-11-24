# Voice Assistant Backend Testing Script
# Make sure the server is running first: uvicorn app.main:app --reload

Write-Host "=== Testing Voice Assistant Backend ===" -ForegroundColor Cyan
Write-Host ""

# Test 1: Health Check
Write-Host "Test 1: Health Check" -ForegroundColor Yellow
try {
    $response = Invoke-WebRequest -Uri "http://127.0.0.1:8000/health" -Method GET -UseBasicParsing
    Write-Host "✅ Status: $($response.StatusCode)" -ForegroundColor Green
    Write-Host "   Response: $($response.Content)" -ForegroundColor Green
} catch {
    Write-Host "❌ Health check failed: $_" -ForegroundColor Red
}
Write-Host ""

# Test 2: Chat Endpoint (Ollama)
Write-Host "Test 2: Chat Endpoint (Ollama)" -ForegroundColor Yellow
try {
    $body = @{
        message = "Hello! Say 'backend is working' if you can read this."
    } | ConvertTo-Json

    $response = Invoke-WebRequest -Uri "http://127.0.0.1:8000/api/chat" -Method POST -Body $body -ContentType "application/json" -UseBasicParsing
    Write-Host "✅ Status: $($response.StatusCode)" -ForegroundColor Green
    $json = $response.Content | ConvertFrom-Json
    Write-Host "   Reply: $($json.reply)" -ForegroundColor Green
} catch {
    Write-Host "❌ Chat endpoint failed: $_" -ForegroundColor Red
    Write-Host "   Make sure Ollama is running (ollama serve) and model is pulled (ollama pull llama3.2)" -ForegroundColor Yellow
}
Write-Host ""

# Test 3: Text-to-Speech
Write-Host "Test 3: Text-to-Speech" -ForegroundColor Yellow
try {
    $body = @{
        text = "Testing text to speech"
        voice = "default"
    } | ConvertTo-Json

    $response = Invoke-WebRequest -Uri "http://127.0.0.1:8000/api/tts" -Method POST -Body $body -ContentType "application/json" -UseBasicParsing
    Write-Host "✅ Status: $($response.StatusCode)" -ForegroundColor Green
    $json = $response.Content | ConvertFrom-Json
    Write-Host "   Content Type: $($json.content_type)" -ForegroundColor Green
    Write-Host "   Audio data received: $($json.audio_base64.Length > 0)" -ForegroundColor Green
} catch {
    Write-Host "❌ TTS endpoint failed: $_" -ForegroundColor Red
}
Write-Host ""

# Test 4: Speech-to-Text (Mock)
Write-Host "Test 4: Speech-to-Text (Mock)" -ForegroundColor Yellow
try {
    # Create a dummy audio file
    $dummyAudio = [byte[]]@(0x52, 0x49, 0x46, 0x46)  # "RIFF" header
    $tempFile = "test_audio.wav"
    $dummyAudio | Set-Content -Path $tempFile -Encoding Byte -ErrorAction SilentlyContinue
    
    $boundary = [System.Guid]::NewGuid().ToString()
    $bodyLines = @()
    $bodyLines += "--$boundary"
    $bodyLines += 'Content-Disposition: form-data; name="file"; filename="test_audio.wav"'
    $bodyLines += 'Content-Type: audio/wav'
    $bodyLines += ""
    $bodyLines += "RIFF"
    $bodyLines += "--$boundary--"
    
    $body = $bodyLines -join "`r`n"
    $bodyBytes = [System.Text.Encoding]::UTF8.GetBytes($body)
    
    $response = Invoke-WebRequest -Uri "http://127.0.0.1:8000/api/stt" -Method POST -ContentType "multipart/form-data; boundary=$boundary" -Body $bodyBytes -UseBasicParsing -ErrorAction SilentlyContinue
    
    if ($response.StatusCode -eq 200) {
        Write-Host "✅ Status: $($response.StatusCode)" -ForegroundColor Green
        $json = $response.Content | ConvertFrom-Json
        Write-Host "   Transcribed: $($json.text)" -ForegroundColor Green
    }
    
    Remove-Item $tempFile -ErrorAction SilentlyContinue
} catch {
    Write-Host "⚠️  STT endpoint test skipped (requires proper multipart form)" -ForegroundColor Yellow
    Write-Host "   You can test this manually via Swagger UI at http://127.0.0.1:8000/docs" -ForegroundColor Yellow
}
Write-Host ""

# Test 5: Email Endpoint (Validation only - won't send without proper SMTP)
Write-Host "Test 5: Email Endpoint (Structure Test)" -ForegroundColor Yellow
try {
    $body = @{
        to = "test@example.com"
        subject = "Test Subject"
        body = "Test body"
    } | ConvertTo-Json

    $response = Invoke-WebRequest -Uri "http://127.0.0.1:8000/api/email" -Method POST -Body $body -ContentType "application/json" -UseBasicParsing
    Write-Host "✅ Status: $($response.StatusCode)" -ForegroundColor Green
    $json = $response.Content | ConvertFrom-Json
    Write-Host "   Response: $($json.status)" -ForegroundColor Green
} catch {
    Write-Host "⚠️  Email endpoint: $_" -ForegroundColor Yellow
    Write-Host "   Make sure SMTP credentials are set in .env file" -ForegroundColor Yellow
}
Write-Host ""

# Summary
Write-Host "=== Testing Complete ===" -ForegroundColor Cyan
Write-Host ""
Write-Host "📝 Additional Testing Options:" -ForegroundColor Cyan
Write-Host '   • Interactive API Docs: http://127.0.0.1:8000/docs' -ForegroundColor White
Write-Host '   • Alternative Docs: http://127.0.0.1:8000/redoc' -ForegroundColor White
Write-Host ""

