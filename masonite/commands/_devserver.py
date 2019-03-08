# Pure-python development wsgi server.
# Parts are borrowed from Adrian Holovaty and the Django Project
#  (https://www.djangoproject.com/).

import logging
import socket
import sys
from wsgiref import simple_server

logging.basicConfig(level=logging.INFO)


def is_broken_pipe_error():
    exc_type, exc_value = sys.exc_info()[:2]
    return issubclass(exc_type, socket.error) and exc_value.args[0] == 32


class WSGIServer(simple_server.WSGIServer):
    """BaseHTTPServer that implements the Python WSGI protocol"""

    request_queue_size = 10

    def __init__(self, *args, ipv6=False, allow_reuse_address=True, **kwargs):
        if ipv6:
            self.address_family = socket.AF_INET6
        self.allow_reuse_address = allow_reuse_address
        super().__init__(*args, **kwargs)

    def handle_error(self, request, client_address):
        if is_broken_pipe_error():
            logging.info("- Broken pipe from %s\n", client_address)
        else:
            super().handle_error(request, client_address)


class ServerHandler(simple_server.ServerHandler):
    http_version = '1.1'

    def handle_error(self):
        # Ignore broken pipe errors, otherwise pass on
        if not is_broken_pipe_error():
            super().handle_error()


class WSGIRequestHandler(simple_server.WSGIRequestHandler):
    protocol_version = 'HTTP/1.1'

    def address_string(self):
        # Short-circuit parent method to not call socket.getfqdn
        return self.client_address[0]

    def log_message(self, format, *args):
        extra = {
            'request': self.request,
            'server_time': self.log_date_time_string(),
        }
        if args[1][0] == '4':
            # 0x16 = Handshake, 0x03 = SSL 3.0 or TLS 1.x
            if args[0].startswith('\x16\x03'):
                extra['status_code'] = 500
                logging.error(
                    "You're accessing the development server over HTTPS, but "
                    "it only supports HTTP.\n", extra=extra,
                )
                return

        if args[1].isdigit() and len(args[1]) == 3:
            status_code = int(args[1])
            extra['status_code'] = status_code

            if status_code >= 500:
                level = logging.error
            elif status_code >= 400:
                level = logging.warning
            else:
                level = logging.info
        else:
            level = logging.info

        level(format, *args, extra=extra)

    def get_environ(self):
        # Strip all headers with underscores in the name before constructing
        # the WSGI environ. This prevents header-spoofing based on ambiguity
        # between underscores and dashes both normalized to underscores in WSGI
        # env vars. Nginx and Apache 2.4+ both do this as well.
        for k in self.headers:
            if '_' in k:
                del self.headers[k]

        return super().get_environ()

    def handle(self):
        """Copy of WSGIRequestHandler.handle() but with different ServerHandler"""
        self.raw_requestline = self.rfile.readline(65537)
        if len(self.raw_requestline) > 65536:
            self.requestline = ''
            self.request_version = ''
            self.command = ''
            self.send_error(414)
            return

        if not self.parse_request():  # An error code has been sent, just exit
            return

        handler = ServerHandler(
            self.rfile, self.wfile, self.get_stderr(), self.get_environ()
        )
        handler.request_handler = self      # backpointer for logging
        handler.run(self.server.get_app())


def _split_module_and_app(moduleapp):
    if ":" in moduleapp:
        parts = moduleapp.split(":")
        return parts[0], parts[1]
    return moduleapp, "application"


def _import_application(module_name, app_name):
    from importlib import import_module
    module = import_module(module_name)
    return getattr(module, app_name)


def run(host, port, wsgi_handler, ipv6=False, httpd_cls=WSGIServer):
    if type(wsgi_handler) == str:
        module_name, app_name = _split_module_and_app(wsgi_handler)
        wsgi_handler = _import_application(module_name, app_name)

    server_address = (host, int(port))
    httpd = httpd_cls(server_address, WSGIRequestHandler, ipv6=ipv6)
    httpd.set_app(wsgi_handler)
    try:
        print('Serving at: http://{}:{}'.format(host, port))
        httpd.serve_forever()
    except KeyboardInterrupt:
        pass
