"""
Network Configuration Template
Copy this to settings.py and update with your new computer's IP address
"""

# Find your IP address:
# Windows: Open Command Prompt and run: ipconfig
# macOS/Linux: Open Terminal and run: ifconfig or ip addr show

# Update ALLOWED_HOSTS with your new IP address
ALLOWED_HOSTS = [
    'localhost',
    '127.0.0.1',
    '0.0.0.0',
    'YOUR_NEW_IP_HERE',  # Replace with your actual IP (e.g., '192.168.1.100')
    '*',  # Allow all hosts for development - remove in production
]

# Example configurations for common networks:
# Home network: '192.168.1.XXX'
# Office network: '10.0.0.XXX' or '172.16.0.XXX'
# Hotel/Public WiFi: varies

# Alternative: Allow entire subnet
# '192.168.1.*' or '10.0.0.*'
