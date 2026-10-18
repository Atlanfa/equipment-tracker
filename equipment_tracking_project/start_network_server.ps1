Write-Host "Starting Django Development Server for Local Network Access" -ForegroundColor Green
Write-Host ""
Write-Host "Your server will be accessible at:" -ForegroundColor Yellow
Write-Host "  - Local: http://localhost:8000" -ForegroundColor Cyan
Write-Host "  - Network: http://YOUR_IP:8000 (replace YOUR_IP with your computer's IP address)" -ForegroundColor Cyan
Write-Host ""
Write-Host "To find your IP address:" -ForegroundColor Magenta
Write-Host "  Windows: ipconfig" -ForegroundColor White
Write-Host "  macOS/Linux: ifconfig" -ForegroundColor White
Write-Host ""
Write-Host "Press Ctrl+C to stop the server" -ForegroundColor Red
Write-Host ""

# Change to the script directory
Set-Location $PSScriptRoot

# Start Django server
python manage.py runserver 0.0.0.0:8000
