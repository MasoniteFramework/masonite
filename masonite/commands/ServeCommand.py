
import time
import os

from hupper.logger import DefaultLogger, LogLevel
from hupper.reloader import Reloader, find_default_monitor_factory
from cleo import Command
from masonite.helpers import has_unmigrated_migrations


class ServeCommand(Command):
    """
    Run the Masonite server.

    serve
        {--p|port=8000 : Specify which port to run the server}
        {--b|host=127.0.0.1 : Specify which ip address to run the server}
        {--r|reload : Make the server automatically reload on file changes}
        {--d|dont-reload : Make the server NOT automatically reload on file changes}
        {--i|reload-interval=1 : Number of seconds to wait to reload after changed are detected}
    """

    def handle(self):
        if has_unmigrated_migrations():
            self.comment("\nYou have unmigrated migrations. Run 'craft migrate' to migrate them\n")

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
