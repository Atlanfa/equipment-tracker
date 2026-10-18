#!/usr/bin/env pwsh
Write-Host "=========================================" -ForegroundColor Green
Write-Host "Equipment Tracking Project Setup" -ForegroundColor Green
Write-Host "=========================================" -ForegroundColor Green
Write-Host ""

# Check if Python is installed
try {
    $pythonVersion = python --version 2>&1
    Write-Host "Python found: $pythonVersion" -ForegroundColor Green
} catch {
    Write-Host "ERROR: Python is not installed or not in PATH" -ForegroundColor Red
    Write-Host "Please install Python from https://python.org" -ForegroundColor Yellow
    Read-Host "Press Enter to exit"
    exit 1
}

Write-Host ""

# Create virtual environment
Write-Host "Creating virtual environment..." -ForegroundColor Yellow
python -m venv venv
if ($LASTEXITCODE -ne 0) {
    Write-Host "ERROR: Failed to create virtual environment" -ForegroundColor Red
    Read-Host "Press Enter to exit"
    exit 1
}

# Activate virtual environment
Write-Host "Activating virtual environment..." -ForegroundColor Yellow
if ($IsWindows -or $env:OS -eq "Windows_NT") {
    & "venv\Scripts\Activate.ps1"
} else {
    & "venv/bin/activate"
}

# Install requirements
Write-Host "Installing dependencies..." -ForegroundColor Yellow
pip install -r requirements.txt
if ($LASTEXITCODE -ne 0) {
    Write-Host "ERROR: Failed to install dependencies" -ForegroundColor Red
    Read-Host "Press Enter to exit"
    exit 1
}

# Run migrations
Write-Host "Setting up database..." -ForegroundColor Yellow
python manage.py migrate
if ($LASTEXITCODE -ne 0) {
    Write-Host "ERROR: Database migration failed" -ForegroundColor Red
    Read-Host "Press Enter to exit"
    exit 1
}

# Collect static files
Write-Host "Collecting static files..." -ForegroundColor Yellow
python manage.py collectstatic --noinput

Write-Host ""
Write-Host "=========================================" -ForegroundColor Green
Write-Host "Setup Complete!" -ForegroundColor Green
Write-Host "=========================================" -ForegroundColor Green
Write-Host ""
Write-Host "To start the server:" -ForegroundColor Cyan
Write-Host "1. Activate environment: venv\Scripts\Activate.ps1 (Windows) or source venv/bin/activate (macOS/Linux)" -ForegroundColor White
Write-Host "2. Run server: python manage.py runserver 0.0.0.0:8000" -ForegroundColor White
Write-Host "3. Or use the startup scripts provided" -ForegroundColor White
Write-Host ""
Write-Host "Your application will be available at:" -ForegroundColor Cyan
Write-Host "- Local: http://localhost:8000" -ForegroundColor White
Write-Host "- Network: http://YOUR_IP:8000" -ForegroundColor White
Write-Host ""
Write-Host "Don't forget to update your IP address in settings.py!" -ForegroundColor Yellow
Write-Host ""
Read-Host "Press Enter to exit"
