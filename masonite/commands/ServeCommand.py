
import time
import os

from hupper.logger import DefaultLogger, LogLevel
from hupper.reloader import Reloader, find_default_monitor_factory
from cleo import Command


class ServeCommand(Command):
    """
    Run the Masonite server

    serve
        {--p|port=8000 : Specify which port to run the server}
        {--b|host=127.0.0.1 : Specify which ip address to run the server}
        {--r|reload : Make the server automatically reload on file changes}
        {--i|reload-interval=1 : Make the server automatically reload on file changes}
    """

    def handle(self):
        # Check for the 2.0 patch.
        self._check_patch()

        if self.option('reload'):
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

            self._run_reloader(reloader, extra_files=[".env"])

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

    def _check_patch(self):
        patched = False

        with open('wsgi.py', 'r') as file:
            # read a list of lines into data
            data = file.readlines()

        # change the line that starts with KEY=
        for line_number, line in enumerate(data):
            if line.startswith("for provider in container.make('Providers'):"):
                patched = True
                break

        if not patched:
            print('\033[93mWARNING: {}\033[0m'.format(
                "Your application does not have a 2.0 patch! You can read more about this patch here: https://dev.to/josephmancuso/masonite-framework-20-patch-3op2"))
