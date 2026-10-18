# Linux Deployment Checklist

## Pre-Transfer Preparation ✅

- [x] Removed all camera/barcode scanning features
- [x] Created cross-platform requirements.txt
- [x] Updated Django settings for network access
- [x] Created Linux setup scripts (setup.sh, start_server.sh)
- [x] Created comprehensive documentation
- [x] Prepared IP configuration tools

## Files to Transfer

### Essential Project Files
- [ ] `equipment_tracking_project/` (entire folder)
- [ ] `db.sqlite3` (database)
- [ ] `order_data/` (CSV data files)
- [ ] `equipment list/` (Excel files)

### Setup and Documentation Files
- [ ] `requirements.txt`
- [ ] `setup.sh` (Linux setup script)
- [ ] `start_server.sh` (Linux server startup)
- [ ] `configure_ip.py` (IP configuration)
- [ ] `SETUP_GUIDE.md` (comprehensive guide)
- [ ] `LINUX_SETUP.md` (Linux-specific instructions)
- [ ] `TRANSFER_CHECKLIST.md` (migration checklist)

## Linux Machine Setup Steps

### 1. Prerequisites Installation
```bash
# Ubuntu/Debian
sudo apt update && sudo apt install python3 python3-pip python3-venv

# CentOS/RHEL/Fedora
sudo dnf install python3 python3-pip python3-venv

# Arch Linux
sudo pacman -S python python-pip
```

### 2. Project Transfer
```bash
# Copy project to home directory
cp -r /path/to/equipment_tracking_project ~/
cd ~/equipment_tracking_project

# Make scripts executable
chmod +x setup.sh start_server.sh configure_ip.py
```

### 3. Environment Setup
```bash
# Run automated setup
./setup.sh

# Or manual setup:
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python manage.py migrate
python manage.py collectstatic --noinput
```

### 4. Network Configuration
```bash
# Find IP address
ip addr show | grep "inet " | grep -v 127.0.0.1

# Configure automatically
python configure_ip.py

# Or edit manually
nano equipment_tracking_project/settings.py
# Update ALLOWED_HOSTS with your IP
```

### 5. Firewall Setup (if needed)
```bash
# Ubuntu/Debian
sudo ufw allow 8000

# CentOS/RHEL/Fedora
sudo firewall-cmd --add-port=8000/tcp --permanent
sudo firewall-cmd --reload
```

### 6. Start Server
```bash
# Quick start
./start_server.sh

# Or manual start
source venv/bin/activate
python manage.py runserver 0.0.0.0:8000
```

## Verification Tests

### Local Access Test
- [ ] Open browser: `http://localhost:8000`
- [ ] Verify homepage loads
- [ ] Test equipment search functionality
- [ ] Test data import features

### Network Access Test
- [ ] Find machine IP: `ip addr show`
- [ ] From another device: `http://YOUR_IP:8000`
- [ ] Verify external access works
- [ ] Test from multiple devices

### Data Integrity Test
- [ ] Verify all CSV files in `order_data/` are present
- [ ] Check Excel files in `equipment list/` folder
- [ ] Test data import/search functionality
- [ ] Verify database migrations completed

## Troubleshooting Quick Fixes

### Permission Issues
```bash
chmod +x *.sh *.py
```

### Python Not Found
```bash
# Use python3 explicitly
python3 manage.py runserver 0.0.0.0:8000
```

### Virtual Environment Issues
```bash
rm -rf venv
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### Network Access Issues
1. Check firewall: `sudo ufw status` or `sudo firewall-cmd --list-all`
2. Verify IP in settings.py matches machine IP
3. Test local access first: `curl http://localhost:8000`
4. Check server binding: should be `0.0.0.0:8000`

## Post-Deployment Tasks

### Security (Optional)
- [ ] Change Django SECRET_KEY in settings.py
- [ ] Set DEBUG=False for production use
- [ ] Configure proper web server (nginx + gunicorn)

### Performance (Optional)
- [ ] Install gunicorn: `pip install gunicorn`
- [ ] Use PostgreSQL for multi-user scenarios
- [ ] Set up regular database backups

### Monitoring (Optional)
- [ ] Set up as systemd service
- [ ] Configure log rotation
- [ ] Monitor disk space usage

## Success Criteria

✅ **Project Successfully Deployed When:**
- Server starts without errors
- Web interface accessible locally and via network
- All equipment tracking features work
- Data import/search functions properly
- No camera/barcode scanning features present
- Documentation is clear and complete

## Quick Commands Reference

```bash
# Setup (one-time)
./setup.sh

# Start server
./start_server.sh

# Configure IP
python configure_ip.py

# Check server status
ps aux | grep python

# Stop server
pkill -f "python manage.py runserver"

# View logs
tail -f nohup.out
```

---

**Total Transfer Size:** ~50-100MB (depending on data files)
**Setup Time:** 5-10 minutes
**Skill Level Required:** Basic Linux command line knowledge
