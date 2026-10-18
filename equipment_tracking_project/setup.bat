@echo off
echo =========================================
echo Equipment Tracking Project Setup
echo =========================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ERROR: Python is not installed or not in PATH
    echo Please install Python from https://python.org
    pause
    exit /b 1
)

echo Python found! Proceeding with setup...
echo.

REM Create virtual environment
echo Creating virtual environment...
python -m venv venv
if %errorlevel% neq 0 (
    echo ERROR: Failed to create virtual environment
    pause
    exit /b 1
)

REM Activate virtual environment
echo Activating virtual environment...
call venv\Scripts\activate.bat

REM Install requirements
echo Installing dependencies...
pip install -r requirements.txt
if %errorlevel% neq 0 (
    echo ERROR: Failed to install dependencies
    pause
    exit /b 1
)

REM Run migrations
echo Setting up database...
python manage.py migrate
if %errorlevel% neq 0 (
    echo ERROR: Database migration failed
    pause
    exit /b 1
)

REM Collect static files
echo Collecting static files...
python manage.py collectstatic --noinput

echo.
echo =========================================
echo Setup Complete!
echo =========================================
echo.
echo To start the server:
echo 1. Run: venv\Scripts\activate.bat
echo 2. Run: python manage.py runserver 0.0.0.0:8000
echo 3. Or double-click: start_network_server.bat
echo.
echo Your application will be available at:
echo - Local: http://localhost:8000
echo - Network: http://YOUR_IP:8000
echo.
echo Don't forget to update your IP address in settings.py!
echo.
pause
