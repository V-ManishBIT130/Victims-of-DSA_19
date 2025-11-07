# Email Monitoring Service - PowerShell Launcher
# Runs the Python monitoring script in the background

Write-Host "================================================================================" -ForegroundColor Cyan
Write-Host "🛡️  EMAIL PHISHING DETECTION - AUTOMATED MONITOR" -ForegroundColor Cyan
Write-Host "================================================================================" -ForegroundColor Cyan
Write-Host ""

$scriptPath = Split-Path -Parent $MyInvocation.MyCommand.Path
Set-Location $scriptPath

# Check if Python is available
try {
    $pythonVersion = python --version 2>&1
    Write-Host "✅ Python found: $pythonVersion" -ForegroundColor Green
} catch {
    Write-Host "❌ Python not found! Please install Python 3.8+" -ForegroundColor Red
    exit 1
}

# Check if monitor script exists
if (-not (Test-Path "monitor_and_process.py")) {
    Write-Host "❌ monitor_and_process.py not found!" -ForegroundColor Red
    exit 1
}

Write-Host "📂 Working directory: $scriptPath" -ForegroundColor Yellow
Write-Host ""
Write-Host "🔄 Starting monitoring service..." -ForegroundColor Cyan
Write-Host "⏱️  Checking every 10 seconds for new emails" -ForegroundColor Cyan
Write-Host "🛑 Press Ctrl+C to stop" -ForegroundColor Yellow
Write-Host "================================================================================" -ForegroundColor Cyan
Write-Host ""

# Run the Python monitoring script
python monitor_and_process.py
