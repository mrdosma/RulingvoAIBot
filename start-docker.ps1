Write-Host "🔍 Checking Docker Desktop status..." -ForegroundColor Blue

# Check if Docker Desktop is running
$dockerProcess = Get-Process "Docker Desktop" -ErrorAction SilentlyContinue
if (-not $dockerProcess) {
    Write-Host "⚠️ Docker Desktop is not running. Starting Docker Desktop..." -ForegroundColor Yellow
    Start-Process "C:\Program Files\Docker\Docker\Docker Desktop.exe"
    Write-Host "⏳ Waiting for Docker Desktop to initialize (this may take a minute)..." -ForegroundColor Yellow
    
    # Wait for Docker to become available
    $attempts = 0
    $maxAttempts = 30
    do {
        $attempts++
        Start-Sleep -Seconds 10
        $dockerRunning = docker info 2>&1 | Select-String "Server Version" -Quiet
        Write-Host "." -NoNewline
        if ($attempts -eq $maxAttempts) {
            Write-Host "`n❌ Timeout waiting for Docker Desktop. Please ensure Docker Desktop is properly installed and running." -ForegroundColor Red
            exit 1
        }
    } while (-not $dockerRunning)
    Write-Host "`n✅ Docker Desktop is now running!" -ForegroundColor Green
} else {
    Write-Host "✅ Docker Desktop is running" -ForegroundColor Green
}

# Start the containers
Write-Host "`n🚀 Starting Docker containers..." -ForegroundColor Blue
docker compose up -d

if ($LASTEXITCODE -eq 0) {
    Write-Host "`n✅ Containers started successfully!" -ForegroundColor Green
    Write-Host "`n📊 Container Status:" -ForegroundColor Blue
    docker compose ps
    
    Write-Host "`n📝 Container Logs:" -ForegroundColor Blue
    Write-Host "Showing logs from the bot container. Press Ctrl+C to exit logs (containers will keep running)." -ForegroundColor Yellow
    docker compose logs -f bot
} else {
    Write-Host "`n❌ Failed to start containers. Please check the error messages above." -ForegroundColor Red
}