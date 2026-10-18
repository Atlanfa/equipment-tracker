import http.server
import ssl
import socketserver
import os
import subprocess
import sys
import threading
import time

def start_django_process():
    """Start Django in the background"""
    os.environ['DJANGO_SETTINGS_MODULE'] = 'equipment_tracking_project.settings'
    
    # Start Django on HTTP first
    django_cmd = [
        sys.executable,
        'manage.py',
        'runserver',
        '127.0.0.1:8001'  # Internal port
    ]
    
    return subprocess.Popen(django_cmd, cwd=os.path.dirname(__file__))

class ProxyHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        import urllib.request
        import urllib.parse
        
        # Forward request to Django
        try:
            url = f'http://127.0.0.1:8001{self.path}'
            response = urllib.request.urlopen(url)
            
            # Send response
            self.send_response(200)
            for header, value in response.headers.items():
                if header.lower() not in ['server', 'date']:
                    self.send_header(header, value)
            self.end_headers()
            
            self.wfile.write(response.read())
        except Exception as e:
            self.send_error(500, f'Proxy error: {str(e)}')
    
    def do_POST(self):
        self.do_GET()

def main():
    print("Starting Equipment Tracking HTTPS Server...")
    
    # Start Django process
    print("Starting Django backend...")
    django_process = start_django_process()
    
    # Wait for Django to start
    time.sleep(3)
    
    # Create HTTPS proxy server
    port = 8443
    
    try:
        with socketserver.TCPServer(("0.0.0.0", port), ProxyHandler) as httpd:
            # Wrap with SSL
            context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
            context.load_cert_chain('localhost.crt', 'localhost.key')
            httpd.socket = context.wrap_socket(httpd.socket, server_side=True)
            
            print(f"HTTPS server running at:")
            print(f"  - https://localhost:{port}")
            print(f"  - https://10.0.0.180:{port}")
            print(f"Press Ctrl+C to stop...")
            
            httpd.serve_forever()
    except KeyboardInterrupt:
        print("\nStopping servers...")
    except Exception as e:
        print(f"Error: {e}")
    finally:
        # Stop Django process
        if 'django_process' in locals():
            django_process.terminate()
            django_process.wait()

if __name__ == "__main__":
    main()
