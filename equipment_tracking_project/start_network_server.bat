@echo off
echo Starting Django Development Server for Local Network Access
echo.
echo Your server will be accessible at:
echo   - Local: http://localhost:8000
echo   - Network: http://YOUR_IP:8000 (replace YOUR_IP with your computer's IP address)
echo.
echo To find your IP address, run: ipconfig
echo Other devices on your network can access at: http://YOUR_IP:8000
echo.
echo Press Ctrl+C to stop the server
echo.
python manage.py runserver 0.0.0.0:8000
pause
