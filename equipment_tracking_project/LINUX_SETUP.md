# Linux Installation Instructions for Equipment Tracking Project

## Quick Start for Linux Systems

### Prerequisites Installation

#### Ubuntu/Debian:
```bash
sudo apt update
sudo apt install python3 python3-pip python3-venv git
```

#### CentOS/RHEL 8+:
```bash
sudo dnf install python3 python3-pip python3-venv git
```

#### Fedora:
```bash
sudo dnf install python3 python3-pip git
```

#### Arch Linux:
```bash
sudo pacman -S python python-pip git
```

### Installation Steps

1. **Transfer the project folder** to your Linux machine:
   ```bash
   # If transferring via USB/external drive:
   cp -r /path/to/equipment_tracking_project ~/
   cd ~/equipment_tracking_project
   
   # If transferring via network (from another computer):
   scp -r user@source-computer:/path/to/equipment_tracking_project ~/
   cd ~/equipment_tracking_project
   ```

2. **Make scripts executable**:
   ```bash
   chmod +x setup.sh
   chmod +x start_server.sh
   ```

3. **Run the setup script**:
   ```bash
   ./setup.sh
   ```

4. **Configure your IP address**:
   ```bash
   # Find your IP
   ip addr show | grep inet | grep -v 127.0.0.1
   
   # Or use the automatic configuration script
   python configure_ip.py
   ```

5. **Start the server**:
   ```bash
   ./start_server.sh
   ```

### Firewall Configuration

If you need to access the application from other computers on the network:

#### Ubuntu/Debian (UFW):
```bash
sudo ufw allow 8000
sudo ufw enable
```

#### CentOS/RHEL/Fedora (firewalld):
```bash
sudo firewall-cmd --add-port=8000/tcp --permanent
sudo firewall-cmd --reload
```

#### Arch Linux (iptables):
```bash
sudo iptables -A INPUT -p tcp --dport 8000 -j ACCEPT
sudo iptables-save > /etc/iptables/iptables.rules
```

### Directory Structure After Setup

```
equipment_tracking_project/
├── venv/                    # Python virtual environment
├── db.sqlite3              # Database file
├── manage.py               # Django management script
├── requirements.txt        # Python dependencies
├── setup.sh               # Linux setup script
├── start_server.sh        # Linux server startup script
├── configure_ip.py        # IP configuration script
├── SETUP_GUIDE.md         # Detailed setup guide
├── equipment_tracking_app/ # Main application
├── equipment_tracking_project/ # Django project settings
├── order_data/            # CSV data files
└── equipment list/        # Equipment spreadsheets
```

### Troubleshooting

#### Permission Issues:
```bash
# Fix script permissions
chmod +x *.sh

# Fix Python script permissions
chmod +x *.py
```

#### Python Path Issues:
```bash
# Use python3 explicitly if python command not found
python3 manage.py runserver 0.0.0.0:8000
```

#### Virtual Environment Issues:
```bash
# Remove and recreate virtual environment
rm -rf venv
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

#### Network Access Issues:
1. Check firewall settings
2. Verify IP address in settings.py
3. Ensure the server is binding to 0.0.0.0:8000
4. Test with `curl http://localhost:8000` first

### Service Configuration (Optional)

To run as a system service:

1. Create service file:
```bash
sudo nano /etc/systemd/system/equipment-tracking.service
```

2. Add service configuration:
```ini
[Unit]
Description=Equipment Tracking Django App
After=network.target

[Service]
Type=simple
User=yourusername
WorkingDirectory=/home/yourusername/equipment_tracking_project
Environment=PATH=/home/yourusername/equipment_tracking_project/venv/bin
ExecStart=/home/yourusername/equipment_tracking_project/venv/bin/python manage.py runserver 0.0.0.0:8000
Restart=always

[Install]
WantedBy=multi-user.target
```

3. Enable and start service:
```bash
sudo systemctl daemon-reload
sudo systemctl enable equipment-tracking
sudo systemctl start equipment-tracking
```

### Performance Tips for Linux

1. **Use Gunicorn for production**:
   ```bash
   pip install gunicorn
   gunicorn equipment_tracking_project.wsgi:application --bind 0.0.0.0:8000
   ```

2. **Enable static file serving**:
   ```bash
   python manage.py collectstatic
   ```

3. **Database optimization**:
   - Consider PostgreSQL for multi-user scenarios
   - Regular database backups

### Quick Commands Summary

```bash
# Setup (one-time)
./setup.sh

# Start server
./start_server.sh

# Check logs
tail -f nohup.out

# Stop server
pkill -f "python manage.py runserver"

# Update IP configuration
python configure_ip.py
```
