@echo off
echo Starting Django HTTPS Development Server for Local Network Access
echo.
echo Your server will be accessible at:
echo   - Local: https://localhost:8000
echo   - Network: https://10.0.0.180:8000
echo.
echo Other devices on your network can access at: https://10.0.0.180:8000
echo.
echo IMPORTANT: You will see security warnings - this is normal for self-signed certificates
echo Click "Advanced" then "Proceed to site" or "Accept the risk" in your browser
echo.
echo Press Ctrl+C to stop the server
echo.
c:/Users/mc_al/Desktop/dashboardV2/.venv/Scripts/python.exe manage.py runserver_plus --cert-file cert.pem --key-file key.pem 0.0.0.0:8000
pause
