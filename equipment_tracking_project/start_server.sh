#!/bin/bash

echo "========================================="
echo "Equipment Tracking Server - Linux"
echo "========================================="
echo

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "ERROR: Virtual environment not found!"
    echo "Please run ./setup.sh first"
    exit 1
fi

# Activate virtual environment
source venv/bin/activate

# Check if Django is installed
if ! python -c "import django" &> /dev/null; then
    echo "ERROR: Django not found in virtual environment"
    echo "Please run ./setup.sh to install dependencies"
    exit 1
fi

# Get IP address for display
IP_ADDRESS=$(hostname -I | awk '{print $1}')
if [ -z "$IP_ADDRESS" ]; then
    IP_ADDRESS=$(ip route get 1 | awk '{print $7; exit}')
fi

echo "Starting Django development server..."
echo "Local access: http://localhost:8000"
echo "Network access: http://$IP_ADDRESS:8000"
echo
echo "Press Ctrl+C to stop the server"
echo

# Start the server
python manage.py runserver 0.0.0.0:8000
