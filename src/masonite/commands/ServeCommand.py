import sys
import hupper
import logging
import socketserver
from wsgiref import simple_server

from .Command import Command

logger = logging.getLogger("masonite.server")


class ThreadedWSGIServer(socketserver.ThreadingMixIn, simple_server.WSGIServer):
    """A threaded version of the WSGIServer"""

    daemon_threads = True


class WSGIRequestHandler(simple_server.WSGIRequestHandler):
    def log_message(self, format, *args):
        extra = {
            "request": self.request,
            "server_time": self.log_date_time_string(),
        }
        if args[1][0] == "4":
            # 0x16 = Handshake, 0x03 = SSL 3.0 or TLS 1.x
            if args[0].startswith("\x16\x03"):
                extra["status_code"] = 500
                logger.error(
                    "You're accessing the development server over HTTPS, but "
                    "it only supports HTTP.",
                    extra=extra,
                )
                return

        if args[1].isdigit() and len(args[1]) == 3:
            status_code = int(args[1])
            extra["status_code"] = status_code

            if status_code >= 500:
                level = logger.error
            elif status_code >= 400:
                level = logger.warning
            else:
                level = logger.info
        else:
            level = logger.info

        level(format, *args, extra=extra)


class ServeCommand(Command):
    """
    Run the Masonite server.

    serve
        {--p|port=8000 : Specify which port to run the server}
        {--b|host=127.0.0.1 : Specify which ip address to run the server}
        {--r|reload : Make the server automatically reload on file changes}
        {--d|dont-reload : Make the server NOT automatically reload on file changes}
        {--i|reload-interval=1 : Number of seconds to wait to reload after changed are detected}
        {--l|live-reload : Make the server automatically refresh your web browser}
        {--t|threaded : Use a multi-threaded development server}
    """

    def __init__(self, application):
        super().__init__()
        self.app = application

    def handle(self):
        if self.option("live-reload"):
            try:
                from livereload import Server
            except ImportError:
                raise ImportError(
                    "Could not find the livereload library. Install it by running 'pip install livereload==2.5.1'"
                )

            import glob

            server = Server(self.app)
            for filepath in glob.glob("resources/templates/**/*/"):
                server.watch(filepath)

            self.line("")
            self.info("Live reload server is starting...")
            self.info(
                "This will only work for templates. Changes to Python files may require a browser refresh."
            )
            self.line("")
            server.serve(
                port=self.option("port"),
                restart_delay=self.option("reload-interval"),
                liveport=5500,
                root=self.app.base_path,
                debug=True,
            )
            return

        reloader = hupper.start_reloader(self.app.make("server.runner"))

        # monitor an extra file
        reloader.watch_files([".env", self.app.get_storage_path()])


def main(args=sys.argv[1:]):
    from wsgi import application

    host = "127.0.0.1"
    port = "8000"
    threaded = False
    if "--host" in args:
        host = args[args.index("--host") + 1]
    if "-b" in args:
        host = args[args.index("-b") + 1]
    if "--port" in args:
        port = args[args.index("--port") + 1]
    if "-p" in args:
        port = args[args.index("-p") + 1]
    if "--threading" in args or "-t" in args:
        threaded = True

    if threaded:
        server_class = ThreadedWSGIServer
    else:
        server_class = simple_server.WSGIServer

    with simple_server.make_server(
        host, int(port), application, server_class, WSGIRequestHandler
    ) as httpd:
        # Respond to requests until process is killed
        print(f"Serving on : http://{host}:{port}")
        httpd.serve_forever()
