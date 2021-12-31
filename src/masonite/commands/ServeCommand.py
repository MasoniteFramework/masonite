import sys

import hupper
import waitress
from .Command import Command


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
    if "--host" in args:
        host = args[args.index("--host") + 1]
    if "-b" in args:
        host = args[args.index("-b") + 1]
    if "--port" in args:
        port = args[args.index("--port") + 1]
    if "-p" in args:
        port = args[args.index("-p") + 1]

    waitress.serve(
        application, host=host, port=port, clear_untrusted_proxy_headers=False
    )
