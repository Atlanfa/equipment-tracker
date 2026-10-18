# Equipment Tracking Project - Setup Guide

## 📦 Project Transfer Instructions

This guide will help you set up the Equipment Tracking Project on a new computer.

## 🔧 Prerequisites

1. **Python 3.8 or higher** - Download from [python.org](https://python.org)
2. **Git** (optional) - For version control
3. **Text Editor/IDE** - VS Code, PyCharm, or similar

## 🚀 Quick Setup (5 minutes)

### Step 1: Extract Project
1. Copy the entire `equipment_tracking_project` folder to your new computer
2. Place it in a convenient location (e.g., `C:\Projects\` or `~/Projects/`)

### Step 2: Set Up Python Environment
Open Command Prompt/Terminal in the project folder and run:

```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### Step 3: Configure for Local Network
1. Find your new computer's IP address:
   ```bash
   # Windows:
   ipconfig
   # macOS/Linux:
   ifconfig
   ```

2. Update `equipment_tracking_project/settings.py`:
   - Replace `10.0.0.180` with your new IP address
   - Or keep `'*'` in ALLOWED_HOSTS for any IP

### Step 4: Initialize Database
```bash
python manage.py migrate
python manage.py collectstatic --noinput
```

### Step 5: Start Server
```bash
# Simple HTTP server (recommended)
python manage.py runserver 0.0.0.0:8000

# Or use the provided batch files:
# Windows: double-click start_network_server.bat
# PowerShell: ./start_network_server.ps1
```

### Step 6: Access Application
- **Local:** http://localhost:8000
- **Network:** http://YOUR_NEW_IP:8000 (replace with actual IP)

## 📁 Project Structure

```
equipment_tracking_project/
├── equipment_tracking_app/        # Main Django app
│   ├── templates/                 # HTML templates
│   ├── static/                    # CSS, JS, images
│   ├── models.py                  # Database models
│   ├── views.py                   # Application logic
│   └── management/commands/       # Custom Django commands
├── equipment_tracking_project/    # Django project settings
│   ├── settings.py               # Configuration
│   ├── urls.py                   # URL routing
│   └── wsgi.py                   # WSGI configuration
├── order_data/                   # CSV data files
├── equipment list/               # Equipment data
├── db.sqlite3                    # Database file
├── manage.py                     # Django management script
├── requirements.txt              # Python dependencies
└── start_network_server.*        # Server startup scripts
```

## 🔧 Configuration Files

### Key Files to Check:
1. **settings.py** - Update ALLOWED_HOSTS with new IP
2. **db.sqlite3** - Database with all your data
3. **requirements.txt** - Python package dependencies

## 🌐 Network Access

The application is configured to work on local networks:

- **Equipment QC Tracking:** View and track equipment by week
- **Warehouse Management:** Search equipment and view locations
- **Dark/Light Mode:** Theme switching
- **Mobile Friendly:** Responsive design

## 🔍 Features Available

### Equipment QC Tracking:
- Weekly equipment schedule view
- Filter by day, equipment type
- Add notes with color highlighting
- Total quantity calculations
- Week navigation

### Warehouse Management:
- Search equipment by name or barcode
- Manual barcode entry
- Equipment location display
- Equipment details and descriptions

## 🛠️ Troubleshooting

### Common Issues:

1. **Port 8000 already in use:**
   ```bash
   python manage.py runserver 0.0.0.0:8080
   ```

2. **Permission denied:**
   - Run as administrator (Windows)
   - Check firewall settings

3. **Database errors:**
   ```bash
   python manage.py migrate
   ```

4. **Missing dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

5. **Static files not loading:**
   ```bash
   python manage.py collectstatic
   ```

## 🔧 Advanced Configuration

### Custom IP Configuration:
Edit `equipment_tracking_project/settings.py`:
```python
ALLOWED_HOSTS = [
    'localhost',
    '127.0.0.1',
    'YOUR_NEW_IP_HERE',  # Replace with actual IP
    '*',  # Allow all IPs (development only)
]
```

### Database Backup:
The `db.sqlite3` file contains all your data. Keep it safe!

### Environment Variables (Optional):
Create `.env` file for sensitive settings:
```
SECRET_KEY=your-secret-key-here
DEBUG=True
```

## 📞 Support

If you encounter issues:
1. Check Python version: `python --version`
2. Check Django installation: `python -m django --version`
3. Review error messages in terminal
4. Ensure all files transferred correctly

## 🎯 Quick Test

After setup, test these features:
1. Access http://localhost:8000
2. Switch between QC Tracking and Warehouse Management
3. Search for equipment
4. Toggle dark/light mode
5. Test on mobile device using network IP

## 🔄 Data Migration

Your existing data in `db.sqlite3` will transfer automatically. The database contains:
- Equipment records
- Location data
- Notes and highlights
- User preferences

---

**✅ Setup Complete!** Your Equipment Tracking system should now be running on the new computer and accessible from the local network.
