# 📋 Transfer Checklist

## Before Transfer
- [ ] Copy entire `equipment_tracking_project` folder
- [ ] Ensure `db.sqlite3` file is included (contains all your data)
- [ ] Verify all files copied correctly

## Files to Transfer
### Essential Files:
- [ ] `manage.py` - Django management script
- [ ] `db.sqlite3` - Your database with all data
- [ ] `requirements.txt` - Python dependencies
- [ ] `equipment_tracking_app/` folder - Main application
- [ ] `equipment_tracking_project/` folder - Django settings
- [ ] `order_data/` folder - CSV data files
- [ ] `equipment list/` folder - Equipment data

### Setup Files (newly created):
- [ ] `SETUP_GUIDE.md` - Complete setup instructions
- [ ] `setup.bat` - Automated setup for Windows
- [ ] `setup.ps1` - Automated setup (PowerShell)
- [ ] `configure_ip.py` - IP configuration script
- [ ] `network_config_template.py` - IP configuration template
- [ ] `start_network_server.bat` - Server startup (Windows)
- [ ] `start_network_server.ps1` - Server startup (PowerShell)

### Optional Files:
- [ ] `README.md` - Project documentation
- [ ] `cert.pem` / `key.pem` - SSL certificates (if needed)
- [ ] Other `.bat` / `.ps1` files

## After Transfer - Quick Setup

### Option 1: Automatic Setup (Recommended)
1. [ ] Double-click `setup.bat` (Windows) or run `./setup.ps1` (PowerShell)
2. [ ] Run `python configure_ip.py` to set IP address
3. [ ] Start server with `start_network_server.bat`

### Option 2: Manual Setup
1. [ ] Open terminal in project folder
2. [ ] Run: `python -m venv venv`
3. [ ] Activate: `venv\Scripts\activate` (Windows) or `source venv/bin/activate` (macOS/Linux)
4. [ ] Install: `pip install -r requirements.txt`
5. [ ] Migrate: `python manage.py migrate`
6. [ ] Update IP in `equipment_tracking_project/settings.py`
7. [ ] Start: `python manage.py runserver 0.0.0.0:8000`

## Verification
- [ ] Access http://localhost:8000
- [ ] Test Equipment QC Tracking mode
- [ ] Test Warehouse Management mode
- [ ] Access from another device: http://YOUR_IP:8000
- [ ] Verify all data is present
- [ ] Test dark/light mode toggle

## Network Access
- [ ] Find new computer's IP address
- [ ] Update `ALLOWED_HOSTS` in settings.py
- [ ] Test access from mobile device
- [ ] Confirm firewall allows Python/port 8000

## Troubleshooting
If something doesn't work:
1. [ ] Check Python version: `python --version`
2. [ ] Check Django: `python -m django --version`
3. [ ] Re-run: `python manage.py migrate`
4. [ ] Check firewall settings
5. [ ] Verify all files transferred

---

## Quick Start Commands

```bash
# Setup (one time)
python -m venv venv
venv\Scripts\activate  # Windows
source venv/bin/activate  # macOS/Linux
pip install -r requirements.txt
python manage.py migrate
python configure_ip.py

# Start server
python manage.py runserver 0.0.0.0:8000
```

## Success Indicators
✅ Python environment created
✅ Dependencies installed
✅ Database migrated
✅ IP address configured
✅ Server starts without errors
✅ Application accessible locally
✅ Application accessible from network
✅ All features working correctly
