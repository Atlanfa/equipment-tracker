#!/bin/bash

echo "========================================="
echo "Equipment Tracking Project Setup (Linux)"
echo "========================================="
echo

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "ERROR: Python 3 is not installed"
    echo "Please install Python 3:"
    echo "  Ubuntu/Debian: sudo apt update && sudo apt install python3 python3-pip python3-venv"
    echo "  CentOS/RHEL: sudo yum install python3 python3-pip"
    echo "  Fedora: sudo dnf install python3 python3-pip"
    echo "  Arch: sudo pacman -S python python-pip"
    exit 1
fi

echo "Python 3 found: $(python3 --version)"
echo

# Create virtual environment
echo "Creating virtual environment..."
python3 -m venv venv
if [ $? -ne 0 ]; then
    echo "ERROR: Failed to create virtual environment"
    echo "You may need to install python3-venv:"
    echo "  Ubuntu/Debian: sudo apt install python3-venv"
    exit 1
fi

# Activate virtual environment
echo "Activating virtual environment..."
source venv/bin/activate

# Upgrade pip
echo "Upgrading pip..."
pip install --upgrade pip

# Install requirements
echo "Installing dependencies..."
pip install -r requirements.txt
if [ $? -ne 0 ]; then
    echo "ERROR: Failed to install dependencies"
    exit 1
fi

# Run migrations
echo "Setting up database..."
python manage.py migrate
if [ $? -ne 0 ]; then
    echo "ERROR: Database migration failed"
    exit 1
fi

# Collect static files
echo "Collecting static files..."
python manage.py collectstatic --noinput

echo
echo "========================================="
echo "Setup Complete!"
echo "========================================="
echo
echo "To start the server:"
echo "1. Activate environment: source venv/bin/activate"
echo "2. Run server: python manage.py runserver 0.0.0.0:8000"
echo "3. Or use: ./start_server.sh"
echo
echo "Your application will be available at:"
echo "- Local: http://localhost:8000"
echo "- Network: http://YOUR_IP:8000"
echo
echo "To find your IP address: ip addr show or ifconfig"
echo "Don't forget to update your IP address in settings.py!"
echo
read -p "Press Enter to continue..."
