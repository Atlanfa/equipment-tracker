Write-Host "Starting Django HTTPS Development Server for Local Network Access" -ForegroundColor Green
Write-Host ""
Write-Host "Your server will be accessible at:" -ForegroundColor Yellow
Write-Host "  - Local: https://localhost:8000" -ForegroundColor Cyan
Write-Host "  - Network: https://10.0.0.180:8000" -ForegroundColor Cyan
Write-Host ""
Write-Host "Other devices on your network can access at: https://10.0.0.180:8000" -ForegroundColor Magenta
Write-Host ""
Write-Host "IMPORTANT: You will see security warnings - this is normal for self-signed certificates" -ForegroundColor Red
Write-Host "Click 'Advanced' then 'Proceed to site' or 'Accept the risk' in your browser" -ForegroundColor Red
Write-Host ""
Write-Host "Press Ctrl+C to stop the server" -ForegroundColor Yellow
Write-Host ""

# Change to the script directory
Set-Location $PSScriptRoot

# Start Django HTTPS server
& "c:/Users/mc_al/Desktop/dashboardV2/.venv/Scripts/python.exe" manage.py runserver_plus --cert-file cert.pem --key-file key.pem 0.0.0.0:8000
