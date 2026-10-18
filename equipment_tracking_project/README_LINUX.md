# Equipment Tracking Project - Linux Ready

## 🐧 Quick Start for Linux

This project has been fully prepared for deployment on Linux systems. All camera and barcode scanning features have been removed, making it perfect for network-accessible equipment tracking.

### ⚡ One-Command Setup

```bash
chmod +x linux_setup_complete.sh
./linux_setup_complete.sh
```

This will automatically:
- Install Python dependencies
- Set up virtual environment
- Configure database
- Detect and configure your IP address
- Set up firewall rules (optional)
- Test the installation

### 🚀 Manual Setup (if needed)

```bash
# 1. Install Python (Ubuntu/Debian)
sudo apt update && sudo apt install python3 python3-pip python3-venv

# 2. Setup environment
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# 3. Initialize database
python manage.py migrate

# 4. Configure IP (optional)
python configure_ip.py

# 5. Start server
python manage.py runserver 0.0.0.0:8000
```

### 🌐 Network Access

After setup, your equipment tracking system will be available at:
- **Local:** http://localhost:8000
- **Network:** http://YOUR_IP:8000

Find your IP with: `ip addr show` or `ifconfig`

### 📁 What's Included

- **Web Application:** Complete Django-based equipment tracking system
- **Database:** SQLite database with equipment data
- **Data Files:** CSV order data and Excel equipment lists
- **Setup Scripts:** Automated installation for Linux
- **Documentation:** Comprehensive setup and transfer guides

### 🔧 Key Features

- ✅ Equipment search and tracking
- ✅ Data import from CSV and Excel files
- ✅ Network accessibility
- ✅ Clean, modern web interface
- ✅ No camera dependencies
- ✅ Cross-platform compatibility

### 📚 Documentation

- `LINUX_SETUP.md` - Detailed Linux setup instructions
- `LINUX_DEPLOYMENT.md` - Complete deployment checklist
- `SETUP_GUIDE.md` - Cross-platform setup guide
- `TRANSFER_CHECKLIST.md` - Migration verification steps

### 🔐 Security Notes

For production deployment:
1. Change the SECRET_KEY in settings.py
2. Set DEBUG=False
3. Configure a proper web server (nginx + gunicorn)
4. Set up regular database backups

### 🆘 Need Help?

1. **Common Issues:** Check `LINUX_DEPLOYMENT.md` troubleshooting section
2. **Setup Problems:** Run `./linux_setup_complete.sh` for automated diagnosis
3. **Network Issues:** Verify firewall settings and IP configuration

### 📊 System Requirements

- **OS:** Any modern Linux distribution
- **Python:** 3.8 or higher
- **RAM:** 512MB minimum (1GB recommended)
- **Storage:** 100MB for application + data
- **Network:** Local network access for multi-user functionality

---

**Ready to deploy!** This project is fully prepared for Linux deployment with no additional configuration needed.
