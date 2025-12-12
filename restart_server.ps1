# Clean Server Restart Script
# Stops all Python processes, clears cache, and restarts server

Write-Host "🔧 Stopping all Python processes..." -ForegroundColor Yellow
taskkill /F /IM python.exe 2>$null
Start-Sleep -Seconds 2

Write-Host "🧹 Clearing Python cache..." -ForegroundColor Yellow
Remove-Item -Recurse -Force backend\__pycache__ -ErrorAction SilentlyContinue
Remove-Item -Recurse -Force backend\routers\__pycache__ -ErrorAction SilentlyContinue
Remove-Item -Recurse -Force backend\database\__pycache__ -ErrorAction SilentlyContinue
Remove-Item -Recurse -Force backend\automation\__pycache__ -ErrorAction SilentlyContinue

Write-Host "✅ Cache cleared!" -ForegroundColor Green
Write-Host ""
Write-Host "🚀 Starting server..." -ForegroundColor Cyan
Write-Host "Server will be available at: http://localhost:8000" -ForegroundColor White
Write-Host ""
Write-Host "⚠️  After server starts:" -ForegroundColor Yellow
Write-Host "   1. Open browser" -ForegroundColor White
Write-Host "   2. Press Ctrl+Shift+R (Hard Refresh)" -ForegroundColor White
Write-Host "   3. Go to http://localhost:8000" -ForegroundColor White
Write-Host ""

uvicorn backend.main:app --reload --port 8000
