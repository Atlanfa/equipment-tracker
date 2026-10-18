import os
import ssl
import socket
from django.core.management.base import BaseCommand
from django.core.management.commands.runserver import Command as RunServerCommand
from django.core.wsgi import get_wsgi_application
from django.conf import settings


class Command(BaseCommand):
    help = 'Run Django development server with HTTPS'

    def add_arguments(self, parser):
        parser.add_argument(
            'addrport', nargs='?',
            help='Optional port number, or ipaddr:port'
        )
        parser.add_argument(
            '--cert-file', dest='cert_file',
            help='SSL certificate file'
        )
        parser.add_argument(
            '--key-file', dest='key_file',
            help='SSL private key file'
        )

    def handle(self, *args, **options):
        import threading
        import time
        from wsgiref.simple_server import make_server, WSGIServer
        from wsgiref.simple_server import WSGIRequestHandler
        import ssl

        # Parse address and port
        addrport = options.get('addrport') or '0.0.0.0:8443'
        if ':' in addrport:
            addr, port = addrport.rsplit(':', 1)
        else:
            addr, port = '0.0.0.0', addrport
        
        port = int(port)

        # Get certificate files
        cert_file = options.get('cert_file') or 'localhost.crt'
        key_file = options.get('key_file') or 'localhost.key'

        if not os.path.exists(cert_file) or not os.path.exists(key_file):
            self.stdout.write(
                self.style.ERROR(f'Certificate files not found: {cert_file}, {key_file}')
            )
            return

        # Get Django WSGI application
        application = get_wsgi_application()

        class SSLWSGIServer(WSGIServer):
            def __init__(self, *args, **kwargs):
                super().__init__(*args, **kwargs)
                # Wrap socket with SSL
                context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
                context.load_cert_chain(cert_file, key_file)
                self.socket = context.wrap_socket(self.socket, server_side=True)

        # Create and start server
        self.stdout.write(f'Starting HTTPS development server at https://{addr}:{port}/')
        self.stdout.write('Quit the server with CTRL-BREAK.')
        
        try:
            httpd = make_server(addr, port, application, server_class=SSLWSGIServer)
            httpd.serve_forever()
        except KeyboardInterrupt:
            self.stdout.write('\nServer stopped.')
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Error starting server: {e}'))
