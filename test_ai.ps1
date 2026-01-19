# Test Real AI Integration
Write-Host "🧪 Testing Real AI Integration" -ForegroundColor Cyan
Write-Host "=" * 50 -ForegroundColor Yellow

# Start server in background
Write-Host "🚀 Starting backend server..." -ForegroundColor Green
$server = Start-Process -FilePath "python" -ArgumentList "debug_server.py" -NoNewWindow -PassThru

# Wait for server to start
Write-Host "⏳ Waiting for server to start..." -ForegroundColor Yellow
Start-Sleep -Seconds 5

# Test health endpoint
Write-Host "🏥 Testing health endpoint..." -ForegroundColor Green
try {
    $response = Invoke-WebRequest -Uri "http://localhost:8000/api/v1/stories/health" -Method GET -TimeoutSec 10
    if ($response.StatusCode -eq 200) {
        $data = $response.Content | ConvertFrom-Json
        Write-Host "✅ Health check successful!" -ForegroundColor Green
        Write-Host "AI Integration Status: $($data.ai_integration)" -ForegroundColor Cyan
        Write-Host "Agent Status: $($data.agents)" -ForegroundColor Cyan

        if ($data.ai_integration -eq "enabled") {
            Write-Host "🎉 REAL AI AGENTS ARE ACTIVE!" -ForegroundColor Green
        } else {
            Write-Host "⚠️ AI integration is disabled - using mock responses" -ForegroundColor Yellow
        }
    } else {
        Write-Host "❌ Health check failed with status: $($response.StatusCode)" -ForegroundColor Red
    }
} catch {
    Write-Host "❌ Cannot connect to server: $($_.Exception.Message)" -ForegroundColor Red
}

# Clean up server
Write-Host "🧹 Stopping server..." -ForegroundColor Yellow
Stop-Process -Id $server.Id -Force

Write-Host ""
Write-Host "=" * 50 -ForegroundColor Yellow
if ($data.ai_integration -eq "enabled") {
    Write-Host "🎉 Real AI integration test PASSED!" -ForegroundColor Green
    Write-Host "Your AI agents are working with real OpenAI API."
} else {
    Write-Host "❌ Real AI integration test FAILED!" -ForegroundColor Red
    Write-Host "Check your API key configuration."
}