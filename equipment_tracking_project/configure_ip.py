#!/usr/bin/env python3
"""
Automatic IP Configuration Script
This script helps update the Django settings with the current computer's IP address.
"""

import socket
import re
import os

def get_local_ip():
    """Get the local IP address of this computer"""
    try:
        # Connect to a remote server to get local IP
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
        s.close()
        return ip
    except Exception:
        return None

def update_settings_file(new_ip):
    """Update the settings.py file with the new IP address"""
    settings_path = os.path.join("equipment_tracking_project", "settings.py")
    
    if not os.path.exists(settings_path):
        print(f"Error: {settings_path} not found!")
        return False
    
    # Read the current settings file
    with open(settings_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Pattern to find ALLOWED_HOSTS
    pattern = r"ALLOWED_HOSTS = \[(.*?)\]"
    match = re.search(pattern, content, re.DOTALL)
    
    if match:
        # Create new ALLOWED_HOSTS configuration
        new_allowed_hosts = f"""ALLOWED_HOSTS = [
    'localhost',
    '127.0.0.1',
    '0.0.0.0',
    '{new_ip}',  # Your local IP address
    '{new_ip.rsplit('.', 1)[0]}.*',  # Allow all devices on your local network
    '*',  # Allow all hosts for local development - remove in production
]"""
        
        # Replace the ALLOWED_HOSTS section
        new_content = re.sub(pattern, new_allowed_hosts, content, flags=re.DOTALL)
        
        # Write back to file
        with open(settings_path, 'w', encoding='utf-8') as f:
            f.write(new_content)
        
        return True
    else:
        print("Could not find ALLOWED_HOSTS in settings.py")
        return False

def main():
    print("========================================")
    print("Equipment Tracking - IP Configuration")
    print("========================================")
    print()
    
    # Get current IP
    current_ip = get_local_ip()
    
    if current_ip:
        print(f"Current IP address detected: {current_ip}")
        print()
        
        # Ask user if they want to update
        response = input(f"Update settings.py with IP {current_ip}? (y/n): ").lower().strip()
        
        if response in ['y', 'yes']:
            if update_settings_file(current_ip):
                print()
                print("✅ Settings updated successfully!")
                print(f"Your application will be accessible at:")
                print(f"  - Local: http://localhost:8000")
                print(f"  - Network: http://{current_ip}:8000")
                print()
                print("You can now start the server with:")
                print("  python manage.py runserver 0.0.0.0:8000")
            else:
                print("❌ Failed to update settings.py")
        else:
            print("Settings not updated.")
    else:
        print("❌ Could not detect IP address automatically.")
        print("Please update settings.py manually with your IP address.")
        print()
        print("To find your IP address:")
        print("  Windows: ipconfig")
        print("  macOS/Linux: ifconfig")
    
    print()
    input("Press Enter to exit...")

if __name__ == "__main__":
    main()
