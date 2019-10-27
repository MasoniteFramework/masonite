
import time
import os

from hupper.logger import DefaultLogger, LogLevel
from hupper.reloader import Reloader, find_default_monitor_factory
from cleo import Command
from ..helpers import has_unmigrated_migrations
from ..exceptions import DriverLibraryNotFound


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

    def handle(self):
        if has_unmigrated_migrations():
            self.comment("\nYou have unmigrated migrations. Run 'craft migrate' to migrate them\n")

        if self.option('live-reload'):
            try:
                from livereload import Server
            except ImportError:
                raise DriverLibraryNotFound("Could not find the livereload library. Install it by running 'pip install livereload==2.5.1'")

            from wsgi import container
            from config import application
            import glob

            server = Server(container.make('WSGI'))
            for filepath in glob.glob('resources/templates/**/*/'):
                server.watch(filepath)

            self.line('')
            self.info('Live reload server is starting...')
            self.info(
                'This will only work for templates. Changes to Python files may require a browser refresh.')
            self.line('')
            application = server.serve(port=self.option('port'), restart_delay=self.option(
                'reload-interval'), liveport=5500, root=application.BASE_DIRECTORY, debug=True)
            return

        if not self.option('dont-reload'):
            logger = DefaultLogger(LogLevel.INFO)

            # worker args are pickled and then passed to the new process
            worker_args = [
                self.option("host"), self.option("port"), "wsgi:application",
            ]

            reloader = Reloader(
                "masonite.commands._devserver.run",
                find_default_monitor_factory(logger),
                logger,
                worker_args=worker_args,
            )

            self._run_reloader(reloader, extra_files=[".env", "storage/"])

        else:
            from wsgi import application
            from ._devserver import run
            run(self.option("host"), self.option("port"), application)

    def _run_reloader(self, reloader, extra_files=[]):
        reloader._capture_signals()
        reloader._start_monitor()
        for blob in extra_files:
            reloader.monitor.add_path(os.path.join(os.getcwd(), blob))
        try:
            while True:
                if not reloader._run_worker():
                    reloader._wait_for_changes()
                time.sleep(float(self.option('reload-interval')))
        except KeyboardInterrupt:
            pass
        finally:
            reloader._stop_monitor()
            reloader._restore_signals()
