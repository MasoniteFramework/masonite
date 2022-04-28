from werkzeug.serving import run_simple

from .Command import Command


class ServeCommand(Command):
    """
    Run the Masonite server.

    serve
        {--p|port=8000 : Specify which port to run the server}
        {--b|host=127.0.0.1 : Specify which ip address to run the server}
        {--d|dont-reload : Make the server NOT automatically reload on file changes}
        {--i|reload-interval=1 : Number of seconds to wait to reload after changed are detected}
        {--l|live-reload : Make the server automatically refresh your web browser}
        {--t|threaded : Handle concurrent requests using threads}
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

        use_reloader = True
        threaded = False
        extra_files = [".env", self.app.get_storage_path()]

        if self.option("dont-reload"):
            use_reloader = False

        if self.option("threaded"):
            threaded = True

        run_simple(
            self.option("host"),
            int(self.option("port")),
            self.app,
            threaded=threaded,
            use_reloader=use_reloader,
            extra_files=extra_files,
            # reloader_interval=
            # more efficient than stat
            reloader_type="watchdog",
        )
