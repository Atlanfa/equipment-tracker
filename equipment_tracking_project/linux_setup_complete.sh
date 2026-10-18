#!/bin/bash

# Equipment Tracking Project - Linux Transfer and Setup Script
# This script automates the complete setup process on a Linux machine

echo "========================================="
echo "Equipment Tracking Project"
echo "Linux Transfer and Setup"
echo "========================================="
echo

# Color codes for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to print colored messages
print_status() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Check if running as root
if [ "$EUID" -eq 0 ]; then
    print_warning "Running as root. Consider using a regular user account."
fi

# Check Linux distribution
if [ -f /etc/os-release ]; then
    . /etc/os-release
    OS=$NAME
    print_status "Detected OS: $OS"
else
    print_warning "Cannot detect Linux distribution"
    OS="Unknown"
fi

# Function to install prerequisites based on distribution
install_prerequisites() {
    print_status "Installing prerequisites..."
    
    case $OS in
        *"Ubuntu"*|*"Debian"*)
            sudo apt update
            sudo apt install -y python3 python3-pip python3-venv python3-dev build-essential
            ;;
        *"CentOS"*|*"Red Hat"*|*"Rocky"*)
            sudo dnf install -y python3 python3-pip python3-venv python3-devel gcc
            ;;
        *"Fedora"*)
            sudo dnf install -y python3 python3-pip python3-venv python3-devel gcc
            ;;
        *"Arch"*)
            sudo pacman -S --noconfirm python python-pip base-devel
            ;;
        *)
            print_warning "Unknown distribution. Please install Python 3, pip, and venv manually."
            ;;
    esac
}

# Check if Python 3 is installed
check_python() {
    if command -v python3 &> /dev/null; then
        PYTHON_VERSION=$(python3 --version | cut -d ' ' -f 2)
        print_success "Python 3 found: $PYTHON_VERSION"
        return 0
    else
        print_error "Python 3 not found"
        return 1
    fi
}

# Check if pip is available
check_pip() {
    if python3 -m pip --version &> /dev/null; then
        print_success "pip is available"
        return 0
    else
        print_error "pip not found"
        return 1
    fi
}

# Check if venv is available
check_venv() {
    if python3 -m venv --help &> /dev/null; then
        print_success "venv is available"
        return 0
    else
        print_error "venv not found"
        return 1
    fi
}

# Setup virtual environment
setup_venv() {
    print_status "Setting up virtual environment..."
    
    if [ -d "venv" ]; then
        print_warning "Virtual environment already exists. Removing..."
        rm -rf venv
    fi
    
    python3 -m venv venv
    if [ $? -eq 0 ]; then
        print_success "Virtual environment created"
        source venv/bin/activate
        pip install --upgrade pip
        return 0
    else
        print_error "Failed to create virtual environment"
        return 1
    fi
}

# Install dependencies
install_dependencies() {
    print_status "Installing Python dependencies..."
    
    if [ -f "requirements.txt" ]; then
        pip install -r requirements.txt
        if [ $? -eq 0 ]; then
            print_success "Dependencies installed successfully"
            return 0
        else
            print_error "Failed to install dependencies"
            return 1
        fi
    else
        print_error "requirements.txt not found"
        return 1
    fi
}

# Setup database
setup_database() {
    print_status "Setting up database..."
    
    python manage.py migrate
    if [ $? -eq 0 ]; then
        print_success "Database migrations completed"
        return 0
    else
        print_error "Database migration failed"
        return 1
    fi
}

# Collect static files
collect_static() {
    print_status "Collecting static files..."
    
    python manage.py collectstatic --noinput
    if [ $? -eq 0 ]; then
        print_success "Static files collected"
        return 0
    else
        print_warning "Static file collection failed (non-critical)"
        return 0
    fi
}

# Configure IP address
configure_ip() {
    print_status "Configuring IP address..."
    
    # Get IP address
    IP_ADDRESS=$(hostname -I | awk '{print $1}')
    if [ -z "$IP_ADDRESS" ]; then
        IP_ADDRESS=$(ip route get 1 | awk '{print $7; exit}')
    fi
    
    if [ ! -z "$IP_ADDRESS" ]; then
        print_success "Detected IP address: $IP_ADDRESS"
        
        if [ -f "configure_ip.py" ]; then
            python configure_ip.py
            print_success "IP configuration completed"
        else
            print_warning "configure_ip.py not found. You may need to manually update settings.py"
        fi
    else
        print_warning "Could not detect IP address automatically"
    fi
}

# Configure firewall
configure_firewall() {
    print_status "Checking firewall configuration..."
    
    # Check if ufw is available (Ubuntu/Debian)
    if command -v ufw &> /dev/null; then
        print_status "Configuring UFW firewall..."
        sudo ufw allow 8000/tcp
        print_success "UFW configured to allow port 8000"
    # Check if firewalld is available (CentOS/RHEL/Fedora)
    elif command -v firewall-cmd &> /dev/null; then
        print_status "Configuring firewalld..."
        sudo firewall-cmd --add-port=8000/tcp --permanent
        sudo firewall-cmd --reload
        print_success "firewalld configured to allow port 8000"
    else
        print_warning "No supported firewall found. You may need to manually configure firewall rules."
    fi
}

# Test installation
test_installation() {
    print_status "Testing installation..."
    
    # Test if server can start
    timeout 5s python manage.py runserver 0.0.0.0:8000 &> /dev/null &
    SERVER_PID=$!
    sleep 3
    
    if kill -0 $SERVER_PID 2> /dev/null; then
        kill $SERVER_PID
        print_success "Server test passed"
        return 0
    else
        print_error "Server test failed"
        return 1
    fi
}

# Main installation process
main() {
    echo
    print_status "Starting Equipment Tracking Project setup..."
    echo
    
    # Check if we're in the right directory
    if [ ! -f "manage.py" ]; then
        print_error "manage.py not found. Please run this script from the project root directory."
        exit 1
    fi
    
    # Step 1: Check existing Python installation
    if ! check_python || ! check_pip || ! check_venv; then
        print_status "Installing missing prerequisites..."
        install_prerequisites
        
        # Check again after installation
        if ! check_python || ! check_pip || ! check_venv; then
            print_error "Prerequisites installation failed. Please install Python 3, pip, and venv manually."
            exit 1
        fi
    fi
    
    # Step 2: Setup virtual environment
    if ! setup_venv; then
        print_error "Virtual environment setup failed"
        exit 1
    fi
    
    # Step 3: Install dependencies
    if ! install_dependencies; then
        print_error "Dependency installation failed"
        exit 1
    fi
    
    # Step 4: Setup database
    if ! setup_database; then
        print_error "Database setup failed"
        exit 1
    fi
    
    # Step 5: Collect static files
    collect_static
    
    # Step 6: Configure IP
    configure_ip
    
    # Step 7: Configure firewall (optional)
    read -p "Configure firewall to allow port 8000? (y/N): " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        configure_firewall
    fi
    
    # Step 8: Test installation
    test_installation
    
    echo
    print_success "========================================="
    print_success "Setup completed successfully!"
    print_success "========================================="
    echo
    
    print_status "To start the server:"
    echo "  1. Activate environment: source venv/bin/activate"
    echo "  2. Start server: python manage.py runserver 0.0.0.0:8000"
    echo "  3. Or use: ./start_server.sh"
    echo
    
    if [ ! -z "$IP_ADDRESS" ]; then
        print_status "Access your application at:"
        echo "  Local: http://localhost:8000"
        echo "  Network: http://$IP_ADDRESS:8000"
    else
        print_status "Access your application at:"
        echo "  Local: http://localhost:8000"
        echo "  Network: http://YOUR_IP:8000"
    fi
    
    echo
    print_status "To find your IP address: ip addr show or ifconfig"
    print_status "For documentation, see: LINUX_SETUP.md"
    echo
}

# Handle Ctrl+C
trap 'echo; print_warning "Setup interrupted by user"; exit 1' INT

# Run main function
main

print_status "Setup script completed."
